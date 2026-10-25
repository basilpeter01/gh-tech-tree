# GitHub Tech Tree

A zero-dependency Python tool that generates a **cybernetic dark-mode SVG dependency graph** showing how your GitHub repositories connect to programming languages via glowing cubic Bézier curves. Designed to be embedded directly into your GitHub Profile README.

---

## Features

- **Zero External Dependencies**: Pure Python standard library (`urllib.request`, `json`, `os`, `sys`, `math`, `html`). No `pip install` required.
- **Living Circuit Effect**: Ambient glowing data packets drift along the Bézier fiber curves with calm rest intervals, giving your profile an active, living feel.
- **Clickable Repository Cards**: Each repository card is wrapped in native SVG `<a>` links; clicking a card opens that GitHub repository directly.
- **Dynamic HUD Telemetry**: Real-time counter pill in the top-left showing the total count of active `STACKS` and `REPOS` with a live indicator light.
- **Proportional Language Progress Bars**: Each repository card features a segmented, color-coded bottom bar representing its exact language distribution.
- **Vector Language Badges**: Circular glowing nodes with embedded vector logos for Python, JavaScript, TypeScript, C, C++, C#, Java, Go, Rust, and more (with clean monogram fallbacks).
- **Intelligent Noise Filtering**: Excludes boilerplate languages (HTML, CSS, Jupyter Notebooks) and filters out low-percentage languages per repo.
- **Automated Updates**: Pre-configured GitHub Actions workflow that updates your graph weekly on a schedule or on manual trigger.

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
| `max_repos` | `int` | `10` | Maximum number of non-fork repositories to inspect (sorted by most recently pushed). |
| `ignore_languages` | `list` | `["HTML", "CSS", ...]` | Languages to ignore entirely (e.g. boilerplate or markup). |
| `pinned_repos` | `list` | `[]` | If non-empty, **only** these specific repository names are processed. |
| `exclude_repos` | `list` | `[]` | List of repository names to hide from the graph. |

---

### 2. Run Locally

Run the generator script with Python 3.8+:

```bash
python generate_tree.py
```

This outputs `tech-tree.svg` in the root of the project.

#### Avoiding GitHub API Rate Limits Locally for Testing (Optonal)
GitHub limits unauthenticated API requests to **60 requests/hour** per IP. If limit hits, provide a GitHub Personal Access Token (**5,000 requests/hour**):

1. Generate a token at [GitHub Settings → Developer Settings → Personal Access Tokens (Classic)](https://github.com/settings/tokens). (No special permissions/scopes are needed to read public repos.)
2. Set the environment variable in your terminal:

- **Windows (PowerShell)**:
  ```powershell
  $env:GH_TOKEN="ghp_your_token_here"
  python generate_tree.py
  ```

- **Linux / macOS (Bash)**:
  ```bash
  export GH_TOKEN=ghp_your_token_here
  python generate_tree.py
  ```

---

### 3. Automate with GitHub Actions

The repository includes an automated workflow at [`.github/workflows/generate.yml`](.github/workflows/generate.yml) that:
- Runs automatically **every Sunday at midnight UTC**.
- Runs on **any push** that modifies `config.json` or `generate_tree.py`.
- Can be triggered manually via the **Actions** tab.
- Commits and pushes the newly generated `tech-tree.svg` back to your repository automatically.

For GitHub Actions to push the updated SVG back to your repository:
1. Go to your repository on GitHub.
2. Navigate to **Settings** → **Actions** → **General**.
3. Under **Workflow permissions**, select **"Read and write permissions"**.
4. Check **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

---

### 4. Embed in Your Profile README

Add the snippet below to your profile `README.md` (or any repository README):

```markdown
<p align="center">
    <img src="https://raw.githubusercontent.com/GITHUB_USERNAME/gh-tech-tree/main/tech-tree.svg" alt="Tech tree svg" width="100%" />
</p>
```

---

## How It Works & Filtering Logic

1. **Repository Selection**:
   - Queries the GitHub API for your public non-forked repositories (sorted by most recently pushed).
   - Skips repos in `exclude_repos` and respects `pinned_repos` if provided.
   - Takes up to `max_repos` candidates.
2. **Language Extraction & Filtering**:
   - Queries `/repos/{username}/{repo}/languages` for exact byte breakdowns.
   - Ignores any language in `ignore_languages` (e.g. HTML, CSS, Jupyter Notebook).
   - A repository is **excluded** from the graph if:
     - It contains 0 code bytes (e.g. Markdown-only profile repos).
     - 100% of its files belong to `ignore_languages`.
     - None of its languages meet the `min_language_percent` threshold.
3. **Graph Geometry**:
   - Unique active languages are placed on the left column in circular glowing badges.
   - Repositories are placed on the right column in glassmorphic cards.
   - Both columns are **vertically centered relative to each other**.
   - Triple-layer cubic Bézier curves (`M x1 y1 C cx1 y1, cx2 y2, x2 y2`) connect languages to repositories with glowing halos and animated pulse capsules.

---

## License

This project is open source and available under the [MIT License](LICENSE).
