import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { 
  Plus, 
  Search, 
  Filter, 
  Calendar, 
  Flag, 
  CheckCircle, 
  Clock,
  MoreVertical,
  Edit,
  Trash2,
  User,
  Sparkles,
  Target,
  Zap,
  AlertCircle,
  X,
  ArrowUpDown,
  ArrowUp,
  ArrowDown
} from 'lucide-react'
import { apiClient } from '../services/apiClient'
import { useAuthToken } from '../hooks/useAuthToken'
import toast from 'react-hot-toast'

const taskSchema = z.object({
  title: z.string().min(1, 'El título de la tarea es requerido'),
  description: z.string().optional(),
  project_id: z.number().min(1, 'Debe seleccionar un proyecto'),
  assignee_id: z.number().optional(),
  priority: z.enum(['low', 'medium', 'high', 'critical']),
  status: z.enum(['todo', 'in_progress', 'in_review', 'done', 'cancelled']),
  due_date: z.string().optional(),
  estimated_hours: z.number().min(0).optional(),
})

type TaskForm = z.infer<typeof taskSchema>

interface Task {
  id: number
  title: string
  description?: string
  project_id: number
  project?: { id: number; name: string }
  assignee_id?: number
  assignee?: { id: number; name: string; email: string }
  priority: string
  status: string
  due_date?: string
  estimated_hours?: number
  created_at: string
  updated_at: string
}

interface Project {
  id: number
  name: string
}

const TasksPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [projectFilter, setProjectFilter] = useState('all')
  const [sortBy, setSortBy] = useState('created_at')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const queryClient = useQueryClient()
  const { isReady } = useAuthToken()

  const { data: tasks, isLoading, error: tasksError } = useQuery({
    queryKey: ['tasks', searchTerm, statusFilter, priorityFilter, projectFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      if (statusFilter !== 'all') params.append('status', statusFilter)
      if (priorityFilter !== 'all') params.append('priority', priorityFilter)
      if (projectFilter !== 'all') params.append('project_id', projectFilter)
      
      const response = await apiClient.get(`/tasks/?${params.toString()}`)
      return response.data as Task[]
    },
    enabled: isReady,
    onError: (error: any) => {
      console.error('Error loading tasks:', error)
      toast.error('Error al cargar las tareas')
    },
  })

  const { data: projects, error: projectsError } = useQuery({
    queryKey: ['projects-list'],
    queryFn: async () => {
      const response = await apiClient.get('/projects/')
      return response.data as Project[]
    },
    enabled: isReady,
    onError: (error: any) => {
      console.error('Error loading projects:', error)
      toast.error('Error al cargar los proyectos')
    },
  })

  const { data: users } = useQuery({
    queryKey: ['users-list'],
    queryFn: async () => {
      try {
        const response = await apiClient.get('/auth/users')
        return response.data as { id: number; name: string; email: string }[]
      } catch (error: any) {
        // Si no tiene permisos para ver usuarios, devolver array vacío
        if (error.response?.status === 403) {
          console.log('No permissions to load users list - using empty list')
          return []
        }
        throw error
      }
    },
    enabled: isReady,
    onError: (error: any) => {
      console.error('Error loading users:', error)
      // No mostrar toast para errores de permisos
      if (error.response?.status !== 403) {
        toast.error('Error al cargar los usuarios')
      }
    },
  })

  const createTaskMutation = useMutation({
    mutationFn: async (data: TaskForm) => {
      const response = await apiClient.post('/tasks/', data)
      return response.data
    },
    onSuccess: (newTask) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      queryClient.invalidateQueries({ queryKey: ['tasks-list'] })
      setIsModalOpen(false)
      reset()
      toast.success('Task created successfully!')
    },
    onError: (error: any) => {
      console.error('Task creation error:', error)
      console.error('Error response:', error.response?.data)
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message || 
                          'Error al crear la tarea'
      toast.error(errorMessage)
    },
  })

  const updateTaskMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: TaskForm }) => {
      const response = await apiClient.put(`/tasks/${id}`, data)
      return response.data
    },
    onSuccess: (updatedTask) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      queryClient.invalidateQueries({ queryKey: ['tasks-list'] })
      setIsModalOpen(false)
      setEditingTask(null)
      reset()
      toast.success('Task updated successfully!')
    },
    onError: (error: any) => {
      console.error('Task update error:', error)
      console.error('Error response:', error.response?.data)
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message || 
                          'Error al actualizar la tarea'
      toast.error(errorMessage)
    },
  })

  const deleteTaskMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/tasks/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      queryClient.invalidateQueries({ queryKey: ['tasks-list'] })
      toast.success('Task deleted successfully!')
    },
    onError: (error: any) => {
      console.error('Task deletion error:', error)
      toast.error(error.response?.data?.detail || 'Failed to delete task')
    },
  })

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<TaskForm>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: '',
      description: '',
      priority: 'medium',
      status: 'todo',
      estimated_hours: 0,
    },
  })

  const onSubmit = (data: TaskForm) => {
    // Limpiar y preparar los datos
    const cleanData: any = {
      title: data.title.trim(),
      project_id: data.project_id,
      priority: data.priority,
      status: data.status,
    }

    // Solo agregar campos opcionales si tienen valores válidos
    if (data.description && data.description.trim()) {
      cleanData.description = data.description.trim()
    }

    if (data.assignee_id && data.assignee_id > 0) {
      cleanData.assignee_id = data.assignee_id
    }

    if (data.due_date && data.due_date.trim()) {
      cleanData.due_date = data.due_date
    }

    if (data.estimated_hours && data.estimated_hours > 0) {
      cleanData.estimated_hours = data.estimated_hours
    }

    console.log('Submitting task data:', cleanData)

    if (editingTask) {
      updateTaskMutation.mutate({ id: editingTask.id, data: cleanData })
    } else {
      createTaskMutation.mutate(cleanData)
    }
  }

  const handleEdit = (task: Task) => {
    setEditingTask(task)
    setValue('title', task.title)
    setValue('description', task.description || '')
    setValue('project_id', task.project_id)
    setValue('assignee_id', task.assignee_id)
    setValue('priority', task.priority as any)
    setValue('status', task.status as any)
    setValue('due_date', task.due_date ? task.due_date.split('T')[0] : '')
    setValue('estimated_hours', task.estimated_hours || 0)
    setIsModalOpen(true)
  }

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      deleteTaskMutation.mutate(id)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'text-danger-600'
      case 'high': return 'text-warning-600'
      case 'medium': return 'text-info-600'
      default: return 'text-success-600'
    }
  }

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'critical': return AlertCircle
      case 'high': return Zap
      case 'medium': return Flag
      default: return Target
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'done': return 'bg-success-100 text-success-700 border border-success-200'
      case 'in_progress': return 'bg-info-100 text-info-700 border border-info-200'
      case 'in_review': return 'bg-warning-100 text-warning-700 border border-warning-200'
      case 'cancelled': return 'bg-danger-100 text-danger-700 border border-danger-200'
      default: return 'bg-gray-100 text-gray-700 border border-gray-200'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'done': return 'Completada'
      case 'in_progress': return 'En Progreso'
      case 'in_review': return 'En Revisión'
      case 'todo': return 'Por Hacer'
      case 'cancelled': return 'Cancelada'
      default: return status
    }
  }

  const getPriorityText = (priority: string) => {
    switch (priority) {
      case 'critical': return 'Crítica'
      case 'high': return 'Alta'
      case 'medium': return 'Media'
      case 'low': return 'Baja'
      default: return priority
    }
  }

  const filteredAndSortedTasks = tasks
    ?.filter(task => {
      const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           (task.description || '').toLowerCase().includes(searchTerm.toLowerCase())
      const matchesStatus = statusFilter === 'all' || task.status === statusFilter
      const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter
      const matchesProject = projectFilter === 'all' || task.project_id.toString() === projectFilter
      return matchesSearch && matchesStatus && matchesPriority && matchesProject
    })
    ?.sort((a, b) => {
      let aValue: any, bValue: any
      
      switch (sortBy) {
        case 'title':
          // Ordenamiento alfabético por primera letra del título
          aValue = a.title.toLowerCase().charAt(0)
          bValue = b.title.toLowerCase().charAt(0)
          // Si las primeras letras son iguales, comparar títulos completos
          if (aValue === bValue) {
            aValue = a.title.toLowerCase()
            bValue = b.title.toLowerCase()
          }
          break
        case 'due_date':
          aValue = a.due_date ? new Date(a.due_date).getTime() : 0
          bValue = b.due_date ? new Date(b.due_date).getTime() : 0
          break
        case 'priority':
          const priorityOrder = { 'critical': 4, 'high': 3, 'medium': 2, 'low': 1 }
          aValue = priorityOrder[a.priority as keyof typeof priorityOrder] || 0
          bValue = priorityOrder[b.priority as keyof typeof priorityOrder] || 0
          break
        case 'estimated_hours':
          aValue = a.estimated_hours || 0
          bValue = b.estimated_hours || 0
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

  if (!isReady) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-secondary-600">Cargando autenticación...</p>
        </div>
      </div>
    )
  }

  // Mostrar errores si los hay
  if (tasksError || projectsError) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-2xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-soft p-6 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-red-800 mb-2">Error al cargar datos</h2>
            <p className="text-red-600 mb-4">
              Hubo un problema al cargar la información. Por favor, verifica tu conexión e intenta nuevamente.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-red-600 text-white px-4 py-2 rounded-soft hover:bg-red-700 transition-colors"
            >
              Recargar página
            </button>
          </div>
        </div>
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
              <div className="p-3 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl shadow-lg">
                <CheckCircle className="h-8 w-8 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-800 font-nunito">Tareas</h1>
              <p className="text-gray-600 font-open-sans">Gestiona y organiza tus tareas</p>
            </div>
          </div>
          <button
            onClick={() => {
              setEditingTask(null)
              reset()
              setIsModalOpen(true)
            }}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-200 flex items-center gap-3 shadow-soft hover:shadow-lg"
          >
            <Plus className="h-5 w-5" />
            Nueva Tarea
          </button>
        </div>

      {/* Filters and Sorting */}
      <div className="bg-white rounded-soft soft-shadow p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
          <div className="relative group">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-secondary-400 group-focus-within:text-primary-500 transition-colors duration-300" />
            <input
              type="text"
              placeholder="Buscar tareas..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 placeholder-secondary-400 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-300 hover:bg-gray-100 font-sans"
            />
          </div>
          
          <div className="relative group">
            <Filter className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-secondary-400 group-focus-within:text-primary-500 transition-colors duration-300" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-300 hover:bg-gray-100 appearance-none cursor-pointer font-sans"
            >
              <option value="all">Todos los Estados</option>
              <option value="todo">Por Hacer</option>
              <option value="in_progress">En Progreso</option>
              <option value="in_review">En Revisión</option>
              <option value="done">Completada</option>
              <option value="cancelled">Cancelada</option>
            </select>
          </div>

          <div className="relative group">
            <Flag className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-secondary-400 group-focus-within:text-primary-500 transition-colors duration-300" />
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-300 hover:bg-gray-100 appearance-none cursor-pointer font-sans"
            >
              <option value="all">Todas las Prioridades</option>
              <option value="low">Baja</option>
              <option value="medium">Media</option>
              <option value="high">Alta</option>
              <option value="critical">Crítica</option>
            </select>
          </div>

          <div className="relative group">
            <User className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-secondary-400 group-focus-within:text-primary-500 transition-colors duration-300" />
            <select
              value={projectFilter}
              onChange={(e) => setProjectFilter(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-300 hover:bg-gray-100 appearance-none cursor-pointer font-sans"
            >
              <option value="all">Todos los Proyectos</option>
              {projects?.map((project) => (
                <option key={project.id} value={project.id.toString()}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>

          {/* Sorting Controls */}
          <div className="relative group">
            <ArrowUpDown className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-secondary-400 group-focus-within:text-primary-500 transition-colors duration-300" />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-300 hover:bg-gray-100 appearance-none cursor-pointer font-sans"
            >
              <option value="created_at">Fecha de creación</option>
              <option value="title">Título (A-Z)</option>
              <option value="due_date">Fecha de vencimiento</option>
              <option value="priority">Prioridad</option>
              <option value="estimated_hours">Horas estimadas</option>
            </select>
          </div>

          <div className="flex items-center">
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
              title={sortOrder === 'asc' ? 'Cambiar a descendente (más reciente primero)' : 'Cambiar a ascendente (más antiguo primero)'}
            >
              {sortOrder === 'asc' ? (
                <ArrowUp className="h-4 w-4" />
              ) : (
                <ArrowDown className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Tasks List */}
      {isLoading ? (
        <div className="space-y-6">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="bg-white rounded-soft soft-shadow p-6">
              <div className="h-6 bg-gray-200 rounded-soft mb-3"></div>
              <div className="h-4 bg-gray-100 rounded-soft mb-4"></div>
              <div className="flex gap-4">
                <div className="h-4 bg-gray-100 rounded-soft w-24"></div>
                <div className="h-4 bg-gray-100 rounded-soft w-20"></div>
                <div className="h-4 bg-gray-100 rounded-soft w-28"></div>
              </div>
            </div>
          ))}
        </div>
      ) : filteredAndSortedTasks?.length === 0 ? (
        <div className="text-center py-16">
          <div className="bg-white rounded-soft soft-shadow p-8 max-w-md mx-auto">
            <div className="h-16 w-16 text-secondary-400 mx-auto mb-6 flex items-center justify-center">
              <svg className="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-dark-700 mb-3">No se encontraron tareas</h3>
            <p className="text-secondary-500 font-sans">Comienza creando tu primera tarea para organizar tu trabajo.</p>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredAndSortedTasks?.map((task, index) => {
            const PriorityIcon = getPriorityIcon(task.priority)
            return (
              <div 
                key={task.id} 
                className="bg-white rounded-soft soft-shadow hover:soft-shadow-lg group transition-all duration-300 hover:scale-[1.02] p-6"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-4 mb-3">
                      <h3 className="text-xl font-semibold text-dark-700 group-hover:text-primary-600 transition-colors duration-300">
                        {task.title}
                      </h3>
                      <div className="flex items-center gap-2">
                        <PriorityIcon className={`h-5 w-5 ${getPriorityColor(task.priority)}`} />
                        <span className="text-xs text-secondary-500 font-medium font-sans">
                          {getPriorityText(task.priority)}
                        </span>
                      </div>
                      <span className={`px-3 py-1 text-xs font-medium rounded-soft ${getStatusColor(task.status)} font-sans`}>
                        {getStatusText(task.status)}
                      </span>
                    </div>

                    {task.description && (
                      <p className="text-secondary-600 text-sm mb-4 leading-relaxed font-sans">
                        {task.description}
                      </p>
                    )}

                    <div className="flex flex-wrap items-center gap-6 text-sm">
                      <div className="flex items-center gap-2 text-secondary-500 hover:text-primary-600 transition-colors duration-300">
                        <User className="h-4 w-4" />
                        <span className="font-sans">{task.project?.name}</span>
                      </div>
                      
                      {task.assignee && (
                        <div className="flex items-center gap-2 text-secondary-500 hover:text-info-600 transition-colors duration-300">
                          <User className="h-4 w-4" />
                          <span className="font-sans">{task.assignee.name}</span>
                        </div>
                      )}
                      
                      {task.due_date && (
                        <div className="flex items-center gap-2 text-secondary-500 hover:text-success-600 transition-colors duration-300">
                          <Calendar className="h-4 w-4" />
                          <span className="font-sans">{new Date(task.due_date).toLocaleDateString()}</span>
                        </div>
                      )}
                      
                      {task.estimated_hours && (
                        <div className="flex items-center gap-2 text-secondary-500 hover:text-warning-600 transition-colors duration-300">
                          <Clock className="h-4 w-4" />
                          <span className="font-sans">{task.estimated_hours}h</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleEdit(task)}
                      className="p-3 text-secondary-400 hover:text-info-600 hover:bg-info-50 rounded-soft transition-all duration-300 hover:scale-110"
                    >
                      <Edit className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(task.id)}
                      className="p-3 text-secondary-400 hover:text-danger-600 hover:bg-danger-50 rounded-soft transition-all duration-300 hover:scale-110"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-soft soft-shadow p-8 w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-dark-700 flex items-center gap-2">
                <Sparkles className="h-6 w-6 text-primary-500" />
                {editingTask ? 'Editar Tarea' : 'Nueva Tarea'}
              </h3>
              <button
                onClick={() => {
                  setIsModalOpen(false)
                  setEditingTask(null)
                  reset()
                }}
                className="text-secondary-400 hover:text-dark-700 transition-colors duration-200 hover:bg-gray-100 rounded-soft p-2"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                  Título
                </label>
                <input
                  {...register('title')}
                  type="text"
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 placeholder-secondary-400 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 font-sans"
                  placeholder="Título de la tarea"
                />
                {errors.title && (
                  <p className="text-danger-600 text-sm mt-2 flex items-center gap-1 font-sans">
                    <AlertCircle className="h-4 w-4" />
                    {errors.title.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                  Descripción
                </label>
                <textarea
                  {...register('description')}
                  rows={3}
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 placeholder-secondary-400 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 resize-none font-sans"
                  placeholder="Descripción de la tarea"
                />
                {errors.description && (
                  <p className="text-danger-600 text-sm mt-2 flex items-center gap-1 font-sans">
                    <AlertCircle className="h-4 w-4" />
                    {errors.description.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                  Proyecto
                </label>
                <select {...register('project_id', { valueAsNumber: true })} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 font-sans">
                  <option value="" className="bg-white text-secondary-500">Seleccionar proyecto</option>
                  {projects?.map((project) => (
                    <option key={project.id} value={project.id} className="bg-white text-dark-700">
                      {project.name}
                    </option>
                  ))}
                </select>
                {errors.project_id && (
                  <p className="text-danger-600 text-sm mt-2 flex items-center gap-1 font-sans">
                    <AlertCircle className="h-4 w-4" />
                    {errors.project_id.message}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                  Asignado a
                </label>
                <select {...register('assignee_id', { valueAsNumber: true })} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 font-sans">
                  <option value="" className="bg-white text-secondary-500">Sin asignar</option>
                  {users?.map((user) => (
                    <option key={user.id} value={user.id} className="bg-white text-dark-700">
                      {user.name} ({user.email})
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                    Prioridad
                  </label>
                  <select {...register('priority')} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 font-sans">
                    <option value="low" className="bg-white text-dark-700">Baja</option>
                    <option value="medium" className="bg-white text-dark-700">Media</option>
                    <option value="high" className="bg-white text-dark-700">Alta</option>
                    <option value="critical" className="bg-white text-dark-700">Crítica</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                    Estado
                  </label>
                  <select {...register('status')} className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 font-sans">
                    <option value="todo" className="bg-white text-dark-700">Por Hacer</option>
                    <option value="in_progress" className="bg-white text-dark-700">En Progreso</option>
                    <option value="in_review" className="bg-white text-dark-700">En Revisión</option>
                    <option value="done" className="bg-white text-dark-700">Completada</option>
                    <option value="cancelled" className="bg-white text-dark-700">Cancelada</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                    Fecha de vencimiento
                  </label>
                  <input
                    {...register('due_date')}
                    type="date"
                    className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 font-sans"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-dark-700 mb-2 font-sans">
                    Horas estimadas
                  </label>
                  <input
                    {...register('estimated_hours', { valueAsNumber: true })}
                    type="number"
                    min="0"
                    step="0.5"
                    className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-soft text-dark-700 placeholder-secondary-400 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all duration-200 hover:bg-gray-100 font-sans"
                    placeholder="0"
                  />
                </div>
              </div>

              <div className="flex gap-3 pt-6">
                <button
                  type="button"
                  onClick={() => {
                    setIsModalOpen(false)
                    setEditingTask(null)
                    reset()
                  }}
                  className="px-6 py-3 text-secondary-600 border border-gray-200 rounded-soft hover:bg-gray-50 hover:text-dark-700 transition-all duration-200 flex-1 font-sans"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={createTaskMutation.isPending || updateTaskMutation.isPending}
                  className="px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white rounded-soft disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 soft-shadow hover:soft-shadow-lg flex items-center gap-2 flex-1 justify-center font-sans"
                >
                  {createTaskMutation.isPending || updateTaskMutation.isPending ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                      Guardando...
                    </>
                  ) : (
                    <>
                      <Zap className="h-4 w-4" />
                      {editingTask ? 'Actualizar' : 'Crear'}
                    </>
                  )}
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

export default TasksPage