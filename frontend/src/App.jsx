// File: frontend/src/App.jsx
/**
 * 🎸 N3EXTPATH - MAIN APP COMPONENT 🎸
 * Professional React app component
 * Built: 2025-08-05 15:45:11 UTC by RICKROLL187
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import React, { useState, useEffect } from 'react'
import LegendaryDashboard from './components/Dashboard'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Mock user login (would be real authentication)
  useEffect(() => {
    const mockLogin = async () => {
      try {
        // Simulate API call to get user
        const response = await fetch('/api/v1/users/rickroll187')
        const data = await response.json()
        
        if (data.success) {
          setUser(data.user)
        }
      } catch (error) {
        console.error('Login error:', error)
        // Set default user for demo
        setUser({
          user_id: 'rickroll187',
          username: 'rickroll187',
          first_name: 'RICKROLL187',
          last_name: 'Legendary Founder',
          role: 'founder',
          department: 'legendary'
        })
      } finally {
        setLoading(false)
      }
    }

    mockLogin()
  }, [])

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <h2>🎸 Loading N3EXTPATH... 🎸</h2>
        <p>WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!</p>
      </div>
    )
  }

  return (
    <div className="App">
      <LegendaryDashboard user={user} />
    </div>
  )
}

export default App
