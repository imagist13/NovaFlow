'use client'

import { useState } from 'react'
import ContentInput from '@/components/ContentInput'
import PlatformSelector from '@/components/PlatformSelector'
import ContentDisplay from '@/components/ContentDisplay'

export default function Home() {
  const [content, setContent] = useState('')
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [results, setResults] = useState<Record<string, any>>({})

  const handleGenerate = async () => {
    if (!content.trim() || selectedPlatforms.length === 0) {
      return
    }

    setIsGenerating(true)
    setResults({})

    try {
      const response = await fetch('/api/adapt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          platforms: selectedPlatforms,
        }),
      })

      if (!response.ok) {
        throw new Error('生成失败')
      }

      const data = await response.json()
      setResults(data.results || {})
    } catch (error) {
      console.error('生成失败:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-12 max-w-7xl">
      {/* Header */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          <span className="bg-gradient-to-r from-primary-600 to-primary-500 bg-clip-text text-transparent">
            NovaFlow
          </span>
        </h1>
        <p className="text-xl text-gray-600 mb-2">
          多平台内容适配工具
        </p>
        <p className="text-gray-500">
          一键将内容智能适配到小红书、抖音、知乎、淘宝等多个平台
        </p>
      </div>

      {/* Main Content */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Left Column - Input */}
        <div className="space-y-6">
          <ContentInput
            value={content}
            onChange={setContent}
            disabled={isGenerating}
          />
          
          <PlatformSelector
            selected={selectedPlatforms}
            onChange={setSelectedPlatforms}
            disabled={isGenerating}
          />

          <button
            onClick={handleGenerate}
            disabled={!content.trim() || selectedPlatforms.length === 0 || isGenerating}
            className="w-full btn-primary text-lg py-4 rounded-xl shadow-lg hover:shadow-xl transition-shadow disabled:shadow-none"
          >
            {isGenerating ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                正在生成...
              </span>
            ) : (
              '开始适配'
            )}
          </button>
        </div>

        {/* Right Column - Results */}
        <div className="space-y-6">
          {Object.keys(results).length === 0 ? (
            <div className="card h-96 flex items-center justify-center text-gray-400">
              <div className="text-center">
                <svg className="mx-auto h-12 w-12 mb-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <p>生成的内容将在这里显示</p>
              </div>
            </div>
          ) : (
            Object.entries(results).map(([platform, result]) => (
              <ContentDisplay
                key={platform}
                platform={platform}
                content={result}
              />
            ))
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-16 text-center text-gray-500 text-sm">
        <p>Powered by NovaFlow • 开源免费</p>
      </footer>
    </main>
  )
}
