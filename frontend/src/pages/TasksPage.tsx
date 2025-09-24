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
  User
} from 'lucide-react'
import { apiClient } from '../services/apiClient'
import toast from 'react-hot-toast'

const taskSchema = z.object({
  title: z.string().min(1, 'Task title is required'),
  description: z.string().min(1, 'Description is required'),
  project_id: z.number().min(1, 'Project is required'),
  assigned_to: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  status: z.enum(['todo', 'in_progress', 'review', 'completed']),
  due_date: z.string().optional(),
  estimated_hours: z.number().min(0).optional(),
})

type TaskForm = z.infer<typeof taskSchema>

interface Task {
  id: number
  title: string
  description: string
  project_id: number
  project?: { id: number; name: string }
  assigned_to?: string
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
  const queryClient = useQueryClient()

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks', searchTerm, statusFilter, priorityFilter, projectFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      if (statusFilter !== 'all') params.append('status', statusFilter)
      if (priorityFilter !== 'all') params.append('priority', priorityFilter)
      if (projectFilter !== 'all') params.append('project_id', projectFilter)
      
      const response = await apiClient.get(`/tasks?${params.toString()}`)
      return response.data as Task[]
    },
  })

  const { data: projects } = useQuery({
    queryKey: ['projects-list'],
    queryFn: async () => {
      const response = await apiClient.get('/projects')
      return response.data as Project[]
    },
  })

  const createTaskMutation = useMutation({
    mutationFn: async (data: TaskForm) => {
      const response = await apiClient.post('/tasks', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      setIsModalOpen(false)
      reset()
      toast.success('Task created successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create task')
    },
  })

  const updateTaskMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: TaskForm }) => {
      const response = await apiClient.put(`/tasks/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      setIsModalOpen(false)
      setEditingTask(null)
      reset()
      toast.success('Task updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update task')
    },
  })

  const deleteTaskMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/tasks/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task deleted successfully!')
    },
    onError: (error: any) => {
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
  })

  const onSubmit = (data: TaskForm) => {
    if (editingTask) {
      updateTaskMutation.mutate({ id: editingTask.id, data })
    } else {
      createTaskMutation.mutate(data)
    }
  }

  const handleEdit = (task: Task) => {
    setEditingTask(task)
    setValue('title', task.title)
    setValue('description', task.description)
    setValue('project_id', task.project_id)
    setValue('assigned_to', task.assigned_to || '')
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
      case 'urgent': return 'text-red-600'
      case 'high': return 'text-orange-600'
      case 'medium': return 'text-yellow-600'
      default: return 'text-green-600'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'in_progress': return 'bg-blue-100 text-blue-800'
      case 'review': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredTasks = tasks?.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         task.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || task.status === statusFilter
    const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter
    const matchesProject = projectFilter === 'all' || task.project_id.toString() === projectFilter
    return matchesSearch && matchesStatus && matchesPriority && matchesProject
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
        <button
          onClick={() => {
            setEditingTask(null)
            reset()
            setIsModalOpen(true)
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          New Task
        </button>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search tasks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input pl-10"
          />
        </div>
        
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input"
        >
          <option value="all">All Status</option>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="review">Review</option>
          <option value="completed">Completed</option>
        </select>

        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
          className="input"
        >
          <option value="all">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="urgent">Urgent</option>
        </select>

        <select
          value={projectFilter}
          onChange={(e) => setProjectFilter(e.target.value)}
          className="input"
        >
          <option value="all">All Projects</option>
          {projects?.map((project) => (
            <option key={project.id} value={project.id.toString()}>
              {project.name}
            </option>
          ))}
        </select>
      </div>

      {/* Tasks List */}
      {isLoading ? (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-3 bg-gray-200 rounded mb-4"></div>
              <div className="flex gap-4">
                <div className="h-3 bg-gray-200 rounded w-20"></div>
                <div className="h-3 bg-gray-200 rounded w-16"></div>
                <div className="h-3 bg-gray-200 rounded w-24"></div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {filteredTasks?.map((task) => (
            <div key={task.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {task.title}
                    </h3>
                    <Flag className={`h-4 w-4 ${getPriorityColor(task.priority)}`} />
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(task.status)}`}>
                      {task.status.replace('_', ' ')}
                    </span>
                  </div>

                  <p className="text-gray-600 text-sm mb-3">
                    {task.description}
                  </p>

                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                    <div className="flex items-center gap-1">
                      <User className="h-4 w-4" />
                      <span>{task.project?.name}</span>
                    </div>
                    
                    {task.assigned_to && (
                      <div className="flex items-center gap-1">
                        <User className="h-4 w-4" />
                        <span>{task.assigned_to}</span>
                      </div>
                    )}
                    
                    {task.due_date && (
                      <div className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        <span>{new Date(task.due_date).toLocaleDateString()}</span>
                      </div>
                    )}
                    
                    {task.estimated_hours && (
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        <span>{task.estimated_hours}h</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleEdit(task)}
                    className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(task.id)}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              {editingTask ? 'Edit Task' : 'Create New Task'}
            </h2>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Task Title
                </label>
                <input
                  {...register('title')}
                  type="text"
                  className="input"
                  placeholder="Enter task title"
                />
                {errors.title && (
                  <p className="text-red-600 text-sm mt-1">{errors.title.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  {...register('description')}
                  rows={3}
                  className="input"
                  placeholder="Enter task description"
                />
                {errors.description && (
                  <p className="text-red-600 text-sm mt-1">{errors.description.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Project
                </label>
                <select {...register('project_id', { valueAsNumber: true })} className="input">
                  <option value="">Select a project</option>
                  {projects?.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.name}
                    </option>
                  ))}
                </select>
                {errors.project_id && (
                  <p className="text-red-600 text-sm mt-1">{errors.project_id.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Assigned To
                </label>
                <input
                  {...register('assigned_to')}
                  type="text"
                  className="input"
                  placeholder="Enter assignee name or email"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Priority
                  </label>
                  <select {...register('priority')} className="input">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status
                  </label>
                  <select {...register('status')} className="input">
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="review">Review</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Due Date
                  </label>
                  <input
                    {...register('due_date')}
                    type="date"
                    className="input"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Estimated Hours
                  </label>
                  <input
                    {...register('estimated_hours', { valueAsNumber: true })}
                    type="number"
                    min="0"
                    step="0.5"
                    className="input"
                    placeholder="0"
                  />
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setIsModalOpen(false)
                    setEditingTask(null)
                    reset()
                  }}
                  className="btn-outline flex-1"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createTaskMutation.isPending || updateTaskMutation.isPending}
                  className="btn-primary flex-1"
                >
                  {createTaskMutation.isPending || updateTaskMutation.isPending
                    ? 'Saving...'
                    : editingTask
                    ? 'Update'
                    : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default TasksPage