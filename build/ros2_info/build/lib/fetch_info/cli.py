import click
from rich.console import Console
from fetch_info.display.panels import render_all
from fetch_info.display.themes import get_theme, list_themes
from fetch_info.collector import system, ros2, workspace
import json, time


def collect(live=False, skip_ws=False, skip_sys=False, timeout=3, updates=True):
    data = {}
    if not skip_sys:
        data["system"] = system.collect_all()
    data["ros2"] = ros2.collect_all(check_live=live, live_timeout=timeout, check_updates=updates)
    if not skip_ws:
        data["workspace"] = workspace.collect_all()
    return data


def interactive_mode(theme_name):
    """Interactive TUI — let the user pick what to view."""
    console = Console()
    theme = get_theme(theme_name)

    menu_items = [
        ("1", "Full System Overview",       "full"),
        ("2", "ROS2 Environment Only",      "ros2"),
        ("3", "System Info Only",           "system"),
        ("4", "Live Nodes/Topics/Services", "live"),
        ("5", "Workspace Info",             "workspace"),
        ("6", "Environment Variables",      "env"),
        ("7", "Export as JSON",             "json"),
        ("8", "Start Web UI",              "web"),
        ("q", "Quit",                      "quit"),
    ]

    from fetch_info.display.logo import get_main_banner
    
    while True:
        console.clear()
        console.print()
        console.print(get_main_banner(theme))
        console.print(f"  [{theme['highlight']}]Interactive Menu[/]\n")
        
        for key, label, _ in menu_items:
            style = theme["error_style"] if key == "q" else theme["value_style"]
            console.print(f"   [{theme['highlight']}]{key}[/]  [{style}]{label}[/]")
        console.print()

        choice = console.input(f"  [{theme['logo_color1']}]Select an option: [/]").strip().lower()

        action = None
        for key, _, act in menu_items:
            if choice == key:
                action = act
                break

        if action is None:
            console.print(f"  [{theme['error_style']}]Invalid choice. Try again.[/]")
            continue

        if action == "quit":
            console.print(f"  [{theme['dim_style']}]Goodbye! 👋[/]")
            break

        if action == "web":
            console.print(f"  [{theme['ok_style']}]Starting web UI...[/]")
            from fetch_info.web import run_web
            run_web(port=8099)
            break

        if action == "json":
            with console.status("[cyan]Collecting...", spinner="dots"):
                data = collect(live=True)
            click.echo(json.dumps(data, indent=2, default=str))
            continue

        with console.status("[cyan]Collecting...", spinner="dots2"):
            if action == "full":
                data = collect(live=True)
                render_all(console, data, theme_name, show_live=True, show_env=True)
            elif action == "ros2":
                data = collect(skip_ws=True, skip_sys=True)
                from fetch_info.display.panels import render_ros2_panel
                render_ros2_panel(console, data, theme)
            elif action == "system":
                data = collect(skip_ws=True, live=False)
                from fetch_info.display.panels import render_system_panel
                render_system_panel(console, data, theme)
            elif action == "live":
                data = collect(live=True, skip_ws=True, skip_sys=True)
                from fetch_info.display.panels import render_live_panel
                render_live_panel(console, data, theme)
            elif action == "workspace":
                data = collect(skip_sys=True, live=False)
                from fetch_info.display.panels import render_workspace_panel
                render_workspace_panel(console, data, theme)
            elif action == "env":
                data = collect(skip_ws=True, skip_sys=True, live=False)
                from fetch_info.display.panels import render_env_panel
                render_env_panel(console, data, theme)

        console.print(f"\n  [{theme['dim_style']}]Press Enter to continue...[/]")
        input()


@click.group(invoke_without_command=True)
@click.option("--theme",    "-t", default="default", type=click.Choice(list_themes()))
@click.option("--live",     "-l", is_flag=True,  help="Show live nodes/topics/services")
@click.option("--watch",    "-w", default=0,     help="Refresh every N seconds")
@click.option("--json",     "out_json", is_flag=True, help="Output raw JSON")
@click.option("--env",      "-e", is_flag=True,  help="Show env vars panel")
@click.option("--interactive", "-i", is_flag=True, help="Interactive TUI mode")
@click.option("--no-system",    is_flag=True)
@click.option("--no-workspace", is_flag=True)
@click.option("--no-updates",   is_flag=True)
@click.option("--logo",         is_flag=True, help="Print ASCII logo only")
@click.option("--timeout",  default=3)
@click.pass_context
def main(ctx, theme, live, watch, out_json, env, interactive, no_system, no_workspace, no_updates, logo, timeout):
    """ROS2 Info — system info tool for ROS2 developers."""
    if ctx.invoked_subcommand:
        return

    if interactive:
        interactive_mode(theme)
        return

    console = Console()

    if logo:
        from fetch_info.display.logo import get_main_banner
        from fetch_info.display.themes import get_theme
        console.print()
        console.print(get_main_banner(get_theme(theme)))
        console.print()
        return

    if out_json:
        with console.status("[cyan]Collecting...", spinner="dots"):
            data = collect(live=True, skip_ws=no_workspace, skip_sys=no_system,
                           timeout=timeout, updates=not no_updates)
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if watch > 0:
        try:
            while True:
                console.clear()
                with console.status("[cyan]Collecting...", spinner="dots2"):
                    data = collect(live=True, skip_ws=no_workspace, skip_sys=no_system,
                                   timeout=timeout, updates=not no_updates)
                render_all(console, data, theme, show_live=True, show_env=env)
                console.print(f"  [dim]Refreshing every {watch}s — Ctrl+C to exit[/]")
                time.sleep(watch)
        except KeyboardInterrupt:
            console.print("\n[dim]Exiting watch mode.[/]")
            return

    with console.status("[cyan]Collecting ROS2 info...", spinner="dots2"):
        data = collect(live=live, skip_ws=no_workspace, skip_sys=no_system,
                       timeout=timeout, updates=not no_updates)
    render_all(console, data, theme, show_live=live, show_env=env)


@main.command("nodes")
@click.option("--theme", "-t", default="default", type=click.Choice(list_themes()))
@click.option("--timeout", default=5)
def cmd_nodes(theme, timeout):
    """List all active ROS2 nodes."""
    from rich.table import Table
    console = Console()
    t = get_theme(theme)
    with console.status("[cyan]Querying nodes...", spinner="dots"):
        nodes = ros2.get_active_nodes(timeout)
    if not nodes:
        console.print("[yellow]No active nodes found. Is ROS2 running?[/]")
        return
    table = Table(title="Active ROS2 Nodes", border_style=t["panel_border"])
    table.add_column("Node", style=t["key_style"])
    table.add_column("Status", style=t["ok_style"])
    for n in nodes:
        table.add_row(n, "● Running")
    console.print(table)


@main.command("topics")
@click.option("--theme", "-t", default="default", type=click.Choice(list_themes()))
@click.option("--verbose", "-v", is_flag=True)
@click.option("--timeout", default=5)
def cmd_topics(theme, verbose, timeout):
    """List all active ROS2 topics."""
    from rich.table import Table
    console = Console()
    t = get_theme(theme)
    with console.status("[cyan]Querying topics...", spinner="dots"):
        topics = ros2.get_active_topics(timeout)
    if not topics:
        console.print("[yellow]No active topics found.[/]")
        return
    table = Table(title=f"Active Topics ({len(topics)})", border_style=t["panel_border"])
    table.add_column("Topic", style=t["key_style"])
    if verbose:
        table.add_column("Type", style=t["value_style"])
    for tp in topics:
        table.add_row(tp["name"], tp["type"]) if verbose else table.add_row(tp["name"])
    console.print(table)


@main.command("packages")
@click.option("--theme", "-t", default="default", type=click.Choice(list_themes()))
@click.option("--filter", "-f", "pkg_filter", default="")
def cmd_packages(theme, pkg_filter):
    """List all installed ROS2 packages."""
    import os
    from rich.columns import Columns
    from rich.text import Text
    console = Console()
    t = get_theme(theme)
    distro = ros2.get_distro()
    if not distro:
        console.print("[red]ROS2 not sourced.[/]")
        return
    ros_share = f"/opt/ros/{distro}/share"
    pkgs = sorted([d for d in os.listdir(ros_share) if os.path.isdir(f"{ros_share}/{d}")])
    if pkg_filter:
        pkgs = [p for p in pkgs if pkg_filter.lower() in p.lower()]
    console.print(f"\n[bold cyan]ROS2 Packages — {distro} ({len(pkgs)} shown)[/]\n")
    console.print(Columns([Text(f"  {p}", style=t["value_style"]) for p in pkgs], equal=True))


@main.command("workspace")
@click.option("--theme", "-t", default="default", type=click.Choice(list_themes()))
def cmd_workspace(theme):
    """Scan for colcon workspaces."""
    from fetch_info.display.panels import render_workspace_panel
    console = Console()
    t = get_theme(theme)
    with console.status("[cyan]Scanning...", spinner="dots"):
        data = {"workspace": workspace.collect_all()}
    render_workspace_panel(console, data, t)


@main.command("env")
@click.option("--theme", "-t", default="default", type=click.Choice(list_themes()))
def cmd_env(theme):
    """Show all ROS2 environment variables."""
    from rich.table import Table
    console = Console()
    t = get_theme(theme)
    env = ros2.get_ros2_environment()
    if not env:
        console.print("[yellow]No ROS2 env vars found. Source ROS2 first.[/]")
        return
    table = Table(title="ROS2 Environment", border_style=t["panel_border"], show_lines=True)
    table.add_column("Variable", style=t["key_style"])
    table.add_column("Value", style=t["value_style"])
    for k, v in env.items():
        table.add_row(k, v)
    console.print(table)


@main.command("themes")
def cmd_themes():
    """Preview all available themes."""
    from rich.text import Text
    console = Console()
    console.print("\n[bold cyan]Available Themes:[/]\n")
    for name in list_themes():
        t = get_theme(name)
        row = Text()
        row.append(f"  {name:<12}", style=f"bold {t['logo_color1']}")
        for key in ["logo_color1", "logo_color2", "logo_color3", "highlight"]:
            c = t.get(key, "#fff")
            if c.startswith("#"):
                row.append("██", style=f"bold {c}")
        row.append(f"  ros2_info --theme {name}", style="dim")
        console.print(row)
    console.print()


@main.command("web")
@click.option("--port", "-p", default=8099, help="Port for web UI")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
def cmd_web(port, host):
    """Launch the ROS2 Info web dashboard."""
    console = Console()
    console.print(f"\n  [bold cyan]🌐 ROS2 Info Web UI[/]")
    console.print(f"  [dim]Starting on http://localhost:{port}[/]\n")
    from fetch_info.web import run_web
    run_web(host=host, port=port)
