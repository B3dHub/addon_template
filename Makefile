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

# Create PR from dev to main using version from toml file
create_pr:
	@echo "Installing toml package..."
	@pip install toml --quiet
	@python -m pip install toml --quiet
	$(eval VERSION := $(shell powershell -command "python -c \"try: import toml; print(toml.load('blender_manifest.toml')['version']); except ModuleNotFoundError: import subprocess; subprocess.check_call(['pip', 'install', 'toml']); import toml; print(toml.load('blender_manifest.toml')['version'])\""))
	@echo "Creating PR for version $(VERSION)..."
	gh pr create --base main --head dev --title "Version $(VERSION)" --body-file CHANGELOG.md

# Merge PR automatically
merge_pr:
	gh pr merge --auto --merge
	@echo "Successfully merged dev into main"

# ===========================================
# Release Management
# ===========================================

# Create GitHub release with version tag and release assets
create_release:
	$(eval version ?= $(VERSION))
	$(eval ROOT_DIR := $(notdir $(CURDIR)))
	gh release create "v$(version)" --target main --title "Version $(version)" --notes-file CHANGELOG.md releases/$(ROOT_DIR)_v$(version).zip

# ===========================================
# Complete Release Workflow
# ===========================================

# Execute full release process: sync, build, PR creation/merge, and release
release: sync build create_pr merge_pr create_release
	@echo "Successfully created release"