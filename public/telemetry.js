/**
 * ShadowGram Client-Side Telemetry SDK (telemetry.js)
 * Document Code: SG-PROTO-00 / Task 3.1
 * Assignee: Alan E Alexander (Role 3: Red-Team Swarm Runner & Client Telemetry Lead)
 * 
 * Strict Compliance:
 * 1. ZERO-PII: Never records key names, characters, or text inputs. Only time deltas (FT, DT).
 * 2. 50ms Throttling on cursor movements to guarantee zero UI lag during live judge testing.
 * 3. Self-contained pure JS HMAC-SHA256 for cryptographic telemetry signing (works on non-HTTPS LAN).
 * 4. Buffers and flushes to Laptop 2 (POST /telemetry) every 1.0s or via navigator.sendBeacon.
 */

(function (window, document) {
  'use strict';

  // --- Configuration ---
  const config = window.__SHADOWGRAM_CONFIG__ || {};
  const BACKEND_ENDPOINT = config.endpoint || (window.location.origin.startsWith('http') ? window.location.origin + '/telemetry' : 'http://localhost:8000/telemetry');
  const FLUSH_INTERVAL_MS = config.flushIntervalMs || 1000;
  const POINTER_THROTTLE_MS = 50;
  const SESSION_SALT = config.sessionSalt || 'shadowgram-hackathena-2026-salt';

  // --- Session State ---
  function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  const sessionId = config.sessionId || (function () {
    let s = sessionStorage.getItem('sg_session_id');
    if (!s) {
      s = generateUUID();
      sessionStorage.setItem('sg_session_id', s);
    }
    return s;
  })();

  const accountId = config.accountId || (function () {
    let a = sessionStorage.getItem('sg_account_id');
    if (!a) {
      a = 'ACC-' + Math.floor(10000 + Math.random() * 90000);
      sessionStorage.setItem('sg_account_id', a);
    }
    return a;
  })();

  // --- Pure JS HMAC-SHA256 (Zero Dependency, Works on HTTP LAN & HTTPS) ---
  function sha256(ascii) {
    function rightRotate(value, amount) {
      return (value >>> amount) | (value << (32 - amount));
    }
    const mathPow = Math.pow;
    const maxWord = mathPow(2, 32);
    let i, j;
    const result = '';
    const words = [];
    const asciiBitLength = ascii.length * 8;
    let hash = sha256.h = sha256.h || [];
    const k = sha256.k = sha256.k || [];
    let primeCounter = k.length;
    const isComposite = {};
    for (let candidate = 2; primeCounter < 64; candidate++) {
      if (!isComposite[candidate]) {
        for (i = 0; i < 313; i += candidate) isComposite[i] = candidate;
        hash[primeCounter] = (mathPow(candidate, 0.5) * maxWord) | 0;
        k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
      }
    }
    hash = hash.slice(0);
    words[asciiBitLength >> 5] |= 0x80 << (24 - (asciiBitLength % 32));
    words[(((asciiBitLength + 64) >> 9) << 4) + 15] = asciiBitLength;
    for (i = 0; i < ascii.length; i++) {
      words[i >> 2] |= ascii.charCodeAt(i) << ((3 - (i % 4)) * 8);
    }
    for (j = 0; j < words.length; j += 16) {
      const w = words.slice(j, j + 16);
      const oldHash = hash.slice(0);
      for (i = 0; i < 64; i++) {
        const w15 = w[i - 15], w2 = w[i - 2];
        const s0 = rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3);
        const s1 = rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10);
        w[i] = (i < 16) ? (w[i] | 0) : ((w[i - 16] + s0 + w[i - 7] + s1) | 0);
        const ch = (hash[4] & hash[5]) ^ (~hash[4] & hash[6]);
        const maj = (hash[0] & hash[1]) ^ (hash[0] & hash[2]) ^ (hash[1] & hash[2]);
        const temp1 = (hash[7] + (rightRotate(hash[4], 6) ^ rightRotate(hash[4], 11) ^ rightRotate(hash[4], 25)) + ch + k[i] + w[i]) | 0;
        const temp2 = ((rightRotate(hash[0], 2) ^ rightRotate(hash[0], 13) ^ rightRotate(hash[0], 22)) + maj) | 0;
        hash = [(temp1 + temp2) | 0, hash[0], hash[1], hash[2], (hash[3] + temp1) | 0, hash[4], hash[5], hash[6]];
      }
      for (i = 0; i < 8; i++) hash[i] = (hash[i] + oldHash[i]) | 0;
    }
    let hex = '';
    for (i = 0; i < 8; i++) {
      for (j = 3; j >= 0; j--) {
        const b = (hash[i] >> (8 * j)) & 255;
        hex += (b < 16 ? '0' : '') + b.toString(16);
      }
    }
    return hex;
  }

  function hmacSha256(message, key) {
    const blockSize = 64;
    if (key.length > blockSize) key = sha256(key);
    let oKeyPad = '', iKeyPad = '';
    for (let i = 0; i < blockSize; i++) {
      const byte = i < key.length ? key.charCodeAt(i) : 0;
      oKeyPad += String.fromCharCode(byte ^ 0x5c);
      iKeyPad += String.fromCharCode(byte ^ 0x36);
    }
    function hexToBinary(hex) {
      let bin = '';
      for (let i = 0; i < hex.length; i += 2) {
        bin += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
      }
      return bin;
    }
    const innerHash = sha256(iKeyPad + message);
    return sha256(oKeyPad + hexToBinary(innerHash));
  }

  // --- Telemetry Buffering ---
  let eventQueue = [];
  let lastKeyUpTime = null;
  const activeKeyDownTimes = new Map();
  let pointerCoords = [];
  let lastPointerSample = 0;
  let pointerDownTime = null;
  let pointerMovesBeforeClick = 0;
  let currentRoute = window.location.pathname;

  // Biometric Digraph Tracking (Zero-PII: No character logging, strictly interval deltas)
  // Common English/Latin financial application digraphs: th, he, in, er, an, re, on, at, en, nd, ti, es, or, te, of, ed, is, it, al, ar
  const COMMON_DIGRAPHS = new Set([
    'th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of', 'ed', 'is', 'it', 'al', 'ar'
  ]);
  let lastKeyChar = null;
  let lastKeyDownTime = null;

  function pushTelemetryEvent(eventType, payload) {
    const timestamp = Date.now() / 1000.0;
    const signPayload = sessionId + ':' + timestamp.toFixed(3);
    const signature = hmacSha256(signPayload, SESSION_SALT);

    const packet = {
      session_id: sessionId,
      account_id: accountId,
      timestamp: timestamp,
      event_type: eventType,
      telemetry_hmac: signature,
      payload: payload
    };
    eventQueue.push(packet);
  }

  // --- Event Listeners ---

  // 1. Keystroke Dynamics & Biometric Digraphs (Zero-PII: No key identifiers transmitted, only delta-t)
  window.addEventListener('keydown', function (e) {
    const now = performance.now();
    let flightTime = null;
    if (lastKeyUpTime !== null) {
      flightTime = Math.max(0, roundToDecimals(now - lastKeyUpTime, 2));
    }
    // Track start time for dwell time calculation
    if (!activeKeyDownTimes.has(e.code || e.keyCode)) {
      activeKeyDownTimes.set(e.code || e.keyCode, now);
    }

    // Biometric Digraph Flight Time (Zero-PII: Characters are only evaluated locally, never stored or sent)
    let digraphFlightTime = null;
    let isCommonDigraph = false;
    const currentChar = (e.key && e.key.length === 1) ? e.key.toLowerCase() : null;

    if (lastKeyChar && currentChar && lastKeyDownTime !== null) {
      const pair = lastKeyChar + currentChar;
      if (COMMON_DIGRAPHS.has(pair)) {
        isCommonDigraph = true;
        digraphFlightTime = Math.max(0, roundToDecimals(now - lastKeyDownTime, 2));
      }
    }
    lastKeyChar = currentChar;
    lastKeyDownTime = now;

    pushTelemetryEvent('keydown', {
      key_flight_time_ms: flightTime,
      digraph_flight_time_ms: digraphFlightTime,
      is_common_digraph: isCommonDigraph,
      route_path: currentRoute
    });
  }, { passive: true });

  window.addEventListener('keyup', function (e) {
    const now = performance.now();
    lastKeyUpTime = now;
    const start = activeKeyDownTimes.get(e.code || e.keyCode);
    let dwellTime = null;
    if (start) {
      dwellTime = Math.max(0, roundToDecimals(now - start, 2));
      activeKeyDownTimes.delete(e.code || e.keyCode);
    }

    pushTelemetryEvent('keyup', {
      key_dwell_time_ms: dwellTime,
      route_path: currentRoute
    });
  }, { passive: true });

  // 2. Pointer Movement & Neuromotor Kinetics (Throttled to 50ms)
  window.addEventListener('pointermove', function (e) {
    pointerMovesBeforeClick++;
    const now = performance.now();
    if (now - lastPointerSample < POINTER_THROTTLE_MS) return;
    lastPointerSample = now;

    pointerCoords.push([
      Math.round(e.clientX),
      Math.round(e.clientY),
      roundToDecimals(Date.now() / 1000.0, 3)
    ]);

    if (pointerCoords.length > 50) {
      pointerCoords.shift();
    }
  }, { passive: true });

  window.addEventListener('pointerdown', function (e) {
    pointerDownTime = performance.now();
    let jerkScore = estimateCurvatureJerk(pointerCoords);
    const isTouch = e.pointerType === 'touch' || ('ontouchstart' in window);

    pushTelemetryEvent('pointerdown', {
      pointer_curvature_jerk: jerkScore,
      pointer_coordinates: pointerCoords.slice(-20),
      mousemove_pre_click_count: pointerMovesBeforeClick,
      is_touch_device: isTouch,
      touch_pressure: roundToDecimals(e.pressure || 0.0, 3),
      touch_radius_x: roundToDecimals(e.width || 0.0, 1),
      route_path: currentRoute
    });
  }, { passive: true });

  window.addEventListener('pointerup', function (e) {
    const now = performance.now();
    let dwellDuration = 50.0;
    if (pointerDownTime !== null) {
      dwellDuration = Math.max(1, roundToDecimals(now - pointerDownTime, 2));
    }
    const preClickMoves = pointerMovesBeforeClick;
    pointerMovesBeforeClick = 0; // Reset for next interaction

    pushTelemetryEvent('pointerdown', {
      click_dwell_duration_ms: dwellDuration,
      mousemove_pre_click_count: preClickMoves,
      route_path: currentRoute
    });
  }, { passive: true });

  // 3. Navigation Route Tracking
  function recordRouteChange(newPath) {
    if (newPath !== currentRoute) {
      const prev = currentRoute;
      currentRoute = newPath;
      pushTelemetryEvent('route_change', {
        route_path: prev + ' -> ' + newPath
      });
    }
  }

  window.addEventListener('popstate', function () {
    recordRouteChange(window.location.pathname);
  });

  // Intercept history.pushState and replaceState
  const origPushState = history.pushState;
  if (origPushState) {
    history.pushState = function () {
      origPushState.apply(this, arguments);
      recordRouteChange(window.location.pathname);
    };
  }

  // 4. Honey-DOM Tripwire Detection
  document.addEventListener('click', function (e) {
    const target = e.target;
    if (target && (target.id === 'honey-dom-profile-sync' || target.getAttribute('data-honey') === 'tripwire')) {
      pushTelemetryEvent('honey_dom_trip', {
        tripwire_id: target.id || '#data-honey-tripwire',
        route_path: currentRoute
      });
    }
  }, true);

  // --- Math Utilities ---
  function roundToDecimals(val, decimals) {
    const factor = Math.pow(10, decimals);
    return Math.round(val * factor) / factor;
  }

  function estimateCurvatureJerk(coords) {
    if (coords.length < 4) return 0.05; // Default organic baseline
    let totalJerk = 0;
    let samples = 0;
    for (let i = 3; i < coords.length; i++) {
      const dt = coords[i][2] - coords[i - 1][2];
      if (dt > 0.001) {
        // d3x/dt3 derivative approximation
        const dx1 = coords[i][0] - coords[i - 1][0];
        const dx0 = coords[i - 1][0] - coords[i - 2][0];
        const d2x = (dx1 - dx0) / dt;
        totalJerk += Math.abs(d2x);
        samples++;
      }
    }
    return samples > 0 ? roundToDecimals(totalJerk / (samples * 1000), 4) : 0.04;
  }

  // --- Periodic Telemetry Flushing ---
  function flushQueue() {
    if (eventQueue.length === 0) return;
    const batch = eventQueue.slice();
    eventQueue = [];

    // Send each packet or batch to Laptop 2
    for (let i = 0; i < batch.length; i++) {
      const packet = batch[i];
      const payloadStr = JSON.stringify(packet);

      if (navigator.sendBeacon && batch.length === 1) {
        const blob = new Blob([payloadStr], { type: 'application/json' });
        navigator.sendBeacon(BACKEND_ENDPOINT, blob);
      } else {
        fetch(BACKEND_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: payloadStr,
          keepalive: true
        }).then(function (resp) {
          return resp.json();
        }).then(function (data) {
          if (data && (data.is_quarantined || data.status === 'quarantined')) {
            window.dispatchEvent(new CustomEvent('shadowgram:quarantined', { detail: data }));
          }
        }).catch(function (err) {
          // Silent local failover: does not crash the client UI
          console.debug('[ShadowGram Telemetry] Ingress offline:', err.message);
        });
      }
    }
  }

  setInterval(flushQueue, FLUSH_INTERVAL_MS);
  window.addEventListener('beforeunload', flushQueue);

  // Expose minimal API for manual trigger or testing
  window.ShadowGramTelemetry = {
    sessionId: sessionId,
    accountId: accountId,
    pushEvent: pushTelemetryEvent,
    flush: flushQueue,
    checkStatus: async function () {
      try {
        const base = BACKEND_ENDPOINT.replace(/\/telemetry$/, '');
        const res = await fetch(base + '/api/session/status?account_id=' + encodeURIComponent(accountId));
        const data = await res.json();
        if (data && (data.is_quarantined || data.status === 'quarantined')) {
          window.dispatchEvent(new CustomEvent('shadowgram:quarantined', { detail: data }));
        }
        return data;
      } catch (e) {
        return null;
      }
    }
  };


  console.log('[ShadowGram] Telemetry SDK initialized for session:', sessionId, 'Account:', accountId);
})(window, document);
