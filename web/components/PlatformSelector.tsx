'use client'

import { useState } from 'react'

const platforms = [
  {
    id: 'xiaohongshu',
    name: '小红书',
    icon: '📕',
    description: '种草分享，图文笔记',
    color: 'bg-red-500',
    bgHover: 'hover:bg-red-50',
    borderHover: 'hover:border-red-300',
  },
  {
    id: 'douyin',
    name: '抖音',
    icon: '🎵',
    description: '短视频口播文案',
    color: 'bg-pink-500',
    bgHover: 'hover:bg-pink-50',
    borderHover: 'hover:border-pink-300',
  },
  {
    id: 'zhihu',
    name: '知乎',
    icon: '💬',
    description: '深度内容，专业问答',
    color: 'bg-blue-500',
    bgHover: 'hover:bg-blue-50',
    borderHover: 'hover:border-blue-300',
  },
  {
    id: 'taobao',
    name: '淘宝',
    icon: '🛒',
    description: '商品详情，营销文案',
    color: 'bg-orange-500',
    bgHover: 'hover:bg-orange-50',
    borderHover: 'hover:border-orange-300',
  },
]

interface PlatformSelectorProps {
  selected: string[]
  onChange: (selected: string[]) => void
  disabled?: boolean
}

export default function PlatformSelector({ selected, onChange, disabled }: PlatformSelectorProps) {
  const [isHovered, setIsHovered] = useState<string | null>(null)

  const togglePlatform = (id: string) => {
    if (disabled) return
    
    if (selected.includes(id)) {
      onChange(selected.filter(s => s !== id))
    } else {
      onChange([...selected, id])
    }
  }

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h2 className="text-lg font-semibold text-gray-900">目标平台</h2>
        <span className="ml-auto text-sm text-gray-500">
          已选择 {selected.length} 个
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {platforms.map((platform) => {
          const isSelected = selected.includes(platform.id)
          const isCurrentlyHovered = isHovered === platform.id

          return (
            <button
              key={platform.id}
              onClick={() => togglePlatform(platform.id)}
              onMouseEnter={() => setIsHovered(platform.id)}
              onMouseLeave={() => setIsHovered(null)}
              disabled={disabled}
              className={`
                relative p-4 rounded-xl border-2 transition-all duration-200 text-left
                ${isSelected
                  ? `${platform.bgHover} ${platform.borderHover} border-current`
                  : 'bg-white border-gray-200 hover:border-gray-300'
                }
                ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
                ${isCurrentlyHovered && !isSelected ? 'shadow-md' : 'shadow-sm'}
              `}
              style={{
                borderColor: isSelected ? undefined : undefined,
              }}
            >
              {isSelected && (
                <div className={`absolute top-2 right-2 w-5 h-5 ${platform.color} rounded-full flex items-center justify-center`}>
                  <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              )}
              
              <div className="flex items-center gap-3">
                <span className="text-2xl">{platform.icon}</span>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{platform.name}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{platform.description}</div>
                </div>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
