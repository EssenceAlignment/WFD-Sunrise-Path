import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { CheckCircle, Target, Zap, TrendingUp, Database, BarChart3, FileText, Rocket } from 'lucide-react'
import './App.css'

function App() {
  const [activeSection, setActiveSection] = useState('overview')

  const integrationAreas = [
    {
      id: 'pattern-registry',
      title: 'Pattern Registry 2.0 Operationalization',
      description: 'Accelerate transition from shadow mode to full deployment',
      impact: '6x pattern coverage, 4x available cascades',
      icon: <Database className="h-6 w-6" />,
      progress: 75,
      tasks: [
        'Automated monitoring & analysis of shadow mode performance',
        'Test suite implementation & execution',
        'Pattern refinement & tuning based on metrics',
        'Documentation & reporting for go/no-go decision'
      ]
    },
    {
      id: 'funding-dashboard',
      title: 'RC Funding Dashboard Enhancement',
      description: 'Optimize real-time funding intelligence and Airtable integration',
      impact: 'Automated data validation, proactive pattern application',
      icon: <BarChart3 className="h-6 w-6" />,
      progress: 85,
      tasks: [
        'Automated data validation & cleaning in Airtable',
        'Proactive AI pattern application for new opportunities',
        'Dashboard KPI monitoring and performance tracking',
        'Smart alerting system for critical deadlines'
      ]
    },
    {
      id: 'dashboard-rollout',
      title: 'RC-Dashboard Rollout Automation',
      description: 'Streamline deployment to 15 WFD managers',
      impact: 'Automated deployment, personalized onboarding',
      icon: <Rocket className="h-6 w-6" />,
      progress: 60,
      tasks: [
        'Automated launcher deployment script creation',
        'Personalized onboarding materials for managers',
        'Automated report generation for WFD managers',
        'Predictive flagging for 90-day shelter limits'
      ]
    },
    {
      id: 'publication-strategy',
      title: 'Publication & Communication Acceleration',
      description: 'Expedite case study drafting and content creation',
      impact: 'Accelerated content generation, enhanced narrative development',
      icon: <FileText className="h-6 w-6" />,
      progress: 40,
      tasks: [
        'Automated content generation for case studies',
        'Story Mode narrative development for funders',
        'Citation & reference management automation',
        'Presentation & keynote development assistance'
      ]
    }
  ]

  const forceMultipliers = [
    { metric: 'Pattern Coverage', before: '6 patterns', after: '36 patterns', improvement: '6x' },
    { metric: 'Available Cascades', before: '6', after: '23+', improvement: '4x' },
    { metric: 'Blind Spot Coverage', before: '25%', after: '75%', improvement: '3x' },
    { metric: 'MCP Integration Time', before: '5-7 days', after: '0-1 day', improvement: '7x faster' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-2 rounded-lg">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Manus Strategic Integration</h1>
                <p className="text-sm text-gray-600 dark:text-gray-300">Recovery Compass Force Multiplication Plan</p>
              </div>
            </div>
            <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
              <CheckCircle className="h-4 w-4 mr-1" />
              Ready for Implementation
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Executive Summary */}
        <section className="mb-12">
          <Card className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="h-6 w-6 text-blue-600" />
                <span>Executive Summary</span>
              </CardTitle>
              <CardDescription>
                Strategic approach for immediate and seamless Manus integration into Recovery Compass
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-6">
                This plan outlines a strategic approach for Manus to immediately and seamlessly integrate into the Recovery Compass project, 
                focusing on force multiplication and aligning with its core directives. By leveraging Manus's capabilities in automation, 
                data analysis, and intelligent orchestration, we can significantly accelerate key milestones, enhance operational efficiency, 
                and amplify the project's impact.
              </p>
              
              {/* Force Multiplication Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
                {forceMultipliers.map((metric, index) => (
                  <Card key={index} className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20">
                    <CardContent className="p-4">
                      <div className="text-sm font-medium text-gray-600 dark:text-gray-400">{metric.metric}</div>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-xs text-gray-500">{metric.before}</span>
                        <TrendingUp className="h-4 w-4 text-green-600" />
                        <span className="text-xs text-gray-500">{metric.after}</span>
                      </div>
                      <div className="text-lg font-bold text-green-600 mt-1">{metric.improvement}</div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Integration Areas */}
        <section>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
            Strategic Integration Areas
          </h2>
          
          <Tabs value={activeSection} onValueChange={setActiveSection} className="w-full">
            <TabsList className="grid w-full grid-cols-4 mb-8">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="pattern-registry">Pattern Registry</TabsTrigger>
              <TabsTrigger value="funding-dashboard">Funding Dashboard</TabsTrigger>
              <TabsTrigger value="dashboard-rollout">Dashboard Rollout</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {integrationAreas.map((area) => (
                  <Card key={area.id} className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-3">
                        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-2 rounded-lg text-white">
                          {area.icon}
                        </div>
                        <span>{area.title}</span>
                      </CardTitle>
                      <CardDescription>{area.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div>
                          <div className="flex justify-between text-sm mb-2">
                            <span>Implementation Progress</span>
                            <span>{area.progress}%</span>
                          </div>
                          <Progress value={area.progress} className="h-2" />
                        </div>
                        <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
                          <p className="text-sm font-medium text-blue-800 dark:text-blue-200">
                            Impact: {area.impact}
                          </p>
                        </div>
                        <Button 
                          onClick={() => setActiveSection(area.id)}
                          className="w-full"
                          variant="outline"
                        >
                          View Details
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {integrationAreas.map((area) => (
              <TabsContent key={area.id} value={area.id} className="space-y-6">
                <Card className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-3">
                      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-2 rounded-lg text-white">
                        {area.icon}
                      </div>
                      <span>{area.title}</span>
                    </CardTitle>
                    <CardDescription>{area.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-6">
                      <div>
                        <div className="flex justify-between text-sm mb-2">
                          <span>Implementation Progress</span>
                          <span>{area.progress}%</span>
                        </div>
                        <Progress value={area.progress} className="h-3" />
                      </div>
                      
                      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-4 rounded-lg">
                        <h4 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">Expected Impact</h4>
                        <p className="text-blue-700 dark:text-blue-300">{area.impact}</p>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Key Implementation Tasks</h4>
                        <div className="space-y-2">
                          {area.tasks.map((task, index) => (
                            <div key={index} className="flex items-start space-x-3">
                              <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                              <span className="text-gray-700 dark:text-gray-300">{task}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            ))}
          </Tabs>
        </section>

        {/* Call to Action */}
        <section className="mt-12">
          <Card className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
            <CardContent className="p-8 text-center">
              <h3 className="text-2xl font-bold mb-4">Ready to Implement</h3>
              <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
                This strategic integration plan aligns perfectly with Recovery Compass's core principles: 
                Environmental Response Design™, Soft Power Philosophy, and Strategic Framework Integration.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button variant="secondary" size="lg" className="bg-white text-blue-600 hover:bg-blue-50">
                  <Target className="h-5 w-5 mr-2" />
                  Begin Implementation
                </Button>
                <Button variant="outline" size="lg" className="border-white text-white hover:bg-white/10">
                  <FileText className="h-5 w-5 mr-2" />
                  Download Full Plan
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-t border-gray-200 dark:border-gray-700 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Strategic Integration Plan by <span className="font-semibold">Manus AI</span> for Recovery Compass
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
              Focused on force multiplication and seamless integration
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

