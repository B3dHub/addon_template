# AGENTS.md

This document is addon-agnostic: it describes the boilerplate's structure and conventions, which apply equally to the template and to any add-on forked from it. Never bake one add-on's specifics into the shared modules.

## Agent Boundaries

Agents write and edit code only. Never commit, build, or release — those belong to the user:

- Never commit or push (`git commit`, `git push`, `make commit`); leave changes uncommitted in the working tree for review
- Never build or release (`make build`, `make release`, `build.bat`, `make create_pr`, `make merge_pr`, `make create_release`, `gh …`)
- Read-only git (`git status`, `git diff`, `git log`) is fine; anything that mutates history, branches, or the working tree is not
- When finished, summarize what changed — the user runs the commit → build → release flow (see Build & Release in `README.md`)

## Blender API Reference

- [Quickstart](https://docs.blender.org/api/current/info_quickstart.html)
- [Overview](https://docs.blender.org/api/current/info_overview.html)
- [API Reference](https://docs.blender.org/api/current/info_api_reference.html)
- [Best Practice](https://docs.blender.org/api/current/info_best_practice.html)
- [Tips & Tricks](https://docs.blender.org/api/current/info_tips_and_tricks.html)
- [Gotchas](https://docs.blender.org/api/current/info_gotcha.html)
- [Advanced](https://docs.blender.org/api/current/info_advanced.html)
- [API Changelog](https://docs.blender.org/api/current/change_log.html)

Distilled API knowledge lives in the `blender-api` skill (`.agents/skills/blender-api/`) —
load it when writing or debugging `bpy` code instead of re-fetching the docs.

## Skills

On-demand workflows live in `.agents/skills/`:

- **`blender-api`** — distilled bpy knowledge (data access, context, operators, registration,
  gotchas, version changes) with per-doc-page references
- **`blender-conventions`** — SOLID, naming, registration patterns, and
  no-unnecessary-abstraction rules for this codebase

Forking the template into a new add-on: follow the checklist in `README.md`. The release
flow is user-driven — see Agent Boundaries.

## Architecture

```
__init__.py            # bl_info only; delegates to source
blender_manifest.toml  # extension metadata (id, version, blender_version_min)
source/
  changelog.py         # XX_OT_changelog operator; parses CHANGELOG.md into a popup
  ops/                 # Operators (XX_OT_*)
  ui/                  # Panels (XX_PT_*), UILists (XX_UL_*), Menus (XX_MT_*)
  utils/
    addon.py           # package, version, version_str, preferences(), tag_redraw(), timer
    icon.py            # loads icons/*.png into `icons` dict (name -> icon_id)
    preview.py         # loads previews/*.png into EnumProperty items
    props.py           # PropertyGroups (XX_PG_*); attaches Scene pointer properties
    prefs.py           # AddonPreferences (XX_AP_*)
    keymap.py          # addon keymaps; register in keyconfigs.addon, not user
    manual.py          # online manual map (bpy.ops idname -> docs page)
```

**Registration pattern**: every module exposes `register()`/`unregister()`; each package `__init__.py` calls its children in order. Classes are registered via `bpy.utils.register_classes_factory(classes)` (or explicit loops when scene properties must be attached, as in `props.py`). New module → add import + call in the parent `__init__.py`.

**Panel mixin**: `ui/panels.py` defines an `Addon` mixin (`bl_space_type`, `bl_region_type`, `bl_category`) that all panels inherit from — change the sidebar category once there.

## Conventions

- **Naming**: Blender class names follow `{ADDON}_{TYPE}_{NAME}`. In the template the add-on prefix is the `XX_` placeholder (`XX_OT_`, `XX_PT_`, `XX_UL_`, `XX_MT_`, `XX_AP_`, `XX_PG_`; operator idnames `xx.*`) — replace it consistently across all files when forking.
- **Operators**: implement `poll()` (guard context) and `description()` classmethods; use `\n` + `•` formatting for keymap hints in tooltips (see the demo operator `ops/test.py`).
- **Properties**: attach to `bpy.types.Scene` in `props.py` with `PointerProperty`; delete them in `unregister()` before unregistering classes.
- **Icons**: drop PNGs into `icons/` (auto-loaded, recursive); reference via `icons["NAME"]` as `icon_value=`. Preview thumbnails go in `previews/` and are exposed through the `enum_previews` callback.
- **Changelog**: `CHANGELOG.md` uses `**Added**` / `**Fixed**` / `**Changed**` / `**Improved**` / `**Removed**` sections with `- ` items — the changelog operator parses this exact format.
- **Docs**: keep `doc_url` in `bl_info`/manifest in sync with `manual.py` and the Help panel links in `ui/panels.py`.

## Coding Principles

- **SOLID**: single-purpose operators/panels/utils; open for extension via the mixin + registration pattern, closed for modification.
- **Clean names**: descriptive, unabbreviated variable and function names (`matching_keymap_items`, not `kmis`). Match the existing docstring style (Args/Returns).
- **No unnecessary abstractions**: prefer direct, readable Blender API calls over wrapper layers. Only add a helper when used more than once and it removes real duplication.
- **Maintainable flow**: linear, obvious execution; early returns over nesting; keep `register`/`unregister` symmetric.
- Follow [Blender best practices](https://docs.blender.org/api/current/info_best_practice.html): style guide compliance, correct use of `poll`, no `bpy.ops` in draw code, style `bpy.context` access safely.

## Gotchas

- `keymap.py`: register keymaps in `keyconfigs.addon` (never `user`), store them in `addon_keymaps`, and remove them on unregister — otherwise they leak between sessions.
- `icon.py`/`preview.py`: preview collections must be removed in `unregister()` or Blender leaks memory; `icon.register()` defensively unregisters first if re-running.
- `changelog.py` reads `CHANGELOG.md` relative to the module file — keep the file at repo root.
- `bl_info` is required for legacy installs even when the manifest exists; keep metadata duplicated and consistent — including `version`, which must be bumped in both places together.
