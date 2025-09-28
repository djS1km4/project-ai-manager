import { useAuthStore } from '../services/authStore'
import { useAuthToken } from '../hooks/useAuthToken'

export const AuthDebug = () => {
  const { user, token, isAuthenticated } = useAuthStore()
  const { isReady, hasHydrated } = useAuthToken()

  if (import.meta.env.PROD) {
    return null
  }

  return (
    <div className="fixed bottom-4 left-4 bg-black bg-opacity-80 text-white p-4 rounded-lg text-xs max-w-sm z-50">
      <h4 className="font-bold mb-2">Auth Debug</h4>
      <div className="space-y-1">
        <div>isAuthenticated: {isAuthenticated ? '✅' : '❌'}</div>
        <div>isReady: {isReady ? '✅' : '❌'}</div>
        <div>hasHydrated: {hasHydrated ? '✅' : '❌'}</div>
        <div>user: {user ? `${user.email}` : 'null'}</div>
        <div>token: {token ? `${token.substring(0, 20)}...` : 'null'}</div>
        <div>localStorage: {localStorage.getItem('auth-storage') ? '✅' : '❌'}</div>
      </div>
    </div>
  )
}