from rich.text import Text

# ── Per-distro ASCII logos ──────────────────────────────────────────────

LOGO_JAZZY = r"""
       ♪ ♫  ♪ ♫
    ╭──────────────╮
    │  ╦╔═╗╔═╗╔═╗╦ │
    │  ║╠═╣╔═╝╔═╝╚╦╝│
    │ ╚╝╩ ╩╚═╝╚═╝ ╩ │
    ╰──────────────╯
   ROS2 Jazzy Jalisco ♪
"""

LOGO_HUMBLE = r"""
    🐢
    ╦ ╦╦ ╦╔╦╗╔╗ ╦  ╔═╗
    ╠═╣║ ║║║║╠╩╗║  ║╣
    ╩ ╩╚═╝╩ ╩╚═╝╩═╝╚═╝
   ROS2 Humble Hawksbill
"""

LOGO_IRON = r"""
    ⚙
    ╦╔═╗╔═╗╔╗╔
    ║╠╦╝║ ║║║║
    ╩╩╚═╚═╝╝╚╝
    ROS2 Iron Irwini
"""

LOGO_ROLLING = r"""
    ◎ ────▶
    ╦═╗╔═╗╦  ╦  ╦╔╗╔╔═╗
    ╠╦╝║ ║║  ║  ║║║║║ ╦
    ╩╚═╚═╝╩═╝╩═╝╩╝╚╝╚═╝
   ROS2 Rolling Ridley ◎
"""

LOGO_KILTED = r"""
    🏴
    ╦╔═╦╦  ╔╦╗╔═╗╔╦╗
    ╠╩╗║║   ║ ║╣  ║║
    ╩ ╩╩╩═╝ ╩ ╚═╝═╩╝
    ROS2 Kilted Kaiju
"""

LOGO_FOXY = r"""
    🦊
    ╔═╗╔═╗═╗╔╦ ╦
    ╠╣ ║ ║╔╩╦╝╚╦╝
    ╚  ╚═╝╩ ╚═ ╩
    ROS2 Foxy Fitzroy
"""

LOGO_GALACTIC = r"""
    ✦
    ╔═╗╔═╗╦  ╔═╗╔═╗╔╦╗╦╔═╗
    ║ ╦╠═╣║  ╠═╣║   ║ ║║
    ╚═╝╩ ╩╩═╝╩ ╩╚═╝ ╩ ╩╚═╝
   ROS2 Galactic Geochelone
"""

LOGO_GENERIC = r"""
 ██████╗  ██████╗ ███████╗██████╗
 ██╔══██╗██╔═══██╗██╔════╝╚════██╗
 ██████╔╝██║   ██║███████╗   ██╔╝
 ██╔══██╗██║   ██║╚════██║╚██╗
 ██║  ██║╚██████╔╝███████║███████╗
 ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
          Robot Operating System 2
"""

DISTRO_LOGOS = {
    "jazzy":    LOGO_JAZZY,
    "humble":   LOGO_HUMBLE,
    "iron":     LOGO_IRON,
    "rolling":  LOGO_ROLLING,
    "kilted":   LOGO_KILTED,
    "foxy":     LOGO_FOXY,
    "galactic": LOGO_GALACTIC,
}


def get_colored_logo(theme, distro=None):
    """Return a Rich Text logo colored with the theme, specific to the ROS2 distro."""
    logo_str = DISTRO_LOGOS.get(distro, LOGO_GENERIC) if distro else LOGO_GENERIC
    lines = logo_str.split('\n')
    text = Text()
    colors = [theme.get(f"logo_color{i+1}", "#22D3EE") for i in range(6)]
    colors.append(theme.get("subtitle_color", "#94A3B8"))
    for i, line in enumerate(lines):
        text.append(line + "\n", style=f"bold {colors[min(i, len(colors)-1)]}")
    return text


MAIN_BANNER = r"""
            ╔══════════════════════════════════════════════════════════════════════════=═══=╗
            ║                                                                               ║
            ║    ██████╗  ██████╗ ███████╗    ██████╗     ██╗   ███╗   ██╗███████╗ ██████╗  ║
            ║    ██╔══██╗██╔═══██╗██╔════╝    ╚════██╗    ██╔╝  ████╗  ██║██╔════╝██╔═══██╗ ║
            ║    ██████╔╝██║   ██║███████╗     █████╔╝    ██╔╝  ██╔██╗ ██║█████╗  ██║   ██║ ║
            ║    ██╔══██╗██║   ██║╚════██║    ██╔═══╝     ██╔╝  ██║╚██╗██║██╔══╝  ██║   ██║ ║
            ║    ██║  ██║╚██████╔╝███████║    ███████╗    ██╔╝  ██║ ╚████║██║     ╚██████╔╝ ║
            ║    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚══════╝    ╚═╝    ╚═╝  ╚═══╝╚═╝      ╚═════╝ ║
            ║        ~"Created by roboticists, for roboticists."                            ║
            ║           ⬡  The fastfetch you always wanted — for ROS2  ⬡                   ║
            ╚═══════════════════════════════════════════════════════════════════════════=══=╝
"""

def get_main_banner(theme):
    """Return the large main banner colored with the theme."""
    lines = MAIN_BANNER.strip("\n").split('\n')
    text = Text()
    color = theme.get("logo_color1", "#22D3EE")
    for line in lines:
        text.append("  " + line + "\n", style=f"bold {color}")
    return text
