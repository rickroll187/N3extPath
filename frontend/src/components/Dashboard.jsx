// File: frontend/src/components/Dashboard.jsx
/**
 * 📊🎸 N3EXTPATH - LEGENDARY DASHBOARD COMPONENT 🎸📊
 * Professional React dashboard with legendary capabilities
 * Built: 2025-08-05 15:28:45 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  Title, 
  Tooltip, 
  Legend,
  ArcElement 
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import './Dashboard.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const LegendaryDashboard = ({ user }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Update time every second (Swiss precision!)
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // Simulate API call
        const response = await fetch('/api/v1/dashboard');
        const data = await response.json();
        
        // Mock data for demonstration
        const mockData = {
          stats: {
            totalEmployees: 187,
            activeOKRs: 45,
            completedReviews: 23,
            teamPerformance: 4.2
          },
          okrProgress: {
            labels: ['Q1 Goals', 'Q2 Goals', 'Q3 Goals', 'Q4 Goals'],
            datasets: [{
              label: 'OKR Progress',
              data: [85, 78, 92, 67],
              backgroundColor: [
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)'
              ],
              borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(75, 192, 192, 1)'
              ],
              borderWidth: 2
            }]
          },
          performanceDistribution: {
            labels: ['Exceeds', 'Meets', 'Below', 'Needs Improvement'],
            datasets: [{
              data: [45, 89, 23, 12],
              backgroundColor: [
                '#4CAF50',
                '#2196F3',
                '#FF9800',
                '#F44336'
              ],
              hoverBackgroundColor: [
                '#45a049',
                '#1976d2',
                '#e68900',
                '#d32f2f'
              ]
            }]
          },
          recentActivities: [
            { id: 1, type: 'okr_update', message: 'Sarah updated Q4 Sales Target to 95%', time: '2 hours ago', user: 'Sarah Johnson' },
            { id: 2, type: 'review_completed', message: 'Performance review completed for Engineering Team', time: '4 hours ago', user: 'Mike Chen' },
            { id: 3, type: 'new_hire', message: 'Welcome Jessica Brown to the Product Team!', time: '1 day ago', user: 'HR Team' },
            { id: 4, type: 'goal_achieved', message: 'Customer Satisfaction goal achieved ahead of schedule', time: '2 days ago', user: 'Support Team' }
          ]
        };
        
        setDashboardData(mockData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  // Special greeting for RICKROLL187
  const getGreeting = () => {
    const hour = currentTime.getHours();
    let timeGreeting;
    
    if (hour < 12) timeGreeting = 'Good Morning';
    else if (hour < 18) timeGreeting = 'Good Afternoon';
    else timeGreeting = 'Good Evening';

    if (user?.username === 'rickroll187') {
      return `🎸 ${timeGreeting}, LEGENDARY FOUNDER RICKROLL187! 🎸`;
    }
    
    return `${timeGreeting}, ${user?.first_name || 'Team Member'}!`;
  };

  // Chart options
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'OKR Progress Overview',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100
      }
    }
  };

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: true,
        text: 'Performance Distribution',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading your legendary dashboard...</p>
      </div>
    );
  }

  return (
    <div className="legendary-dashboard">
      {/* Header Section */}
      <div className="dashboard-header">
        <div className="greeting-section">
          <h1>{getGreeting()}</h1>
          <p className="current-time">
            {currentTime.toLocaleString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
              timeZoneName: 'short'
            })}
          </p>
          {user?.username === 'rickroll187' && (
            <div className="legendary-badge">
              <span>🏆 LEGENDARY FOUNDER STATUS ACTIVE 🏆</span>
            </div>
          )}
        </div>
        
        <div className="quick-actions">
          <button className="action-btn primary">📊 View Reports</button>
          <button className="action-btn secondary">🎯 Update OKRs</button>
          <button className="action-btn tertiary">👥 Team Chat</button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>{dashboardData?.stats.totalEmployees}</h3>
            <p>Total Employees</p>
            <span className="stat-change positive">+12 this month</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>{dashboardData?.stats.activeOKRs}</h3>
            <p>Active OKRs</p>
            <span className="stat-change positive">+5 this week</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <h3>{dashboardData?.stats.completedReviews}</h3>
            <p>Completed Reviews</p>
            <span className="stat-change neutral">On track</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <h3>{dashboardData?.stats.teamPerformance}</h3>
            <p>Avg Performance</p>
            <span className="stat-change positive">+0.3 improvement</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <Bar data={dashboardData?.okrProgress} options={chartOptions} />
        </div>
        
        <div className="chart-container">
          <Doughnut data={dashboardData?.performanceDistribution} options={doughnutOptions} />
        </div>
      </div>

      {/* Recent Activities */}
      <div className="activities-section">
        <h2>🔥 Recent Activities</h2>
        <div className="activities-list">
          {dashboardData?.recentActivities.map((activity) => (
            <div key={activity.id} className={`activity-item ${activity.type}`}>
              <div className="activity-icon">
                {activity.type === 'okr_update' && '🎯'}
                {activity.type === 'review_completed' && '📋'}
                {activity.type === 'new_hire' && '👋'}
                {activity.type === 'goal_achieved' && '🏆'}
              </div>
              <div className="activity-content">
                <p className="activity-message">{activity.message}</p>
                <div className="activity-meta">
                  <span className="activity-user">{activity.user}</span>
                  <span className="activity-time">{activity.time}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Legendary Footer */}
      <div className="dashboard-footer">
        <p>🎸 Built with legendary precision by the N3EXTPATH team 🎸</p>
        <p>WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!</p>
        {user?.username === 'rickroll187' && (
          <p className="legendary-signature">✨ Swiss precision meets legendary fun ✨</p>
        )}
      </div>
    </div>
  );
};

export default LegendaryDashboard;
