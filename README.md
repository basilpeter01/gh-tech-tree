# GitHub Tech Tree

A zero-dependency Python tool that generates a **dark-mode SVG dependency graph** showing how your GitHub repositories connect to programming languages via smooth cubic Bézier curves. Designed to be embedded directly into your GitHub Profile README.

<p align="center">
  <img src="tech-tree.svg" alt="Tech Dependency Graph" width="100%" />
</p>

---

## Features

- **Zero External Dependencies**: Pure Python standard library (`urllib.request`, `json`, `os`, `sys`, `math`, `html`). No `pip install` required.
- **Bipartite Graph Layout**: Deterministic geometry with languages on the left, repositories on the right, connected by Bézier curves.
- **Official GitHub Colors**: Automatically maps 35+ languages to their official GitHub color scheme.
- **Noise Filtering**: Ignores boilerplate languages (HTML, CSS, Jupyter Notebooks) and filters out low-percentage languages per repo.
- **Automated Updates**: Pre-configured GitHub Actions workflow that updates your graph weekly on a schedule or on manual trigger.
- **Dark Mode Native**: Styled to match GitHub's dark theme with interactive hover highlights.

---

## Repository Structure

```
gh-tech-tree/
├── .github/
│   └── workflows/
│       └── generate.yml      # Automated GitHub Action workflow
├── config.json               # Active user configuration
├── config.example.json       # Template configuration
├── generate_tree.py          # Core generator engine
├── requirements.txt          # Requirements file (empty by design)
├── tech-tree.svg             # Generated output SVG
└── README.md
```

---

## Quick Start

### 1. Configure (`config.json`)

Edit [`config.json`](config.json) to set your GitHub username and filter preferences:

```json
{
  "github_username": "YOUR_GITHUB_USERNAME",
  "min_language_percent": 2.0,
  "max_repos": 10,
  "ignore_languages": [
    "HTML",
    "CSS",
    "Shell",
    "Batchfile",
    "Jupyter Notebook"
  ],
  "pinned_repos": [],
  "exclude_repos": []
}
```

#### Configuration Options

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `github_username` | `string` | `"YOUR_GITHUB_USERNAME"` | GitHub handle whose public repos will be visualized. |
| `min_language_percent` | `float` | `2.0` | Minimum % of total repo bytes a language must have to be shown. |
| `max_repos` | `int` | `10` | Maximum number of non-fork repositories to display (sorted by most recently pushed). |
| `ignore_languages` | `list` | `["HTML", "CSS", ...]` | Languages to ignore entirely (e.g. boilerplate or markup). |
| `pinned_repos` | `list` | `[]` | If non-empty, **only** these specific repository names are processed. |
| `exclude_repos` | `list` | `[]` | List of repository names to hide from the graph. |

---

### 2. Run Locally

Run the generator script with Python 3.8+:

```bash
python generate_tree.py
```

This generates `tech-tree.svg` in the root of the project.

#### Avoiding GitHub API Rate Limits Locally
GitHub limits unauthenticated requests to **60 requests/hour** per IP. If you run the script frequently on your machine, provide a GitHub Personal Access Token (increases quota to **5,000 requests/hour**):

1. Generate a token at [GitHub Settings → Developer Settings → Personal Access Tokens (Classic)](https://github.com/settings/tokens). No special scopes are needed for reading public repositories.
2. Set the environment variable before running:

- **PowerShell (Windows)**:
  ```powershell
  $env:GH_TOKEN="ghp_your_token_here"
  python generate_tree.py
  ```

- **Command Prompt (CMD)**:
  ```cmd
  set GH_TOKEN=ghp_your_token_here
  python generate_tree.py
  ```

- **Linux / macOS (Bash/Zsh)**:
  ```bash
  export GH_TOKEN=ghp_your_token_here
  python generate_tree.py
  ```

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
