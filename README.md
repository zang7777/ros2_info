# ROS2 Info ⊙
        ╔══════════════════════════════════════════════════════════════════════===════╗
        ║                                                                             ║
        ║    ██████╗  ██████╗ ███████╗    ██████╗     ██╗   ███╗   ██╗███████╗ ██████╗║
        ║    ██╔══██╗██╔═══██╗██╔════╝    ╚════██╗    ██╔╝  ████╗  ██║██╔════╝██╔═══██╗
        ║    ██████╔╝██║   ██║███████╗     █████╔╝    ██╔╝  ██╔██╗ ██║█████╗  ██║   ██║
        ║    ██╔══██╗██║   ██║╚════██║    ██╔═══╝     ██╔╝  ██║╚██╗██║██╔══╝  ██║   ██║
        ║    ██║  ██║╚██████╔╝███████║    ███████╗    ██╔╝  ██║ ╚████║██║     ╚██████╔╝
        ║    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚══════╝    ╚═╝    ╚═╝  ╚═══╝╚═╝      ╚═════╝ 
        ║            ~"Created by roboticists, for roboticists   ║                                                                             ║
        ║           ⬡  The fastfetch you always wanted — for ROS2  ⬡                 ║
        ╚═════════════════════════════════════════════════════════════════════===═════╝

        
                            A beautiful, interactive Fastfetch-like system information tool and web dashboard built specifically for **ROS2 developers**. 


<div align="center">

[![ROS2](https://img.shields.io/badge/ROS2-Jazzy%20%7C%20Humble%20%7C%20Iron%20%7C%20Rolling-22D3EE?style=for-the-badge&logo=ros&logoColor=white)](https://docs.ros.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3B82F6?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)
[![colcon](https://img.shields.io/badge/Built%20with-colcon-F97316?style=for-the-badge)](https://colcon.readthedocs.io)

*Born from frustration. Built for roboticists.*

</div>

## 💡 Why was this created? 
 🧠 The Genesis (aka "The Rant")

Let’s be real. We all love `fastfetch`. It makes us feel like elite hackers when we see that ASCII distro logo and realize we’re only idling at 400MB of RAM on our lean KDE Plasma setup. 🐧💻

But as **ROS2 developers**, we live in a simulation of our own creation—a simulation of multiple sourcing environments, competing DDS implementations, and the eternal mystery of "Which Domain ID am I on again?"

We looked at `fastfetch` and thought:

> "This is great, but does it know if my TF-Luna LiDAR node is actually publishing, or if my Link Budget calculation just collapsed in a high-frequency filter failure?" 🤔💥

It didn't. And we were tired of the "Sourcing Dance":
1. Open Terminal A. Source Jazzy. Run bridge.
2. Open Terminal B. Source Humble. Wonder why nothing talks.
3. Open Terminal C. Check `ros2 node list`. Realize we aren't sourced at all.
4. **Kernel Panic (Internal).** 🤯

**ROS2 Info** was engineered to synthesize environmental telemetrics with live robotics runtime data. We needed a canonical "Source of Truth" that looked good enough to satisfy our terminal Rice addiction (CLI) while being accessible enough to monitor from a smartphone during hardware integration (WebUI).

We created this because **Efficiency** is not just about compute cycles; it's about **Developer Experience (DX)**.

*(And because looking at distro-aware ASCII art makes the wait for `colcon build` to finish slightly less agonizing.)* 🎨

🚀 Key Features
🖥️ CLI (Fastfetch Mode)
Distro-Aware ASCII Art: Automatically detects your ROS2 distro (Jazzy, Humble, Foxy, etc.) and displays a unique, stylized ASCII logo.

System & Environment Stats: OS version, CPU, Memory usage, ROS2 version, DDS middleware, and Domain ID at a glance.

Workspace Auto-Detection: Scans and displays your sourced colcon workspaces and their build status.

📊 Real-time Robotics Pulse
Live Watch Mode: Instantly see active nodes, topics, services, and actions.

Interactive TUI: A built-in terminal user interface powered by click and rich to selectively view different system panels.

🌐 Web Dashboard (Inspired by ros.org)
Elegant, Light-Themed Web UI: A modern dashboard that live-updates your system and ROS2 stats.

Community Integration: Seamlessly embeds the official ROS2 community blog for news and updates.

### 🚀 How to Use

*(Ensure you have sourced your ROS2 environment first: `source /opt/ros/jazzy/setup.bash`)*

### 1. Standard Info Fetch
Run the command directly to print a beautiful fastfetch-style summary to your terminal:
```bash
ros2 run ros2_info ros2_info
```

### 2. Live Watch Mode
Keep the terminal open and automatically refresh the runtime stats (nodes/topics) every 2 seconds:
```bash
ros2 run ros2_info ros2_info --watch 2
```

### 3. Interactive Menu
Don't want to type flags? Open the interactive terminal UI to browse your system:
```bash
ros2 run ros2_info ros2_info --interactive
```

### 4. 🌐 Web Dashboard
Launch a rich, interactive web UI that you can view in your browser (defaults to `http://localhost:8099`):
```bash
ros2 run ros2_info ros2_info web
```

### 5. Other Commands
```bash
ros2 run ros2_info ros2_info nodes     # List all active nodes
ros2 run ros2_info ros2_info topics    # List all active topics
ros2 run ros2_info ros2_info packages  # List installed ROS2 packages
ros2 run ros2_info ros2_info env       # Show ROS2 environment variables
```

*Built with Python, Click, Rich, and Flask. Designed for roboticists.*

---
# ros2_info
