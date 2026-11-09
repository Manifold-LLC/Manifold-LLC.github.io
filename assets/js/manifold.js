/* Manifold LLC - the hero drawing as a live model, with a four-step lesson. No dependencies. */
(function () {
  "use strict";
  var fig = document.getElementById("manifold");
  if (!fig || !window.HTMLCanvasElement) return;
  var stage = fig.querySelector(".manifold-stage");
  var img = stage && stage.querySelector("img");
  var caption = fig.querySelector("figcaption");
  if (!stage || !img || !caption) return;

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ink = "#16181d", accent = "#1e3a5f", warn = "#8a3b1f", tint = "rgba(30,58,95,0.10)";

  // The same surface as scripts/surface.py, so the still drawing and the live one agree.
  function z(u, v) { return 0.70 * Math.sin(1.15 * u) * Math.cos(0.85 * v) + 0.20 * Math.sin(2.1 * u + 0.7 * v) - 0.10 * u * v; }
  var U0 = -2.4, U1 = 2.4, V0 = -1.9, V1 = 1.9;
  var view = { elev: 1.12, azim: 0.50, zoom: 1, focus: null };
  var ZOOM = 2.6;
  // One camera per step: azimuth, elevation, zoom. The zoom centres on the highlighted sample, or on the stray point in step 4.
  var CAM = [
    { a: 0.50, e: 1.12, z: 1.0 },
    { a: 0.85, e: 1.00, z: 1.25 },
    { a: 0.70, e: 1.05, z: ZOOM },
    { a: 1.20, e: 0.98, z: 1.0 },
    { a: 0.15, e: 0.72, z: 1.35 }
  ];
  function rot(x, y, zz) {
    var ca = Math.cos(view.azim), sa = Math.sin(view.azim);
    var x1 = x * ca - y * sa, y1 = x * sa + y * ca;
    var ce = Math.cos(view.elev), se = Math.sin(view.elev);
    return [x1, y1 * ce - zz * se, y1 * se + zz * ce]; // [screen x, depth, screen y]
  }

  var steps = [
    { label: "The drawing", text: "A two-dimensional manifold, drawn as a wire grid. Drag to turn it, then use the arrows to step through a short lesson." },
    { label: "Data", text: "Data lives on a surface. Images, signals and text are high-dimensional, but real examples sit near a thin, curved surface inside that space: the data manifold. A model's job is to learn that surface from samples." },
    { label: "Up close", text: "Up close, it looks flat. Move in on any sample and the surface is nearly a plane, so a model interpolates well between examples it has seen. Most demos live here." },
    { label: "Far away", text: "Far away, it bends. Extend the flat patch and it points into empty space, but a model asked about a region it never saw answers with the same confidence. That is extrapolation, and it is where programs get hurt." },
    { label: "Off the surface", text: "Some inputs are not on the surface at all: a new sensor, a different theater, a corrupted file. The model still returns an answer. Scoring against data it never saw, from the places it will actually be used, is how you find out." }
  ];
  var step = 0, fadeT = null;

  // Build the stage: canvas replaces the still image; buttons and a live caption follow it.
  var canvas = document.createElement("canvas");
  canvas.setAttribute("role", "img");
  canvas.setAttribute("tabindex", "0");
  canvas.setAttribute("aria-label", "Wire-grid drawing of a curved surface. Drag to turn it, or use shift with the left and right arrow keys and the up and down keys.");
  stage.appendChild(canvas);
  img.hidden = true; img.style.display = "none";
  var ctx = canvas.getContext("2d");

  // A stepper: previous and next arrows with the step name between them. Left and right keys step too.
  var nav = document.createElement("div");
  nav.className = "lesson";
  nav.setAttribute("aria-label", "A short lesson on the data manifold");
  function arrow(dir, label) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "lesson-arrow"; b.setAttribute("aria-label", label);
    b.innerHTML = dir < 0 ? "&larr;" : "&rarr;";
    b.addEventListener("click", function () { setStep(step + dir); });
    return b;
  }
  var prev = arrow(-1, "Previous step"), next = arrow(1, "Next step");
  var title = document.createElement("span"); title.className = "lesson-title";
  var num = document.createElement("span"); num.className = "n";
  var name = document.createElement("span");
  title.appendChild(num); title.appendChild(name);
  nav.appendChild(prev); nav.appendChild(title); nav.appendChild(next);
  caption.textContent = "";
  var text = document.createElement("p");
  text.className = "lesson-text";
  text.setAttribute("aria-live", "polite");
  caption.appendChild(nav); caption.appendChild(text);
  fig.addEventListener("keydown", function (e) {
    if (e.target === canvas && e.shiftKey) return; // shift plus arrows turns the surface, below
    if (e.key === "ArrowRight") { setStep(step + 1); e.preventDefault(); }
    else if (e.key === "ArrowLeft") { setStep(step - 1); e.preventDefault(); }
  });

  function setStep(i) {
    if (i < 0 || i >= steps.length) return;
    step = i;
    num.textContent = i ? ("0" + i + " / 0" + (steps.length - 1)) : "";
    name.textContent = steps[i].label;
    prev.disabled = i === 0; next.disabled = i === steps.length - 1;
    // Cross-fade the text under the arrows in step with the camera move.
    text.classList.add("is-fading");
    clearTimeout(fadeT);
    fadeT = setTimeout(function () { text.textContent = steps[i].text; text.classList.remove("is-fading"); }, reduced ? 0 : 200);
    var c = CAM[i];
    go(c.a, c.e, c.z, i === 4 ? [TOP[0], TOP[1], z(TOP[0], TOP[1]) + 0.45] : [P[0], P[1], z(P[0], P[1])]);
  }

  // Deterministic sample points on the surface.
  var seed = 7; function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
  var samples = []; for (var k = 0; k < 44; k++) { var su = U0 + 0.3 + (U1 - U0 - 0.6) * rnd(), sv = V0 + 0.3 + (V1 - V0 - 0.6) * rnd(); samples.push([su, sv, z(su, sv)]); }
  var P = [0.35, -0.25]; // the sample we zoom in on
  var DU = 1.45, DV = 0.4;
  var FAR, TOP;
  function tangent(u, v, du, dv) { var h = 1e-3; var zu = (z(u + h, v) - z(u - h, v)) / (2 * h), zv = (z(u, v + h) - z(u, v - h)) / (2 * h); return [u + du, v + dv, z(u, v) + zu * du + zv * dv]; }

  FAR = tangent(P[0], P[1], DU, DV); TOP = [-0.6, 1.0, z(-0.6, 1.0) + 0.9];
  var W, H, sc, ox, oy, dpr;
  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var r = stage.getBoundingClientRect(); W = Math.max(1, Math.round(r.width)); H = Math.round(W * 620 / 760);
    canvas.width = W * dpr; canvas.height = H * dpr; canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }
  function proj(p) { var r = rot(p[0], p[1], p[2]); return [ox + r[0] * sc, oy - r[2] * sc, r[1]]; }

  function draw() {
    // Fit the rotated grid into the canvas on every frame.
    var lines = [], i, j, n = 44, nu = 22, nv = 15;
    for (i = 0; i <= nu; i++) { var u = U0 + (U1 - U0) * i / nu, L = []; for (j = 0; j <= n; j++) { var v = V0 + (V1 - V0) * j / n; L.push(rot(u, v, z(u, v))); } lines.push(L); }
    for (j = 0; j <= nv; j++) { var vv = V0 + (V1 - V0) * j / nv, M = []; for (i = 0; i <= n; i++) { var uu = U0 + (U1 - U0) * i / n; M.push(rot(uu, vv, z(uu, vv))); } lines.push(M); }
    var x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, d0 = 1e9, d1 = -1e9;
    lines.forEach(function (L) { L.forEach(function (p) { if (p[0] < x0) x0 = p[0]; if (p[0] > x1) x1 = p[0]; if (p[2] < y0) y0 = p[2]; if (p[2] > y1) y1 = p[2]; if (p[1] < d0) d0 = p[1]; if (p[1] > d1) d1 = p[1]; }); });
    var extra = step === 3 ? [FAR, tangent(P[0], P[1], DU + 0.1, DV + 0.2), tangent(P[0], P[1], DU + 0.1, -DV - 0.2)] : step === 4 ? [TOP] : [];
    extra.forEach(function (q) { var r = rot(q[0], q[1], q[2]); if (r[0] < x0) x0 = r[0]; if (r[0] > x1) x1 = r[0]; if (r[2] < y0) y0 = r[2]; if (r[2] > y1) y1 = r[2]; });
    var fit = extra.length ? 0.84 : 0.92;
    sc = Math.min(W * fit / (x1 - x0), H * fit / (y1 - y0)); ox = W / 2 - (x0 + x1) / 2 * sc; oy = H / 2 + (y0 + y1) / 2 * sc;
    if (view.zoom > 1) { // zoom toward the highlighted sample, keeping it at the centre
      var fp = view.focus || [P[0], P[1], z(P[0], P[1])];
      var f = rot(fp[0], fp[1], fp[2]), t = Math.min(1, (view.zoom - 1) / (ZOOM - 1) * 1.6);
      var fx = ox + f[0] * sc, fy = oy - f[2] * sc;
      sc *= view.zoom; ox = fx + (ox - fx) * view.zoom; oy = fy + (oy - fy) * view.zoom;
      ox += (W / 2 - fx) * t; oy += (H / 2 - fy) * t;
    }
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    lines.map(function (L) { var d = 0; L.forEach(function (p) { d += p[1]; }); return { d: d / L.length, L: L }; })
      .sort(function (a, b) { return b.d - a.d; })
      .forEach(function (o) {
        var t = (o.d - d0) / (d1 - d0 + 1e-9);
        ctx.globalAlpha = 0.95 - 0.67 * t; ctx.lineWidth = 1.15 - 0.65 * t; ctx.strokeStyle = ink;
        ctx.beginPath(); o.L.forEach(function (p, k) { var X = ox + p[0] * sc, Y = oy - p[2] * sc; if (k) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }); ctx.stroke();
      });
    ctx.globalAlpha = 1;
    if (step >= 1) samples.forEach(function (s) { dot(proj(s), 2.6, accent); });
    if (step === 2) { patch(0.32, 0.26); dot(proj([P[0], P[1], z(P[0], P[1])]), 4.5, accent); }
    if (step === 3) {
      patch(DU + 0.1, DV + 0.2);
      var far = FAR, truth = [far[0], far[1], z(far[0], far[1])];
      dashed(proj(far), proj(truth), warn);
      dot(proj(truth), 3.2, ink); ring(proj(far), 5, warn);
      tag(proj(far), "what the model says", warn, -10); tag(proj(truth), "what is true", ink, 16);
      dot(proj([P[0], P[1], z(P[0], P[1])]), 4.5, accent);
    }
    if (step === 4) {
      var top = TOP, base = [top[0], top[1], z(top[0], top[1])];
      dashed(proj(top), proj(base), warn); ring(proj(top), 6, warn); tag(proj(top), "not on the surface", warn, -10);
    }
    canvas.setAttribute("aria-label", "Wire-grid drawing of a curved surface. " + steps[step].text);
  }
  function dot(p, r, c) { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, 6.2832); ctx.fill(); }
  function ring(p, r, c) { ctx.strokeStyle = c; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, 6.2832); ctx.stroke(); }
  function dashed(a, b, c) { ctx.save(); ctx.strokeStyle = c; ctx.lineWidth = 1.2; ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); ctx.restore(); }
  function tag(p, s, c, dy) {
    ctx.font = "500 11px 'IBM Plex Mono', ui-monospace, monospace"; ctx.fillStyle = c;
    var w = ctx.measureText(s).width, left = p[0] + 10 + w > W - 4;
    var y = p[1] + (dy || -8); if (y < 14) y = p[1] + 18;
    ctx.textAlign = left ? "right" : "left"; ctx.fillText(s, left ? p[0] - 10 : p[0] + 10, y); ctx.textAlign = "left";
  }
  function patch(du, dv) {
    var c = [tangent(P[0], P[1], -0.3, -dv), tangent(P[0], P[1], du, -dv), tangent(P[0], P[1], du, dv), tangent(P[0], P[1], -0.3, dv)].map(proj);
    ctx.fillStyle = tint; ctx.strokeStyle = accent; ctx.lineWidth = 1;
    ctx.beginPath(); c.forEach(function (p, k) { if (k) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]); }); ctx.closePath(); ctx.fill(); ctx.stroke();
  }

  // Turning: pointer drag, arrow keys, and short animated moves between steps.
  var drag = null, anim = null;
  canvas.style.touchAction = "none";
  canvas.addEventListener("pointerdown", function (e) { stopAnim(); drag = { x: e.clientX, y: e.clientY, a: view.azim, el: view.elev }; canvas.setPointerCapture(e.pointerId); canvas.classList.add("is-dragging"); });
  canvas.addEventListener("pointermove", function (e) { if (!drag) return; view.azim = drag.a + (e.clientX - drag.x) * 0.008; view.elev = clamp(drag.el + (e.clientY - drag.y) * 0.006); draw(); });
  function end() { drag = null; canvas.classList.remove("is-dragging"); }
  canvas.addEventListener("pointerup", end); canvas.addEventListener("pointercancel", end);
  canvas.addEventListener("keydown", function (e) {
    var k = e.key;
    if (k === "ArrowUp") view.elev = clamp(view.elev - 0.06); else if (k === "ArrowDown") view.elev = clamp(view.elev + 0.06);
    else if (e.shiftKey && k === "ArrowLeft") view.azim -= 0.08; else if (e.shiftKey && k === "ArrowRight") view.azim += 0.08; else return;
    stopAnim(); e.preventDefault(); e.stopPropagation(); draw();
  });
  function clamp(x) { return Math.max(0.25, Math.min(1.5, x)); }
  function stopAnim() { if (anim) { cancelAnimationFrame(anim); anim = null; } }
  function go(a, el, zm, focus) {
    stopAnim();
    if (focus) view.focus = focus;
    if (reduced) { view.azim = a; view.elev = clamp(el); view.zoom = zm; draw(); return; }
    var a0 = view.azim, e0 = view.elev, z0 = view.zoom, t0 = null;
    function frame(ts) { if (!t0) t0 = ts; var t = Math.min(1, (ts - t0) / 1100), s = t * t * (3 - 2 * t); view.azim = a0 + (a - a0) * s; view.elev = clamp(e0 + (el - e0) * s); view.zoom = z0 + (zm - z0) * s; draw(); if (t < 1) anim = requestAnimationFrame(frame); }
    anim = requestAnimationFrame(frame);
  }

  window.addEventListener("resize", size);
  size(); setStep(0);
})();
