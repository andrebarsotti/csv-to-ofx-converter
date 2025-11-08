# GitHub Actions Setup Guide

Complete guide for setting up automated builds and releases for the CSV to OFX Converter.

## Overview

The project uses GitHub Actions to automatically build standalone executables for Windows, macOS, and Linux whenever you create a release tag.

## What Gets Automated

✅ **Build on 3 platforms** - Linux, Windows, macOS
✅ **Create executables** - Self-contained, no Python needed
✅ **Generate checksums** - SHA256 for all files
✅ **Create release** - Automatic GitHub release with notes
✅ **Upload artifacts** - All executables attached to release

## Prerequisites

### 1. GitHub Repository

- [ ] Project is in a GitHub repository
- [ ] You have push access
- [ ] Actions are enabled (Settings > Actions > Allow all actions)

### 2. Repository Setup

The following files must be in your repository:

```
.github/
  workflows/
    build-and-release.yml     ← GitHub Actions workflow
csv_to_ofx_converter.spec     ← PyInstaller configuration
build.sh                      ← Linux/macOS build script
build.bat                     ← Windows build script
.gitignore                    ← Ignore build artifacts
src/
  csv_to_ofx_converter.py     ← Main application
README.md                     ← Documentation
README.pt-BR.md              ← Portuguese documentation
```

## Initial Setup

### Step 1: Push Files to GitHub

If you haven't already:

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Add GitHub Actions workflow for automated builds"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/conversor-csv-ofx.git

# Push to GitHub
git push -u origin main
```

### Step 2: Verify Actions are Enabled

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Actions** → **General** (left sidebar)
4. Under "Actions permissions", ensure:
   - ✅ **Allow all actions and reusable workflows** is selected
5. Under "Workflow permissions", ensure:
   - ✅ **Read and write permissions** is selected
   - ✅ **Allow GitHub Actions to create and approve pull requests** is checked
6. Click **Save**

### Step 3: Update README URLs

Replace placeholder URLs in README files:

**README.md:**
```markdown
# Change this:
[Releases page](https://github.com/andrebarsotti/conversor-csv-ofx/releases)

# To your actual URL:
[Releases page](https://github.com/andrebarsotti/conversor-csv-ofx/releases)
```

Do the same in `README.pt-BR.md`.

## Creating Your First Release

### Step 1: Prepare for Release

1. **Ensure all tests pass:**
   ```bash
   python3 -m unittest tests.test_converter -v
   ```

2. **Update version numbers** in README files (if needed)

3. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Prepare for v1.1.0 release"
   git push origin main
   ```

### Step 2: Create and Push Tag

```bash
# Create a version tag (use semantic versioning)
git tag -a v1.1.0 -m "Release version 1.1.0 - Date validation feature"

# Push the tag to GitHub
git push origin v1.1.0
```

### Step 3: Watch the Magic Happen

1. Go to your repository on GitHub
2. Click **Actions** tab
3. You should see a new workflow run called "Build and Release"
4. Click on it to watch progress

The workflow will:
- ⏳ Build executables for Linux, Windows, and macOS (5-10 minutes)
- ⏳ Generate checksums
- ⏳ Create release notes
- ⏳ Publish GitHub release with all files

### Step 4: Verify Release

1. Go to **Releases** tab in your repository
2. You should see your new release `v1.1.0`
3. Click on it to verify:
   - ✅ Release notes are present
   - ✅ Three executables are attached
   - ✅ Checksums file is attached
   - ✅ Download links work

## Workflow Details

### When It Runs

The workflow triggers on:

1. **Tag push** (automatic):
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

2. **Manual trigger** (via GitHub UI):
   - Actions → Build and Release → Run workflow

### Build Matrix

| Platform | OS | Python | Output |
|----------|-----|--------|---------|
| Linux | ubuntu-latest | 3.11 | csv-to-ofx-converter-linux-x64 |
| Windows | windows-latest | 3.11 | csv-to-ofx-converter-windows-x64.exe |
| macOS | macos-latest | 3.11 | csv-to-ofx-converter-macos-x64 |

### Build Steps

For each platform:

1. **Checkout code** - Get latest code from repository
2. **Setup Python 3.11** - Install Python environment
3. **Install PyInstaller** - Install build tool
4. **Build executable** - Create standalone app
5. **Upload artifact** - Store for release

Finally:

6. **Download all artifacts** - Collect from all platforms
7. **Generate checksums** - SHA256 for verification
8. **Create release** - Publish with notes and files

## Customization

### Change Python Version

Edit `.github/workflows/build-and-release.yml`:

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'  # Change here
```

### Add Application Icon

1. Create icon files (`.ico` for Windows, `.icns` for macOS)
2. Add to repository
3. Update `csv_to_ofx_converter.spec`:
   ```python
   icon='path/to/icon.ico'
   ```

### Include Additional Files

Update `.github/workflows/build-and-release.yml`:

**Linux/macOS:**
```yaml
--add-data "LICENSE:." \
--add-data "docs:docs" \
```

**Windows:**
```yaml
--add-data "LICENSE;." `
--add-data "docs;docs" `
```

### Change Executable Name

Edit workflow file:

```yaml
artifact_name: my-custom-name
asset_name: my-custom-name-linux-x64
```

## Troubleshooting

### Workflow Doesn't Start

**Problem:** No workflow run after pushing tag

**Solutions:**
1. Check tag format: Must be `v*.*.*` (e.g., `v1.0.0`)
2. Verify tag is pushed: `git ls-remote --tags origin`
3. Check Actions are enabled in Settings
4. Look for typos in workflow file name

### Build Fails

**Problem:** Red X on workflow run

**Solutions:**
1. Click on failed job to see error
2. Check Python version compatibility
3. Verify all imports are available
4. Test build locally first: `./build.sh`
5. Check workflow syntax: Use GitHub's validator

### Release Not Created

**Problem:** Build succeeds but no release

**Solutions:**
1. Check if release already exists (can't duplicate)
2. Verify `GITHUB_TOKEN` permissions
3. Ensure `create-release` job ran
4. Look for errors in "Create Release" step

### Executables Too Large

**Problem:** Files over 100MB

**Solutions:**
1. Enable UPX compression in spec file
2. Exclude unnecessary modules
3. Check what's being included: `pyinstaller --log-level DEBUG`

### Windows Executable Flagged as Virus

**Problem:** Antivirus blocks executable

**Why:** Unsigned executables trigger warnings

**Solutions:**
1. Add disclaimer in release notes
2. Provide SHA256 checksums for verification
3. Consider code signing certificate ($$$)
4. Upload to VirusTotal and share report

## Manual Workflow Trigger

Sometimes you want to trigger a build without creating a tag:

1. Go to **Actions** tab
2. Click **Build and Release** in left sidebar
3. Click **Run workflow** button (top right)
4. Select branch
5. Click **Run workflow**

Note: This builds but doesn't create a release (no tag).

## Monitoring Builds

### Email Notifications

GitHub sends email notifications on workflow failures by default.

**To customize:**
1. Settings → Notifications
2. Configure Actions notifications

### Status Badges

Add to README.md:

```markdown
![Build Status](https://github.com/YOUR_USERNAME/conversor-csv-ofx/workflows/Build%20and%20Release/badge.svg)
```

### Build History

- **Actions** tab shows all workflow runs
- Click on any run for detailed logs
- Filter by event type, status, branch, etc.

## Best Practices

### 1. Test Locally First

Always build and test locally before creating a release:

```bash
./build.sh
./dist/csv-to-ofx-converter
```

### 2. Use Pre-releases

For major versions, create a beta first:

```bash
git tag v2.0.0-beta
git push origin v2.0.0-beta
```

Then mark as pre-release in GitHub UI.

### 3. Semantic Versioning

Follow semantic versioning:
- `v1.0.0` - Initial release
- `v1.1.0` - New features
- `v1.1.1` - Bug fixes
- `v2.0.0` - Breaking changes

### 4. Keep Build Cache

GitHub caches dependencies between runs. Don't clear unless needed.

### 5. Document Changes

Update CHANGELOG section in README before each release.

## Security Considerations

### Secrets Management

If you need secrets:

1. Go to Settings → Secrets and variables → Actions
2. Click **New repository secret**
3. Add secret name and value
4. Reference in workflow:
   ```yaml
   env:
     MY_SECRET: ${{ secrets.MY_SECRET }}
   ```

### Code Signing

For production apps, consider signing:

**Windows:**
- Get code signing certificate
- Add certificate to secrets
- Update workflow to sign exe

**macOS:**
- Need Apple Developer account ($99/year)
- Get Developer ID certificate
- Update workflow to sign and notarize

## Cost Considerations

### GitHub Actions Usage

- **Public repos:** Unlimited minutes (free)
- **Private repos:** 2,000 minutes/month (free tier)

**Average build time:** ~5-10 minutes total (all platforms)

**Builds per month:**
- 1 release/week = ~40 minutes/month
- Well within free tier

### Storage

- **Artifacts retention:** 90 days default
- **Release assets:** No limit
- Large files in releases don't count against quota

## Support

### Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [BUILD.md](BUILD.md) - Detailed build guide
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) - Release process

### Getting Help

If you encounter issues:

1. Check workflow logs in Actions tab
2. Review this guide
3. Test build locally
4. Search GitHub Actions documentation
5. Open an issue with:
   - Error message
   - Workflow run link
   - What you've tried

## Quick Reference

### Create Release
```bash
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

### Delete Release
```bash
# Delete tag locally and remotely
git tag -d v1.2.0
git push origin :refs/tags/v1.2.0

# Delete release on GitHub UI
```

### Test Locally
```bash
# Build
./build.sh

# Test
./dist/csv-to-ofx-converter

# Clean
rm -rf build dist
```

### Check Build Status
```bash
# List recent workflow runs
gh run list

# View specific run
gh run view RUN_ID

# Watch live
gh run watch
```

---

**Ready to release?** Follow the steps above and your first automated build will be ready in minutes!

**Questions?** Check [BUILD.md](BUILD.md) for more detailed information.
