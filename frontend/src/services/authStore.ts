import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { apiClient } from './apiClient'

interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
  is_admin: boolean
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
          const response = await apiClient.post('/auth/login', {
            email,
            password,
          })

          const { access_token, user } = response.data

          set({
            token: access_token,
            user,
            isAuthenticated: true,
          })
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
      },

      register: async (email: string, password: string, fullName: string) => {
        try {
          // Generate username from email (before @ symbol)
          const username = email.split('@')[0]
          
          const response = await apiClient.post('/auth/register', {
            email,
            username,
            full_name: fullName,
            password,
          })

          const { access_token, user } = response.data

          set({
            token: access_token,
            user,
            isAuthenticated: true,
          })
        } catch (error) {
          console.error('Registration failed:', error)
          throw error
        }
      },
    }),
    {
      name: 'auth-storage',
      onRehydrateStorage: () => (state) => {
        if (state?.token && state?.isAuthenticated) {
          console.log('Auth token restored from storage')
        }
      },
    }
  )
)