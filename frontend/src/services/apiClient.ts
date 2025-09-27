import axios from 'axios'

export const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    
    // Skip auth for login/register endpoints
    if (config.url?.includes('/auth/login') || config.url?.includes('/auth/register')) {
      console.log('⚠️ Skipping auth for login/register endpoint')
      return config
    }

    // Get token from localStorage (Zustand persist format)
    const authStorage = localStorage.getItem('auth-storage')
    
    if (authStorage) {
      try {
        const parsedAuth = JSON.parse(authStorage)
        
        // Zustand persist stores data in nested structure: { state: { token, user, isAuthenticated }, version: 0 }
        const token = parsedAuth.state?.token
        const isAuthenticated = parsedAuth.state?.isAuthenticated
        
        console.log('🔐 Auth check:', { 
          hasToken: !!token, 
          isAuthenticated, 
          tokenLength: token?.length || 0 
        })
        
        if (token && isAuthenticated && typeof token === 'string' && token.length > 0) {
          config.headers.Authorization = `Bearer ${token}`
          console.log('✅ Token added to request')
        } else {
          console.log('❌ No valid token found')
        }
      } catch (error) {
        console.error('❌ Error parsing auth storage:', error)
      }
    } else {
      console.log('❌ No auth storage found')
    }
    
    return config
  },
  (error) => {
    console.error('❌ Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.method?.toUpperCase()} ${response.config.url}`)
    return response
  },
  (error) => {
    const status = error.response?.status
    const method = error.config?.method?.toUpperCase()
    const url = error.config?.url
    const errorDetail = error.response?.data?.detail || error.message
    
    console.error(`❌ API Error: ${status} ${method} ${url}`, {
      status,
      detail: errorDetail,
      response: error.response?.data
    })
    
    // Handle authentication errors (401 and 403)
    if (status === 401 || status === 403) {
      console.log(`🔒 ${status} Authentication Error - checking error details`)
      
      // Check if it's a token-related error or general auth failure
      const errorMessage = error.response?.data?.detail || ''
      
      // Only redirect for specific authentication failures, not all 403s
      if (status === 401 || 
          errorMessage.includes('Invalid token') || 
          errorMessage.includes('Token expired') || 
          errorMessage.includes('Could not validate credentials')) {
        
        console.log('🚪 Authentication failed - clearing auth and redirecting to login')
        
        // Clear all auth-related storage
        localStorage.removeItem('auth-storage')
        sessionStorage.clear()
        
        // Show user-friendly message
        if (typeof window !== 'undefined') {
          // Create a temporary notification
          const notification = document.createElement('div')
          notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 16px 24px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 14px;
            max-width: 300px;
          `
          notification.textContent = 'Tu sesión ha expirado. Redirigiendo al login...'
          document.body.appendChild(notification)
          
          // Remove notification and redirect after 2 seconds
          setTimeout(() => {
            document.body.removeChild(notification)
            window.location.href = '/login'
          }, 2000)
        } else {
          // Fallback for non-browser environments
          window.location.href = '/login'
        }
      } else {
        console.log('🔍 Auth error but not token-related:', errorMessage)
        // For 403 errors that are not token-related, just log and continue
        // This allows the component to handle the error appropriately
      }
    }
    
    return Promise.reject(error)
  }
)

export default apiClient