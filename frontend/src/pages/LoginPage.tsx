import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuthStore } from '../services/authStore'
import { Brain, Mail, Lock, Eye, EyeOff } from 'lucide-react'
import toast from 'react-hot-toast'

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

const registerSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  fullName: z.string().min(2, 'Full name must be at least 2 characters'),
})

type LoginForm = z.infer<typeof loginSchema>
type RegisterForm = z.infer<typeof registerSchema>

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { login, register } = useAuthStore()

  const loginForm = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  })

  const registerForm = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  })

  const onLoginSubmit = async (data: LoginForm) => {
    setIsLoading(true)
    try {
      await login(data.email, data.password)
      toast.success('Welcome back!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  const onRegisterSubmit = async (data: RegisterForm) => {
    setIsLoading(true)
    try {
      await register(data.email, data.password, data.fullName)
      toast.success('Account created successfully!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-full blur-3xl floating-animation"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-full blur-3xl floating-animation" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-blue-600/10 to-purple-600/10 rounded-full blur-3xl floating-animation" style={{animationDelay: '4s'}}></div>
      </div>

      <div className="max-w-md w-full space-y-8 relative z-10">
        <div className="text-center">
          <div className="mx-auto h-20 w-20 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl flex items-center justify-center glow-effect floating-animation">
            <Brain className="h-10 w-10 text-white" />
          </div>
          <div className="mt-6 space-y-1">
            <h2 className="text-5xl font-black tracking-tight leading-none">
              <span className="block text-gradient-modern font-logo">PROJECT</span>
              <span className="block text-gradient-ai font-logo text-6xl -mt-2">AI</span>
              <span className="block text-gradient-modern font-logo -mt-1">MANAGER</span>
            </h2>
          </div>
          <p className="mt-3 text-slate-400 text-lg">
            {isLogin ? 'Bienvenido de vuelta' : 'Crea tu cuenta'}
          </p>
        </div>

        <div className="card-glass glow-effect">
          {isLogin ? (
            <form onSubmit={loginForm.handleSubmit(onLoginSubmit)} className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-slate-300 mb-2">
                  Correo Electrónico
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    {...loginForm.register('email')}
                    type="email"
                    className="input pl-12"
                    placeholder="tu@email.com"
                  />
                </div>
                {loginForm.formState.errors.email && (
                  <p className="mt-2 text-sm text-red-400 flex items-center">
                    <span className="w-1 h-1 bg-red-400 rounded-full mr-2"></span>
                    {loginForm.formState.errors.email.message}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-semibold text-slate-300 mb-2">
                  Contraseña
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    {...loginForm.register('password')}
                    type={showPassword ? 'text' : 'password'}
                    className="input pl-12 pr-12"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-4 flex items-center text-slate-400 hover:text-white transition-colors"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
                {loginForm.formState.errors.password && (
                  <p className="mt-2 text-sm text-red-400 flex items-center">
                    <span className="w-1 h-1 bg-red-400 rounded-full mr-2"></span>
                    {loginForm.formState.errors.password.message}
                  </p>
                )}
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary w-full py-4 text-lg font-semibold"
              >
                {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
              </button>
            </form>
          ) : (
            <form onSubmit={registerForm.handleSubmit(onRegisterSubmit)} className="space-y-6">
              <div>
                <label htmlFor="fullName" className="block text-sm font-semibold text-slate-300 mb-2">
                  Nombre Completo
                </label>
                <div className="relative">
                  <input
                    {...registerForm.register('fullName')}
                    type="text"
                    className="input"
                    placeholder="Tu nombre completo"
                  />
                </div>
                {registerForm.formState.errors.fullName && (
                  <p className="mt-2 text-sm text-red-400 flex items-center">
                    <span className="w-1 h-1 bg-red-400 rounded-full mr-2"></span>
                    {registerForm.formState.errors.fullName.message}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-slate-300 mb-2">
                  Correo Electrónico
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    {...registerForm.register('email')}
                    type="email"
                    className="input pl-12"
                    placeholder="tu@email.com"
                  />
                </div>
                {registerForm.formState.errors.email && (
                  <p className="mt-2 text-sm text-red-400 flex items-center">
                    <span className="w-1 h-1 bg-red-400 rounded-full mr-2"></span>
                    {registerForm.formState.errors.email.message}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-semibold text-slate-300 mb-2">
                  Contraseña
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-slate-400" />
                  </div>
                  <input
                    {...registerForm.register('password')}
                    type={showPassword ? 'text' : 'password'}
                    className="input pl-12 pr-12"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-4 flex items-center text-slate-400 hover:text-white transition-colors"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
                {registerForm.formState.errors.password && (
                  <p className="mt-2 text-sm text-red-400 flex items-center">
                    <span className="w-1 h-1 bg-red-400 rounded-full mr-2"></span>
                    {registerForm.formState.errors.password.message}
                  </p>
                )}
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary w-full py-4 text-lg font-semibold"
              >
                {isLoading ? 'Creando cuenta...' : 'Crear Cuenta'}
              </button>
            </form>
          )}

          <div className="mt-8 text-center">
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="text-slate-400 hover:text-white text-sm font-medium transition-colors duration-300 relative group"
            >
              <span className="relative z-10">
                {isLogin
                  ? "¿No tienes cuenta? Regístrate"
                  : '¿Ya tienes cuenta? Inicia sesión'}
              </span>
              <span className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"></span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage