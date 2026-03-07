const CACHE_NAME = 'adhd-streak-v1';
const ASSETS = ['/', '/index.html', '/manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).catch(() => caches.match('/index.html')))
  );
});

// Push notifications for habit reminders
self.addEventListener('push', e => {
  const data = e.data?.json() || { title: 'ADHD-Streak', body: 'Time to check in your habits!' };
  e.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icon-192.png',
      badge: '/icon-192.png',
      tag: 'habit-reminder',
      renotify: true,
      actions: [
        { action: 'checkin', title: 'Check In' },
        { action: 'snooze', title: 'Snooze 1hr' }
      ]
    })
  );
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  if (e.action === 'checkin') {
    e.waitUntil(clients.openWindow('/?action=checkin'));
  }
});
