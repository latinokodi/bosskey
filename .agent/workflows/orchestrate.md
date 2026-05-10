---
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
---

# Multi-Agent Orchestration

You are now in **ORCHESTRATION MODE**. Your task: coordinate specialized agents to solve this complex problem using `intelligent-routing` and `parallel-agents`.

## Task to Orchestrate
$ARGUMENTS

---

## 🔴 CRITICAL: Minimum Agent Requirement

> ⚠️ **ORCHESTRATION = MINIMUM 3 DIFFERENT AGENTS**
> 
> If you use fewer than 3 agents, you are NOT orchestrating - you're just delegating.
> 
> **Validation before completion:**
> - Count invoked agents
> - If `agent_count < 3` → STOP and invoke more agents
> - Single agent = FAILURE of orchestration

### Agent Selection Matrix

| Task Type | REQUIRED Agents (minimum) |
|-----------|---------------------------|
| **Kodi Addon** | kodi-expert, site-to-kodi, media-engineer, test-engineer |
| **Web App** | frontend-specialist, backend-specialist, test-engineer |
| **API** | backend-specialist, security-auditor, test-engineer |
| **UX/Design** | ui-ux-pro-max, performance-optimizer, seo-specialist |
| **Security** | security-auditor, penetration-tester, devops-engineer |
| **Scraping/Bots** | playwright-actor-engineer, api-reverse-engineer, test-engineer |
| **CLI Tools** | python-cli-architect, devops-engineer, test-engineer |

---

## 🛡️ Intelligent Routing

Use the `intelligent-routing` skill to automatically select the best specialists based on the task domains.

---

## 🔴 STRICT 2-PHASE ORCHESTRATION

### PHASE 1: PLANNING (Sequential)

| Step | Agent | Action |
|------|-------|--------|
| 1 | `project-planner` | Create `implementation_plan.md` |
| 2 | `architect` | Trade-off analysis & tech stack selection |

### PHASE 2: IMPLEMENTATION (Parallel via `parallel-agents`)

| Parallel Group | Agents |
|----------------|--------|
| Logic & Media | `kodi-expert`, `site-to-kodi`, `media-engineer` |
| Security & DB | `security-auditor`, `database-architect` |
| UI & Polish | `ui-ux-pro-max`, `frontend-specialist`, `documentation-writer` |

---

## Specialized Agents Reference

| Agent | Domain | Specialization |
|-------|--------|----------------|
| `kodi-expert` | Kodi 21+ | WindowXML, Kodi API, Addon structure |
| `site-to-kodi` | Extraction | Streaming site conversion, deep iframe extraction |
| `media-engineer` | Media | FFmpeg, HLS, Video resolution |
| `ui-ux-pro-max` | Premium UI | 50+ styles, Design systems |
| `security-auditor` | Security | Vulnerability-scanner, OWASP |
| `api-reverse-engineer` | API | Deep payload analysis, obfuscation bypass |
| `python-cli-architect` | CLI | Async, cyber-neon aesthetics, robust Python |
| `playwright-actor-engineer` | Browser | Puppeteer bots, Apify container stealth |

---

## Verification (MANDATORY)

The Orchestrator must ensure all work is verified using master scripts:
```bash
python .agent/scripts/checklist.py .
```

---

## Output Format

```markdown
## 🎼 Orchestration Report

### 1. Task Summary
[Original task synthesis]

### 2. Specialist Coordination
| Agent | Role | Status |
|-------|------|--------|
| [Name] | [Focus] | ✅ |

### 3. Verification Score
- **Quality Score:** [0-100] (from checklist.py)
- **Security Check:** ✅ Zero High-Risk Findings

### 4. Key Artifacts
- [Implementation Plan](path)
- [Walkthrough](path)
```

---

## 🔴 EXIT GATE

1. ✅ **Agent Count:** `invoked_agents >= 3`
2. ✅ **Master Script:** `checklist.py` returns success
3. ✅ **Documentation:** Both Plan and Walkthrough completed
