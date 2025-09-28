import { ReactNode, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../services/authStore'
import { useNotifications } from './Notification'
import {
  LayoutDashboard,
  FolderOpen,
  CheckSquare,
  Brain,
  LogOut,
  Menu,
  X,
  Sparkles,
  Settings,
} from 'lucide-react'

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { addNotification, NotificationContainer } = useNotifications()

  const handleLogout = () => {
    addNotification({
      message: 'Cerrando sesión...',
      type: 'info',
      duration: 2000
    })
    setTimeout(() => {
      logout()
    }, 1000)
  }

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard, description: 'Vista general' },
    { name: 'Proyectos', href: '/projects', icon: FolderOpen, description: 'Gestión de proyectos' },
    { name: 'Tareas', href: '/tasks', icon: CheckSquare, description: 'Lista de tareas' },
    { name: 'IA Insights', href: '/ai-insights', icon: Brain, description: 'Análisis inteligente' },
    ...(user?.is_admin ? [{ name: 'Administración', href: '/admin/users', icon: Settings, description: 'Gestión de usuarios' }] : []),
  ]



  return (
    <div className="min-h-screen gradient-bg">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/20 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-72 transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex h-full flex-col sidebar-card m-3 mr-0 rounded-r-none">
          {/* Logo */}
          <div className="flex h-20 items-center justify-between px-6 border-b border-gray-200">
            <div className="flex items-center gap-3">
              <div className="icon-container-primary">
                <Sparkles className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-xl font-display font-bold text-gradient">
                  Project AI
                </h1>
                <p className="text-xs font-sans text-secondary-500 tracking-wide">Manager</p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 text-secondary-400 hover:text-dark-700 hover:bg-gray-100 rounded-soft transition-all duration-200"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`nav-item group flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-soft transition-all duration-200 ${
                    isActive
                      ? 'bg-white text-dark-700 soft-shadow-colored border border-primary-200'
                      : 'text-secondary-600 hover:text-dark-700 hover:bg-gray-50 hover:soft-shadow'
                  }`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className={`h-5 w-5 transition-colors duration-200 ${
                    isActive ? 'text-primary-600' : 'text-secondary-400 group-hover:text-primary-600'
                  }`} />
                  <span className="font-sans tracking-wide">{item.name}</span>
                  {isActive && (
                    <div className="ml-auto h-2 w-2 rounded-full bg-primary-500 shadow-sm" />
                  )}
                </Link>
              );
            })}
          </nav>

          {/* User section */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex items-center gap-3 p-3 rounded-soft bg-white soft-shadow border border-gray-100">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-success-400 to-info-400 text-white font-semibold text-sm shadow-sm">
                {user?.full_name?.charAt(0) || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-dark-700 truncate">
                  {user?.full_name || 'Usuario'}
                </p>
                <p className="text-xs text-secondary-500 truncate">
                  {user?.email || 'usuario@ejemplo.com'}
                </p>
              </div>
              <button 
                onClick={handleLogout}
                className="p-2 text-secondary-400 hover:text-danger-500 hover:bg-danger-50 rounded-soft transition-all duration-200"
                title="Cerrar sesión"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-72">
        {/* Mobile header */}
        <div className="sticky top-0 z-40 flex h-16 items-center gap-x-4 bg-white soft-shadow border-b border-gray-200 px-4 sm:gap-x-6 sm:px-6 lg:hidden">
          <button
            type="button"
            className="p-2.5 text-secondary-400 hover:text-dark-700 hover:bg-gray-100 rounded-soft transition-all duration-200"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-5 w-5" />
          </button>
          <div className="flex-1 text-sm font-semibold leading-6 text-dark-700">
            Project AI Manager
          </div>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-r from-success-400 to-info-400 text-white font-semibold text-xs shadow-sm">
              {user?.full_name?.charAt(0) || 'U'}
            </div>
          </div>
        </div>

        <div className="lg:pl-0">
          <main className="min-h-screen">
            {children}
          </main>
        </div>
      </div>
      
      {/* Notification Container */}
      <NotificationContainer />
    </div>
  )
}

export default Layout