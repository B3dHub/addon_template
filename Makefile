# ===========================================
# Package Building and Distribution
# ===========================================

# Create wheel for qbpy package and organize output
wheel:
	python setup.py build bdist_wheel
	if not exist wheels mkdir wheels
	if exist dist\*.whl cmd /c "move dist\*.whl wheels"
	cmd /c "rmdir /s /q build dist qbpy.egg-info"

# ===========================================
# Git Operations
# ===========================================

# Commit changes to dev branch
commit:
	$(eval msg ?= $(filter-out $@,$(MAKECMDGOALS)))
	@if "$(msg)"=="" (echo Please provide a commit message: make commit "your message" & exit 1)
	git status
	git add .
	git status
	git commit -m "$(msg)"
	git push origin

%:
	@:

# Sync local branch with remote (defaults to dev branch)
sync:
	$(eval branch ?= dev)
	git fetch origin
	git checkout $(branch)
	git pull origin $(branch)

# Build project using build.bat script (defaults to dev branch)
build:
	$(eval branch ?= dev)
	cmd /c "build.bat $(branch)"
	@echo "Successfully built the release zip"

# ===========================================
# Pull Request Management
# ===========================================

# Get version from TOML file
get_version:
	@echo "Installing toml module..."
	@python -m pip install toml --quiet --user 2>nul || python -m pip install toml --quiet 2>nul || pip install toml --quiet 2>nul
	@echo "Extracting version from blender_manifest.toml..."
	$(eval VERSION := $(shell python -c "import toml; print(toml.load('blender_manifest.toml')['version'])" 2>nul))
	@if "$(VERSION)"=="" (echo ERROR: Failed to extract version from blender_manifest.toml & exit 1)
	@echo "Version extracted: $(VERSION)"

# Create PR from dev to main
create_pr: get_version
	gh pr create --base main --head dev --title "Version $(VERSION)" --body-file CHANGELOG.md

# Merge PR automatically
merge_pr: get_version
	gh pr merge --auto --merge
	@echo "Successfully merged dev into main"

# ===========================================
# Release Management
# ===========================================

# Create GitHub release with version tag and release assets
create_release: get_version
	$(eval ROOT_DIR := $(notdir $(CURDIR)))
	@echo "Creating release with version: $(VERSION)"
	gh release create "v$(VERSION)" --target main --title "Version $(VERSION)" --notes-file CHANGELOG.md releases/$(ROOT_DIR)_v$(VERSION).zip

# ===========================================
# Complete Release Workflow
# ===========================================

# Execute full release process: sync, build, PR creation/merge, and release
release: sync build create_pr merge_pr create_release
	@echo "Successfully created release"