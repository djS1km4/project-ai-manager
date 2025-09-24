import { useQuery } from '@tanstack/react-query'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { 
  FolderOpen, 
  CheckCircle, 
  Clock, 
  AlertTriangle,
  TrendingUp,
  Users,
  Calendar,
  DollarSign
} from 'lucide-react'
import { apiClient } from '../services/apiClient'

interface DashboardStats {
  totalProjects: number
  activeProjects: number
  completedProjects: number
  totalTasks: number
  completedTasks: number
  overdueTasks: number
  totalBudget: number
  usedBudget: number
}

interface ProjectStatus {
  name: string
  value: number
  color: string
}

const DashboardPage = () => {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const response = await apiClient.get('/dashboard/stats')
      return response.data as DashboardStats
    },
  })

  const { data: projectsData, isLoading: projectsLoading } = useQuery({
    queryKey: ['dashboard-projects'],
    queryFn: async () => {
      const response = await apiClient.get('/projects?limit=5')
      return response.data
    },
  })

  const { data: tasksData, isLoading: tasksLoading } = useQuery({
    queryKey: ['dashboard-tasks'],
    queryFn: async () => {
      const response = await apiClient.get('/tasks?limit=10')
      return response.data
    },
  })

  const projectStatusData: ProjectStatus[] = [
    { name: 'Active', value: stats?.activeProjects || 0, color: '#3B82F6' },
    { name: 'Completed', value: stats?.completedProjects || 0, color: '#10B981' },
    { name: 'On Hold', value: (stats?.totalProjects || 0) - (stats?.activeProjects || 0) - (stats?.completedProjects || 0), color: '#F59E0B' },
  ]

  const taskCompletionData = [
    { name: 'Jan', completed: 12, total: 20 },
    { name: 'Feb', completed: 18, total: 25 },
    { name: 'Mar', completed: 15, total: 22 },
    { name: 'Apr', completed: 22, total: 28 },
    { name: 'May', completed: 25, total: 30 },
    { name: 'Jun', completed: 20, total: 24 },
  ]

  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date().toLocaleDateString()}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <FolderOpen className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Projects</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.totalProjects || 0}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Completed Tasks</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.completedTasks || 0}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Clock className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending Tasks</p>
              <p className="text-2xl font-bold text-gray-900">
                {(stats?.totalTasks || 0) - (stats?.completedTasks || 0)}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Overdue Tasks</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.overdueTasks || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Project Status Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Status</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={projectStatusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {projectStatusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Task Completion Trend */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Task Completion Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={taskCompletionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="completed" fill="#10B981" name="Completed" />
              <Bar dataKey="total" fill="#E5E7EB" name="Total" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Projects and Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Projects */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recent Projects</h3>
            <a href="/projects" className="text-primary-600 hover:text-primary-500 text-sm font-medium">
              View all
            </a>
          </div>
          <div className="space-y-3">
            {projectsLoading ? (
              <div className="animate-pulse space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-16 bg-gray-200 rounded"></div>
                ))}
              </div>
            ) : (
              projectsData?.slice(0, 5).map((project: any) => (
                <div key={project.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">{project.name}</h4>
                    <p className="text-sm text-gray-600">{project.description}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    project.status === 'completed' 
                      ? 'bg-green-100 text-green-800'
                      : project.status === 'active'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {project.status}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Tasks */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recent Tasks</h3>
            <a href="/tasks" className="text-primary-600 hover:text-primary-500 text-sm font-medium">
              View all
            </a>
          </div>
          <div className="space-y-3">
            {tasksLoading ? (
              <div className="animate-pulse space-y-3">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="h-12 bg-gray-200 rounded"></div>
                ))}
              </div>
            ) : (
              tasksData?.slice(0, 5).map((task: any) => (
                <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-3 ${
                      task.status === 'completed' 
                        ? 'bg-green-500'
                        : task.priority === 'high'
                        ? 'bg-red-500'
                        : task.priority === 'medium'
                        ? 'bg-yellow-500'
                        : 'bg-gray-500'
                    }`}></div>
                    <div>
                      <h4 className="font-medium text-gray-900">{task.title}</h4>
                      <p className="text-sm text-gray-600">{task.project?.name}</p>
                    </div>
                  </div>
                  <span className="text-xs text-gray-500">
                    {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No due date'}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Budget Overview */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Budget Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="p-3 bg-blue-100 rounded-lg inline-block mb-2">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
            <p className="text-sm text-gray-600">Total Budget</p>
            <p className="text-xl font-bold text-gray-900">
              ${(stats?.totalBudget || 0).toLocaleString()}
            </p>
          </div>
          <div className="text-center">
            <div className="p-3 bg-green-100 rounded-lg inline-block mb-2">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <p className="text-sm text-gray-600">Used Budget</p>
            <p className="text-xl font-bold text-gray-900">
              ${(stats?.usedBudget || 0).toLocaleString()}
            </p>
          </div>
          <div className="text-center">
            <div className="p-3 bg-yellow-100 rounded-lg inline-block mb-2">
              <Calendar className="h-6 w-6 text-yellow-600" />
            </div>
            <p className="text-sm text-gray-600">Remaining</p>
            <p className="text-xl font-bold text-gray-900">
              ${((stats?.totalBudget || 0) - (stats?.usedBudget || 0)).toLocaleString()}
            </p>
          </div>
        </div>
        <div className="mt-4">
          <div className="bg-gray-200 rounded-full h-2">
            <div 
              className="bg-primary-600 h-2 rounded-full" 
              style={{ 
                width: `${stats?.totalBudget ? (stats.usedBudget / stats.totalBudget) * 100 : 0}%` 
              }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {stats?.totalBudget ? ((stats.usedBudget / stats.totalBudget) * 100).toFixed(1) : 0}% of budget used
          </p>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage