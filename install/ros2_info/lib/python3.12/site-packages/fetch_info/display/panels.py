import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich import box
from fetch_info.display.logo import get_colored_logo


def _bar(pct, width=20):
    fill = int(width * pct / 100)
    color = "red" if pct >= 90 else "yellow" if pct >= 70 else "cyan"
    t = Text()
    t.append("█" * fill, style=color)
    t.append("░" * (width - fill), style="grey30")
    t.append(f" {pct:.1f}%", style="white")
    return t


def render_header(console, theme, hostname, distro):
    console.print()
    console.print(get_colored_logo(theme, distro=distro))
    row = Text()
    row.append(f"  {hostname}", style=f"bold {theme['logo_color1']}")
    row.append("  ●  ", style=theme["dim_style"])
    row.append(f"ROS2 {distro.capitalize()}" if distro else "ROS2 not sourced",
               style=f"bold {theme['highlight']}" if distro else theme["error_style"])
    console.print(row)
    console.print(Rule(style=theme["panel_border"]))


def render_ros2_panel(console, data, theme):
    ros = data.get("ros2", {})
    tbl = Table.grid(padding=(0, 2))
    tbl.add_column(style=theme["key_style"], no_wrap=True, min_width=22)
    tbl.add_column(style=theme["value_style"])

    distro = ros.get("distro")
    di = ros.get("distro_info", {})
    if distro:
        dt = Text()
        dt.append(di.get("full", distro.capitalize()), style=f"bold {theme['highlight']}")
        if di.get("lts"):
            dt.append("  LTS", style=theme["ok_style"])
        tbl.add_row("  ROS2 Distro", dt)

        eol = di.get("eol", "Unknown")
        from datetime import datetime
        et = Text()
        try:
            if eol != "N/A":
                d = datetime.strptime(eol, "%Y-%m")
                if d < datetime.now():
                    et.append(f"EOL: {eol}  ⚠ EXPIRED", style=theme["error_style"])
                elif (d - datetime.now()).days < 180:
                    et.append(f"EOL: {eol}  Expiring Soon", style=theme["warn_style"])
                else:
                    et.append(f"Supported until {eol}", style=theme["ok_style"])
            else:
                et.append("Rolling — No EOL", style=theme["warn_style"])
        except:
            et.append(eol)
        tbl.add_row("  Support Status", et)
    else:
        tbl.add_row("  ROS2 Distro", Text("Not sourced — run: source /opt/ros/<distro>/setup.bash",
                                           style=theme["error_style"]))

    tbl.add_row("  ROS2 CLI", Text("Available ✓" if ros.get("available") else "Not found",
                                    style=theme["ok_style"] if ros.get("available") else theme["error_style"]))
    tbl.add_row("  DDS",        ros.get("dds", "Unknown"))
    tbl.add_row("  Domain ID",  str(ros.get("domain_id", "0")))

    ws = ros.get("workspace_source")
    tbl.add_row("  Workspace",  ws if ws else Text("None sourced", style=theme["dim_style"]))

    pkg = ros.get("packages", {})
    if pkg.get("total", 0):
        tbl.add_row("  Pkgs Installed", str(pkg["total"]))
        cats = pkg.get("categories", {})
        if cats:
            ct = Text()
            for i, c in enumerate(list(cats.keys())[:6]):
                if i: ct.append("  •  ", style=theme["dim_style"])
                ct.append(c, style=theme["highlight"])
            tbl.add_row("  Categories", ct)

    last_upd = ros.get("last_updated")
    if last_upd:
        tbl.add_row("  Last Updated", Text(last_upd, style=theme["value_style"]))

    upd = ros.get("updates")
    if upd:
        ut = Text()
        if "up to date" in upd.lower():
            ut.append("✓ " + upd, style=theme["ok_style"])
        else:
            ut.append("⚠ " + upd, style=theme["warn_style"])
        tbl.add_row("  Updates", ut)

    console.print(Panel(tbl, title=f"[{theme['section_title']}]  ROS2 Environment[/]",
                        border_style=theme["panel_border"], padding=(0,1), box=box.ROUNDED))


def render_system_panel(console, data, theme):
    sys = data.get("system", {})
    if not sys: return
    tbl = Table.grid(padding=(0, 2))
    tbl.add_column(style=theme["key_style"], no_wrap=True, min_width=22)
    tbl.add_column(style=theme["value_style"])

    osi = sys.get("os", {})
    os_str = f"{osi.get('name','')} {osi.get('version','')}".strip()
    if osi.get("codename"): os_str += f" ({osi['codename']})"
    tbl.add_row("  OS",        os_str)
    tbl.add_row("  Kernel",    osi.get("kernel", "Unknown"))
    tbl.add_row("  Arch",      osi.get("arch", "Unknown"))
    tbl.add_row("  Uptime",    sys.get("uptime", "Unknown"))
    tbl.add_row("  Shell",     sys.get("shell", "Unknown"))
    tbl.add_row("  Python",    sys.get("python", "Unknown"))

    cpu = sys.get("cpu", {})
    if cpu:
        model = cpu.get("model", "Unknown")
        if len(model) > 45: model = model[:42] + "..."
        tbl.add_row("  CPU", f"{model} ({cpu.get('cores','?')}C/{cpu.get('threads','?')}T)")

    gpu = sys.get("gpu")
    if gpu: tbl.add_row("  GPU", gpu)

    mem = sys.get("memory", {})
    if mem and mem.get("total_gb", 0):
        mt = Text()
        mt.append(f"{mem['used_gb']} / {mem['total_gb']} GB  ")
        mt.append_text(_bar(mem["percent"]))
        tbl.add_row("  RAM", mt)

    disk = sys.get("disk", {})
    if disk and disk.get("total_gb", 0):
        dt = Text()
        dt.append(f"{disk['used_gb']} / {disk['total_gb']} GB  ")
        dt.append_text(_bar(disk["percent"]))
        tbl.add_row("  Disk", dt)

    console.print(Panel(tbl, title=f"[{theme['section_title']}]  System Info[/]",
                        border_style=theme["panel_border"], padding=(0,1), box=box.ROUNDED))


def render_live_panel(console, data, theme):
    ros = data.get("ros2", {})
    nodes    = ros.get("nodes", [])
    topics   = ros.get("topics", [])
    services = ros.get("services", [])
    actions  = ros.get("actions", [])

    tbl = Table.grid(padding=(0, 2))
    tbl.add_column(style=theme["key_style"], no_wrap=True, min_width=22)
    tbl.add_column(style=theme["value_style"])

    def fmt_list(items, limit=4, bullet="●", style=None):
        t = Text()
        style = style or theme["value_style"]
        if not items:
            return Text("None", style=theme["dim_style"])
        for i, item in enumerate(items[:limit]):
            if i: t.append("\n" + " " * 24)
            t.append(f"{bullet} ", style=theme["ok_style"])
            t.append(item, style=style)
        if len(items) > limit:
            t.append(f"\n{' '*24}... and {len(items)-limit} more", style=theme["dim_style"])
        return t

    tbl.add_row(f"  Nodes ({len(nodes)})",    fmt_list(nodes))
    tbl.add_row(f"  Topics ({len(topics)})",   fmt_list([t['name'] for t in topics]))
    tbl.add_row(f"  Services ({len(services)})", fmt_list([s for s in services if "parameter" not in s][:8]))
    if actions:
        tbl.add_row(f"  Actions ({len(actions)})", fmt_list(actions, bullet="▶"))

    console.print(Panel(tbl, title=f"[{theme['section_title']}]  Live Runtime[/]",
                        border_style=theme["panel_border"], padding=(0,1), box=box.ROUNDED))


def render_workspace_panel(console, data, theme):
    workspaces = data.get("workspace", {}).get("workspaces", [])
    if not workspaces:
        console.print(Panel(
            Text("  No colcon workspaces found.\n  mkdir -p ~/ros2_ws/src && cd ~/ros2_ws && colcon build",
                 style=theme["dim_style"]),
            title=f"[{theme['section_title']}]  Workspaces[/]",
            border_style=theme["panel_border"], box=box.ROUNDED))
        return

    tbl = Table.grid(padding=(0, 2))
    tbl.add_column(style=theme["key_style"], no_wrap=True, min_width=22)
    tbl.add_column(style=theme["value_style"])

    for ws in workspaces:
        wt = Text(ws["path"], style=f"bold {theme['highlight']}")
        tbl.add_row("  Workspace", wt)
        st = Text()
        st.append(f"{ws['package_count']} packages", style=theme["ok_style"])
        st.append("  |  ", style=theme["dim_style"])
        st.append("Built ✓" if ws.get("has_install") else "Not built",
                  style=theme["ok_style"] if ws.get("has_install") else theme["warn_style"])
        tbl.add_row("    Stats", st)
        pkgs = [p["name"] for p in ws.get("packages", [])[:6]]
        if pkgs: tbl.add_row("    Packages", "  ".join(pkgs))
        tbl.add_row("", "")

    console.print(Panel(tbl, title=f"[{theme['section_title']}]  Workspaces[/]",
                        border_style=theme["panel_border"], padding=(0,1), box=box.ROUNDED))


def render_env_panel(console, data, theme):
    env = data.get("ros2", {}).get("environment", {})
    if not env: return
    tbl = Table.grid(padding=(0, 2))
    tbl.add_column(style=theme["key_style"], no_wrap=True, min_width=30)
    tbl.add_column(style=theme["value_style"])
    for k, v in env.items():
        tbl.add_row(f"  {k}", v)
    console.print(Panel(tbl, title=f"[{theme['section_title']}]  Environment Vars[/]",
                        border_style=theme["panel_border"], padding=(0,1), box=box.ROUNDED))


def render_footer(console, theme):
    console.print(Rule(style=theme["panel_border"]))
    t = Text()
    t.append("  Tips: ", style=f"bold {theme['logo_color1']}")
    for tip in ["--live", "--watch 2", "--theme matrix", "--json", "--interactive", "web", "nodes", "topics"]:
        t.append(f"ros2_info {tip}  ", style=theme["dim_style"])
    console.print(t)
    console.print()


def render_all(console, data, theme_name, show_live=False, show_env=False):
    from fetch_info.display.themes import get_theme
    theme = get_theme(theme_name)
    sys_data = data.get("system", {})
    hostname = sys_data.get("hostname", "unknown")
    distro   = data.get("ros2", {}).get("distro")
    
    render_header(console, theme, hostname, distro)
    render_ros2_panel(console, data, theme)
    if show_live or data.get("ros2", {}).get("nodes"):
        render_live_panel(console, data, theme)
    if sys_data:
        render_system_panel(console, data, theme)
    render_workspace_panel(console, data, theme)
    if show_env:
        render_env_panel(console, data, theme)
    render_footer(console, theme)
