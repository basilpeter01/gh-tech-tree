# GitHub Tech Tree

A zero-dependency Python tool that generates a **dark-mode SVG dependency graph** showing how your GitHub repositories connect to programming languages via smooth cubic Bézier curves. Designed to be embedded directly into your GitHub Profile README.

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
  "github_username": "GITHUB_USERNAME",
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
| `github_username` | `string` | `"GITHUB_USERNAME"` | GitHub handle whose public repos will be visualized. |
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

---

### 3. Automate with GitHub Actions

The repository includes an automated workflow at [`.github/workflows/generate.yml`](.github/workflows/generate.yml) that:
- Runs automatically **every Sunday at midnight UTC**.
- Runs whenever you push changes to `config.json` or `generate_tree.py`.
- Can be triggered manually via the **Actions** tab (**Run workflow** button).
- Uses the built-in `GITHUB_TOKEN` secret (automatic 5,000 requests/hr rate limit).
- Commits and pushes the freshly generated `tech-tree.svg` back to your branch automatically.

#### Important: Enable Workflow Write Permissions
For GitHub Actions to push the updated SVG back to your repository:
1. Go to your repository on GitHub.
2. Navigate to **Settings** → **Actions** → **General**.
3. Under **Workflow permissions**, select **"Read and write permissions"**.
4. Click **Save**.

---

### 4. Embed in Your Profile README

Add the snippet below to your profile `README.md` (or any repository README):

```markdown
<p align="center">
  <img src="https://raw.githubusercontent.com/GITHUB_USERNAME/gh-tech-tree/main/tech-tree.svg" alt="Tech Dependency Graph" />
</p>
```

> Replace `GITHUB_USERNAME` with your GitHub username.

---

## How It Works

1. **Repository Fetching**: Queries the GitHub REST API (`/users/{username}/repos`) and filters out forks and excluded repositories.
2. **Language Extraction**: Queries `/repos/{username}/{repo}/languages` for exact byte breakdowns. Calculates percentage share and drops any languages below `min_language_percent` or in `ignore_languages`.
3. **Graph Geometry**:
   - Languages sorted alphabetically and placed on the left column.
   - Repositories placed on the right column.
   - Smooth cubic Bézier curves calculated: `M (x1, y1) C (x1+140, y1), (x2-140, y2), (x2, y2)`.
4. **SVG Generation**: Compiles into a standalone SVG with embedded styling, rounded card nodes, and XML-safe text escaping.

---

## License

This project is open source and available under the [MIT License](LICENSE).
