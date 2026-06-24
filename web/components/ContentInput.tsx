'use client'

import { useState } from 'react'

interface ContentInputProps {
  value: string
  onChange: (value: string) => void
  disabled?: boolean
}

export default function ContentInput({ value, onChange, disabled }: ContentInputProps) {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
        </div>
        <h2 className="text-lg font-semibold text-gray-900">原始内容</h2>
      </div>
      
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        disabled={disabled}
        placeholder="在这里输入你想要适配的内容..."
        className={`w-full h-64 px-4 py-3 rounded-lg border transition-all duration-200 resize-none outline-none ${
          isFocused
            ? 'border-primary-500 ring-2 ring-primary-200'
            : 'border-gray-300'
        } ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
      />
      
      <div className="mt-2 text-right text-sm text-gray-500">
        {value.length} 字
      </div>
    </div>
  )
}
