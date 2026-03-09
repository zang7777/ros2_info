"""
ROS2 Info — Web Dashboard Server
Flask-based web server serving a premium dark-mode dashboard.
"""

import json
import threading
from flask import Flask, jsonify, render_template, Response
from fetch_info.collector import system, ros2, workspace
import os
import urllib.request
import xml.etree.ElementTree as ET


def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    app = Flask(__name__, template_folder=template_dir)

    def _collect_all():
        data = {}
        data["system"] = system.collect_all()
        data["ros2"] = ros2.collect_all(check_live=True, live_timeout=3, check_updates=True)
        data["workspace"] = workspace.collect_all()
        return data

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/info")
    def api_info():
        data = _collect_all()
        return jsonify(data)

    @app.route("/api/blog")
    def api_blog():
        """Fetch and parse the official ROS2 blog RSS feed."""
        entries = []
        try:
            urls = [
                "https://planet.ros.org/rss20.xml",
                "https://discourse.ros.org/latest.rss",
            ]
            for url in urls:
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "ROS2Info/1.0"})
                    with urllib.request.urlopen(req, timeout=8) as resp:
                        xml_data = resp.read().decode("utf-8", errors="replace")

                    root = ET.fromstring(xml_data)

                    # RSS 2.0 format
                    for item in root.findall(".//item")[:15]:
                        title = item.findtext("title", "")
                        link = item.findtext("link", "")
                        pub_date = item.findtext("pubDate", "")
                        desc = item.findtext("description", "")
                        # Clean up HTML from description
                        if desc:
                            import re
                            desc = re.sub(r'<[^>]+>', '', desc)
                            desc = desc.strip()[:200]
                            if len(desc) == 200:
                                desc += "..."
                        entries.append({
                            "title": title,
                            "link": link,
                            "date": pub_date,
                            "summary": desc,
                            "source": "Planet ROS" if "planet" in url else "ROS Discourse",
                        })
                    if entries:
                        break
                except Exception:
                    continue
        except Exception as e:
            entries = [{"title": "Could not fetch blog feed", "link": "", "date": "", "summary": str(e), "source": ""}]

        return jsonify(entries[:12])

    return app


def run_web(host="0.0.0.0", port=8099):
    app = create_app()
    app.run(host=host, port=port, debug=False)
