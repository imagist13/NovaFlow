'use client'

import { useState } from 'react'

const platformInfo = {
  xiaohongshu: { name: '小红书', icon: '📕', color: 'text-red-600', bg: 'bg-red-50' },
  douyin: { name: '抖音', icon: '🎵', color: 'text-pink-600', bg: 'bg-pink-50' },
  zhihu: { name: '知乎', icon: '💬', color: 'text-blue-600', bg: 'bg-blue-50' },
  taobao: { name: '淘宝', icon: '🛒', color: 'text-orange-600', bg: 'bg-orange-50' },
}

interface ContentDisplayProps {
  platform: string
  content: any
}

export default function ContentDisplay({ platform, content }: ContentDisplayProps) {
  const [copied, setCopied] = useState(false)
  const info = platformInfo[platform as keyof typeof platformInfo] || { name: platform, icon: '📄', color: 'text-gray-600', bg: 'bg-gray-50' }

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('复制失败:', err)
    }
  }

  const handleCopyAll = () => {
    const text = `
${content.title ? `标题: ${content.title}\n\n` : ''}${content.content}\n${content.hashtags?.length ? `\n标签: ${content.hashtags.map((tag: string) => '#' + tag).join(' ')}` : ''}
    `.trim()
    handleCopy(text)
  }

  return (
    <div className="card hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className={`w-10 h-10 ${info.bg} rounded-lg flex items-center justify-center`}>
            <span className="text-xl">{info.icon}</span>
          </div>
          <div>
            <h3 className={`font-semibold ${info.color}`}>{info.name}</h3>
            <p className="text-xs text-gray-500">已适配</p>
          </div>
        </div>
        
        <button
          onClick={handleCopyAll}
          className="btn-secondary text-sm flex items-center gap-1.5"
        >
          {copied ? (
            <>
              <svg className="w-4 h-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              已复制
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              复制
            </>
          )}
        </button>
      </div>

      {/* Content */}
      <div className="space-y-4">
        {/* Title */}
        {content.title && (
          <div>
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1.5">
              标题
            </div>
            <div className="text-lg font-semibold text-gray-900 leading-tight">
              {content.title}
            </div>
          </div>
        )}

        {/* Content */}
        <div>
          <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1.5">
            正文
          </div>
          <div className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {content.content}
          </div>
        </div>

        {/* Hashtags */}
        {content.hashtags && content.hashtags.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
              标签
            </div>
            <div className="flex flex-wrap gap-2">
              {content.hashtags.map((tag: string, index: number) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-sm font-medium"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
