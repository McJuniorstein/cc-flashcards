/* CC Flashcards service worker — cache the app shell + deck for offline use.
   The cache name embeds a build-time version (replaced by scripts/build_app.py)
   so a new build evicts stale entries automatically. */

const VERSION = "__CACHE_VERSION__";
const CACHE_NAME = `cc-flashcards-${VERSION}`;
const SHELL = [
  "./",
  "./index.html",
  "./app.js",
  "./style.css",
  "./cards.json",
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(names => Promise.all(
        names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;
  // Only handle same-origin requests (CSP is locked to 'self' anyway)
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Stale-while-revalidate for cards.json so a fresh deck shows up on next load
  if (url.pathname.endsWith("/cards.json")) {
    event.respondWith(
      caches.open(CACHE_NAME).then(cache =>
        cache.match(req).then(cached => {
          const network = fetch(req).then(resp => {
            if (resp.ok) cache.put(req, resp.clone());
            return resp;
          }).catch(() => cached);
          return cached || network;
        })
      )
    );
    return;
  }

  // Cache-first for everything else (shell)
  event.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(resp => {
      if (resp.ok && resp.type === "basic") {
        const copy = resp.clone();
        caches.open(CACHE_NAME).then(c => c.put(req, copy));
      }
      return resp;
    }))
  );
});
