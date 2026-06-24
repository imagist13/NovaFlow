import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { content, platforms } = await request.json()

    if (!content || !platforms || platforms.length === 0) {
      return NextResponse.json(
        { error: '缺少必要参数' },
        { status: 400 }
      )
    }

    // TODO: 调用后端 Python API
    // 暂时返回模拟数据，实际使用时替换为真实 API 调用
    const results: Record<string, any> = {}

    for (const platform of platforms) {
      // 模拟生成内容
      results[platform] = generateMockContent(platform, content)
    }

    return NextResponse.json({
      success: true,
      results,
    })
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    )
  }
}

function generateMockContent(platform: string, sourceContent: string) {
  const platformConfigs: Record<string, { titleLen: number; contentLen: string }> = {
    xiaohongshu: { titleLen: 15, contentLen: '适中' },
    douyin: { titleLen: 20, contentLen: '简短' },
    zhihu: { titleLen: 30, contentLen: '详细' },
    taobao: { titleLen: 25, contentLen: '营销' },
  }

  const config = platformConfigs[platform] || { titleLen: 20, contentLen: '适中' }

  const titles: Record<string, string[]> = {
    xiaohongshu: ['必看！私藏好物分享 🌟', '亲测有效！强烈推荐', '绝绝子！这个真的太好用了'],
    douyin: ['这个一定要看到最后！', '分享一个超棒的体验', '必须曝光！真的太厉害了'],
    zhihu: ['深度解析：为什么这个值得关注', '专业测评：实际体验分享', '全面解读：功能与使用心得'],
    taobao: ['爆款推荐！性价比超高', '热销商品真实测评', '必买清单！入手不后悔'],
  }

  const platforms = ['xiaohongshu', 'douyin', 'zhihu', 'taobao']
  const titleOptions = titles[platform] || titles.xiaohongshu
  const randomTitle = titleOptions[Math.floor(Math.random() * titleOptions.length)]

  const hashtags: Record<string, string[]> = {
    xiaohongshu: ['种草', '好物分享', '私藏', '推荐', '测评'],
    douyin: ['必看', '好物', '分享', '推荐', '种草'],
    zhihu: ['测评', '体验', '分析', '专业', '分享'],
    taobao: ['好物', '推荐', '爆款', '性价比', '测评'],
  }

  const platformHashtags = hashtags[platform] || hashtags.xiaohongshu
  const selectedHashtags = platformHashtags.slice(0, 3 + Math.floor(Math.random() * 3))

  return {
    title: randomTitle,
    content: `${sourceContent}\n\n这是一段为${platform}平台优化的内容。内容经过专业调整，符合平台调性和用户喜好。包含${config.contentLen}的描述和精准的标签设置，有助于提升内容曝光和互动。`,
    hashtags: selectedHashtags,
  }
}
