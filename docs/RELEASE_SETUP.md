# Creating GitHub Release for X4 ShipMatrix v1.0.0

Canonical workflow reference: `docs/BUILD_RELEASE_WORKFLOW.md`

##  Prerequisites

1. **GitHub Repository**: Make sure `jongreg288/X4_Ship_Parse` exists on GitHub
2. **Git Setup**: Repository is connected to GitHub remote
3. **Release Files**: Both executables built and ready for distribution
4. **Version Consistency**: All version numbers updated to v1.0.0

##  Steps to Create Release

### One-command prerelease automation (recommended for 0.x)

From the project root:

```powershell
python build_scripts/release_prerelease.py
```

What it does:
- Builds `X4 ShipMatrix.exe` and `X4_Updater.exe`
- Builds installer `X4_ShipMatrix_v<version>_Setup.exe`
- Stages assets in `releases/latest`
- Creates or updates GitHub prerelease `v<version>`

Optional:

```powershell
python build_scripts/release_prerelease.py --skip-build
python build_scripts/release_prerelease.py --notes-file release_notes.md
```

### Method 1: GitHub Web Interface (Recommended)

1. **Navigate to Releases**:
   - Go to https://github.com/jongreg288/X4_Ship_Parse
   - Click "Releases" tab
   - Click "Create a new release"

2. **Release Configuration**:
   ```
   Tag version: v1.0.0
   Release title: X4 ShipMatrix v1.0.0 - Multi-Language Revolution!
   Target: main branch
   ```

3. **Upload Assets**:
   - **Required**: `X4 ShipMatrix.exe`
   - **Required**: `X4_ShipMatrix_v<version>_Setup.exe`
   - **Optional**: `X4_Updater.exe`

4. **Release Notes**:
   ```markdown
   # X4 ShipMatrix v1.0.0 - Multi-Language Revolution! 

   ##  Major Features
   - **Multi-Language Support**: Automatic detection of 14+ languages
   - **Windowed GUI**: Clean interface without console window
   - **Smart Data Extraction**: Direct CAT/DAT reading with XRCatTool
   - **Dual Update System**: Choose automatic or manual updates

   ##  Download Options
   
   ### Full Package (Recommended) - 79 MB
   - `X4_Ship_Parser.exe` - Main application  
   - `X4_Updater.exe` - Automatic update checker
   
   ### Standalone Package - 64.6 MB
   - `X4_Ship_Parser.exe` - Main application only (manual updates)

   ##  Supported Languages
   English, German, French, Spanish, Italian, Russian, Polish, Czech, Turkish, 
   Japanese, Korean, Chinese (Simplified), Chinese (Traditional)

   ##  Quick Start
   1. Download your preferred package
   2. Run X4_Ship_Parser.exe
   3. Application auto-detects X4 installation and language
   4. Enjoy ship statistics in your native language!
   ```

### Method 2: GitHub CLI (Advanced)

```bash
# Install GitHub CLI first
gh release create v1.0.0 \
  --title "X4 ShipMatrix v1.0.0 - Multi-Language Revolution!" \
  --notes-file release_notes.md \
  X4_Ship_Parser.exe \
  X4_Updater.exe
```

### Method 3: Git Tags + Manual Upload

```bash
# Create and push tag
git tag -a v1.0.0 -m "X4 ShipMatrix v1.0.0"
git push origin v1.0.0

# Then go to GitHub web interface to upload files
```

##  Files to Include in Release

### Essential Files
- `X4 ShipMatrix.exe` - Main application
- `X4_ShipMatrix_v<version>_Setup.exe` - Installer package
- `README_USERS.txt` - User instructions

### Optional Files  
- `X4_Updater.exe` - Automatic updater

### Do NOT Include
- Development files (`development/` folder)
- Source code (keep repository for that)
- Build artifacts

##  Post-Release Setup

1. **Test Update System**:
   ```bash
   # Test that updater can find the release
   distro/X4_Updater.exe
   ```

2. **Update Documentation**:
   - Update README with download links
   - Add installation instructions
   - Document new features

3. **Version Increment** (for next development cycle):
   ```python
   # In standalone_updater.py
   CURRENT_VERSION = "1.0.1"  # Update for next development cycle
   
   # In version_info.txt
   Update version numbers for next release
   ```

##  Release API Endpoint

Once created, your release will be available at:
```
https://api.github.com/repos/jongreg288/X4_Ship_Parse/releases/latest
```

This endpoint will return JSON with:
- Release information
- Download URLs for assets
- Version numbers
- Release notes

##  Verification

After creating the release:

1. **Check API Response**:
   ```powershell
   Invoke-RestMethod https://api.github.com/repos/jongreg288/X4_Ship_Parse/releases/latest
   ```

2. **Test Updater**:
   - Run `X4_Updater.exe`
   - Should detect "no updates available" (since you're on latest)

3. **Test Downloads**:
   - Download files from release page
   - Verify file sizes and functionality

---

**The GitHub releases API endpoint will automatically exist once you create your first release through any of the methods above!** 