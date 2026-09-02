# Addon-Template

A Blender add-on template for [B3dHub](https://github.com/B3dHub) projects. Dual-mode: ships
both a legacy `bl_info` (root `__init__.py`, Blender 3.3+) and an extension
`blender_manifest.toml` (Blender 4.2+), so the same code installs as a classic add-on or a
Blender Extension.

## Usage

Scaffold a new add-on from the template — clone into a temp dir inside your (empty)
add-on folder, move everything up, then drop the template dir and its git history:

```powershell
cd <your_addon_dir>
git clone --depth 1 https://github.com/B3dHub/addon_template.git template
Move-Item template\* . -Exclude .git
Remove-Item template -Recurse -Force
```

Then fork the template into your add-on:

1. Replace the `XX_` placeholder prefix consistently across all files
   (`XX_OT_`, `XX_PT_`, `XX_UL_`, `XX_MT_`, `XX_AP_`, `XX_PG_`; operator idnames `xx.*`)
2. Update `bl_info` in the root `__init__.py` (name, author, description, category, location)
3. Update `blender_manifest.toml` (`id` = root folder name with underscores, name, tagline,
   maintainer, tags)
4. Replace the demo operator/panel/property group with your own, keeping the same patterns
5. Update `manual.py` and the Help panel links to your documentation
6. Bump the version in **both** `bl_info["version"]` and `blender_manifest.toml` together

The template is dependency-free. B3dHub add-ons that need `qbpy` add it in their own
repository (private submodule or bundled wheel) — it is proprietary and must not ship
in this public template.

See [AGENTS.md](AGENTS.md) for the full architecture and conventions, and the
`.agents/skills/` folder for agent workflows (API knowledge, conventions).

## Structure

```
__init__.py            # bl_info only; delegates register/unregister to source
blender_manifest.toml  # extension metadata (Blender 4.2+)
source/
  changelog.py         # changelog popup operator; parses CHANGELOG.md
  ops/                 # operators (XX_OT_*)
  ui/                  # panels (XX_PT_*), UILists (XX_UL_*), menus (XX_MT_*)
  utils/
    addon.py           # package/version/preferences/timer helpers
    icon.py            # loads icons/*.png as icon_value ids
    preview.py         # loads previews/*.png as enum thumbnails
    props.py           # property groups (XX_PG_*); attaches Scene pointers
    prefs.py           # add-on preferences (XX_AP_*)
    keymap.py          # addon keymaps (keyconfigs.addon, leak-free)
    manual.py          # online manual map (bpy.ops idname -> docs page)
icons/                 # drop PNG icons here (auto-loaded, recursive)
previews/              # drop PNG preview thumbnails here
```

## Build & Release

Windows-first; `make` targets wrap `build.bat` and the `gh` CLI. Work happens on `dev`;
releases flow `dev -> PR -> main -> GitHub release`.

```
make sync            # fetch + checkout dev + pull
make build           # clone, strip .git/.github, zip into releases/
make create_pr       # PR dev -> main titled with the manifest version
make merge_pr        # auto-merge the PR
make release         # full flow: sync, build, PR, merge, tag v{version}, attach zip
make commit msg="…"  # stage, commit, push
```

Requirements: [Blender](https://www.blender.org/download/) (3.3+ for legacy installs,
4.2+ for extensions), [WinRAR](https://www.winrar.com/) (zipping), [GitHub CLI](https://cli.github.com/) (`gh`).
