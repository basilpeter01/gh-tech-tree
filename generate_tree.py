#!/usr/bin/env python3
"""
GitHub Repository-Language Dependency Graph Generator
Generates a standalone dark-mode SVG showing a bipartite graph
of Languages (left) ↔ Repositories (right) with cubic Bézier curves.
Zero external dependencies — uses only the Python standard library.
"""

import os
import json
import math
import urllib.request

CONFIG_FILE = "config.json"
OUTPUT_SVG = "tech-tree.svg"

# Palette mapped to official GitHub language colors
LANG_COLORS = {
    "Python": "#3572A5",
    "C": "#555555",
    "C++": "#f34b7d",
    "C#": "#178600",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Rust": "#dea584",
    "Go": "#00ADD8",
    "Java": "#b07219",
    "Kotlin": "#A97BFF",
    "Swift": "#F05138",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Dart": "#00B4AB",
    "Lua": "#000080",
    "Scala": "#c22d40",
    "R": "#198CE7",
    "MATLAB": "#e16737",
    "Haskell": "#5e5086",
    "Elixir": "#6e4a7e",
    "Clojure": "#db5855",
    "Perl": "#0298c3",
    "Zig": "#ec915c",
    "Nim": "#ffc200",
    "Julia": "#a270ba",
    "OCaml": "#3be133",
    "Erlang": "#B83998",
    "Objective-C": "#438eff",
    "Assembly": "#6E4C13",
    "PowerShell": "#012456",
    "Makefile": "#427819",
    "Dockerfile": "#384d54",
    "HCL": "#844FBA",
    "Nix": "#7e7eff",
    "Vue": "#41b883",
    "Svelte": "#ff3e00",
    "SCSS": "#c6538c",
    "Default": "#8b949e",
}


def fetch_json(url, token=None):
    """Fetch JSON from a URL, optionally authenticated."""
    headers = {"User-Agent": "GitHub-Tech-Tree-Engine"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def fetch_all_repos(username, token=None):
    """Paginate through all public repos for a user."""
    all_repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed&page={page}"
        batch = fetch_json(url, token)
        if not batch:
            break
        all_repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return all_repos


def run():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    username = config["github_username"]
    if username == "YOUR_GITHUB_USERNAME":
        print("ERROR: Please set your GitHub username in config.json")
        return

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    min_pct = config.get("min_language_percent", 4.0)
    ignore_langs = set(config.get("ignore_languages", []))
    max_repos = config.get("max_repos", 6)
    pinned_repos = config.get("pinned_repos", [])
    exclude_repos = set(config.get("exclude_repos", []))

    # ── 1. Fetch public repos ──────────────────────────────────────────
    print(f"Fetching repositories for @{username} ...")
    repos = fetch_all_repos(username, token)

    selected_repos = []
    for r in repos:
        if r["fork"]:
            continue
        if r["name"] in exclude_repos:
            continue
        if pinned_repos and r["name"] not in pinned_repos:
            continue
        selected_repos.append(r["name"])
        if len(selected_repos) >= max_repos:
            break

    if not selected_repos:
        print("No repositories matched the filter criteria.")
        return

    # ── 2. Fetch language breakdown per repo ───────────────────────────
    repo_lang_map = {}
    distinct_languages = set()

    for repo_name in selected_repos:
        lang_url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
        print(f"  → analysing {repo_name} ...")
        data = fetch_json(lang_url, token)
        total_bytes = sum(data.values())
        if total_bytes == 0:
            continue

        active_langs = []
        for lang, count in data.items():
            if lang in ignore_langs:
                continue
            pct = (count / total_bytes) * 100
            if pct >= min_pct:
                active_langs.append(lang)
                distinct_languages.add(lang)

        if active_langs:
            repo_lang_map[repo_name] = active_langs

    # Active lists for layout
    languages = sorted(list(distinct_languages))
    repositories = list(repo_lang_map.keys())

    if not languages or not repositories:
        print("No matching language/repo data found after filtering.")
        return

    print(f"  Languages: {languages}")
    print(f"  Repos:     {repositories}")

    # ── 3. Geometry & Layout ───────────────────────────────────────────
    WIDTH = 800
    NODE_HEIGHT = 38
    SPACING = 20

    col1_y_start = 70
    col2_y_start = 70

    total_col1_h = len(languages) * (NODE_HEIGHT + SPACING)
    total_col2_h = len(repositories) * (NODE_HEIGHT + SPACING)
    HEIGHT = max(total_col1_h, total_col2_h) + 120

    # Center columns vertically when one has fewer items
    if total_col1_h < total_col2_h:
        col1_y_start += (total_col2_h - total_col1_h) / 2
    else:
        col2_y_start += (total_col1_h - total_col2_h) / 2

    lang_coords = {}
    for i, lang in enumerate(languages):
        y = col1_y_start + i * (NODE_HEIGHT + SPACING)
        lang_coords[lang] = (160, y + NODE_HEIGHT / 2)

    repo_coords = {}
    for j, repo in enumerate(repositories):
        y = col2_y_start + j * (NODE_HEIGHT + SPACING)
        repo_coords[repo] = (WIDTH - 180, y + NODE_HEIGHT / 2)

    # ── 4. Generate SVG ───────────────────────────────────────────────
    svg_elements = []

    # Connecting cubic Bézier curves
    for repo, langs in repo_lang_map.items():
        x2, y2 = repo_coords[repo]
        for lang in langs:
            if lang in lang_coords:
                x1, y1 = lang_coords[lang]
                color = LANG_COLORS.get(lang, LANG_COLORS["Default"])
                cx1 = x1 + 140
                cx2 = x2 - 140
                path_d = f"M {x1} {y1} C {cx1} {y1}, {cx2} {y2}, {x2} {y2}"
                svg_elements.append(
                    f'<path d="{path_d}" fill="none" stroke="{color}" '
                    f'stroke-opacity="0.45" stroke-width="2" />'
                )

    # Language nodes (left column)
    for lang, (x, y) in lang_coords.items():
        color = LANG_COLORS.get(lang, LANG_COLORS["Default"])
        box_x = 30
        box_y = y - NODE_HEIGHT / 2
        svg_elements.append(
            f'<g class="node">'
            f'<rect x="{box_x}" y="{box_y}" width="140" height="{NODE_HEIGHT}" '
            f'rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />'
            f'<circle cx="{box_x + 18}" cy="{y}" r="5" fill="{color}" />'
            f'<text x="{box_x + 32}" y="{y + 4}" fill="#c9d1d9" '
            f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" '
            f'font-size="13" font-weight="600">{lang}</text>'
            f'</g>'
        )

    # Repository nodes (right column)
    for repo, (x, y) in repo_coords.items():
        box_x = WIDTH - 200
        box_y = y - NODE_HEIGHT / 2
        display_name = repo if len(repo) <= 18 else repo[:16] + ".."
        svg_elements.append(
            f'<g class="node">'
            f'<rect x="{box_x}" y="{box_y}" width="170" height="{NODE_HEIGHT}" '
            f'rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.5" />'
            f'<text x="{box_x + 14}" y="{y + 4}" fill="#58a6ff" '
            f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" '
            f'font-size="12" font-weight="600">{display_name}</text>'
            f'</g>'
        )

    # Header / Title
    header = (
        f'<text x="35" y="38" fill="#8b949e" '
        f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" '
        f'font-size="12" font-weight="700" letter-spacing="1">'
        f'ACTIVE TECH ECOSYSTEM</text>'
        f'<line x1="30" y1="52" x2="{WIDTH - 30}" y2="52" '
        f'stroke="#21262d" stroke-width="1" />'
    )

    full_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="100%">\n'
        f'<style>\n'
        f'  .node:hover rect {{ stroke: #58a6ff; transition: stroke 0.2s ease; }}\n'
        f'</style>\n'
        f'<rect width="100%" height="100%" fill="#0d1117" rx="10" />\n'
        f'{header}\n'
        f'{"".join(svg_elements)}\n'
        f'</svg>'
    )

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(full_svg)

    print(f"✔ Graph generated successfully → {OUTPUT_SVG}")


if __name__ == "__main__":
    run()
