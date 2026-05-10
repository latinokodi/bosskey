---
description: Transform any streaming website (movies/TV/anime) into a functional Kodi video addon. Handles Blogger, PHP, WordPress/DooPlay with deep iframe extraction, de-duplication, and bundled Cryptodome. Use for creating plugin.video addons.
---

# Site to Kodi Workflow

You are in **SITE TO KODI MODE**. Your task: transform a streaming website into a fully functional Kodi video addon using the `site-to-kodi-addon` skill.

## Task to Execute
$ARGUMENTS

---

## 🔴 CRITICAL: 4-Phase Addon Creation Process

### PHASE 1: SITE ANALYSIS (Sequential)

| Step | Action | Output |
|------|--------|--------|
| 1 | Analyze site structure | `site_analysis.md` |
| 2 | Identify content types | Categories detected |
| 3 | Map navigation patterns | URL structure |
| 4 | Detect video sources | Embed domains (internal/external) |
| 5 | Test API/JSON feeds | Data extraction method |
| 6 | Check for encryption needs | Mega/Cryptodome requirement |

**Key Analysis Points:**
- Blogger-based? → Use JSON feed API (`/feeds/posts/default?alt=json`)
- WordPress/DooPlay? → Check URL patterns, admin-ajax.php
- Custom PHP? → POST endpoints for video loading
- Internal players? → Need deep iframe extraction
- Anti-bot measures? → Header requirements
- Encryption/Mega? → Bundle Cryptodome

### PHASE 2: ADDON SCAFFOLDING (Sequential)

| Step | Component | Template |
|------|-----------|----------|
| 1 | `addon.xml` | Manifest with dependencies |
| 2 | Entry point | `{addon_name}.py` |
| 3 | Router | `resources/lib/modules/router.py` |
| 4 | Navigation | `resources/lib/modules/navigation.py` |
| 5 | Kodi utils | `resources/lib/utils/kodi.py` |
| 6 | Base provider | `resources/lib/providers/base_provider.py` |
| 7 | Cryptodome (if needed) | `resources/lib/Cryptodome/` |

**Directory Structure:**
```
plugin.video.{name}/
├── addon.xml
├── {name}.py                    # Entry point
├── resources/
│   ├── img/
│   │   ├── icon.png
│   │   └── fanart.jpg
│   ├── lib/
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── kodi.py          # Kodi utilities
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   ├── router.py        # URL routing
│   │   │   ├── navigation.py    # Menu navigation
│   │   │   ├── settings.py      # Settings (optional)
│   │   │   └── packer.py        # JS unpacker
│   │   ├── Cryptodome/          # Bundled for portability (if needed)
│   │   │   ├── __init__.py
│   │   │   ├── Cipher/
│   │   │   ├── Protocol/
│   │   │   └── ...
│   │   └── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base_provider.py # Base class
│   │   │   ├── {site_name}.py   # Main provider
│   │   │   └── resolvers/
│   │   │   │   ├── __init__.py  # Resolver routing
│   │   │   │   ├── streamwish.py
│   │   │   │   ├── voe.py
│   │   │   │   ├── filemoon.py
│   │   │   │   ├── mega.py      # If encryption needed
│   │   │   │   └── ... (other resolvers)
```

### PHASE 3: PROVIDER IMPLEMENTATION (Parallel via `parallel-agents`)

| Parallel Group | Components |
|----------------|------------|
| **Content Extraction** | `get_main_page()`, `search()`, `load()` with de-duplication |
| **Video Link Extraction** | `load_links()` with deep iframe extraction |
| **Resolvers** | Domain-specific URL resolvers + Cryptodome if needed |
| **Navigation UI** | Menu hierarchy, pagination |

**Provider Interface Methods:**
```python
class SiteProvider(BaseProvider):
    def get_main_page(self, page: int, filter_type: str) -> List[Dict]
    def search(self, query: str) -> List[Dict]
    def load(self, url: str) -> Optional[Dict]
    def load_links(self, url: str) -> List[Dict]  # Deep iframe extraction
    def resolve_url(self, embed_url: str) -> Optional[Dict]
    def _deduplicate_items(self, items: List[Dict]) -> List[Dict]
    def _extract_from_internal_player(self, url: str) -> List[Dict]
```

### PHASE 4: TESTING & PACKAGING (Sequential)

| Step | Action | Command |
|------|--------|---------|
| 1 | Verify addon structure | Check all required files |
| 2 | Test de-duplication | Verify no duplicate entries |
| 3 | Test deep extraction | Verify external host extraction |
| 4 | Test video playback | Resolve sample URLs |
| 5 | Test encryption (if bundled) | Verify Cryptodome works |
| 6 | Create ZIP package | Use zipper script |

---

## 🔧 Required Agents

| Agent | Role | Phase |
|-------|------|-------|
| `site-to-kodi` | Provider logic & extraction | 1, 2, 3 |
| `kodi-expert` | Kodi API, UI structure | 2, 4 |
| `media-engineer` | Resolvers, HLS, encryption | 3 |

---

## 📋 Site Type Detection Matrix

| Site Pattern | Detection Method | Provider Approach |
|--------------|------------------|-------------------|
| **Blogger-based** | URL contains `.blogspot.` or Blogger JSON feed | Use `/feeds/posts/default?alt=json` API, `_SV_LINKS` extraction |
| **WordPress/DooPlay** | URL patterns `/pelicula/`, `/serie/`, admin-ajax | HTML parsing, de-duplication, title cleaning |
| **Custom PHP** | `.php` endpoints, POST requests | POST to `serv.php`, `vcap.php` |
| **Cloudflare** | 403 on initial request | Add headers, delay requests |
| **Datalife Engine** | DLE patterns | HTML parsing with regex |
| **Mega/Encryption** | mega.nz links or encrypted payloads | Bundle Cryptodome |

---

## 🔍 Deep iframe Extraction Flow

```
load_links(url)
    │
    ├─► Find embed containers (iframe, data-url)
    │       │
    │       ├─► External host directly? (StreamWish, VOE, Filemoon)
    │       │       └─► resolve_url() → direct stream
    │       │
    │       └─► Internal player? (player.php, embed.php, same domain)
    │               │
    │               └─► _extract_from_internal_player()
    │                       ├─► Direct iframe to external host
    │                       ├─► JavaScript URL variables
    │                       ├─► Base64 encoded URLs
    │                       ├─► JSON config extraction
    │                       └─► De-duplicate found sources
```

---

## 🛡️ Robustness Features

### De-duplication Patterns

| Level | Method | Key |
|-------|--------|-----|
| **Content Items** | `_deduplicate_items()` | URL + normalized title |
| **Episodes** | `_deduplicate_episodes()` | Season-Episode number |
| **Sources** | `seen_urls set` in `load_links()` | URL |

### Title Cleaning (DooPlay)

```python
def _clean_title(title: str) -> str:
    # Remove DooPlay suffixes
    title = re.sub(r'\s*\|\s*Ver Online\s*$', '', title, flags=re.I)
    title = re.sub(r'\s*\|\s*Descargar\s*$', '', title, flags=re.I)
    title = re.sub(r'\s*Online\s*$', '', title, flags=re.I)
    title = re.sub(r'\s*Gratis\s*$', '', title, flags=re.I)
    return ' '.join(title.split()).strip()
```

---

## 🔐 Cryptodome Bundling (Portability)

When to bundle:
- Site uses Mega.nz links
- Site uses custom encryption for video URLs
- External Kodi modules unavailable

Structure:
```
resources/lib/Cryptodome/
├── __init__.py
├── Cipher/
│   ├── __init__.py
│   ├── AES.py
│   ├── _mode_cbc.py
│   ├── _errors.py
│   └── ...
├── Protocol/
│   ├── __init__.py
│   ├── KDF.py
│   └── ...
├── Hash/
│   ├── __init__.py
│   ├── SHA256.py
│   └── ...
```

---

## 🛠️ Resolver Requirements

Based on site embeds, implement resolvers for:

| Domain | Resolver File | Method |
|--------|---------------|--------|
| StreamWish | `streamwish.py` | Packer unpack, m3u8 extraction |
| VOE | `voe.py` | Regex m3u8 from response |
| Filemoon | `filemoon.py` | Base64 decode, m3u8 |
| VidHide | `vidhide.py` | Redirect chain, m3u8 |
| DoodStream | `dood.py` | Token extraction, redirect |
| MixDrop | `mixdrop.py` | JSON response, direct URL |
| UqLoad | `uqload.py` | Source tag extraction |
| StreamTape | `streamtape.py` | Redirect + bot check |
| OK.ru | `okru.py` | Direct MP4 extraction |
| Mega | `mega.py` | Cryptodome AES decryption |
| GoodStream | `goodstream.py` | M3U8 from config |
| Fastream | `fastream.py` | M3U8 extraction |
| Vimeos | `vimeos.py` | JSON config parsing |

---

## 🎬 Navigation Pattern Templates

### Single Provider (FuegoCine Style)
```python
# Root menu shows provider categories directly
def root_menu(params=None):
    categories = provider.categories
    for name, filter_type in categories.items():
        url = build_url("provider_content", provider=provider.name, label=filter_type)
        add_directory_item(url, build_list_item(name))
```

### Multi Provider (Nativo Style)
```python
# Root menu shows content types (Movies, Series, Anime)
def root_menu(params=None):
    for category in ["movies", "series", "anime", "doramas"]:
        url = build_url("category_list", category=category)
        add_directory_item(url, build_list_item(category))
```

---

## 🔴 EXIT GATE

Before completion, verify:

1. ✅ **Addon XML Valid**: `addon.xml` has correct extension point
2. ✅ **Entry Point Works**: Router receives `sys.argv[2]` param_string
3. ✅ **Provider Loaded**: `__init__.py` exports provider instances
4. ✅ **De-duplication**: No duplicate items in listings
5. ✅ **Deep Extraction**: Internal players resolve to external hosts
6. ✅ **Navigation Complete**: Root → Category → Content → Detail → Play
7. ✅ **Resolvers Ready**: At least 3 resolver domains covered
8. ✅ **Cryptodome (if needed)**: Bundled and working
9. ✅ **ZIP Created**: Proper structure for Kodi installation

---

## 📊 Quality Score

After implementation, run:
```bash
python .agent/scripts/checklist.py plugin.video.{name}/
```

---

## Output Format

```markdown
## 🎬 Kodi Addon Creation Report

### 1. Site Analysis
- **Site Type**: [Blogger/DooPlay/PHP/WordPress/Custom]
- **Content Types**: [Movies/Series/Anime]
- **Embed Domains**: [StreamWish, VOE, Filemoon...]
- **Internal Players**: [Yes/No - needs deep extraction]
- **Anti-Bot**: [Yes/No - measures detected]
- **Encryption**: [Yes/No - Cryptodome bundled]

### 2. Addon Structure
| Component | Status | File |
|-----------|--------|------|
| addon.xml | ✅ | `addon.xml` |
| Entry | ✅ | `{name}.py` |
| Router | ✅ | `resources/lib/modules/router.py` |
| Provider | ✅ | `resources/lib/providers/{site}.py` |
| Resolvers | ✅ | `resources/lib/providers/resolvers/` |
| Cryptodome | ✅/N/A | `resources/lib/Cryptodome/` |

### 3. Provider Methods
| Method | Implemented | De-dup | Deep Extract |
|--------|-------------|--------|--------------|
| `get_main_page()` | ✅ | ✅ | N/A |
| `search()` | ✅ | ✅ | N/A |
| `load()` | ✅ | ✅ | N/A |
| `load_links()` | ✅ | ✅ | ✅ |

### 4. Verification
- **Quality Score**: [0-100]
- **De-duplication**: ✅ No duplicates found
- **Deep Extraction**: ✅ External hosts extracted
- **ZIP Package**: `plugin.video.{name}-{version}.zip`

### 5. Installation Instructions
1. Copy ZIP to Kodi `packages` folder
2. Install from ZIP in Kodi
3. Configure if needed (settings)
4. Test playback with sample content
```