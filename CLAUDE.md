# CLAUDE.md — Repository Guide for AI Assistants

## Repository Overview

**`jt09990/jt09990`** is a GitHub profile README repository. When a repository shares its name with its owner, GitHub automatically renders the `README.md` from the default branch on the owner's public profile page. This repository's primary artifact is therefore `README.md`.

**Current state:** Freshly initialised — no prior commits exist.

---

## Repository Structure

```
jt09990/
├── CLAUDE.md        # This file — AI assistant guide
└── README.md        # GitHub profile page content (primary artifact)
```

Additional assets (images, badges, workflow files) may be added over time under conventional paths:
- `.github/workflows/` — GitHub Actions
- `assets/` or `images/` — Static media referenced by the README

---

## Development Workflow

### Branching Convention

- **Default branch:** `main`
- **Feature branches:** `claude/<short-description>-<id>` (e.g. `claude/add-claude-documentation-ebIhW`)
- Always develop on the designated feature branch; never push directly to `main` without an explicit pull request.

### Making Changes

1. Work on the current feature branch.
2. Commit with clear, descriptive messages that explain *why*, not just *what*.
3. Push with tracking: `git push -u origin <branch-name>`
4. Open a pull request only when explicitly requested.

### Git Push Retry Policy

If a push fails due to a network error, retry up to 4 times with exponential backoff: 2 s → 4 s → 8 s → 16 s.

---

## Key Conventions for AI Assistants

### General

- **No unsolicited pull requests.** Commit and push to the feature branch; wait for explicit instruction before opening a PR.
- **No force-pushes** to `main` or `master` under any circumstances.
- **No `--no-verify`** or hook-bypass flags unless the user explicitly requests it.
- Always create **new commits** rather than amending, unless the user explicitly asks for an amend.

### Code & Content Style

- Default to **no comments** in code unless the *why* is non-obvious.
- No multi-paragraph docstrings or comment blocks — one short line maximum.
- Do not add features, refactors, or abstractions beyond what the task requires.
- Match the scope of changes strictly to what was requested.

### Commit Messages

- Concise (1–2 sentences), present-tense imperative style.
- Focus on the *why* (motivation, intent) rather than the *what* (mechanical change).
- Append the Claude session URL as a trailer:
  ```
  https://claude.ai/code/session_<id>
  ```

### Destructive Actions

Always confirm with the user before:
- Deleting files or branches
- Force-pushing
- `git reset --hard` or `git checkout .`
- Any action that affects shared state (pushing, commenting on issues/PRs, external API calls)

---

## README Guidelines

Because `README.md` renders on a public GitHub profile:

- Keep content professional and concise.
- Prefer relative links and GitHub-hosted images over external CDNs where possible.
- Test badge/shield URLs before committing to avoid broken images.
- GitHub flavoured Markdown (GFM) is the rendering target — avoid non-GFM extensions.

---

## No Existing Codebase

This repository contains no application code, tests, build system, or dependencies at the time of writing. If any of these are added, update this file to document:

- **Build / install commands**
- **Test commands and how to run them**
- **Linting / formatting tools and configuration**
- **Environment variables and secrets management**
- **CI/CD pipeline structure**
