import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'NovaFlow - 多平台内容适配工具',
  description: '基于 AI 的多平台内容适配工具，一键将内容适配到小红书、抖音、知乎、淘宝等多个平台',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
