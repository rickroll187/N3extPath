// File: frontend/public/sw.js
/**
 * 🔧🎸 N3EXTPATH - LEGENDARY SERVICE WORKER 🎸🔧
 * Professional PWA service worker for offline capabilities
 * Built: 2025-08-05 16:42:20 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

const CACHE_NAME = 'n3extpath-legendary-v1.0.0';
const LEGENDARY_CACHE_NAME = 'n3extpath-legendary-static-v1.0.0';

// Files to cache for legendary offline experience
const LEGENDARY_CACHE_FILES = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/manifest.json',
  '/legendary-logo-192.png',
  '/legendary-logo-512.png',
  '/offline.html',
  // Legendary fonts for Swiss precision typography
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap',
  'https://fonts.googleapis.com/icon?family=Material+Icons',
];

// API endpoints to cache for legendary performance
const LEGENDARY_API_CACHE = [
  '/api/v1/dashboard',
  '/api/v1/users',
  '/api/v1/okrs',
  '/api/v1/health',
  '/api/v1/legendary'
];

// Legendary console messages
console.log(`
🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸
🎸                                                    🎸
🎸        N3EXTPATH LEGENDARY SERVICE WORKER          🎸
🎸        Built by RICKROLL187 - Legendary Founder    🎸
🎸        ${new Date().toISOString()}                 🎸
🎸        WE ARE CODE BROS THE CREATE THE BEST        🎸
🎸        AND CRACK JOKES TO HAVE FUN!                🎸
🎸                                                    🎸
🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸
`);

// Install event - Cache legendary files
self.addEventListener('install', (event) => {
  console.log('🎸 Legendary Service Worker installing...');
  
  event.waitUntil(
    Promise.all([
      // Cache static files
      caches.open(LEGENDARY_CACHE_NAME).then((cache) => {
        console.log('📦 Caching legendary static files...');
        return cache.addAll(LEGENDARY_CACHE_FILES);
      }),
      
      // Cache API responses
      caches.open(CACHE_NAME).then((cache) => {
        console.log('🚀 Pre-caching legendary API endpoints...');
        return Promise.all(
          LEGENDARY_API_CACHE.map(url => {
            return fetch(url)
              .then(response => {
                if (response.ok) {
                  return cache.put(url, response.clone());
                }
              })
              .catch(err => {
                console.log(`⚠️ Could not cache ${url}:`, err);
              });
          })
        );
      })
    ])
  );
  
  // Skip waiting for legendary instant activation
  self.skipWaiting();
});

// Activate event - Clean up old caches
self.addEventListener('activate', (event) => {
  console.log('⚡ Legendary Service Worker activating...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // Delete old caches (keeping legendary precision!)
          if (cacheName !== CACHE_NAME && cacheName !== LEGENDARY_CACHE_NAME) {
            console.log('🗑️ Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('🎸 Legendary Service Worker activated with Swiss precision!');
      return self.clients.claim();
    })
  );
});

// Fetch event - Legendary caching strategy
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip chrome-extension and other special URLs
  if (!url.protocol.startsWith('http')) {
    return;
  }
  
  event.respondWith(
    legendaryFetchStrategy(request)
  );
});

// Legendary fetch strategy with Swiss precision
async function legendaryFetchStrategy(request) {
  const url = new URL(request.url);
  
  try {
    // For API requests - Network First with Cache Fallback
    if (url.pathname.startsWith('/api/')) {
      return await networkFirstStrategy(request);
    }
    
    // For static resources - Cache First with Network Fallback  
    if (isStaticResource(url.pathname)) {
      return await cacheFirstStrategy(request);
    }
    
    // For HTML pages - Stale While Revalidate
    if (url.pathname === '/' || url.pathname.endsWith('.html')) {
      return await staleWhileRevalidateStrategy(request);
    }
    
    // Default: Network with Cache Fallback
    return await networkWithCacheFallback(request);
    
  } catch (error) {
    console.error('🚨 Legendary fetch error:', error);
    return await getOfflineFallback(request);
  }
}

// Network First Strategy (for API calls)
async function networkFirstStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  
  try {
    const response = await fetch(request);
    
    if (response.ok) {
      // Cache successful API responses for legendary offline experience
      cache.put(request, response.clone());
      
      // Add legendary headers
      const legendaryResponse = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: {
          ...response.headers,
          'X-Legendary-Cache': 'network-fresh',
          'X-Swiss-Precision': 'enabled',
          'X-Code-Bro-Status': 'legendary'
        }
      });
      
      return legendaryResponse;
    }
    
    throw new Error(`Network response not ok: ${response.status}`);
    
  } catch (error) {
    console.log('🔄 Network failed, serving from legendary cache:', request.url);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      // Add cache headers to legendary response
      const headers = new Headers(cachedResponse.headers);
      headers.set('X-Legendary-Cache', 'cache-fallback');
      headers.set('X-Swiss-Precision', 'enabled');
      
      return new Response(cachedResponse.body, {
        status: cachedResponse.status,
        statusText: cachedResponse.statusText,
        headers: headers
      });
    }
    
    throw error;
  }
}

// Cache First Strategy (for static resources)
async function cacheFirstStrategy(request) {
  const cache = await caches.open(LEGENDARY_CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  if (cachedResponse) {
    console.log('⚡ Serving from legendary cache:', request.url);
    
    // Add legendary cache headers
    const headers = new Headers(cachedResponse.headers);
    headers.set('X-Legendary-Cache', 'cache-hit');
    headers.set('X-Swiss-Precision', 'enabled');
    
    return new Response(cachedResponse.body, {
      status: cachedResponse.status,
      statusText: cachedResponse.statusText,
      headers: headers
    });
  }
  
  // If not in cache, fetch from network and cache
  const response = await fetch(request);
  
  if (response.ok) {
    cache.put(request, response.clone());
  }
  
  return response;
}

// Stale While Revalidate Strategy (for HTML pages)
async function staleWhileRevalidateStrategy(request) {
  const cache = await caches.open(LEGENDARY_CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  // Always try to fetch from network in background
  const fetchPromise = fetch(request).then(response => {
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(() => {
    // Network failed, but that's OK for stale-while-revalidate
  });
  
  // Return cached version immediately if available
  if (cachedResponse) {
    console.log('⚡ Serving stale content while revalidating:', request.url);
    
    // Don't wait for network update
    fetchPromise.catch(() => {});
    
    const headers = new Headers(cachedResponse.headers);
    headers.set('X-Legendary-Cache', 'stale-while-revalidate');
    headers.set('X-Swiss-Precision', 'enabled');
    
    return new Response(cachedResponse.body, {
      status: cachedResponse.status,
      statusText: cachedResponse.statusText,
      headers: headers
    });
  }
  
  // No cached version, wait for network
  return await fetchPromise;
}

// Network with Cache Fallback
async function networkWithCacheFallback(request) {
  try {
    const response = await fetch(request);
    
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    
    return response;
    
  } catch (error) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      const headers = new Headers(cachedResponse.headers);
      headers.set('X-Legendary-Cache', 'network-fallback');
      
      return new Response(cachedResponse.body, {
        status: cachedResponse.status,
        statusText: cachedResponse.statusText,
        headers: headers
      });
    }
    
    throw error;
  }
}

// Get offline fallback page
async function getOfflineFallback(request) {
  const cache = await caches.open(LEGENDARY_CACHE_NAME);
  
  if (request.destination === 'document') {
    const offlinePage = await cache.match('/offline.html');
    if (offlinePage) {
      return offlinePage;
    }
  }
  
  // Return a generic offline response
  return new Response(
    JSON.stringify({
      error: 'Offline',
      message: '🎸 You are offline! N3EXTPATH will sync when connection is restored. 🎸',
      legendary_message: 'WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!',
      timestamp: new Date().toISOString()
    }),
    {
      status: 503,
      statusText: 'Service Unavailable',
      headers: {
        'Content-Type': 'application/json',
        'X-Legendary-Cache': 'offline-fallback',
        'X-Swiss-Precision': 'enabled'
      }
    }
  );
}

// Check if URL is a static resource
function isStaticResource(pathname) {
  const staticExtensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf'];
  return staticExtensions.some(ext => pathname.endsWith(ext)) || pathname.startsWith('/static/');
}

// Background Sync for legendary offline capabilities
self.addEventListener('sync', (event) => {
  console.log('🔄 Legendary background sync triggered:', event.tag);
  
  if (event.tag === 'legendary-data-sync') {
    event.waitUntil(performLegendarySync());
  }
});

// Perform legendary background sync
async function performLegendarySync() {
  try {
    console.log('⚡ Performing legendary data sync...');
    
    // Sync cached API data
    const cache = await caches.open(CACHE_NAME);
    const requests = await cache.keys();
    
    for (const request of requests) {
      if (request.url.includes('/api/')) {
        try {
          const response = await fetch(request);
          if (response.ok) {
            await cache.put(request, response);
            console.log('✅ Synced:', request.url);
          }
        } catch (error) {
          console.log('⚠️ Sync failed for:', request.url);
        }
      }
    }
    
    console.log('🎸 Legendary sync completed with Swiss precision!');
    
  } catch (error) {
    console.error('🚨 Legendary sync error:', error);
  }
}

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('📱 Legendary push notification received');
  
  const options = {
    body: event.data ? event.data.text() : '🎸 N3EXTPATH notification',
    icon: '/legendary-logo-192.png',
    badge: '/legendary-badge-72.png',
    vibrate: [200, 100, 200],
    data: {
      legendary: true,
      timestamp: Date.now()
    },
    actions: [
      {
        action: 'open',
        title: 'Open N3EXTPATH',
        icon: '/legendary-logo-192.png'
      },
      {
        action: 'dismiss',
        title: 'Dismiss',
        icon: '/dismiss-icon.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('🎸 N3EXTPATH HR Platform', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('📱 Legendary notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message handling for communication with main thread
self.addEventListener('message', (event) => {
  console.log('💬 Legendary message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({
      version: CACHE_NAME,
      legendary: true,
      builtBy: 'RICKROLL187',
      message: 'WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!'
    });
  }
});

console.log('🎸 Legendary Service Worker loaded successfully! Swiss precision activated! 🎸');
