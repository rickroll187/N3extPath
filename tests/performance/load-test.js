// File: tests/performance/load-test.js
/**
 * ⚡🎸 N3EXTPATH - LEGENDARY LOAD TESTING 🎸⚡
 * Professional performance testing with Swiss precision
 * Built: 2025-08-05 19:17:18 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import http from 'k6/http';
import ws from 'k6/ws';
import { check, group, sleep, fail } from 'k6';
import { Rate, Trend, Counter, Gauge } from 'k6/metrics';
import { SharedArray } from 'k6/data';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

// 🎸 LEGENDARY METRICS CONFIGURATION 🎸
const legendaryErrorRate = new Rate('legendary_errors');
const swissPrecisionTrend = new Trend('swiss_precision_response_time');
const codeBroCounter = new Counter('code_bro_requests');
const rickroll187Gauge = new Gauge('rickroll187_success_rate');

// Test configuration with legendary settings
export const options = {
  stages: [
    // Warm-up with Swiss precision
    { duration: '2m', target: 20 },   // Warm-up
    { duration: '5m', target: 100 },  // Ramp-up to normal load
    { duration: '10m', target: 100 }, // Stay at normal load
    { duration: '3m', target: 200 },  // Spike test
    { duration: '2m', target: 200 },  // Hold spike
    { duration: '5m', target: 50 },   // Scale down
    { duration: '2m', target: 0 },    // Cool down
  ],
  
  // Legendary performance thresholds
  thresholds: {
    // 🎸 LEGENDARY PERFORMANCE REQUIREMENTS 🎸
    'http_req_duration': ['p(95)<2000', 'p(99)<5000'], // Swiss precision response times
    'http_req_failed': ['rate<0.05'], // 95% success rate minimum
    'legendary_errors': ['rate<0.01'], // Legendary error rate < 1%
    'code_bro_requests': ['count>1000'], // Minimum code bro requests
    'rickroll187_success_rate': ['value>0.99'], // RICKROLL187 success rate > 99%
  },
  
  // Test scenarios
  scenarios: {
    // Basic load test
    legendary_load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 50 },
        { duration: '10m', target: 50 },
        { duration: '5m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
    
    // Spike test for legendary resilience
    swiss_precision_spike: {
      executor: 'ramping-vus',
      startTime: '20m',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 300 },
        { duration: '5m', target: 300 },
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
    
    // RICKROLL187 exclusive test
    rickroll187_exclusive: {
      executor: 'constant-vus',
      vus: 5,
      duration: '30m',
      exec: 'legendaryUserTest',
    },
    
    // WebSocket test
    websocket_legendary: {
      executor: 'constant-vus',
      vus: 10,
      duration: '10m',
      exec: 'websocketTest',
    },
  },
};

// 🎸 TEST DATA WITH LEGENDARY USERS 🎸
const testUsers = new SharedArray('test_users', function () {
  return [
    // Regular users
    { username: 'test_user_1', password: 'TestPass123!', type: 'regular' },
    { username: 'test_user_2', password: 'TestPass123!', type: 'regular' },
    { username: 'test_user_3', password: 'TestPass123!', type: 'regular' },
    
    // Legendary user
    { username: 'rickroll187', password: 'LegendaryPass123!', type: 'legendary' },
    
    // Manager users
    { username: 'manager_1', password: 'ManagerPass123!', type: 'manager' },
    { username: 'hr_manager_1', password: 'HRPass123!', type: 'hr_manager' },
  ];
});

// Base URL configuration
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const WS_URL = __ENV.WS_URL || 'ws://localhost:8000/ws';

// 🎸 LEGENDARY UTILITY FUNCTIONS 🎸
function getRandomUser() {
  return testUsers[Math.floor(Math.random() * testUsers.length)];
}

function getLegendaryUser() {
  return testUsers.find(user => user.type === 'legendary');
}

function logLegendaryMetric(metric, value, isLegendary = false) {
  if (isLegendary) {
    console.log(`🎸 LEGENDARY METRIC: ${metric} = ${value} 🎸`);
  }
}

function checkSwissPrecision(response, testName) {
  const responseTime = response.timings.duration;
  swissPrecisionTrend.add(responseTime);
  
  const isSwissPrecision = responseTime < 1000; // < 1 second = Swiss precision
  
  if (isSwissPrecision) {
    console.log(`⚡ Swiss Precision achieved in ${testName}: ${responseTime}ms`);
  }
  
  return isSwissPrecision;
}

// 🎸 AUTHENTICATION HELPERS 🎸
function authenticate(user) {
  const loginResponse = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify({
    username: user.username,
    password: user.password,
    remember_me: false,
  }), {
    headers: {
      'Content-Type': 'application/json',
      'X-Test-Run': 'legendary-load-test',
      'X-Swiss-Precision': 'enabled',
    },
  });

  const authSuccess = check(loginResponse, {
    'authentication successful': (r) => r.status === 200,
    'auth response time < 2s': (r) => r.timings.duration < 2000,
  });

  if (!authSuccess) {
    legendaryErrorRate.add(1);
    fail(`Authentication failed for ${user.username}`);
  }

  const authData = loginResponse.json();
  const accessToken = authData.access_token;
  
  // Special handling for legendary users
  if (user.type === 'legendary') {
    logLegendaryMetric('legendary_auth_success', 1, true);
    rickroll187Gauge.add(1);
    
    check(loginResponse, {
      'legendary user authenticated': (r) => authData.user && authData.user.is_legendary === true,
      'legendary token received': (r) => accessToken && accessToken.length > 0,
    });
  }

  return accessToken;
}

// 🎸 MAIN LOAD TEST FUNCTION 🎸
export default function loadTest() {
  group('🎸 Legendary Load Test Suite', function () {
    const user = getRandomUser();
    const accessToken = authenticate(user);
    codeBroCounter.add(1);

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      'X-Test-User-Type': user.type,
    };

    // Add legendary headers for legendary users
    if (user.type === 'legendary') {
      headers['X-Legendary-User'] = 'true';
      headers['X-Swiss-Precision'] = 'maximum';
      headers['X-Code-Bro-Energy'] = 'infinite';
    }

    // 🎸 TEST HEALTH CHECK 🎸
    group('Health Check', function () {
      const healthResponse = http.get(`${BASE_URL}/health`, { headers });
      
      const healthCheck = check(healthResponse, {
        'health check successful': (r) => r.status === 200,
        'health response includes legendary founder': (r) => {
          const data = r.json();
          return data.legendary_founder === 'rickroll187';
        },
        'swiss precision mode active': (r) => {
          const data = r.json();
          return data.swiss_precision === true;
        },
      });

      checkSwissPrecision(healthResponse, 'Health Check');
      
      if (!healthCheck) {
        legendaryErrorRate.add(1);
      }
    });

    // 🎸 TEST USER PROFILE 🎸
    group('User Profile', function () {
      const profileResponse = http.get(`${BASE_URL}/api/users/me`, { headers });
      
      const profileCheck = check(profileResponse, {
        'profile retrieved successfully': (r) => r.status === 200,
        'profile contains user data': (r) => {
          const data = r.json();
          return data.username && data.email;
        },
      });

      checkSwissPrecision(profileResponse, 'User Profile');
      
      // Special checks for legendary users
      if (user.type === 'legendary') {
        const legendaryCheck = check(profileResponse, {
          'legendary user profile': (r) => {
            const data = r.json();
            return data.is_legendary === true && data.username === 'rickroll187';
          },
        });
        
        if (legendaryCheck) {
          logLegendaryMetric('legendary_profile_success', 1, true);
        }
      }

      if (!profileCheck) {
        legendaryErrorRate.add(1);
      }
    });

    // 🎸 TEST DASHBOARD DATA 🎸
    group('Dashboard Analytics', function () {
      const dashboardResponse = http.get(`${BASE_URL}/api/analytics/dashboard`, { headers });
      
      const dashboardCheck = check(dashboardResponse, {
        'dashboard data retrieved': (r) => r.status === 200,
        'dashboard contains metrics': (r) => {
          const data = r.json();
          return data.user_stats && data.performance_metrics && data.okr_metrics;
        },
      });

      checkSwissPrecision(dashboardResponse, 'Dashboard Analytics');

      // Test legendary dashboard for legendary users
      if (user.type === 'legendary') {
        const legendaryDashResponse = http.get(`${BASE_URL}/api/analytics/legendary-dashboard`, { headers });
        
        const legendaryDashCheck = check(legendaryDashResponse, {
          'legendary dashboard accessible': (r) => r.status === 200,
          'legendary metrics present': (r) => {
            const data = r.json();
            return data.legendary_metrics && data.legendary_metrics.rickroll187_status;
          },
        });
        
        if (legendaryDashCheck) {
          logLegendaryMetric('legendary_dashboard_success', 1, true);
          rickroll187Gauge.add(1);
        }
      }

      if (!dashboardCheck) {
        legendaryErrorRate.add(1);
      }
    });

    // 🎸 TEST PERFORMANCE REVIEWS 🎸
    group('Performance Reviews', function () {
      // Get performance reviews
      const reviewsResponse = http.get(`${BASE_URL}/api/performance/reviews`, { headers });
      
      const reviewsCheck = check(reviewsResponse, {
        'performance reviews retrieved': (r) => r.status === 200,
        'reviews is array': (r) => Array.isArray(r.json()),
      });

      checkSwissPrecision(reviewsResponse, 'Performance Reviews');

      // Create a test performance review
      const newReview = {
        user_id: `test-user-${Math.random().toString(36).substr(2, 9)}`,
        reviewer_id: `reviewer-${Math.random().toString(36).substr(2, 9)}`,
        period_start: '2024-01-01',
        period_end: '2024-06-30',
        overall_score: 4.0 + Math.random(),
        technical_skills_score: 4.0 + Math.random(),
        communication_score: 4.0 + Math.random(),
        comments: `Load test review created at ${new Date().toISOString()}`,
        is_legendary: user.type === 'legendary',
        swiss_precision_score: user.type === 'legendary' ? 98.5 + Math.random() * 1.5 : null,
        code_bro_rating: user.type === 'legendary' ? 9 + Math.random() : null,
      };

      const createResponse = http.post(`${BASE_URL}/api/performance/reviews`, JSON.stringify(newReview), { headers });
      
      const createCheck = check(createResponse, {
        'performance review created': (r) => r.status === 201,
        'created review has ID': (r) => {
          const data = r.json();
          return data.review_id && data.review_id.length > 0;
        },
      });

      checkSwissPrecision(createResponse, 'Create Performance Review');

      if (!reviewsCheck || !createCheck) {
        legendaryErrorRate.add(1);
      }
    });

    // 🎸 TEST OKR MANAGEMENT 🎸
    group('OKR Management', function () {
      // Get OKRs
      const okrsResponse = http.get(`${BASE_URL}/api/okr/okrs`, { headers });
      
      const okrsCheck = check(okrsResponse, {
        'OKRs retrieved successfully': (r) => r.status === 200,
        'OKRs is array': (r) => Array.isArray(r.json()),
      });

      checkSwissPrecision(okrsResponse, 'OKR Management');

      // Create a test OKR
      const newOKR = {
        title: `Load Test OKR ${Math.random().toString(36).substr(2, 5)}`,
        description: 'OKR created during load testing with Swiss precision',
        key_results: [
          {
            title: 'Achieve Swiss Precision',
            target_value: 100,
            current_value: 50 + Math.random() * 50,
            unit: '%',
          },
        ],
        target_date: '2024-12-31',
        is_legendary: user.type === 'legendary',
        swiss_precision_target: user.type === 'legendary' ? 99.9 : null,
        code_bro_challenge: user.type === 'legendary',
      };

      const createOKRResponse = http.post(`${BASE_URL}/api/okr/okrs`, JSON.stringify(newOKR), { headers });
      
      const createOKRCheck = check(createOKRResponse, {
        'OKR created successfully': (r) => r.status === 201,
        'created OKR has ID': (r) => {
          const data = r.json();
          return data.okr_id && data.okr_id.length > 0;
        },
      });

      checkSwissPrecision(createOKRResponse, 'Create OKR');

      if (!okrsCheck || !createOKRCheck) {
        legendaryErrorRate.add(1);
      }
    });

    // Random sleep to simulate user think time
    sleep(Math.random() * 3 + 1); // 1-4 seconds
  });
}

// 🎸 LEGENDARY USER](#)*

