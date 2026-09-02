# AGENTS.md

Blender add-on template (B3dHub). Dual-mode: ships both legacy `bl_info` (root `__init__.py`, Blender 3.3+) and an extension `blender_manifest.toml` (Blender 4.2+). All real code lives in `source/`; the root `__init__.py` only delegates `register`/`unregister`.

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

Forking the template into a new add-on: follow the checklist in `README.md`. Version bumps
and the `make release` flow are documented under Build & Release below.

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

- **Naming**: `XX_` is the placeholder prefix — replace consistently across all files when forking (`XX_OT_`, `XX_PT_`, `XX_UL_`, `XX_MT_`, `XX_AP_`, `XX_PG_`; operator idnames `xx.*`). Keep the Blender class-name convention: `{ADDON}_{TYPE}_{NAME}`.
- **Operators**: implement `poll()` (guard context) and `description()` classmethods; use `\n` + `•` formatting for keymap hints in tooltips (see `ops/test.py`).
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
- `bl_info` is required for legacy installs even when the manifest exists; keep metadata duplicated and consistent.
