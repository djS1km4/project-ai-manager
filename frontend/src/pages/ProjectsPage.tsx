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
  DollarSign, 
  Users, 
  MoreVertical,
  Edit,
  Trash2,
  Eye
} from 'lucide-react'
import { apiClient } from '../services/apiClient'
import toast from 'react-hot-toast'

const projectSchema = z.object({
  name: z.string().min(1, 'Project name is required'),
  description: z.string().min(1, 'Description is required'),
  start_date: z.string(),
  due_date: z.string(),
  budget: z.number().min(0, 'Budget must be positive'),
  status: z.enum(['planning', 'active', 'on_hold', 'completed', 'cancelled']),
})

type ProjectForm = z.infer<typeof projectSchema>

interface Project {
  id: number
  name: string
  description: string
  start_date: string
  due_date: string
  budget: number
  status: string
  created_at: string
  updated_at: string
}

const ProjectsPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingProject, setEditingProject] = useState<Project | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const queryClient = useQueryClient()

  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects', searchTerm, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      if (statusFilter !== 'all') params.append('status', statusFilter)
      
      const response = await apiClient.get(`/projects?${params.toString()}`)
      return response.data as Project[]
    },
  })

  const createProjectMutation = useMutation({
    mutationFn: async (data: ProjectForm) => {
      const response = await apiClient.post('/projects', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setIsModalOpen(false)
      reset()
      toast.success('Project created successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create project')
    },
  })

  const updateProjectMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: ProjectForm }) => {
      const response = await apiClient.put(`/projects/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setIsModalOpen(false)
      setEditingProject(null)
      reset()
      toast.success('Project updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update project')
    },
  })

  const deleteProjectMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/projects/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      toast.success('Project deleted successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to delete project')
    },
  })

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<ProjectForm>({
    resolver: zodResolver(projectSchema),
  })

  const onSubmit = (data: ProjectForm) => {
    if (editingProject) {
      updateProjectMutation.mutate({ id: editingProject.id, data })
    } else {
      createProjectMutation.mutate(data)
    }
  }

  const handleEdit = (project: Project) => {
    setEditingProject(project)
    setValue('name', project.name)
    setValue('description', project.description)
    setValue('start_date', project.start_date.split('T')[0])
    setValue('due_date', project.due_date.split('T')[0])
    setValue('budget', project.budget)
    setValue('status', project.status as any)
    setIsModalOpen(true)
  }

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      deleteProjectMutation.mutate(id)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-blue-100 text-blue-800'
      case 'completed': return 'bg-green-100 text-green-800'
      case 'on_hold': return 'bg-yellow-100 text-yellow-800'
      case 'cancelled': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredProjects = projects?.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || project.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
        <button
          onClick={() => {
            setEditingProject(null)
            reset()
            setIsModalOpen(true)
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          New Project
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search projects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input pl-10"
          />
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input pl-10 pr-8"
          >
            <option value="all">All Status</option>
            <option value="planning">Planning</option>
            <option value="active">Active</option>
            <option value="on_hold">On Hold</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {/* Projects Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-3 bg-gray-200 rounded mb-4"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects?.map((project) => (
            <div key={project.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-900 truncate">
                  {project.name}
                </h3>
                <div className="relative">
                  <button className="p-1 hover:bg-gray-100 rounded">
                    <MoreVertical className="h-4 w-4 text-gray-400" />
                  </button>
                  <div className="absolute right-0 mt-1 w-32 bg-white rounded-md shadow-lg border border-gray-200 z-10 hidden group-hover:block">
                    <button
                      onClick={() => handleEdit(project)}
                      className="flex items-center gap-2 w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
                    >
                      <Edit className="h-3 w-3" />
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="flex items-center gap-2 w-full px-3 py-2 text-sm text-red-600 hover:bg-red-50"
                    >
                      <Trash2 className="h-3 w-3" />
                      Delete
                    </button>
                  </div>
                </div>
              </div>

              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {project.description}
              </p>

              <div className="space-y-2 mb-4">
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Calendar className="h-4 w-4" />
                  <span>
                    {new Date(project.start_date).toLocaleDateString()} - {new Date(project.due_date).toLocaleDateString()}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <DollarSign className="h-4 w-4" />
                  <span>${project.budget.toLocaleString()}</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(project.status)}`}>
                  {project.status.replace('_', ' ')}
                </span>
                <button className="text-primary-600 hover:text-primary-500 text-sm font-medium">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              {editingProject ? 'Edit Project' : 'Create New Project'}
            </h2>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Project Name
                </label>
                <input
                  {...register('name')}
                  type="text"
                  className="input"
                  placeholder="Enter project name"
                />
                {errors.name && (
                  <p className="text-red-600 text-sm mt-1">{errors.name.message}</p>
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
                  placeholder="Enter project description"
                />
                {errors.description && (
                  <p className="text-red-600 text-sm mt-1">{errors.description.message}</p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Start Date
                  </label>
                  <input
                    {...register('start_date')}
                    type="date"
                    className="input"
                  />
                  {errors.start_date && (
                    <p className="text-red-600 text-sm mt-1">{errors.start_date.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Due Date
                  </label>
                  <input
                    {...register('due_date')}
                    type="date"
                    className="input"
                  />
                  {errors.due_date && (
                    <p className="text-red-600 text-sm mt-1">{errors.due_date.message}</p>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Budget
                </label>
                <input
                  {...register('budget', { valueAsNumber: true })}
                  type="number"
                  min="0"
                  step="0.01"
                  className="input"
                  placeholder="0.00"
                />
                {errors.budget && (
                  <p className="text-red-600 text-sm mt-1">{errors.budget.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select {...register('status')} className="input">
                  <option value="planning">Planning</option>
                  <option value="active">Active</option>
                  <option value="on_hold">On Hold</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
                {errors.status && (
                  <p className="text-red-600 text-sm mt-1">{errors.status.message}</p>
                )}
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setIsModalOpen(false)
                    setEditingProject(null)
                    reset()
                  }}
                  className="btn-outline flex-1"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createProjectMutation.isPending || updateProjectMutation.isPending}
                  className="btn-primary flex-1"
                >
                  {createProjectMutation.isPending || updateProjectMutation.isPending
                    ? 'Saving...'
                    : editingProject
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

export default ProjectsPage