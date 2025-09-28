import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { 
  Plus, 
  Search, 
  Filter, 
  Calendar, 
  DollarSign, 
  Users, 
  MoreVertical,
  Edit,
  Trash2,
  X,
  Star,
  FolderOpen,
  ArrowUp,
  ArrowDown
} from 'lucide-react'
import { apiClient } from '../services/apiClient'
import { useAuthToken } from '../hooks/useAuthToken'
import toast from 'react-hot-toast'

const projectSchema = z.object({
  name: z.string().min(1, 'El nombre del proyecto es requerido'),
  description: z.string().optional(),
  start_date: z.string().optional().or(z.literal('')).transform(val => val === '' ? undefined : val),
  end_date: z.string().optional().or(z.literal('')).transform(val => val === '' ? undefined : val),
  budget: z.number().min(0).optional().or(z.literal('')).transform(val => val === '' ? undefined : val),
  status: z.enum(['planning', 'active', 'on_hold', 'completed', 'cancelled']),
})

type ProjectForm = z.infer<typeof projectSchema>

interface Project {
  id: number
  name: string
  description?: string
  start_date?: string
  end_date?: string
  budget?: number
  status: string
  created_at: string
  updated_at: string
  owner_id: number
  owner?: { id: number; full_name: string; email: string }
  task_count?: number
  completed_tasks?: number
  progress?: number
}

const ProjectsPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingProject, setEditingProject] = useState<Project | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [sortBy, setSortBy] = useState('created_at')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [activeDropdown, setActiveDropdown] = useState<number | null>(null)
  const queryClient = useQueryClient()
  const { isReady } = useAuthToken()

  // Effect to close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Element
      // Only close if clicking outside the dropdown and not on buttons inside it
      if (activeDropdown !== null && 
          !target.closest('.dropdown-menu') && 
          !target.closest('.dropdown-trigger')) {
        console.log('🔄 Closing dropdown due to outside click')
        setActiveDropdown(null)
      }
    }

    if (activeDropdown !== null) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [activeDropdown])

  const { data: projects = [], isLoading } = useQuery({
    queryKey: ['projects', searchTerm, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      if (statusFilter !== 'all') params.append('status', statusFilter)
      
      const response = await apiClient.get(`/projects/?${params.toString()}`)
      return response.data as Project[]
    },
    enabled: isReady,
  })

  const createProjectMutation = useMutation({
    mutationFn: async (data: ProjectForm) => {
      const response = await apiClient.post('/projects/', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setIsModalOpen(false)
      setEditingProject(null)
      reset()
      toast.success('Proyecto creado exitosamente')
    },
    onError: (error: any) => {
      console.error('Error creating project:', error)
      let errorMessage = 'Error al crear el proyecto'
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Manejar errores de validación de Pydantic
          errorMessage = error.response.data.detail
            .map((err: any) => `${err.loc?.join('.')}: ${err.msg}`)
            .join(', ')
        } else if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail
        }
      }
      
      toast.error(errorMessage)
    },
  })

  const updateProjectMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: ProjectForm }) => {
      console.log('🔄 Updating project:', { id, data })
      const response = await apiClient.put(`/projects/${id}`, data)
      console.log('✅ Project update response:', response.data)
      return response.data
    },
    onSuccess: (updatedProject) => {
      console.log('✅ Project updated successfully:', updatedProject)
      console.log('🔄 Invalidating queries and resetting state')
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      console.log('🔄 Closing modal and clearing editing state')
      setIsModalOpen(false)
      setEditingProject(null)
      reset()
      console.log('✅ State reset completed')
      toast.success('Proyecto actualizado exitosamente')
    },
    onError: (error: any) => {
      console.error('❌ Error updating project:', error)
      console.error('❌ Error response:', error.response?.data)
      
      let errorMessage = 'Error al actualizar el proyecto'
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Manejar errores de validación de Pydantic
          errorMessage = error.response.data.detail
            .map((err: any) => `${err.loc?.join('.')}: ${err.msg}`)
            .join(', ')
        } else if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail
        }
      }
      
      toast.error(errorMessage)
    },
  })

  const deleteProjectMutation = useMutation({
    mutationFn: async (id: number) => {
      console.log('🗑️ Deleting project:', id)
      await apiClient.delete(`/projects/${id}`)
      console.log('✅ Project deleted successfully')
    },
    onSuccess: () => {
      console.log('✅ Project deletion confirmed, invalidating queries')
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setActiveDropdown(null)
      toast.success('Proyecto eliminado exitosamente')
    },
    onError: (error: any) => {
      console.error('❌ Error deleting project:', error)
      console.error('❌ Error response:', error.response?.data)
      
      let errorMessage = 'Error al eliminar el proyecto'
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Manejar errores de validación de Pydantic
          errorMessage = error.response.data.detail
            .map((err: any) => `${err.loc?.join('.')}: ${err.msg}`)
            .join(', ')
        } else if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail
        }
      }
      
      toast.error(errorMessage)
    },
  })

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ProjectForm>({
    resolver: zodResolver(projectSchema),
  })

  const handleDeleteProject = (id: number) => {
    console.log('🗑️ handleDeleteProject called with id:', id)
    if (window.confirm('¿Estás seguro de que quieres eliminar este proyecto?')) {
      console.log('✅ User confirmed deletion, calling mutation')
      deleteProjectMutation.mutate(id)
    } else {
      console.log('❌ User cancelled deletion')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'planning': return 'bg-blue-100 text-blue-800'
      case 'active': return 'bg-green-100 text-green-800'
      case 'on_hold': return 'bg-yellow-100 text-yellow-800'
      case 'completed': return 'bg-purple-100 text-purple-800'
      case 'cancelled': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'planning': return 'Planificación'
      case 'active': return 'Activo'
      case 'on_hold': return 'En Pausa'
      case 'completed': return 'Completado'
      case 'cancelled': return 'Cancelado'
      default: return status
    }
  }

  const filteredAndSortedProjects = projects
    .filter(project => {
      const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           project.description?.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesStatus = statusFilter === 'all' || project.status === statusFilter
      return matchesSearch && matchesStatus
    })
    .sort((a, b) => {
      let aValue: any, bValue: any
      
      switch (sortBy) {
        case 'name':
          // Ordenamiento alfabético por primera letra del nombre
          aValue = a.name.toLowerCase().charAt(0)
          bValue = b.name.toLowerCase().charAt(0)
          // Si las primeras letras son iguales, comparar nombres completos
          if (aValue === bValue) {
            aValue = a.name.toLowerCase()
            bValue = b.name.toLowerCase()
          }
          break
        case 'start_date':
          aValue = a.start_date ? new Date(a.start_date).getTime() : 0
          bValue = b.start_date ? new Date(b.start_date).getTime() : 0
          break
        case 'end_date':
          aValue = a.end_date ? new Date(a.end_date).getTime() : 0
          bValue = b.end_date ? new Date(b.end_date).getTime() : 0
          break
        case 'budget':
          aValue = a.budget || 0
          bValue = b.budget || 0
          break
        case 'created_at':
        default:
          // Ordenamiento por fecha de creación (más reciente primero por defecto)
          // Asegurar que las fechas se parseen correctamente
          aValue = a.created_at ? new Date(a.created_at).getTime() : 0
          bValue = b.created_at ? new Date(b.created_at).getTime() : 0
          // Si alguna fecha es inválida, usar 0
          if (isNaN(aValue)) aValue = 0
          if (isNaN(bValue)) bValue = 0
          break
      }
      
      // Para strings, usar localeCompare para mejor ordenamiento
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        if (sortOrder === 'asc') {
          return aValue.localeCompare(bValue)
        } else {
          return bValue.localeCompare(aValue)
        }
      }
      
      // Para números y fechas
      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : aValue < bValue ? -1 : 0
      } else {
        return aValue < bValue ? 1 : aValue > bValue ? -1 : 0
      }
    })

  const onSubmit = (data: ProjectForm) => {
    // Transform date fields to datetime format for backend
    const transformedData = {
      ...data,
      start_date: data.start_date ? `${data.start_date}T00:00:00` : undefined,
      end_date: data.end_date ? `${data.end_date}T23:59:59` : undefined,
    }

    // Remove undefined values to avoid sending them
    Object.keys(transformedData).forEach(key => {
      if (transformedData[key as keyof typeof transformedData] === undefined) {
        delete transformedData[key as keyof typeof transformedData]
      }
    })

    if (editingProject) {
      updateProjectMutation.mutate({ id: editingProject.id, data: transformedData })
    } else {
      createProjectMutation.mutate(transformedData)
    }
  }

  const openEditModal = (project: Project) => {
    console.log('🖊️ openEditModal called with project:', project)
    console.log('🔍 Current editingProject state:', editingProject)
    console.log('🔍 Current isModalOpen state:', isModalOpen)
    
    // Asegurar que el estado anterior se limpie
    if (editingProject) {
      console.log('⚠️ Previous editingProject found, clearing state')
      setEditingProject(null)
      setIsModalOpen(false)
      reset()
    }
    
    // Pequeña pausa para asegurar que el estado se actualice
    setTimeout(() => {
      console.log('🔄 Setting new editing state')
      setEditingProject(project)
      const formData = {
        name: project.name,
        description: project.description || '',
        start_date: project.start_date || '',
        end_date: project.end_date || '',
        budget: project.budget ?? undefined,
        status: project.status as any,
      }
      console.log('📝 Setting form data:', formData)
      reset(formData)
      setIsModalOpen(true)
      console.log('✅ Modal opened for editing')
    }, 100)
  }

  const openCreateModal = () => {
    setEditingProject(null)
    reset({
      name: '',
      description: '',
      start_date: '',
      end_date: '',
      budget: 0,
      status: 'planning',
    })
    setIsModalOpen(true)
  }

  if (!isReady) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-br from-green-500 to-blue-600 rounded-xl shadow-lg">
                <FolderOpen className="h-8 w-8 text-white" />
              </div>
              <Star className="h-6 w-6 text-yellow-500" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-800 font-nunito">Proyectos</h1>
              <p className="text-gray-600 font-open-sans">Gestiona y supervisa todos tus proyectos</p>
            </div>
          </div>
          <button
            onClick={openCreateModal}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-200 flex items-center gap-3 shadow-soft hover:shadow-lg"
          >
            <Plus className="h-5 w-5" />
            Nuevo Proyecto
          </button>
        </div>

      {/* Filters and Sorting */}
      <div className="flex flex-col lg:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Buscar proyectos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Status Filter */}
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent min-w-[160px]"
            >
              <option value="all">Todos los estados</option>
              <option value="planning">Planificación</option>
              <option value="active">Activo</option>
              <option value="on_hold">En Pausa</option>
              <option value="completed">Completado</option>
              <option value="cancelled">Cancelado</option>
            </select>
          </div>

          {/* Sort By */}
          <div className="flex items-center gap-2">
            <Calendar className="w-5 h-5 text-gray-400" />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent min-w-[140px]"
            >
              <option value="created_at">Fecha de creación</option>
              <option value="name">Nombre (A-Z)</option>
              <option value="start_date">Fecha de inicio</option>
              <option value="end_date">Fecha de fin</option>
              <option value="budget">Presupuesto</option>
            </select>
          </div>

          {/* Sort Order */}
          <button
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
            title={sortOrder === 'asc' ? 'Cambiar a descendente (más reciente primero)' : 'Cambiar a ascendente (más antiguo primero)'}
          >
            {sortOrder === 'asc' ? (
              <ArrowUp className="w-4 h-4" />
            ) : (
              <ArrowDown className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>

      {/* Projects Grid */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      ) : filteredAndSortedProjects.length === 0 ? (
        <div className="text-center py-12">
          <div className="w-24 h-24 mx-auto mb-4 text-gray-300">
            <svg fill="currentColor" viewBox="0 0 24 24">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {searchTerm || statusFilter !== 'all' ? 'No se encontraron proyectos' : 'No hay proyectos'}
          </h3>
          <p className="text-gray-500 mb-4">
            {searchTerm || statusFilter !== 'all' 
              ? 'Intenta ajustar los filtros de búsqueda'
              : 'Comienza creando tu primer proyecto'
            }
          </p>
          {!searchTerm && statusFilter === 'all' && (
            <button
              onClick={openCreateModal}
              className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Plus className="w-5 h-5 mr-2" />
              Crear Proyecto
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {filteredAndSortedProjects.map((project) => (
            <div key={project.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{project.name}</h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                    {getStatusText(project.status)}
                  </span>
                </div>
                <div className="relative">
                  <button 
                    onClick={() => setActiveDropdown(activeDropdown === project.id ? null : project.id)}
                    className="dropdown-trigger p-1 text-gray-400 hover:text-gray-600"
                  >
                    <MoreVertical className="w-5 h-5" />
                  </button>
                  {activeDropdown === project.id && (
                    <div className="dropdown-menu absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200">
                      <div className="py-1">
                        <button
                          onMouseDown={(e) => {
                            e.preventDefault()
                            e.stopPropagation()
                            console.log('🖊️ Edit button clicked for project:', project.id)
                            openEditModal(project)
                            setActiveDropdown(null)
                          }}
                          className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                        >
                          <Edit className="w-4 h-4 mr-2" />
                          Editar
                        </button>
                        <button
                          onMouseDown={(e) => {
                            e.preventDefault()
                            e.stopPropagation()
                            console.log('🗑️ Delete button clicked for project:', project.id)
                            handleDeleteProject(project.id)
                            setActiveDropdown(null)
                          }}
                          className="flex items-center px-4 py-2 text-sm text-red-600 hover:bg-gray-100 w-full text-left"
                        >
                          <Trash2 className="w-4 h-4 mr-2" />
                          Eliminar
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {project.description && (
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">{project.description}</p>
              )}

              <div className="space-y-2 text-sm text-gray-500">
                {project.start_date && (
                  <div className="flex items-center">
                    <Calendar className="w-4 h-4 mr-2" />
                    Inicio: {new Date(project.start_date).toLocaleDateString()}
                  </div>
                )}
                {project.budget && (
                  <div className="flex items-center">
                    <DollarSign className="w-4 h-4 mr-2" />
                    Presupuesto: ${project.budget.toLocaleString()}
                  </div>
                )}
                {project.owner && (
                  <div className="flex items-center">
                    <Users className="w-4 h-4 mr-2" />
                    Propietario: {project.owner.full_name}
                  </div>
                )}
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">
                    Tareas: {project.completed_tasks || 0}/{project.task_count || 0}
                  </span>
                  <span className="text-gray-500">
                    {project.progress || 0}% completado
                  </span>
                </div>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${project.progress || 0}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">
                {editingProject ? 'Editar Proyecto' : 'Nuevo Proyecto'}
              </h2>
              <button
                onClick={() => {
                  setIsModalOpen(false)
                  setEditingProject(null)
                  reset()
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre del Proyecto *
                </label>
                <input
                  type="text"
                  {...register('name')}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Ingresa el nombre del proyecto"
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descripción
                </label>
                <textarea
                  {...register('description')}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Describe el proyecto"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fecha de Inicio
                  </label>
                  <input
                    type="date"
                    {...register('start_date')}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fecha de Fin
                  </label>
                  <input
                    type="date"
                    {...register('end_date')}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Presupuesto
                </label>
                <input
                  type="number"
                  step="0.01"
                  {...register('budget', { valueAsNumber: true })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="0.00"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Estado
                </label>
                <select
                  {...register('status')}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="planning">Planificación</option>
                  <option value="active">Activo</option>
                  <option value="on_hold">En Pausa</option>
                  <option value="completed">Completado</option>
                  <option value="cancelled">Cancelado</option>
                </select>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setIsModalOpen(false)
                    setEditingProject(null)
                    reset()
                  }}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={createProjectMutation.isPending || updateProjectMutation.isPending}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {createProjectMutation.isPending || updateProjectMutation.isPending
                    ? 'Guardando...'
                    : editingProject
                    ? 'Actualizar'
                    : 'Crear'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      </div>
    </div>
  )
}

export default ProjectsPage