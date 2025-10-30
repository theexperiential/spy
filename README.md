# Spy - Machine Identity Wallpaper Generator

A simple Python application that generates a custom desktop wallpaper displaying your computer's hostname. Perfect for identifying machines in multi-machine setups, labs, or remote desktop environments.

**Know your machine at a glance.**

## Features

- **Automatic Hostname Detection**: Fetches and displays the Windows PC hostname
- **Large Bold Text**: Hostname displayed in very large, easy-to-read white text (centered)
- **Corner Labels**: Smaller light grey hostname text in all four corners (visible even with windows open)
- **Pixel Mapping Grid**: 100-pixel grid overlay for screen calibration and pixel mapping
- **Aspect Ratio Circle**: Large circle for verifying screen aspect ratio accuracy
- **Display Boundary Markers**: Thin red border marking the exact display edges
- **DPI-Aware Resolution Detection**: Automatically detects your true screen resolution (4K, 1440p, etc.)
- **One-Click Execution**: Run once to instantly update your desktop wallpaper
- **Persistent Storage**: Saves wallpaper file to AppData for future reference

## Visual Design

- **Background**: Dark gray (#2b2b2b)
- **Grid**: Subtle gray lines every 100 pixels
- **Circle**: Large circle (same color as grid) for aspect ratio verification
- **Border**: 3-pixel red border around display edges
- **Center Text**: White, bold, large hostname (120pt)
- **Corner Text**: Light grey, smaller hostname labels (60pt) in all four corners

## Project Structure

```
spy/
├── spy.py                      # Main application
├── requirements.txt            # Python dependencies
├── build.bat                   # Build script for creating .exe
├── README.md                   # This file
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
├── assets/                     # Icon and asset files
│   ├── spy_icon.ico           # Application icon (multi-resolution)
│   ├── spy_icon.png           # Icon preview
│   └── create_icon.py         # Icon generator script
├── dist/                       # Build output (executable)
│   └── spy.exe                # Standalone executable (after build)
└── build/                      # PyInstaller temp files (gitignored)
```

## Requirements

- Windows 11 (or Windows 10)
- Python 3.7 or higher

## Installation

### Option 1: Run from Source (Development)

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Install Dependencies**:
   ```batch
   pip install -r requirements.txt
   ```

3. **Run the Script**:
   ```batch
   python spy.py
   ```

### Option 2: Create Standalone Executable (Distribution)

Build a single `.exe` file that can run on any Windows machine without Python installed:

1. **Install PyInstaller**:
   ```batch
   pip install pyinstaller
   ```

2. **Build the Executable**:
   ```batch
   build.bat
   ```

   Or manually:
   ```batch
   python -m PyInstaller --onefile --console --name spy --icon=assets/spy_icon.ico spy.py
   ```

3. **Find Your Executable**:
   - Located in `dist\spy.exe`
   - File size: ~20-30 MB
   - No dependencies required on target machines

4. **Deploy**:
   - Copy `spy.exe` to any Windows 11 machine
   - Double-click to run
   - Desktop wallpaper updates instantly

## Usage

### Quick Start

Simply run the application:

```batch
python spy.py
```

Or double-click `spy.exe` if you built the standalone version.

### Two Modes Available

When you run Spy, you'll be prompted to choose:

**1. Quick Mode (Default)** - Press Enter
- Uses sensible defaults
- Generates wallpaper instantly
- Perfect for quick deployment

**2. Advanced Mode** - Enter `2`
- Fully customize your wallpaper
- Choose colors for all elements
- Toggle features on/off
- Perfect for specific requirements

### Advanced Mode Options

In Advanced Mode, you can customize:

#### Background
- Background color (RGB)

#### Grid
- Show/hide grid
- Grid color (RGB)
- Grid spacing (10-500 pixels)

#### Aspect Ratio Circle
- Show/hide circle
- Uses grid color
- Perfect circle sized to fit screen

#### Border
- Show/hide border
- Border color (RGB)
- Border width (1-20 pixels)

#### Text
- Show/hide center hostname text
- Center text color (RGB)
- Font size (20-500)
- Show/hide corner hostname labels
- Corner text color (RGB)

### What Happens

1. Select your mode (Quick or Advanced)
2. Application detects your computer's hostname
3. Detects your primary monitor resolution (DPI-aware for 4K/HiDPI displays)
4. Generates a custom wallpaper image with your chosen settings
5. Saves the image to `%APPDATA%\hostname_wallpaper.bmp`
6. Sets it as your desktop wallpaper automatically

### Default Settings (Quick Mode)

- **Background**: Dark gray (#2b2b2b)
- **Grid**: Subtle gray, 100px spacing
- **Circle**: Full height/width perfect circle (2px thick)
- **Border**: 3px red border
- **Center Text**: White, 240pt (auto-scales for long hostnames), bold
- **Corner Text**: Light grey, 60pt, positioned to avoid Windows taskbar

### File Location

The generated wallpaper is saved to:
```
C:\Users\<YourUsername>\AppData\Roaming\hostname_wallpaper.bmp
```

This file is kept for reference and can be manually applied again if needed.

## Deployment to Multiple Machines

### For IT Administrators

**Method 1: Executable Distribution**
1. Build the standalone executable once
2. Copy `spy.exe` to each target machine
3. Run it (can be automated via logon script, Group Policy, or task scheduler)

**Method 2: Automated Deployment**
```batch
REM Example logon script
\\server\share\spy.exe
```

**Method 3: PowerShell Remote Execution**
```powershell
# Copy and execute on remote machines
Invoke-Command -ComputerName PC1,PC2,PC3 -ScriptBlock {
    & "C:\Deploy\hostname_wallpaper.exe"
}
```

## Customization

You can modify the script to customize:

- **Background Color**: Change `BACKGROUND_COLOR` (line 15)
- **Grid Spacing**: Change `GRID_SPACING` (line 17)
- **Grid Color**: Change `GRID_COLOR` (line 16)
- **Border Color**: Change `BORDER_COLOR` (line 18)
- **Border Width**: Change `BORDER_WIDTH` (line 19)
- **Text Size**: Change `FONT_SIZE` (line 21)
- **Text Color**: Change `TEXT_COLOR` (line 20)

Example:
```python
BACKGROUND_COLOR = (0, 0, 0)  # Pure black
GRID_SPACING = 50  # Finer grid
FONT_SIZE = 150  # Larger text
```

## Troubleshooting

### "No module named 'PIL'" Error
Install dependencies:
```batch
pip install pillow screeninfo
```

### "Could not detect screen resolution" Warning
The script will automatically fall back to 1920x1080. You can manually set your resolution in the code if needed.

### Wallpaper Doesn't Change
- Make sure you're running on Windows 11/10
- Try running the script as Administrator
- Check that the wallpaper file was created in AppData\Roaming

### Font Appears Small or Default
The script tries multiple font paths. If issues persist, install Arial font or modify the `FONT_SIZE` constant to a larger value.

### Multi-Monitor Setup
The script uses the primary monitor's resolution. Windows will display the wallpaper according to your wallpaper settings (Fit, Fill, Stretch, Tile, Center, or Span).

## Technical Details

### Screen Resolution Detection
- Uses `screeninfo` library to detect primary monitor
- Falls back to 1920x1080 if detection fails
- Compatible with multiple monitor setups

### Wallpaper Setting Method
- Uses Windows API `SystemParametersInfoW` via `ctypes`
- Updates Windows registry to persist wallpaper
- Works on Windows 10 and Windows 11

### Image Format
- Saved as BMP (Bitmap) format
- Ensures maximum compatibility with Windows wallpaper system
- Uncompressed for best quality

## License

Free to use and modify for personal or commercial purposes.

## Support

For issues or questions, please check:
- Script output for error messages
- Windows Event Viewer for system-level issues
- Verify Python and dependencies are correctly installed

## Git Repository Setup

This project is ready for Git version control:

### Recommended Workflow:

1. **Initialize repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Spy v1.0"
   ```

2. **Executables**: The `.gitignore` is configured to:
   - **Exclude** `build/` folder (PyInstaller temp files)
   - **Exclude** `dist/*.exe` by default
   - **Keep** source code, documentation, and icon files

3. **For releases**: Manually create GitHub releases and attach `spy.exe`:
   ```bash
   # After building
   # Go to GitHub > Releases > Create new release
   # Attach dist/spy.exe as a binary asset
   ```

   This approach keeps your repository lean while making executables available to users.

4. **Alternative**: If you want to track the exe in git:
   - Remove the `dist/*.exe` line from `.gitignore`
   - Use Git LFS for large binary files (recommended)

## Version History

- **v1.1.0** (2025-10-29): Enhanced text and interactive configuration
  - **Quick Mode**: One-click default settings
  - **Advanced Mode**: Full customization
  - **2x Larger Center Text**: Now 240pt (was 120pt) for better visibility
  - **Auto-Scaling Text**: Prevents cropping of long hostnames - automatically scales down while maintaining readability
  - **Taskbar-Aware**: Bottom corner text positioned to avoid Windows taskbar
  - Customize all colors (background, grid, border, text)
  - Toggle features on/off (grid, circle, border, text)
  - Adjust grid spacing, border width, font size
  - Circle now full height/width (perfect circle)
  - Circle 2x thicker than grid lines for visibility
  - Version display in console output

- **v1.0** (2025-10-29): Initial release
  - Hostname detection with googly eyes icon 👀
  - DPI-aware resolution detection (4K/HiDPI support)
  - Center text (white, large, bold)
  - Corner labels (light grey, smaller)
  - Grid overlay (100px) - perfectly aligned
  - Large aspect ratio circle (aligned to grid)
  - Red border
  - Auto wallpaper setting
  - Standalone executable support
