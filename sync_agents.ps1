# Propagate shared boilerplate (AGENTS.md, .agents/, build.bat, Makefile) from this
# template into every sibling Blender add-on.
# One command:  powershell -NoProfile -ExecutionPolicy Bypass -File sync_agents.ps1
#        or:    make sync_agents
$ErrorActionPreference = 'Stop'

$source = $PSScriptRoot
$root = Split-Path -Parent $source

# Repos that keep their own config (not overwritten).
$exclude = @('addon_template', 'bui')

# Shared files copied verbatim, and the shared directory mirrored.
$files = @('AGENTS.md', 'build.bat', 'Makefile')
$sourceSkills = Join-Path $source '.agents'
if (-not (Test-Path -LiteralPath $sourceSkills)) {
    throw "Source .agents missing in $source"
}

$targets = Get-ChildItem -LiteralPath $root -Directory | Where-Object {
    $_.Name -notin $exclude -and
    (Test-Path -LiteralPath (Join-Path $_.FullName 'blender_manifest.toml'))
}

$results = foreach ($target in $targets) {
    $repo = $target.FullName
    $destSkills = Join-Path $repo '.agents'

    # Never mirror through a link - it would write into the template.
    if (Test-Path -LiteralPath $destSkills) {
        $linkType = (Get-Item -LiteralPath $destSkills -Force).LinkType
        if ($linkType -eq 'Junction' -or $linkType -eq 'SymbolicLink') {
            [IO.Directory]::Delete($destSkills, $false)
        }
    }

    $changed = $false
    foreach ($file in $files) {
        $sourceFile = Join-Path $source $file
        if (-not (Test-Path -LiteralPath $sourceFile)) { continue }
        $destFile = Join-Path $repo $file
        $before = if (Test-Path -LiteralPath $destFile) { (Get-FileHash -LiteralPath $destFile -Algorithm MD5).Hash } else { '' }
        Copy-Item -LiteralPath $sourceFile -Destination $destFile -Force
        if ((Get-FileHash -LiteralPath $destFile -Algorithm MD5).Hash -ne $before) { $changed = $true }
    }

    robocopy $sourceSkills $destSkills /MIR /NJH /NJS /NDL /NFL /NP /NS /NC | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed for $($target.Name) (exit $LASTEXITCODE)" }
    if ($LASTEXITCODE -ge 1) { $changed = $true }

    [pscustomobject]@{ Addon = $target.Name; Changed = $changed }
}

$results | Format-Table -AutoSize
$updated = @($results | Where-Object Changed).Count
Write-Host "Synced $($results.Count) add-ons ($updated updated)."
