/* CC Flashcards — single-file vanilla JS app.
   Budget: < 30KB gzipped. No framework, no router, no third-party deps. */

(() => {
  "use strict";

  const DOMAIN_NAMES = {
    1: "D1 — Security Principles",
    2: "D2 — BC, DR & IR",
    3: "D3 — Access Controls",
    4: "D4 — Network Security",
    5: "D5 — Security Operations",
  };

  const STORAGE = {
    known:  "cc-flashcards.known.v1",
    review: "cc-flashcards.review.v1",
    theme:  "cc-flashcards.theme.v1",
  };

  // --- State -------------------------------------------------------------

  /** @type {Array<{id:string,front:string,back:string,source_doc:string,source_section:?string,source_chain:string[],answer_type:string,primary_domain:number}>} */
  let deck = [];

  let session = {
    queue: /** @type {string[]} */ ([]),  // card ids in play order
    index: 0,
    knownThisSession: /** @type {Set<string>} */ (new Set()),
    reviewThisSession: /** @type {Set<string>} */ (new Set()),
  };

  // --- localStorage helpers ---------------------------------------------

  function loadSet(key) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return new Set();
      const arr = JSON.parse(raw);
      return new Set(Array.isArray(arr) ? arr : []);
    } catch { return new Set(); }
  }
  function saveSet(key, set) {
    try { localStorage.setItem(key, JSON.stringify([...set])); }
    catch { /* full-storage / private-mode — fail silently per UX rules */ }
  }

  const knownIds  = loadSet(STORAGE.known);
  const reviewIds = loadSet(STORAGE.review);

  // --- DOM helpers -------------------------------------------------------

  const $  = (sel, el = document) => el.querySelector(sel);
  const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));

  function show(viewId) {
    $$(".view").forEach(v => v.hidden = (v.id !== viewId));
    if (viewId === "view-study") $("#card").focus();
    if (viewId === "view-setup") $("#main").focus();
  }

  // --- Theme handling ----------------------------------------------------

  function applyTheme(mode) {
    document.documentElement.setAttribute("data-theme", mode);
    const icon = $("[data-theme-icon]");
    if (icon) icon.textContent = mode;
    const btn = $("#theme-toggle");
    if (btn) btn.setAttribute("aria-pressed", mode === "dark" ? "true" : "false");
  }
  function cycleTheme() {
    const cur = localStorage.getItem(STORAGE.theme) || "auto";
    const next = cur === "auto" ? "light" : cur === "light" ? "dark" : "auto";
    localStorage.setItem(STORAGE.theme, next);
    applyTheme(next);
  }
  applyTheme(localStorage.getItem(STORAGE.theme) || "auto");

  // --- Setup view --------------------------------------------------------

  function renderSetupCounts() {
    $("[data-count='all']").textContent     = deck.length;
    $("[data-count='review']").textContent  = reviewIds.size;
    $$("[data-count='known']").forEach(el => el.textContent = knownIds.size);
    $$("[data-count='review']").forEach(el => el.textContent = reviewIds.size);
  }

  function renderDomainGrid() {
    const counts = new Map();
    deck.forEach(c => counts.set(c.primary_domain, (counts.get(c.primary_domain) || 0) + 1));
    const grid = $("#domain-grid");
    grid.innerHTML = "";
    [1, 2, 3, 4, 5].forEach(d => {
      const n = counts.get(d) || 0;
      if (!n) return;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "mode-button";
      btn.dataset.mode = "domain";
      btn.dataset.domain = String(d);
      btn.innerHTML = `<span class="mode-label">${escapeHtml(DOMAIN_NAMES[d])}</span><span class="mode-count">${n}</span>`;
      grid.appendChild(btn);
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
  }

  // --- Session builders --------------------------------------------------

  function startSession(mode, domainFilter) {
    let pool = deck.slice();
    if (mode === "domain") {
      pool = pool.filter(c => c.primary_domain === domainFilter);
    } else if (mode === "review") {
      pool = pool.filter(c => reviewIds.has(c.id));
      if (pool.length === 0) {
        announce("No cards marked for review yet. Mark some as 'Review again' first.");
        return;
      }
    } else if (mode === "random") {
      pool = [pool[Math.floor(Math.random() * pool.length)]];
    }
    // Shuffle for everything except a single-card random
    if (mode !== "random") shuffle(pool);

    session.queue = pool.map(c => c.id);
    session.index = 0;
    session.knownThisSession.clear();
    session.reviewThisSession.clear();
    show("view-study");
    renderCurrentCard();
  }

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // --- Study view --------------------------------------------------------

  function currentCard() {
    const id = session.queue[session.index];
    return deck.find(c => c.id === id);
  }

  function renderCurrentCard() {
    const card = currentCard();
    if (!card) { finishSession(); return; }
    const root = $("#card");
    root.dataset.face = "front";
    $("[data-card='front']").textContent  = card.front;
    $("[data-card='back']").textContent   = card.back;
    $("[data-card='source']").textContent = formatSource(card);
    $("[data-card='chain']").textContent  = (card.source_chain || []).join(" → ");
    const at = $("[data-card='answer-type']");
    at.textContent = card.answer_type;
    at.dataset.type = card.answer_type;
    $("[data-meta='position']").textContent =
      `Card ${session.index + 1} of ${session.queue.length}`;
    $("[data-meta='domain']").textContent = DOMAIN_NAMES[card.primary_domain] || "";
    root.focus();
  }

  function formatSource(card) {
    let s = card.source_doc;
    if (card.source_section) s += `, ${card.source_section}`;
    return s;
  }

  function flipCard() {
    const root = $("#card");
    root.dataset.face = root.dataset.face === "front" ? "back" : "front";
  }

  function mark(kind) {
    const card = currentCard();
    if (!card) return;
    if (kind === "known") {
      knownIds.add(card.id);
      reviewIds.delete(card.id);
      session.knownThisSession.add(card.id);
    } else {
      reviewIds.add(card.id);
      knownIds.delete(card.id);
      session.reviewThisSession.add(card.id);
    }
    saveSet(STORAGE.known, knownIds);
    saveSet(STORAGE.review, reviewIds);
    advance();
  }

  function advance() {
    session.index += 1;
    if (session.index >= session.queue.length) finishSession();
    else renderCurrentCard();
  }

  function finishSession() {
    $("[data-done='known']").textContent  = session.knownThisSession.size;
    $("[data-done='review']").textContent = session.reviewThisSession.size;
    renderSetupCounts();
    show("view-done");
  }

  // --- Keyboard ----------------------------------------------------------

  function onKey(e) {
    const studying = !$("#view-study").hidden;
    if (!studying) return;
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    if (e.key === " " || e.key === "Enter") { e.preventDefault(); flipCard(); }
    else if (e.key === "k" || e.key === "K") { e.preventDefault(); mark("known"); }
    else if (e.key === "r" || e.key === "R") { e.preventDefault(); mark("review"); }
    else if (e.key === "Escape") { show("view-setup"); }
  }

  // --- Announcer for live regions ---------------------------------------

  function announce(msg) {
    let live = document.getElementById("live-region");
    if (!live) {
      live = document.createElement("p");
      live.id = "live-region";
      live.className = "visually-hidden";
      live.setAttribute("aria-live", "assertive");
      document.body.appendChild(live);
    }
    live.textContent = "";
    setTimeout(() => { live.textContent = msg; }, 50);
  }

  // --- Wire up event listeners -------------------------------------------

  function bindEvents() {
    // Mode buttons (event delegation; covers dynamically-added domain buttons too)
    $("#main").addEventListener("click", e => {
      const btn = e.target.closest(".mode-button");
      if (!btn) return;
      const mode = btn.dataset.mode;
      const domain = btn.dataset.domain ? Number(btn.dataset.domain) : undefined;
      startSession(mode === "domain" ? "domain" : mode, domain);
    });

    $("#theme-toggle").addEventListener("click", cycleTheme);

    $("#card").addEventListener("click", flipCard);
    $("#flip-card").addEventListener("click", flipCard);
    $("#mark-known").addEventListener("click", () => mark("known"));
    $("#mark-review").addEventListener("click", () => mark("review"));

    $("#exit-session").addEventListener("click", () => show("view-setup"));
    $("#study-again").addEventListener("click", () => show("view-setup"));

    $("#reset-progress").addEventListener("click", () => {
      if (!confirm("Reset all Known and Review-again markings? This can't be undone.")) return;
      knownIds.clear();
      reviewIds.clear();
      saveSet(STORAGE.known, knownIds);
      saveSet(STORAGE.review, reviewIds);
      renderSetupCounts();
      announce("Progress reset.");
    });

    document.addEventListener("keydown", onKey);
  }

  // --- Boot --------------------------------------------------------------

  async function boot() {
    try {
      const resp = await fetch("cards.json", { cache: "no-cache" });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      deck = await resp.json();
    } catch (err) {
      $("#view-setup").innerHTML = `
        <h2>Cards failed to load.</h2>
        <p>Reload the page once you're back online. Error: ${escapeHtml(String(err))}</p>
      `;
      return;
    }
    renderSetupCounts();
    renderDomainGrid();
    bindEvents();
    show("view-setup");

    // Service worker registration (non-blocking; failures are logged not surfaced)
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("service-worker.js").catch(() => {});
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
