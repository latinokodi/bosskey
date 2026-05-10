# lku toolkit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit

---

## 📋 Overview

lku toolkit is a modular system consisting of:

- **27 Specialist Agents** - Role-based AI personas
- **66 Skills** - Domain-specific knowledge modules
- **11 Workflows** - Slash command procedures

---

## 🏗️ Directory Structure

```plaintext
.agent/
├── ARCHITECTURE.md          # This file
├── agents/                  # 27 Specialist Agents
├── skills/                  # 66 Skills
├── workflows/               # 11 Slash Commands
├── rules/                   # Global Rules
└── scripts/                 # Master Validation Scripts
```

---

## 🤖 Agents (27)

Specialist AI personas for different domains.

| Agent                    | Focus                      | Skills Used                                              |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| `orchestrator`           | Multi-agent coordination   | parallel-agents, behavioral-modes                        |
| `project-planner`        | Discovery, task planning   | brainstorming, plan-writing, architecture                |
| `frontend-specialist`    | Web UI/UX                  | frontend-design, react-best-practices, tailwind-patterns |
| `backend-specialist`     | API, business logic        | api-patterns, nodejs-best-practices, database-design     |
| `database-architect`     | Schema, SQL                | database-design, prisma-expert                           |
| `mobile-developer`       | iOS, Android, RN           | mobile-design                                            |
| `game-developer`         | Game logic, mechanics      | game-development                                         |
| `devops-engineer`        | CI/CD, Docker              | deployment-procedures, docker-expert                     |
| `security-auditor`       | Security compliance        | vulnerability-scanner, red-team-tactics                  |
| `penetration-tester`     | Offensive security         | red-team-tactics                                         |
| `test-engineer`          | Testing strategies         | testing-patterns, tdd-workflow, webapp-testing           |
| `debugger`               | Root cause analysis        | systematic-debugging                                     |
| `performance-optimizer`  | Speed, Web Vitals          | performance-profiling                                    |
| `seo-specialist`         | Ranking, visibility        | seo-fundamentals, geo-fundamentals                       |
| `documentation-writer`   | Manuals, docs              | documentation-templates                                  |
| `product-manager`        | Requirements, user stories | plan-writing, brainstorming                              |
| `product-owner`          | Strategy, backlog, MVP     | plan-writing, brainstorming                              |
| `qa-automation-engineer` | E2E testing, CI pipelines  | webapp-testing, testing-patterns                         |
| `code-archaeologist`     | Legacy code, refactoring   | clean-code, code-review-checklist                        |
| `explorer-agent`         | Codebase analysis          | -                                                        |
| `kodi-expert`            | Kodi 21 Omega+, WindowXML  | kodi-addon-expert, python-patterns, i18n                 |
| `site-to-kodi`           | Streaming site to Kodi addon | site-to-kodi-addon, web-scraper, protocol-reverse-engineering |
| `media-engineer`         | FFmpeg, deduplication      | python-patterns, performance-profiling                   |
| `ui-ux-pro-max`          | Premium UI/UX design       | ui-ux-pro-max, frontend-design, tailwind-patterns        |
| `api-reverse-engineer`   | API Payload Analysis       | protocol-reverse-engineering, reverse-engineer           |
| `python-cli-architect`   | Premium Python CLI tools   | python-pro, async-python-patterns, bash-pro              |
| `playwright-actor-engineer` | Automation & Browser bots | playwright-skill, apify-ultimate-scraper, web-scraper |

---

## 🧩 Skills (66)

Modular knowledge domains that agents can load on-demand based on task context.

### Python & Scripting

| Skill                            | Description                                          |
| -------------------------------- | ---------------------------------------------------- |
| `python-pro`                     | Advanced Python paradigms, structure, and PEP8       |
| `async-python-patterns`          | High-concurrency asyncio and threading patterns      |
| `python-performance-optimization`| Profiling and speed tuning for heavy data tasks      |
| `python-testing-patterns`        | Pytest, Mocking, and coverage for Python             |
| `python-patterns`                | Base Python standards and FastAPI structures         |
| `bash-pro`                       | Advanced shell automation and terminal aesthetics    |
| `fastapi-pro`                    | High-performance async API development               |

### Web Scraping & Reverse Engineering

| Skill                         | Description                                            |
| ----------------------------- | ------------------------------------------------------ |
| `playwright-skill`            | Modern browser automation with Playwright              |
| `web-scraper`                 | General scraping logic and anti-detection              |
| `apify-ultimate-scraper`      | Scalable serverless browser actors                     |
| `protocol-reverse-engineering`| Deciphering undocumented network calls and encryption  |
| `reverse-engineer`            | Binary and application logic deconstruction            |
| `seek-and-analyze-video`      | Targeted HLS/M3U8 analysis and extraction              |

### Architecture & Engineering

| Skill                    | Description                                         |
| ------------------------ | --------------------------------------------------- |
| `architecture-patterns`  | Clean, Hexagonal, and Domain-Driven Design          |
| `api-design-principles`  | REST, GraphQL, and SDK architecture                 |
| `error-handling-patterns`| Robust fail-safe and logging strategies             |
| `debugging-strategies`   | Systematic root-cause isolation                     |
| `git-advanced-workflows` | Rebase-heavy, multi-branch, and submodule flows     |
| `clean-code`             | Coding standards and maintainability (Global)        |

### Frontend & UI

| Skill                   | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `frontend-ui-dark-ts`   | Premium Cyber-Neon / Dark Mode TypeScript components                  |
| `ui-ux-designer`        | Information architecture and user flow journey design                 |
| `react-best-practices`  | React & Next.js performance optimization (Vercel - 45 rules)          |
| `nextjs-react-expert`   | React & Next.js performance optimization (Vercel - 57 rules)          |
| `web-design-guidelines` | Web UI audit - 100+ rules for accessibility, UX, performance (Vercel) |
| `tailwind-patterns`     | Tailwind CSS v4 utilities                                             |
| `frontend-design`       | UI/UX patterns, design systems                                        |
| `ui-ux-pro-max`         | Premium editorial design: 50 styles, 21 palettes, 50 fonts            |
| `app-optimizer`         | Comprehensive app audit and performance/UI optimization               |

### Backend & Database

| Skill                   | Description                    |
| ----------------------- | ------------------------------ |
| `api-patterns`          | REST, GraphQL, tRPC            |
| `nestjs-expert`         | NestJS modules, DI, decorators |
| `nodejs-best-practices` | Node.js async, modules         |
| `database-design`       | Schema design, optimization    |
| `prisma-expert`         | Prisma ORM, migrations         |

### Testing & Quality

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `testing-patterns`      | Jest, Vitest, strategies |
| `webapp-testing`        | E2E, Playwright          |
| `tdd-workflow`          | Test-driven development  |
| `code-review-checklist` | Code review standards    |
| `lint-and-validate`     | Linting, validation      |

### Security

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `vulnerability-scanner` | Security auditing, OWASP |
| `red-team-tactics`      | Offensive security       |

### Mobile & Game Dev

| Skill           | Description           |
| --------------- | --------------------- |
| `mobile-design` | Mobile UI/UX patterns |
| `game-development`| Game logic, mechanics |

### Other Key Skills

| Skill                 | Description                                    |
| --------------------- | ---------------------------------------------- |
| `kodi-addon-expert`   | Kodi addon development (Python 3, Omega v21+)  |
| `site-to-kodi-addon`  | Streaming site to Kodi addon (Blogger, DooPlay, deep iframe) |
| `mcp-builder`         | Model Context Protocol                         |
| `i18n-localization`   | Internationalization                           |
| `intelligent-routing` | Automatic agent selection and task routing     |
| `svg-icon-generator`  | Context-aware SVG icon generation utilities    |

---

## 🔄 Workflows (11)

Slash command procedures. Invoke with `/command`.

| Command          | Description              |
| ---------------- | ------------------------ |
| `/brainstorm`    | Socratic discovery       |
| `/create`        | Create new features      |
| `/debug`         | Debug issues             |
| `/deploy`        | Deploy application       |
| `/enhance`       | Improve existing code    |
| `/orchestrate`   | Multi-agent coordination |
| `/plan`          | Task breakdown           |
| `/preview`       | Preview changes          |
| `/status`        | Check project status     |
| `/test`          | Run tests                |
| `/ui-ux-pro-max` | Design with 50 styles    |

---

## 📊 Statistics

| Metric              | Value                         |
| ------------------- | ----------------------------- |
| **Total Agents**    | 27                            |
| **Total Skills**    | 67                            |
| **Total Workflows** | 11                            |
| **Total Scripts**   | 2 (master) + 24 (skill-level) |
| **Coverage**        | ~95% Python/Web development   |

---

## 🔗 Quick Reference

| Need              | Agent                     | Skills                                     |
| ----------------- | ------------------------- | ------------------------------------------ |
| Web App           | `frontend-specialist`     | react-best-practices, frontend-design      |
| API               | `backend-specialist`      | api-patterns, nodejs-best-practices        |
| **Undocumented API**| `api-reverse-engineer`    | protocol-reverse-engineering, reverse-engineer |
| **Scraping Bot**  | `playwright-actor-engineer`| playwright-skill, apify-ultimate-scraper   |
| **Python CLI**    | `python-cli-architect`    | python-pro, async-python-patterns          |
| **Kodi Addon**    | `site-to-kodi`            | site-to-kodi-addon, kodi-addon-expert      |
| Security          | `security-auditor`        | vulnerability-scanner                      |
| Testing           | `test-engineer`           | testing-patterns, webapp-testing           |
| Plan              | `project-planner`         | brainstorming, plan-writing                |

---

Updated at: 2026-04-13
