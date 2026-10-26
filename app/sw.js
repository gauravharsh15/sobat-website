// Sobat web app service worker. Pages: network first, the saved copy only
// when offline, so an update is never hidden. Built files have content
// hashes in their names, so they're cached once and reused. Nothing else
// (the database, Google) is touched.
const CACHE = 'sobat-app-v1';
const SHELL = '/app/';

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.add(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== self.location.origin || !url.pathname.startsWith('/app/')) return;
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(SHELL, copy));
          return res;
        })
        .catch(() => caches.match(SHELL)),
    );
    return;
  }
  if (url.pathname.startsWith('/app/_expo/') || url.pathname.startsWith('/app/assets/') || url.pathname.startsWith('/app/icons/')) {
    event.respondWith(
      caches.match(req).then((hit) => hit || fetch(req).then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      })),
    );
  }
});

// Browser notifications (lib/web-push.ts, sent by the web-push Edge
// Function): show them, and open their ride when tapped.
self.addEventListener('push', (event) => {
  let m = {};
  try {
    m = event.data ? event.data.json() : {};
  } catch {
    m = { body: event.data ? event.data.text() : '' };
  }
  event.waitUntil(
    self.registration.showNotification(m.title || 'Sobat', {
      body: m.body || '',
      icon: '/app/icons/icon-192.png',
      badge: '/app/icons/icon-192.png',
      data: { url: m.url || '/home' },
    }),
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const target = '/app' + ((event.notification.data && event.notification.data.url) || '/home');
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windows) => {
      const open = windows.find((w) => new URL(w.url).pathname.startsWith('/app'));
      if (open) return open.focus().then(() => open.navigate(target));
      return self.clients.openWindow(target);
    }),
  );
});
