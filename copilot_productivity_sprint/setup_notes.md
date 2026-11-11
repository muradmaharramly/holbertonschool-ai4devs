# Environment Setup Notes

## Purpose

This document records the environment, IDE, AI assistant, runtime versions, and configuration steps used to run a controlled coding productivity sprint comparing manual development against GitHub Copilot-assisted development.

## System and Toolchain Versions

All versions below were verified directly on the host machine prior to starting the sprint tasks.

| Category | Tool | Verified Version / Identifier | Notes |
| :--- | :--- | :--- | :--- |
| Operating System | Microsoft Windows | `Microsoft Windows NT 10.0.26300.0` (x64) | Windows 11 host |
| Primary IDE | Visual Studio Code | `1.145.2` (`c4453f8ea430795f941c1b2ff6c9321135a74a02`, x64) | Primary benchmark IDE |
| AI Assistant (VS Code) | GitHub Copilot (`copilot-chat`) | `0.73.0` (`completionsCoreVersion`: `1.378.1799`) | Bundled built-in extension in VS Code `1.145.2` |
| Secondary IDE | Cursor | `2.5.26` (`7d96c2a03bb088ad367615e9da1a3fe20fbbc6a0`, x64) | Installed on host; not used as primary baseline IDE |
| Version Control | Git | `2.44.1.windows.1` | Remote repository hosted on GitHub |
| Python Runtime | Python / pip | `3.12.2` / `pip 24.0` | System Python (`AppData\Local\Programs\Python\Python312`) |
| JavaScript Runtime | Node.js / npm | `v24.12.0` / `10.9.2` | Includes built-in `node:test` runner |

## IDE and GitHub Copilot Setup

### 1. Visual Studio Code and Built-in Copilot

In VS Code `1.145.2`, GitHub Copilot is shipped as a built-in extension (`github.copilot-chat` v`0.73.0` with inline completions core `1.378.1799`) under `resources/app/extensions/copilot`, removing the need for a separate legacy `GitHub.copilot` marketplace install.

Setup and authentication steps:
1. Launch VS Code (`1.145.2`) and open the Accounts menu in the Activity Bar.
2. Sign in with the GitHub account that holds an active GitHub Copilot entitlement and authorize VS Code OAuth access.
3. Confirm the Copilot status icon in the bottom-right status bar reports an active connection with no sign-in or quota errors.
4. Open the Chat view (`Ctrl+Alt+I`) and verify inline ghost-text completions respond in a scratch file before beginning the AI-assisted phase.

### 2. Baseline VS Code User Configuration

The active user configuration at `%APPDATA%\Code\User\settings.json` includes:
- `"files.autoSave": "afterDelay"`
- `"git.autofetch": true`
- `"git.enableSmartCommit": true`
- `"git.confirmSync": false`
- `"git.openRepositoryInParentFolders": "always"`
- Language formatters configured for HTML (`vscode.html-language-features`), CSS (`esbenp.prettier-vscode`), and JavaScript (`vscode.typescript-language-features`).

### 3. Controlled Sprint Isolation (Manual vs. AI-Assisted)

To keep measurements between the manual baseline and the AI-assisted run valid, all AI completions and chat features must be explicitly disabled during the manual phase and re-enabled for the AI-assisted phase.

**Manual (No-AI) Phase — workspace `.vscode/settings.json`:**

```json
{
  "github.copilot.enable": {
    "*": false
  },
  "github.copilot.nextEditSuggestions.enabled": false,
  "github.copilot.editor.enableCodeActions": false,
  "github.copilot.completions.chat.enabled": false
}
```

In addition, third-party AI extensions installed in the user profile (`yongnianliu.vscode-chatgpt-private@3.9.8`) must be disabled for the workspace (`Extensions` -> `Disable (Workspace)`) before starting the manual timer. Standard non-AI editor diagnostics (`usernamehw.errorlens`) and syntax tooling remain consistent across both phases.

**AI-Assisted Phase — workspace `.vscode/settings.json`:**

```json
{
  "github.copilot.enable": {
    "*": true
  },
  "github.copilot.nextEditSuggestions.enabled": true,
  "github.copilot.editor.enableCodeActions": true,
  "github.copilot.completions.chat.enabled": true
}
```

## Installed VS Code Extensions

The following extensions were verified via `code --list-extensions --show-versions`:

| Category | Extension ID | Version | Role in Environment |
| :--- | :--- | :--- | :--- |
| AI / Chat | `copilot-chat` (built-in) | `0.73.0` | GitHub Copilot inline completions and chat |
| AI / Chat | `yongnianliu.vscode-chatgpt-private` | `3.9.8` | Third-party chat extension (disabled during sprint runs) |
| Formatting & Diagnostics | `esbenp.prettier-vscode` | `12.4.0` | Code formatting |
| Formatting & Diagnostics | `usernamehw.errorlens` | `3.30.0` | Inline diagnostic and lint highlighting |
| Formatting & Diagnostics | `aaron-bond.better-comments` | `3.2.0` | Comment categorization |
| Git & Execution | `donjayamanne.githistory` | `0.6.20` | Git commit and file history inspection |
| Git & Execution | `formulahendry.code-runner` | `0.12.2` | Single-file execution helper |
| Language & Web Support | `ms-dotnettools.csharp` | `11.7.18` | C# language support |
| Language & Web Support | `ms-dotnettools.csdevkit` | `11.9.39` | C# project tooling |
| Language & Web Support | `ms-dotnettools.vscode-dotnet-runtime` | `3.2.0` | .NET runtime resolver |
| Language & Web Support | `dsznajder.es7-react-js-snippets` | `4.4.3` | React/JS snippets |
| Language & Web Support | `xabikos.javascriptsnippets` | `1.8.0` | ES6 JavaScript snippets |
| Language & Web Support | `mgmcdermott.vscode-language-babel` | `0.0.40` | JSX/Babel syntax highlighting |
| Language & Web Support | `ritwickdey.liveserver` | `5.7.10` | Local static preview server |
| Language & Web Support | `formulahendry.auto-rename-tag` | `0.1.10` | Paired HTML/XML tag renaming |
| Language & Web Support | `sporiley.css-auto-prefix` | `0.3.0` | CSS vendor prefixing |
| Language & Web Support | `ysemeniuk.emmet-live` | `1.0.0` | Live Emmet expansion |
| Editor & UI | `pkief.material-icon-theme` | `5.40.0` | File icon theme |
| Editor & UI | `johnpapa.winteriscoming` | `1.5.0` | Color theme |
| Editor & UI | `whizkydee.material-palenight-theme` | `2.0.5` | Color theme |
| Other | `abusaidm.html-snippets` | `0.2.1` | HTML snippets |
| Other | `bracketpaircolordlw.bracket-pair-color-dlw` | `0.0.6` | Bracket colorization |
| Other | `jakewilson.vscode-picture` | `1.0.0` | Image preview helper |
| Other | `l7ssha.tag-inserter` | `1.4.0` | Tag insertion helper |
| Other | `lolkush.quickstart` | `0.1.0` | Quick template helper |
| Other | `robertz.code-snapshot` | `0.2.1` | Code screenshot export |
| Other | `sidthesloth.html5-boilerplate` | `1.1.1` | HTML5 starter template |
| Other | `taodongwu.ejs-snippets` | `0.1.0` | EJS snippets |
| Other | `walkme.html5-extension-pack` | `1.0.0` | HTML5 extension pack |
| Other | `whtouche.vscode-js-console-utils` | `0.7.0` | Console log shortcut |

## Testing, Coverage, and Time-Tracking Preparation

### Test Frameworks

Verification on the host showed neither `pytest` (`python -m pytest --version` returned `No module named pytest`) nor `jest` is installed globally.

To avoid polluting the global interpreter when running Python or JavaScript sprint benchmarks:
- **Python tasks**: create an isolated virtual environment per project and install `pytest` and `pytest-cov`:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install pytest pytest-cov
  ```
- **JavaScript tasks**: use Node.js `v24.12.0` built-in test runner (`node --test --experimental-test-coverage`) or install `jest` locally (`npm install -D jest`) inside the task directory.

### Time Tracking

Active development time, test-fixing time, and prompt iteration time will be logged per task using a stopwatch alongside recorded start/end UTC+4 timestamps. If automated IDE telemetry is needed in subsequent tasks, `WakaTime.vscode-wakatime` can be installed via `code --install-extension WakaTime.vscode-wakatime` and linked to a WakaTime API key.

## Verification Commands

Executed commands and observed outcomes on `2026-11-11`:

```powershell
git --version                              # git version 2.44.1.windows.1
python --version                           # Python 3.12.2
node --version                             # v24.12.0
npm --version                              # 10.9.2
code --version                             # 1.145.2 (c4453f8ea430795f941c1b2ff6c9321135a74a02, x64)
code --list-extensions --show-versions     # Listed 29 user extensions; built-in copilot-chat 0.73.0 verified
cursor --version                           # 2.5.26 (7d96c2a03bb088ad367615e9da1a3fe20fbbc6a0, x64)
```
