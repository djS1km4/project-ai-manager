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
  Sparkles,
  Zap,
  Shield,
  Activity,
  Cpu,
  Eye,
  Star
} from 'lucide-react'
import { apiClient } from '../services/apiClient'
import toast from 'react-hot-toast'

interface AIInsight {
  id: number
  project_id: number
  project_name: string
  insight_type: string
  title: string
  description: string
  recommendations?: string
  confidence_score: number
  created_at: string
  priority?: string
  data_source?: string
}



const AIInsightsPage = () => {
  const [selectedProject, setSelectedProject] = useState<number | null>(null)
  const [analysisType, setAnalysisType] = useState<'risk' | 'progress' | 'team'>('risk')

  const { data: insights, isLoading: insightsLoading, refetch: refetchInsights } = useQuery({
    queryKey: ['ai-insights'],
    queryFn: async () => {
      const response = await apiClient.get('/ai-insights/dashboard/insights')
      return response.data.insights as AIInsight[]
    },
  })

  const { data: projects } = useQuery({
    queryKey: ['projects-list'],
    queryFn: async () => {
      const response = await apiClient.get('/projects')
      return response.data
    },
  })

  const { data: projectInsights, isLoading: analysisLoading } = useQuery({
    queryKey: ['project-insights', selectedProject],
    queryFn: async () => {
      if (!selectedProject) return null
      const response = await apiClient.get(`/ai-insights/project/${selectedProject}/insights`)
      return response.data as AIInsight[]
    },
    enabled: !!selectedProject,
  })

  const generateInsightMutation = useMutation({
    mutationFn: async (projectId: number) => {
      // Use specific endpoint based on analysis type
      let endpoint = ''
      let analysisTypeText = ''
      
      switch (analysisType) {
        case 'risk':
          endpoint = `/ai-insights/project/${projectId}/analyze/risk`
          analysisTypeText = 'Evaluación de Riesgos'
          break
        case 'progress':
          endpoint = `/ai-insights/project/${projectId}/analyze/progress`
          analysisTypeText = 'Predicción de Progreso'
          break
        case 'team':
          endpoint = `/ai-insights/project/${projectId}/analyze/team`
          analysisTypeText = 'Rendimiento del Equipo'
          break
        default:
          endpoint = `/ai-insights/analyze-project/${projectId}?analysis_type=all`
          analysisTypeText = 'Análisis Completo'
      }
      
      const response = await apiClient.post(endpoint)
      return { ...response.data, analysisTypeText }
    },
    onSuccess: (data) => {
      refetchInsights()
      toast.success(`${data.analysisTypeText} generado exitosamente!`)
    },
    onError: (error: any) => {
      console.error('AI Insights error:', error)
      toast.error(error.response?.data?.detail || 'Error al generar el análisis')
    },
  })

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'risk': return <AlertTriangle className="h-5 w-5 text-red-600" />
      case 'progress': return <TrendingUp className="h-5 w-5 text-blue-600" />
      case 'team': return <Users className="h-5 w-5 text-green-600" />
      case 'budget_forecast': return <BarChart3 className="h-5 w-5 text-purple-600" />
      case 'resource_optimization': return <Target className="h-5 w-5 text-orange-600" />
      default: return <Brain className="h-5 w-5 text-primary-600" />
    }
  }

  const getInsightColors = (type: string) => {
    switch (type) {
      case 'risk': 
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          text: 'text-red-700',
          iconBg: 'bg-red-100',
          iconBorder: 'border-red-200',
          gradient: 'from-red-500 to-red-600'
        }
      case 'progress': 
        return {
          bg: 'bg-blue-50',
          border: 'border-blue-200',
          text: 'text-blue-700',
          iconBg: 'bg-blue-100',
          iconBorder: 'border-blue-200',
          gradient: 'from-blue-500 to-blue-600'
        }
      case 'team': 
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          text: 'text-green-700',
          iconBg: 'bg-green-100',
          iconBorder: 'border-green-200',
          gradient: 'from-green-500 to-green-600'
        }
      case 'budget_forecast': 
        return {
          bg: 'bg-purple-50',
          border: 'border-purple-200',
          text: 'text-purple-700',
          iconBg: 'bg-purple-100',
          iconBorder: 'border-purple-200',
          gradient: 'from-purple-500 to-purple-600'
        }
      case 'resource_optimization': 
        return {
          bg: 'bg-orange-50',
          border: 'border-orange-200',
          text: 'text-orange-700',
          iconBg: 'bg-orange-100',
          iconBorder: 'border-orange-200',
          gradient: 'from-orange-500 to-orange-600'
        }
      default: 
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-200',
          text: 'text-gray-700',
          iconBg: 'bg-gray-100',
          iconBorder: 'border-gray-200',
          gradient: 'from-gray-500 to-gray-600'
        }
    }
  }

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-emerald-700 bg-emerald-100 border-emerald-200'
    if (score >= 0.6) return 'text-amber-700 bg-amber-100 border-amber-200'
    return 'text-red-700 bg-red-100 border-red-200'
  }





  const getAnalysisTypeText = (type: string) => {
    switch (type) {
      case 'risk': return 'Evaluación de Riesgos'
      case 'progress': return 'Predicción de Progreso'
      case 'team': return 'Rendimiento del Equipo'
      default: return 'Análisis General'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="p-4 bg-gradient-to-br from-purple-100 to-blue-100 border border-purple-200 rounded-2xl shadow-lg">
                <Brain className="h-8 w-8 text-purple-600" />
              </div>
              <Sparkles className="h-6 w-6 text-yellow-500 animate-pulse" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent font-nunito">🧠 IA Insights</h1>
              <p className="text-gray-600 font-open-sans">✨ Análisis inteligente y predicciones para tus proyectos</p>
            </div>
          </div>
          <button
            onClick={() => refetchInsights()}
            disabled={insightsLoading}
            className="bg-primary-500 hover:bg-primary-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-200 flex items-center gap-3 shadow-soft hover:shadow-lg disabled:cursor-not-allowed"
          >
            <RefreshCw className={`h-5 w-5 ${insightsLoading ? 'animate-spin' : ''}`} />
            Actualizar Insights
          </button>
        </div>

        {/* Project Analysis Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Project Selection */}
        <div className="bg-white rounded-xl shadow-soft border border-gray-200 p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2 font-nunito">
            <Cpu className="h-6 w-6 text-info-600" />
            Análisis de Proyecto
          </h3>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3 font-open-sans">
                Seleccionar Proyecto
              </label>
              <select
                value={selectedProject || ''}
                onChange={(e) => setSelectedProject(e.target.value ? Number(e.target.value) : null)}
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 shadow-soft"
              >
                <option value="">Elegir un proyecto</option>
                {projects?.map((project: any) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3 font-open-sans">
                Tipo de Análisis
              </label>
              <div className="space-y-3">
                {[
                  { value: 'risk', label: '🔴 Evaluación de Riesgos', icon: Shield, bgColor: 'bg-red-100', textColor: 'text-red-700', borderColor: 'border-red-300' },
                  { value: 'progress', label: '🔵 Predicción de Progreso', icon: Activity, bgColor: 'bg-blue-100', textColor: 'text-blue-700', borderColor: 'border-blue-300' },
                  { value: 'team', label: '🟢 Rendimiento del Equipo', icon: Users, bgColor: 'bg-green-100', textColor: 'text-green-700', borderColor: 'border-green-300' },
                ].map(({ value, label, icon: Icon, bgColor, textColor, borderColor }) => (
                  <button
                    key={value}
                    onClick={() => setAnalysisType(value as any)}
                    className={`w-full flex items-center gap-3 p-4 rounded-lg border transition-all duration-200 ${
                      analysisType === value
                        ? `${bgColor} ${textColor} ${borderColor} shadow-soft`
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50 text-gray-700'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span className="text-sm font-medium font-open-sans">{label}</span>
                    {analysisType === value && <Star className="h-4 w-4 ml-auto text-warning-500" />}
                  </button>
                ))}
              </div>
            </div>

            {selectedProject && (
              <button
                onClick={() => generateInsightMutation.mutate(selectedProject)}
                disabled={generateInsightMutation.isPending}
                className="w-full px-6 py-4 bg-primary-500 hover:bg-primary-600 disabled:bg-gray-400 text-white rounded-lg disabled:cursor-not-allowed transition-all duration-200 shadow-soft hover:shadow-lg flex items-center gap-2 justify-center"
              >
                {generateInsightMutation.isPending ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                    Generando...
                  </>
                ) : (
                  <>
                    <Zap className="h-5 w-5" />
                    {analysisType === 'risk' && 'Evaluar Riesgos'}
                    {analysisType === 'progress' && 'Predecir Progreso'}
                    {analysisType === 'team' && 'Analizar Equipo'}
                    {!analysisType && 'Generar Insight'}
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Analysis Results */}
        <div className="lg:col-span-2">
          {analysisLoading ? (
            <div className="bg-white rounded-xl shadow-soft border border-gray-200 p-8">
              <div className="flex flex-col items-center justify-center h-64 space-y-4">
                <div className="relative">
                  <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-200 border-t-primary-500"></div>
                  <Brain className="absolute inset-0 m-auto h-6 w-6 text-primary-600" />
                </div>
                <div className="text-center">
                  <p className="text-gray-800 font-medium font-nunito">Analizando proyecto...</p>
                  <p className="text-gray-600 text-sm mt-1 font-open-sans">La IA está procesando los datos</p>
                </div>
              </div>
            </div>
          ) : projectInsights && projectInsights.length > 0 ? (
            <div className="space-y-6">
              {/* Show project insights */}
              <div className="bg-white rounded-xl shadow-soft border border-gray-200 p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-3 bg-gradient-to-br from-blue-100 to-purple-100 border border-blue-200 rounded-xl shadow-lg">
                    <Brain className="h-6 w-6 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent font-nunito">🎯 Insights del Proyecto</h3>
                  <Sparkles className="h-5 w-5 text-yellow-500 animate-bounce" />
                </div>
                
                <div className="space-y-4">
                  {projectInsights.slice(0, 5).map((insight) => {
                    const colors = getInsightColors(insight.insight_type)
                    return (
                      <div key={insight.id} className={`${colors.bg} border ${colors.border} rounded-xl p-6 transition-all duration-300 hover:shadow-lg`}>
                        <div className="flex items-start justify-between mb-6">
                          <div className="flex items-center gap-5">
                            <div className={`p-3 ${colors.iconBg} border ${colors.iconBorder} rounded-xl shadow-sm flex-shrink-0`}>
                              {getInsightIcon(insight.insight_type)}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-4 mb-2">
                                 <h4 className={`font-bold ${colors.text} font-nunito text-lg leading-tight`}>{insight.title}</h4>
                                 <span 
                                   className="px-4 py-2 bg-white/80 backdrop-blur-sm border border-gray-300 rounded-full text-xs font-bold text-gray-700 shadow-sm hover:bg-white hover:shadow-md transition-all duration-200 cursor-pointer flex items-center gap-2 h-8"
                                   onClick={() => toast.success(`Proyecto: ${insight.project_name}`, { duration: 3000, icon: '📁' })}
                                   title={`Proyecto: ${insight.project_name}`}
                                 >
                                   📁 <span className="truncate max-w-[120px]">{insight.project_name}</span>
                                 </span>
                               </div>
                              <p className={`text-sm ${colors.text} opacity-80 capitalize font-open-sans flex items-center gap-2`}>
                                {getAnalysisTypeText(insight.insight_type)}
                                <Sparkles className="h-3 w-3" />
                              </p>
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-3 flex-shrink-0">
                            <span className={`px-4 py-2 text-xs font-bold rounded-full border ${getConfidenceColor(insight.confidence_score)} shadow-sm h-8 flex items-center justify-center min-w-[100px]`}>
                              {Math.round(insight.confidence_score * 100)}% confianza
                            </span>
                            <span className="text-xs text-gray-500 flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {new Date(insight.created_at).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                        
                        <div className="mb-4">
                          <p className={`${colors.text} font-open-sans leading-relaxed text-base`}>{insight.description}</p>
                        </div>
                        
                        {insight.recommendations && (
                          <div className="bg-white/70 backdrop-blur-sm border border-white/50 rounded-lg p-4 shadow-sm">
                            <h5 className={`font-semibold ${colors.text} mb-3 flex items-center gap-2 font-nunito`}>
                              <Lightbulb className={`h-4 w-4 ${colors.text}`} />
                              Recomendaciones:
                            </h5>
                            <p className={`text-sm ${colors.text} opacity-90 font-open-sans leading-relaxed`}>{insight.recommendations}</p>
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
              
              {/* Analysis sections now removed since we're using the new insight structure */}
            </div>
          ) : selectedProject ? (
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
              <div className="text-center py-16">
                <div className="relative mb-6">
                  <Brain className="h-16 w-16 text-primary-600 mx-auto" />
                  <Sparkles className="h-6 w-6 text-warning-600 absolute -top-2 -right-2" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-3 font-nunito">No hay insights disponibles</h3>
                <p className="text-gray-600 max-w-md mx-auto font-open-sans">
                  Este proyecto aún no tiene insights generados. Usa el botón "Generar Insight" para crear análisis con IA.
                </p>
                <div className="mt-6">
                  <Zap className="h-8 w-8 text-primary-600 mx-auto" />
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
              <div className="text-center py-16">
                <div className="relative mb-6">
                  <Brain className="h-16 w-16 text-primary-600 mx-auto" />
                  <Sparkles className="h-6 w-6 text-warning-600 absolute -top-2 -right-2" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-3 font-nunito">Selecciona un Proyecto</h3>
                <p className="text-gray-600 max-w-md mx-auto font-open-sans">Elige un proyecto para ver insights y análisis impulsados por IA.</p>
                <div className="mt-6">
                  <Eye className="h-8 w-8 text-primary-600 mx-auto" />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Recent Insights */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-gradient-to-br from-green-100 to-emerald-100 border border-green-200 rounded-xl shadow-lg">
            <Brain className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="text-xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent font-nunito">📊 Insights Recientes de IA</h3>
          <Sparkles className="h-5 w-5 text-yellow-500 animate-spin" />
        </div>
        
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
            {insights.slice(0, 10).map((insight) => {
              const colors = getInsightColors(insight.insight_type)
              return (
                <div key={insight.id} className={`${colors.bg} border ${colors.border} rounded-xl p-6 transition-all duration-300 hover:shadow-lg hover:scale-[1.02]`}>
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <div className={`p-3 ${colors.iconBg} border ${colors.iconBorder} rounded-xl shadow-sm`}>
                        {getInsightIcon(insight.insight_type)}
                      </div>
                      <div>
                        <div className="flex items-center gap-3 mb-1">
                           <h4 className={`font-bold ${colors.text} font-nunito text-lg`}>{insight.title}</h4>
                           <span 
                             className="px-3 py-1 bg-white/80 backdrop-blur-sm border border-gray-300 rounded-full text-xs font-bold text-gray-700 shadow-sm hover:bg-white hover:shadow-md transition-all duration-200 cursor-pointer h-8 flex items-center"
                             onClick={() => toast.success(`Proyecto: ${insight.project_name}`, { duration: 3000, icon: '📁' })}
                             title={`Proyecto: ${insight.project_name}`}
                           >
                             📁 {insight.project_name}
                           </span>
                         </div>
                        <p className={`text-sm ${colors.text} opacity-80 capitalize flex items-center gap-2 font-open-sans`}>
                          {getAnalysisTypeText(insight.insight_type)}
                          <Zap className={`h-3 w-3 ${colors.text}`} />
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <span className={`px-4 py-2 text-xs font-bold rounded-full border ${getConfidenceColor(insight.confidence_score)} shadow-sm`}>
                        {(insight.confidence_score * 100).toFixed(0)}% confianza
                      </span>
                      <span className="text-xs text-gray-500 flex items-center gap-1 font-open-sans">
                        <Clock className="h-3 w-3" />
                        {new Date(insight.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <p className={`${colors.text} text-sm leading-relaxed font-open-sans opacity-90`}>{insight.description}</p>
                    {insight.recommendations && (
                      <div className="bg-white/50 backdrop-blur-sm border border-white/30 rounded-lg p-3">
                        <p className={`text-xs ${colors.text} opacity-80 font-open-sans flex items-center gap-2`}>
                          <Lightbulb className="h-3 w-3" />
                          <span className="font-medium">Recomendación:</span> {insight.recommendations}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="relative mb-6">
              <Brain className="h-12 w-12 text-primary-600 mx-auto" />
              <Sparkles className="h-4 w-4 text-warning-600 absolute -top-1 -right-1" />
            </div>
            <p className="text-gray-600 font-open-sans">No hay insights de IA disponibles aún. ¡Genera algunos insights para comenzar!</p>
          </div>
        )}
      </div>
    </div>
  </div>
  )
}

export default AIInsightsPage