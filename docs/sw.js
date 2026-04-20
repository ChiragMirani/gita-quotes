// Minimal offline service worker for Gita Quotes.
// Caches the static shell + verse data on install. Network-first for HTML so
// updates land quickly; cache-first for assets and the data JSON.

const CACHE = "gita-v2";
const SHELL = [
  "./",
  "./index.html",
  "./about.html",
  "./data.json",
  "./static/styles.css",
  "./manifest.webmanifest",
  "./apple-touch-icon.png",
  "./favicon-192.png",
  "./favicon-512.png",
  "./favicon-32.png",
  "./favicon.ico"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  // HTML: network first, fall back to cache so updates ship fast.
  if (req.headers.get("accept") && req.headers.get("accept").includes("text/html")) {
    event.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
        return res;
      }).catch(() => caches.match(req).then((m) => m || caches.match("./")))
    );
    return;
  }

  // Everything else (CSS, JSON, icons): cache first, network fallback, write-through.
  event.respondWith(
    caches.match(req).then((cached) => cached || fetch(req).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(req, copy));
      return res;
    }))
  );
});
