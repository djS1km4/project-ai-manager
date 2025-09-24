import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { apiClient } from './apiClient'

interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  register: (email: string, password: string, fullName: string) => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        try {
          const formData = new FormData()
          formData.append('username', email)
          formData.append('password', password)

          const response = await apiClient.post('/auth/login', formData, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          })

          const { access_token, user } = response.data

          set({
            token: access_token,
            user,
            isAuthenticated: true,
          })

          // Set default authorization header
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        } catch (error) {
          console.error('Login failed:', error)
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
        
        // Remove authorization header
        delete apiClient.defaults.headers.common['Authorization']
      },

      register: async (email: string, password: string, fullName: string) => {
        try {
          const response = await apiClient.post('/auth/register', {
            email,
            password,
            full_name: fullName,
          })

          const { access_token, user } = response.data

          set({
            token: access_token,
            user,
            isAuthenticated: true,
          })

          // Set default authorization header
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        } catch (error) {
          console.error('Registration failed:', error)
          throw error
        }
      },
    }),
    {
      name: 'auth-storage',
      onRehydrateStorage: () => (state) => {
        if (state?.token) {
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${state.token}`
        }
      },
    }
  )
)