#!/usr/bin/env python3
"""
GitHub Repository-Language Dependency Graph Generator
Generates a standalone dark-mode SVG showing a cybernetic bipartite graph
of Languages (left) ↔ Repositories (right) with glowing cubic Bézier curves,
circular language badges, and repository cards with language percentage bars.
No external dependencies — pure Python standard library.
"""

import html
import json
import math
import os
import sys
import urllib.error
import urllib.request

CONFIG_FILE = "config.json"
OUTPUT_SVG = "tech-tree.svg"

# Colour Palette for Languages
LANG_COLORS = {
    "Python": "#38bdf8",       # Luminous Sky Blue / Cyan
    "JavaScript": "#facc15",   # Electric Gold / Yellow
    "TypeScript": "#3b82f6",   # Vivid Royal Azure
    "C": "#818cf8",            # Electric Indigo / Periwinkle (replaces #555555)
    "C++": "#f43f5e",          # Vivid Rose / Hot Pink
    "C#": "#a855f7",           # Electric Purple / Violet
    "Java": "#f97316",         # Radiant Amber Orange (replaces #B07219)
    "Rust": "#fb923c",         # Terracotta Coral
    "Go": "#00add8",           # Cyan Teal
    "Kotlin": "#c084fc",       # Soft Violet
    "Swift": "#ff6b4a",        # Flame Red-Orange
    "Ruby": "#e11d48",         # Ruby Red
    "PHP": "#a78bfa",          # Lavender Purple
    "Dart": "#14b8a6",         # Electric Teal
    "Lua": "#60a5fa",          # Moon Blue
    "Scala": "#ef4444",        # Crimson Red
    "R": "#22d3ee",            # Bright Aqua
    "MATLAB": "#f59e0b",       # Golden Amber
    "Haskell": "#8b5cf6",      # Purple
    "Elixir": "#c084fc",       # Orchid
    "Clojure": "#4ade80",      # Lime Green
    "Perl": "#38bdf8",         # Sky Blue
    "Zig": "#f59e0b",          # Amber
    "Nim": "#eab308",          # Yellow
    "Julia": "#a855f7",        # Violet
    "OCaml": "#f97316",        # Orange
    "Erlang": "#ec4899",       # Pink
    "Objective-C": "#0284c7",  # Deep Sky
    "Assembly": "#94a3b8",     # Silver Gray
    "PowerShell": "#38bdf8",   # PowerShell Cyan
    "Makefile": "#4ade80",     # Terminal Green
    "Dockerfile": "#0ea5e9",   # Docker Blue
    "HCL": "#818cf8",          # Hashi Indigo
    "Nix": "#67e8f9",          # Ice Cyan
    "Vue": "#41b883",          # Vue Emerald
    "Svelte": "#ff3e00",       # Svelte Orange-Red
    "SCSS": "#ec4899",         # Sass Pink
    "HTML": "#f97316",         # HTML Orange
    "CSS": "#3b82f6",          # CSS Blue
    "Shell": "#22c55e",        # Bash Green
    "Default": "#94a3b8",      # Slate
}


def fetch_json(url, token=None):
    """Fetch JSON from a URL, optionally authenticated with a token."""
    headers = {"User-Agent": "GitHub-Tech-Tree-Engine"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("\nGitHub API Rate Limit Exceeded (HTTP 403).")
            print("   GitHub limits unauthenticated requests to 60/hour per IP.")
            print("   Solutions:")
            print("   1. In GitHub Actions, authentication is automatic (5000/hr).")
            print("   2. Locally, provide a token: $env:GH_TOKEN=\"your_github_token\"")
            sys.exit(1)
        elif e.code == 404:
            print(f"\nResource not found (HTTP 404): {url}")
            print("   Please check the username or repository name in config.json.")
            sys.exit(1)
        else:
            print(f"\nGitHub API Error HTTP {e.code}: {e.reason}")
            sys.exit(1)
    except urllib.error.URLError as e:
        print(f"\nNetwork Connection Error: {e.reason}")
        print("   Please check your internet connection.")
        sys.exit(1)


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


def format_bytes(bytes_count):
    """Format byte count into human-readable string (KB, MB, GB)."""
    if bytes_count >= 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024 * 1024):.1f}GB"
    elif bytes_count >= 1024 * 1024:
        return f"{bytes_count / (1024 * 1024):.1f}MB"
    elif bytes_count >= 1024:
        return f"{bytes_count / 1024:.1f}KB"
    else:
        return f"{bytes_count}B"


def render_lang_icon(lang, color, cx, cy):
    """Render a sleek vector icon or monogram inside the circular badge."""
    icon_svg = []

    if lang == "Python":
        # Python dual snakes logo
        icon_svg.append(f'''
        <g transform="translate({cx - 13}, {cy - 13}) scale(0.81)">
            <path fill="#387eb8" d="M15.88 0c-4.42 0-4.14 1.91-4.14 1.91v2.01h4.21v.6H9.72S6.7 4.14 6.7 8.56s2.63 4.3 2.63 4.3h1.57v-2.12s-.09-2.52 2.52-2.52h4.34s2.38.08 2.38-2.38V2.38S20.3 0 15.88 0zm-2.4 1.34a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6z"/>
            <path fill="#ffe873" d="M16.12 32c4.42 0 4.14-1.91 4.14-1.91v-2.01h-4.21v-.6h6.23s3.02.38 3.02-4.04-2.63-4.3-2.63-4.3h-1.57v2.12s.09 2.52-2.52 2.52h-4.34s-2.38-.08-2.38 2.38v3.46s-.16 2.38 4.26 2.38zm2.4-1.34a.8.8 0 1 1 0-1.6.8.8 0 0 1 0 1.6z"/>
        </g>''')

    elif lang == "JavaScript":
        # Yellow square badge with JS
        bx, by = cx - 12, cy - 12
        icon_svg.append(f'''
        <rect x="{bx}" y="{by}" width="24" height="24" rx="4" fill="#f7df1e" />
        <text x="{cx}" y="{cy + 5}" fill="#000000" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11.5" font-weight="900" text-anchor="middle">JS</text>
        ''')

    elif lang == "TypeScript":
        # Blue square badge with TS
        bx, by = cx - 12, cy - 12
        icon_svg.append(f'''
        <rect x="{bx}" y="{by}" width="24" height="24" rx="4" fill="#2563eb" />
        <text x="{cx}" y="{cy + 5}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11.5" font-weight="900" text-anchor="middle">TS</text>
        ''')

    elif lang == "C":
        # Hexagonal C badge (Indigo)
        icon_svg.append(f'''
        <polygon points="{cx},{cy - 13} {cx + 12},{cy - 6} {cx + 12},{cy + 6} {cx},{cy + 13} {cx - 12},{cy + 6} {cx - 12},{cy - 6}" fill="#4338ca" stroke="#818cf8" stroke-width="1.2"/>
        <text x="{cx}" y="{cy + 5}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="800" text-anchor="middle">C</text>
        ''')

    elif lang == "C++":
        # Hexagonal C++ badge
        icon_svg.append(f'''
        <polygon points="{cx},{cy - 13} {cx + 13},{cy - 6} {cx + 13},{cy + 6} {cx},{cy + 13} {cx - 13},{cy + 6} {cx - 13},{cy - 6}" fill="#be123c" stroke="#f43f5e" stroke-width="1"/>
        <text x="{cx}" y="{cy + 4}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="9" font-weight="800" text-anchor="middle">C++</text>
        ''')

    elif lang == "C#":
        # Hexagonal C# badge
        icon_svg.append(f'''
        <polygon points="{cx},{cy - 13} {cx + 13},{cy - 6} {cx + 13},{cy + 6} {cx},{cy + 13} {cx - 13},{cy + 6} {cx - 13},{cy - 6}" fill="#7e22ce" stroke="#a855f7" stroke-width="1"/>
        <text x="{cx}" y="{cy + 4}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="9.5" font-weight="800" text-anchor="middle">C#</text>
        ''')

    elif lang == "Rust":
        # Gear / R
        icon_svg.append(f'''
        <circle cx="{cx}" cy="{cy}" r="12" fill="#ea580c" />
        <text x="{cx}" y="{cy + 5}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="900" text-anchor="middle">R</text>
        ''')

    elif lang == "Go":
        # Cyan badge with GO
        bx, by = cx - 12, cy - 9
        icon_svg.append(f'''
        <rect x="{bx}" y="{by}" width="24" height="18" rx="5" fill="#00add8" />
        <text x="{cx}" y="{cy + 4.5}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="10.5" font-weight="900" text-anchor="middle">GO</text>
        ''')

    elif lang == "Java":
        # Java badge (Radiant Amber Orange)
        icon_svg.append(f'''
        <circle cx="{cx}" cy="{cy}" r="12" fill="#c2410c" stroke="#f97316" stroke-width="1.2" />
        <text x="{cx}" y="{cy + 4}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="8.5" font-weight="900" text-anchor="middle">JAVA</text>
        ''')

    else:
        # Monogram fallback for any other language
        label = (lang[:3] if len(lang) > 3 else lang).upper()
        font_size = "9" if len(label) == 3 else "11"
        icon_svg.append(f'''
        <circle cx="{cx}" cy="{cy}" r="11" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="1" />
        <text x="{cx}" y="{cy + 4}" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="{font_size}" font-weight="800" text-anchor="middle">{label}</text>
        ''')

    return "".join(icon_svg)


def run():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    username = config["github_username"]
    if username in ("YOUR_GITHUB_USERNAME", "GITHUB_USERNAME"):
        print("ERROR: Please set your GitHub username in config.json")
        return

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    min_pct = config.get("min_language_percent", 2.0)
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
    repo_breakdowns = {}
    distinct_languages = set()
    total_indexed_bytes = 0

    for repo_name in selected_repos:
        lang_url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
        print(f"  → analysing {repo_name} ...")
        data = fetch_json(lang_url, token)
        total_bytes = sum(data.values())
        if total_bytes == 0:
            continue

        active_langs = []
        breakdown_items = []

        # Filter out ignored languages to compute valid proportion
        valid_total = sum(count for lang, count in data.items() if lang not in ignore_langs)
        if valid_total == 0:
            continue

        for lang, count in data.items():
            if lang in ignore_langs:
                continue
            pct = (count / valid_total) * 100
            if pct >= min_pct:
                active_langs.append(lang)
                distinct_languages.add(lang)
                breakdown_items.append({
                    "lang": lang,
                    "pct": pct,
                    "color": LANG_COLORS.get(lang, LANG_COLORS["Default"])
                })

        if active_langs:
            repo_lang_map[repo_name] = active_langs
            repo_breakdowns[repo_name] = breakdown_items
            total_indexed_bytes += valid_total

    # Active lists for layout
    languages = sorted(list(distinct_languages))
    repositories = list(repo_lang_map.keys())

    if not languages or not repositories:
        print("No matching language/repo data found after filtering.")
        return

    print(f"  Languages ({len(languages)}): {languages}")
    print(f"  Repos ({len(repositories)}):     {repositories}")

    # ── 3. Geometry & Layout ───────────────────────────────────────────
    WIDTH = 1000
    NODE_GAP = 76          # Vertical spacing between node centers
    HEADER_HEIGHT = 88

    total_col1_h = len(languages) * NODE_GAP
    total_col2_h = len(repositories) * NODE_GAP
    content_h = max(total_col1_h, total_col2_h)
    HEIGHT = content_h + HEADER_HEIGHT + 70

    col1_y_start = HEADER_HEIGHT + (content_h - total_col1_h) / 2 + NODE_GAP / 2
    col2_y_start = HEADER_HEIGHT + (content_h - total_col2_h) / 2 + NODE_GAP / 2

    # Left column: badge center at cx = 205
    LANG_CX = 205
    BADGE_R = 23
    PORT_X1 = LANG_CX + BADGE_R + 2

    # Right column: repo card
    CARD_W = 215
    CARD_H = 46
    CARD_X = WIDTH - CARD_W - 55
    PORT_X2 = CARD_X

    lang_coords = {}
    for i, lang in enumerate(languages):
        y = col1_y_start + i * NODE_GAP
        lang_coords[lang] = (LANG_CX, y)

    repo_coords = {}
    for j, repo in enumerate(repositories):
        y = col2_y_start + j * NODE_GAP
        repo_coords[repo] = (PORT_X2, y)

    # ── 4. Generate SVG ───────────────────────────────────────────────
    svg_elements = []

    # Defs: Dot grid pattern, card clip paths
    defs_content = [
        '<defs>',
        '  <pattern id="dot-grid" width="22" height="22" patternUnits="userSpaceOnUse">',
        '    <circle cx="11" cy="11" r="0.9" fill="#1b283d" opacity="0.65" />',
        '  </pattern>',
    ]

    for idx, repo in enumerate(repositories):
        ry = repo_coords[repo][1] - CARD_H / 2
        defs_content.append(
            f'  <clipPath id="clip-card-{idx}">'
            f'<rect x="{CARD_X}" y="{ry}" width="{CARD_W}" height="{CARD_H}" rx="8" />'
            f'</clipPath>'
        )

    defs_content.append('</defs>')
    svg_elements.append("\n".join(defs_content))

    # Background
    svg_elements.append(
        f'<rect width="100%" height="100%" fill="#060913" />\n'
        f'<rect width="100%" height="100%" fill="url(#dot-grid)" />'
    )

    # Header / Title Bar & Telemetry HUD
    title_text = "RECENT WORKSPACE"
    total_repos_count = len(repos)
    all_profile_languages = {
        r["language"]
        for r in repos
        if r.get("language") and r["language"] not in ignore_langs
    }
    total_stacks_count = len(all_profile_languages | distinct_languages)

    header = (
        f'<g class="header">\n'
        f'  <!-- Main Title Bar -->\n'
        f'  <line x1="55" y1="28" x2="385" y2="28" stroke="#162338" stroke-width="1.2" />\n'
        f'  <circle cx="385" cy="28" r="2" fill="#38bdf8" fill-opacity="0.6" />\n'
        f'  <text x="{WIDTH // 2}" y="32" fill="#64748b" '
        f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" '
        f'font-size="11" font-weight="700" letter-spacing="3" text-anchor="middle">{title_text}</text>\n'
        f'  <circle cx="615" cy="28" r="2" fill="#38bdf8" fill-opacity="0.6" />\n'
        f'  <line x1="615" y1="28" x2="{WIDTH - 55}" y2="28" stroke="#162338" stroke-width="1.2" />\n'
        f'\n'
        f'  <!-- Top-Left Telemetry Legend Pill -->\n'
        f'  <g class="hud-counters">\n'
        f'    <rect x="55" y="44" width="245" height="22" rx="6" fill="#09101d" stroke="#162338" stroke-width="1" />\n'
        f'    <circle cx="68" cy="55" r="3" fill="#22c55e" />\n'
        f'    <circle cx="68" cy="55" r="6" fill="none" stroke="#22c55e" stroke-opacity="0.25" stroke-width="1" />\n'
        f'    <text x="79" y="59" fill="#64748b" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" '
        f'font-size="9.5" font-weight="700" letter-spacing="0.8">\n'
        f'      <tspan fill="#38bdf8">REPOS:</tspan> <tspan fill="#e2e8f0">{len(repositories)} OF {total_repos_count}</tspan>'
        f'      <tspan fill="#334155">  |  </tspan>'
        f'      <tspan fill="#38bdf8">STACKS:</tspan> <tspan fill="#e2e8f0">{len(languages)} OF {total_stacks_count}</tspan>\n'
        f'    </text>\n'
        f'  </g>\n'
        f'</g>'
    )
    svg_elements.append(header)

    # ── Connecting Cubic Bézier Curves ─────────────────────
    curve_elements = []
    dx = (PORT_X2 - PORT_X1) * 0.44

    curve_idx = 0
    for repo, langs in repo_lang_map.items():
        x2, y2 = repo_coords[repo]
        for lang in langs:
            if lang not in lang_coords:
                continue
            cx, y1 = lang_coords[lang]
            x1 = PORT_X1
            color = LANG_COLORS.get(lang, LANG_COLORS["Default"])
            cx1 = x1 + dx
            cx2 = x2 - dx
            path_d = f"M {x1} {y1} C {cx1} {y1}, {cx2} {y2}, {x2} {y2}"
            delay = (curve_idx * 0.35) % 3.0

            # Layer 1: Soft diffuse glow
            curve_elements.append(
                f'<path d="{path_d}" fill="none" stroke="{color}" '
                f'stroke-opacity="0.16" stroke-width="4.5" stroke-linecap="round" />'
            )
            # Layer 2: Core fiber line
            curve_elements.append(
                f'<path d="{path_d}" fill="none" stroke="{color}" '
                f'stroke-opacity="0.75" stroke-width="1.7" stroke-linecap="round" class="fiber" />'
            )
            # Layer 3: Signal packet ping
            curve_elements.append(
                f'<path d="{path_d}" fill="none" stroke="#ffffff" '
                f'stroke-opacity="0.85" stroke-width="2" stroke-linecap="round" class="pulse-line" '
                f'style="animation-delay: {delay:.2f}s;" />'
            )
            curve_idx += 1

    svg_elements.append("".join(curve_elements))

    # ── Language Nodes (Left Column) ──────────────────────────────────
    for lang, (cx, cy) in lang_coords.items():
        color = LANG_COLORS.get(lang, LANG_COLORS["Default"])
        escaped_lang = html.escape(lang)

        # Label pill on the left of badge
        pill_w = max(55, len(lang) * 7.5 + 18)
        pill_x = cx - 36 - pill_w
        pill_y = cy - 11

        node_svg = [
            f'<g class="node-lang">',
            # Name Pill
            f'<rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="22" rx="11" '
            f'fill="#0a101d" stroke="{color}" stroke-opacity="0.4" stroke-width="1" />',
            f'<text x="{pill_x + pill_w / 2}" y="{cy + 4}" fill="{color}" '
            f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" '
            f'font-size="11" font-weight="600" text-anchor="middle">{escaped_lang}</text>',

            # Outer diffuse aura
            f'<circle cx="{cx}" cy="{cy}" r="35" fill="{color}" fill-opacity="0.04" stroke="{color}" stroke-opacity="0.12" stroke-width="1" />',
            # Glowing concentric ring
            f'<circle cx="{cx}" cy="{cy}" r="28" fill="{color}" fill-opacity="0.08" stroke="{color}" stroke-opacity="0.4" stroke-width="1.6" />',
            # Base dark badge circle
            f'<circle cx="{cx}" cy="{cy}" r="{BADGE_R}" fill="#080e1a" stroke="{color}" stroke-width="2" />',

            # Embedded Vector Icon
            render_lang_icon(lang, color, cx, cy),

            # Right port anchor dot
            f'<circle cx="{PORT_X1}" cy="{cy}" r="5" fill="none" stroke="{color}" stroke-opacity="0.5" stroke-width="1" />',
            f'<circle cx="{PORT_X1}" cy="{cy}" r="2.5" fill="{color}" />',
            f'</g>'
        ]
        svg_elements.append("".join(node_svg))

    # ── Repository Nodes (Right Column) ───────────────────────────────
    octocat_path = (
        "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38"
        " 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13"
        "-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66"
        ".07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15"
        "-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27"
        ".68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12"
        ".51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48"
        " 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"
    )

    for idx, (repo, (x, y)) in enumerate(repo_coords.items()):
        box_x = CARD_X
        box_y = y - CARD_H / 2
        display_name = repo if len(repo) <= 20 else repo[:18] + ".."
        escaped_name = html.escape(display_name)

        # Build bottom language progress bar
        breakdown = repo_breakdowns.get(repo, [])
        bar_h = 4
        bar_y = box_y + CARD_H - bar_h
        bar_rects = []
        curr_x = box_x

        for item in breakdown:
            seg_w = (item["pct"] / 100.0) * CARD_W
            bar_rects.append(
                f'<rect x="{curr_x:.2f}" y="{bar_y}" width="{seg_w:.2f}" height="{bar_h}" fill="{item["color"]}" />'
            )
            curr_x += seg_w

        repo_url = f"https://github.com/{username}/{repo}"
        repo_svg = [
            f'<a href="{repo_url}" xlink:href="{repo_url}" target="_blank" rel="noopener noreferrer" class="repo-link">',
            f'<g class="node-repo">',
            # Left port anchor dot
            f'<circle cx="{PORT_X2}" cy="{y}" r="5" fill="none" stroke="#38bdf8" stroke-opacity="0.5" stroke-width="1" />',
            f'<circle cx="{PORT_X2}" cy="{y}" r="2.5" fill="#38bdf8" />',

            # Glassmorphic Card
            f'<rect x="{box_x}" y="{box_y}" width="{CARD_W}" height="{CARD_H}" rx="8" '
            f'fill="#0c1424" stroke="#1c2d4a" stroke-width="1.4" class="card-bg" />',

            # Octocat Icon
            f'<g transform="translate({box_x + 12}, {y - 10}) scale(0.95)">'
            f'<path fill="#708da9" d="{octocat_path}"/>'
            f'</g>',

            # Repo Name Text
            f'<text x="{box_x + 36}" y="{y - 1}" fill="#cbd5e1" '
            f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" '
            f'font-size="12" font-weight="600">{escaped_name}</text>',

            # Bottom Language Breakdown Progress Bar
            f'<g clip-path="url(#clip-card-{idx})">',
            f'<rect x="{box_x}" y="{bar_y}" width="{CARD_W}" height="{bar_h}" fill="#162338" />',
            "".join(bar_rects),
            f'</g>',

            f'</g>',
            f'</a>'
        ]
        svg_elements.append("".join(repo_svg))

    full_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="100%">\n'
        f'<style>\n'
        f'  @keyframes pulse {{\n'
        f'    0% {{ stroke-dashoffset: 0; opacity: 0; }}\n'
        f'    4% {{ opacity: 1; }}\n'
        f'    48% {{ opacity: 1; }}\n'
        f'    55% {{ stroke-dashoffset: -650; opacity: 0; }}\n'
        f'    100% {{ stroke-dashoffset: -650; opacity: 0; }}\n'
        f'  }}\n'
        f'  .pulse-line {{\n'
        f'    stroke-dasharray: 20 800;\n'
        f'    animation: pulse 6s ease-in-out infinite;\n'
        f'  }}\n'
        f'  .repo-link {{ text-decoration: none; cursor: pointer; }}\n'
        f'  .card-bg {{ transition: stroke 0.25s ease, stroke-width 0.25s ease; }}\n'
        f'  .repo-link:hover .card-bg {{ stroke: #38bdf8; stroke-width: 1.8; }}\n'
        f'  .repo-link:hover text {{ fill: #ffffff; }}\n'
        f'  .node-lang:hover circle {{ stroke-opacity: 0.9; }}\n'
        f'</style>\n'
        f'{"".join(svg_elements)}\n'
        f'</svg>'
    )

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(full_svg)

    print(f"Graph generated successfully → {OUTPUT_SVG}")


if __name__ == "__main__":
    run()
