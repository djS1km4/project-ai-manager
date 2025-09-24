import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { 
  Brain, 
  TrendingUp, 
  AlertTriangle, 
  Target, 
  Users, 
  BarChart3,
  RefreshCw,
  Lightbulb,
  Clock,
  CheckCircle
} from 'lucide-react'
import { apiClient } from '../services/apiClient'
import toast from 'react-hot-toast'

interface AIInsight {
  id: number
  project_id: number
  project_name: string
  insight_type: string
  content: string
  confidence_score: number
  created_at: string
}

interface ProjectAnalysis {
  project_id: number
  project_name: string
  risk_assessment: {
    level: string
    factors: string[]
    recommendations: string[]
  }
  progress_prediction: {
    completion_probability: number
    estimated_completion_date: string
    potential_delays: string[]
  }
  team_performance: {
    productivity_score: number
    bottlenecks: string[]
    suggestions: string[]
  }
}

const AIInsightsPage = () => {
  const [selectedProject, setSelectedProject] = useState<number | null>(null)
  const [analysisType, setAnalysisType] = useState<'risk' | 'progress' | 'team'>('risk')

  const { data: insights, isLoading: insightsLoading, refetch: refetchInsights } = useQuery({
    queryKey: ['ai-insights'],
    queryFn: async () => {
      const response = await apiClient.get('/ai/insights')
      return response.data as AIInsight[]
    },
  })

  const { data: projects } = useQuery({
    queryKey: ['projects-list'],
    queryFn: async () => {
      const response = await apiClient.get('/projects')
      return response.data
    },
  })

  const { data: analysis, isLoading: analysisLoading } = useQuery({
    queryKey: ['project-analysis', selectedProject],
    queryFn: async () => {
      if (!selectedProject) return null
      const response = await apiClient.get(`/ai/analyze/${selectedProject}`)
      return response.data as ProjectAnalysis
    },
    enabled: !!selectedProject,
  })

  const generateInsightMutation = useMutation({
    mutationFn: async (projectId: number) => {
      const response = await apiClient.post(`/ai/generate-insight/${projectId}`)
      return response.data
    },
    onSuccess: () => {
      refetchInsights()
      toast.success('New AI insight generated!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to generate insight')
    },
  })

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'risk': return <AlertTriangle className="h-5 w-5 text-red-500" />
      case 'progress': return <TrendingUp className="h-5 w-5 text-blue-500" />
      case 'team': return <Users className="h-5 w-5 text-green-500" />
      default: return <Brain className="h-5 w-5 text-purple-500" />
    }
  }

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100'
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'high': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Insights</h1>
          <p className="text-gray-600">AI-powered project analysis and recommendations</p>
        </div>
        <button
          onClick={() => refetchInsights()}
          className="btn-outline flex items-center gap-2"
        >
          <RefreshCw className="h-4 w-4" />
          Refresh
        </button>
      </div>

      {/* Project Analysis Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Project Selection */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Analysis</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Project
              </label>
              <select
                value={selectedProject || ''}
                onChange={(e) => setSelectedProject(e.target.value ? Number(e.target.value) : null)}
                className="input"
              >
                <option value="">Choose a project</option>
                {projects?.map((project: any) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Analysis Type
              </label>
              <div className="space-y-2">
                {[
                  { value: 'risk', label: 'Risk Assessment', icon: AlertTriangle },
                  { value: 'progress', label: 'Progress Prediction', icon: TrendingUp },
                  { value: 'team', label: 'Team Performance', icon: Users },
                ].map(({ value, label, icon: Icon }) => (
                  <button
                    key={value}
                    onClick={() => setAnalysisType(value as any)}
                    className={`w-full flex items-center gap-3 p-3 rounded-lg border transition-colors ${
                      analysisType === value
                        ? 'border-primary-500 bg-primary-50 text-primary-700'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span className="text-sm font-medium">{label}</span>
                  </button>
                ))}
              </div>
            </div>

            {selectedProject && (
              <button
                onClick={() => generateInsightMutation.mutate(selectedProject)}
                disabled={generateInsightMutation.isPending}
                className="btn-primary w-full flex items-center gap-2"
              >
                <Brain className="h-4 w-4" />
                {generateInsightMutation.isPending ? 'Generating...' : 'Generate Insight'}
              </button>
            )}
          </div>
        </div>

        {/* Analysis Results */}
        <div className="lg:col-span-2">
          {analysisLoading ? (
            <div className="card">
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>
            </div>
          ) : analysis ? (
            <div className="space-y-6">
              {/* Risk Assessment */}
              {analysisType === 'risk' && analysis.risk_assessment && (
                <div className="card">
                  <div className="flex items-center gap-3 mb-4">
                    <AlertTriangle className="h-6 w-6 text-red-500" />
                    <h3 className="text-lg font-semibold text-gray-900">Risk Assessment</h3>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-medium text-gray-600">Risk Level:</span>
                      <span className={`px-3 py-1 text-sm font-medium rounded-full ${getRiskColor(analysis.risk_assessment.level)}`}>
                        {analysis.risk_assessment.level}
                      </span>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Risk Factors:</h4>
                      <ul className="space-y-1">
                        {analysis.risk_assessment.factors.map((factor, index) => (
                          <li key={index} className="flex items-start gap-2 text-sm text-gray-600">
                            <span className="w-1.5 h-1.5 bg-red-400 rounded-full mt-2 flex-shrink-0"></span>
                            {factor}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Recommendations:</h4>
                      <ul className="space-y-1">
                        {analysis.risk_assessment.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start gap-2 text-sm text-gray-600">
                            <Lightbulb className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {/* Progress Prediction */}
              {analysisType === 'progress' && analysis.progress_prediction && (
                <div className="card">
                  <div className="flex items-center gap-3 mb-4">
                    <TrendingUp className="h-6 w-6 text-blue-500" />
                    <h3 className="text-lg font-semibold text-gray-900">Progress Prediction</h3>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">
                          {(analysis.progress_prediction.completion_probability * 100).toFixed(0)}%
                        </div>
                        <div className="text-sm text-gray-600">Completion Probability</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-lg font-bold text-green-600">
                          {new Date(analysis.progress_prediction.estimated_completion_date).toLocaleDateString()}
                        </div>
                        <div className="text-sm text-gray-600">Estimated Completion</div>
                      </div>
                    </div>

                    {analysis.progress_prediction.potential_delays.length > 0 && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Potential Delays:</h4>
                        <ul className="space-y-1">
                          {analysis.progress_prediction.potential_delays.map((delay, index) => (
                            <li key={index} className="flex items-start gap-2 text-sm text-gray-600">
                              <Clock className="h-4 w-4 text-orange-500 mt-0.5 flex-shrink-0" />
                              {delay}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Team Performance */}
              {analysisType === 'team' && analysis.team_performance && (
                <div className="card">
                  <div className="flex items-center gap-3 mb-4">
                    <Users className="h-6 w-6 text-green-500" />
                    <h3 className="text-lg font-semibold text-gray-900">Team Performance</h3>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">
                        {(analysis.team_performance.productivity_score * 100).toFixed(0)}%
                      </div>
                      <div className="text-sm text-gray-600">Productivity Score</div>
                    </div>

                    {analysis.team_performance.bottlenecks.length > 0 && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Bottlenecks:</h4>
                        <ul className="space-y-1">
                          {analysis.team_performance.bottlenecks.map((bottleneck, index) => (
                            <li key={index} className="flex items-start gap-2 text-sm text-gray-600">
                              <AlertTriangle className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                              {bottleneck}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Suggestions:</h4>
                      <ul className="space-y-1">
                        {analysis.team_performance.suggestions.map((suggestion, index) => (
                          <li key={index} className="flex items-start gap-2 text-sm text-gray-600">
                            <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                            {suggestion}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="card">
              <div className="text-center py-12">
                <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Analysis Available</h3>
                <p className="text-gray-600">Select a project to view AI-powered insights and analysis.</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Recent Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent AI Insights</h3>
        
        {insightsLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-3/4"></div>
              </div>
            ))}
          </div>
        ) : insights && insights.length > 0 ? (
          <div className="space-y-4">
            {insights.slice(0, 10).map((insight) => (
              <div key={insight.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-3">
                    {getInsightIcon(insight.insight_type)}
                    <div>
                      <h4 className="font-medium text-gray-900">{insight.project_name}</h4>
                      <p className="text-sm text-gray-600 capitalize">{insight.insight_type} Insight</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getConfidenceColor(insight.confidence_score)}`}>
                      {(insight.confidence_score * 100).toFixed(0)}% confidence
                    </span>
                    <span className="text-xs text-gray-500">
                      {new Date(insight.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <p className="text-gray-700 text-sm">{insight.content}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Brain className="h-8 w-8 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600">No AI insights available yet. Generate some insights to get started!</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default AIInsightsPage