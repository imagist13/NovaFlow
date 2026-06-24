"""NovaFlow CLI 入口."""

import asyncio
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .platforms.registry import PlatformRegistry
from .platforms.base_platform import PlatformContent

app = typer.Typer(
    name="novaflow",
    help="NovaFlow - 多平台内容适配工具",
    add_completion=False,
)

console = Console()


@app.command()
def init():
    """初始化 NovaFlow 配置."""
    console.print(Panel.fit(
        "[bold green]NovaFlow[/bold green] - 多平台内容适配工具\n\n"
        "请创建 .env 文件配置以下环境变量：\n\n"
        "OPENAI_API_KEY=your_api_key\n"
        "LLM_PROVIDER=openai\n"
        "LLM_MODEL=gpt-4\n"
        "LLM_TEMPERATURE=0.7",
        title="初始化提示",
        border_style="green"
    ))


@app.command()
def list_platforms():
    """列出所有可用平台."""
    table = Table(title="支持的平台")
    table.add_column("名称", style="cyan")
    table.add_column("显示名称", style="green")
    table.add_column("最大标题长度", style="yellow")
    table.add_column("最大内容长度", style="yellow")
    
    for name in PlatformRegistry.list_platforms():
        platform = PlatformRegistry.get(name)
        config = platform.config
        table.add_row(
            name,
            config.display_name,
            str(config.max_title_length),
            str(config.max_content_length),
        )
    
    console.print(table)


@app.command()
def platform_info(platform: str):
    """查看特定平台的详细信息."""
    try:
        p = PlatformRegistry.get(platform)
        console.print(Panel.fit(
            f"[bold]{p.config.display_name}[/bold]\n\n"
            + p.get_platform_rules(),
            title=f"平台规则 - {platform}",
            border_style="blue"
        ))
    except ValueError as e:
        console.print(f"[bold red]错误:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def adapt(
    content: str = typer.Option(..., "--content", "-c", help="要适配的内容"),
    platforms: str = typer.Option(..., "--platforms", "-p", help="目标平台，逗号分隔"),
):
    """将内容适配到指定平台."""
    platform_list = [p.strip() for p in platforms.split(",")]
    
    console.print(f"\n[bold]正在适配内容到:[/bold] {', '.join(platform_list)}\n")
    
    for platform_name in platform_list:
        try:
            platform = PlatformRegistry.get(platform_name)
            
            with console.status(f"[bold green]正在处理 {platform.config.display_name}..."):
                result = platform.transform_sync(content)
            
            console.print(Panel.fit(
                platform.format_output(result),
                title=f"✓ {platform.config.display_name}",
                border_style="green"
            ))
            console.print()
            
        except ValueError as e:
            console.print(f"[bold red]错误:[/bold red] 未知平台: {platform_name}")
        except Exception as e:
            console.print(f"[bold red]错误:[/bold red] 处理 {platform_name} 失败: {e}")


@app.command()
def interactive():
    """交互式模式 - 逐步输入内容并选择平台."""
    console.print(Panel.fit(
        "[bold green]NovaFlow 交互式模式[/bold green]\n\n"
        "按 Ctrl+C 退出",
        border_style="green"
    ))
    
    while True:
        try:
            content = console.input("\n[bold cyan]请输入原始内容:[/bold cyan]\n> ")
            
            if not content.strip():
                console.print("[yellow]内容不能为空[/yellow]")
                continue
            
            console.print("\n[bold cyan]可用平台:[/bold cyan]")
            for i, name in enumerate(PlatformRegistry.list_platforms(), 1):
                platform = PlatformRegistry.get(name)
                console.print(f"  {i}. {platform.config.display_name} ({name})")
            
            platform_input = console.input("\n[bold cyan]选择平台 (逗号分隔编号或名称):[/bold cyan] ")
            
            selected_platforms = []
            for item in platform_input.split(","):
                item = item.strip()
                if item.isdigit():
                    idx = int(item) - 1
                    platforms = PlatformRegistry.list_platforms()
                    if 0 <= idx < len(platforms):
                        selected_platforms.append(platforms[idx])
                else:
                    selected_platforms.append(item)
            
            console.print()
            for platform_name in selected_platforms:
                try:
                    platform = PlatformRegistry.get(platform_name)
                    
                    with console.status(f"[bold green]正在处理 {platform.config.display_name}..."):
                        result = platform.transform_sync(content)
                    
                    console.print(Panel.fit(
                        platform.format_output(result),
                        title=f"✓ {platform.config.display_name}",
                        border_style="green"
                    ))
                    console.print()
                    
                except ValueError as e:
                    console.print(f"[bold red]错误:[/bold red] 未知平台: {platform_name}")
                except Exception as e:
                    console.print(f"[bold red]错误:[/bold red] 处理 {platform_name} 失败: {e}")
        
        except KeyboardInterrupt:
            console.print("\n\n[bold]再见![/bold]")
            break


def main():
    """主入口."""
    app()


if __name__ == "__main__":
    main()
