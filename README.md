# Spy 👀

**Instantly identify your Windows PC with a custom hostname wallpaper.**

Perfect for multi-machine setups, labs, or remote desktop environments.

![Spy Desktop Wallpaper Example](assets/screenshots/example.png)

## Quick Start

**Download:** [Latest Release](https://github.com/theexperiential/spy/releases)

Just run `spy.exe` - that's it! Your desktop wallpaper updates with your hostname.

## Features

- 🖥️ **Large hostname text** - visible at a glance
- 📍 **Corner labels** - visible even with windows open
- 📐 **Grid & circle overlay** - for pixel mapping/calibration
- 🎨 **Quick or Advanced mode** - use defaults or customize everything
- 🔍 **4K/HiDPI aware** - detects true screen resolution
- ⚡ **Auto-scaling** - long hostnames never get cropped

## Usage

### Quick Mode (Default)
Just press Enter. Uses sensible defaults.

### Advanced Mode
Enter `2` to customize:
- Background, grid, border, text colors
- Toggle features on/off
- Adjust sizes and spacing

## Build From Source

```bash
pip install -r requirements.txt
python spy.py
```

**Create executable:**
```bash
build.bat
```

## Deployment

For IT admins deploying to multiple machines:

```powershell
# Copy spy.exe to machines
\\server\share\spy.exe

# Or via logon script, Group Policy, etc.
```

## Default Settings

- Background: Dark gray
- Grid: 100px spacing
- Circle: Full screen height (perfect circle)
- Border: 3px red
- Center text: Auto-sized based on resolution (1080p=120pt, 1440p=160pt, 4K=240pt)
- Corner text: 60pt light grey (customizable in Advanced mode)

## License

MIT - Free to use and modify.
