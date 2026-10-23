# GitHub Tech Tree

A zero-dependency Python tool that generates a **dark-mode SVG dependency graph** showing how your GitHub repositories connect to programming languages.

![Tech Dependency Graph](tech-tree.svg)

## Quick Start

### 1. Configure

Edit [`config.json`](config.json) and set your GitHub username:

```json
{
  "github_username": "your-actual-username",
  "min_language_percent": 4.0,
  "max_repos": 6,
  "ignore_languages": ["HTML", "CSS", "Shell", "Batchfile", "Jupyter Notebook"],
  "pinned_repos": [],
  "exclude_repos": []
}
```

| Key                    | Description                                                        |
| ---------------------- | ------------------------------------------------------------------ |
| `github_username`      | Your GitHub handle (required)                                      |
| `min_language_percent` | Minimum % of bytes a language must occupy to appear (default `4`)  |
| `max_repos`            | Maximum number of repos to include (default `6`)                   |
| `ignore_languages`     | Languages to always skip (boilerplate like HTML/CSS)               |
| `pinned_repos`         | If non-empty, **only** these repos are considered                  |
| `exclude_repos`        | Repos to explicitly exclude                                        |

### 2. Run Locally

```bash
python generate_tree.py
```

This creates `tech-tree.svg` in the project root.

> **Tip:** Set the `GH_TOKEN` environment variable to avoid rate limits:
> ```bash
> export GH_TOKEN=ghp_xxxxxxxxxxxx
> python generate_tree.py
> ```

### 3. Automate via GitHub Actions

Push this repo to GitHub. The included workflow ([`.github/workflows/generate.yml`](.github/workflows/generate.yml)) will:
- Run **every Sunday at midnight UTC**
- Run on **any push** that modifies `config.json` or `generate_tree.py`
- Run on **manual trigger** from the Actions tab
- Auto-commit the updated `tech-tree.svg`

### 4. Embed in Your Profile README

```markdown
<p align="center">
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/gh-readme-gen/main/tech-tree.svg" alt="Tech Dependency Graph" />
</p>
```

Replace `YOUR_USERNAME` with your GitHub handle.

## How It Works

1. Fetches your public repositories via the GitHub API
2. Retrieves language byte breakdowns for each repo
3. Filters out forks, excluded repos, and low-percentage boilerplate languages
4. Builds a bipartite graph: **Languages** (left) ↔ **Repositories** (right)
5. Renders a standalone SVG with cubic Bézier curves and GitHub's dark-mode palette

## Requirements

**None.** Uses only the Python standard library (`urllib.request`, `json`, `os`, `math`).

## License

MIT
