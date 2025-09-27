import { useEffect, useState } from 'react'
import { useAuthStore } from '../services/authStore'

// Helper function to check if JWT token is expired
const isTokenExpired = (token: string): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const currentTime = Date.now() / 1000
    return payload.exp < currentTime
  } catch (error) {
    console.error('Error parsing token:', error)
    return true // Treat invalid tokens as expired
  }
}

export const useAuthToken = () => {
  const { token, isAuthenticated, logout } = useAuthStore()
  const [isReady, setIsReady] = useState(false)
  const [hasHydrated, setHasHydrated] = useState(false)

  useEffect(() => {
    // Simple hydration check with timeout fallback
    const hydrationTimeout = setTimeout(() => {
      setHasHydrated(true)
      setIsReady(true)
    }, 100) // Very short timeout

    // Check localStorage immediately
    const authStorage = localStorage.getItem('auth-storage')

    if (authStorage) {
      try {
        const parsedAuth = JSON.parse(authStorage)
        const storedToken = parsedAuth.state?.token
        
        // Check if token is expired
        if (storedToken && isTokenExpired(storedToken)) {
          console.log('🔒 Token expired, logging out...')
          logout()
          clearTimeout(hydrationTimeout)
          setHasHydrated(true)
          setIsReady(true)
          return
        }
        
        // If we have a stored token, consider hydrated
        if (storedToken) {
          clearTimeout(hydrationTimeout)
          setHasHydrated(true)
          setIsReady(true)
          return
        }
      } catch (error) {
        console.error('Error parsing auth storage:', error)
        localStorage.removeItem('auth-storage')
        logout()
      }
    }

    // If no stored auth, we're ready immediately
    if (!authStorage) {
      clearTimeout(hydrationTimeout)
      setHasHydrated(true)
      setIsReady(true)
    }

    return () => {
      clearTimeout(hydrationTimeout)
    }
  }, []) // Only run once on mount

  // Separate effect for token expiration checking
  useEffect(() => {
    if (!token || !isAuthenticated || !isReady) return

    const checkTokenExpiration = () => {
      if (isTokenExpired(token)) {
        console.log('🔒 Token expired during session, logging out...')
        logout()
      }
    }

    // Check immediately
    checkTokenExpiration()

    // Check every 5 minutes
    const interval = setInterval(checkTokenExpiration, 5 * 60 * 1000)
    
    return () => clearInterval(interval)
  }, [token, isAuthenticated, isReady, logout])

  const finalIsAuthenticated = isAuthenticated && token && !isTokenExpired(token)

  return {
    token,
    isAuthenticated: finalIsAuthenticated,
    isReady,
    hasHydrated
  }
}