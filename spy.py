"""
Spy - Machine Identity Wallpaper Generator
Instantly identifies your PC by displaying the hostname on your desktop
with a grid overlay and red border for pixel mapping purposes.
"""

__version__ = "1.1.0"
__author__ = "Spy Contributors"

from PIL import Image, ImageDraw, ImageFont
import socket
import ctypes
import os
import sys

# Default Configuration
DEFAULT_CONFIG = {
    'background_color': (43, 43, 43),  # Dark gray
    'grid_color': (60, 60, 60),  # Subtle gray
    'grid_spacing': 100,  # pixels
    'border_color': (255, 0, 0),  # Red
    'border_width': 3,  # pixels
    'text_color': (255, 255, 255),  # White
    'corner_text_color': (169, 169, 169),  # Light grey
    'font_size': 240,  # Very large, bold text
    'show_center_text': True,
    'show_corner_text': True,
    'show_grid': True,
    'show_circle': True,
    'show_border': True
}


def parse_color(color_str):
    """Parse color string in format 'R,G,B' to tuple."""
    try:
        parts = [int(x.strip()) for x in color_str.split(',')]
        if len(parts) == 3 and all(0 <= p <= 255 for p in parts):
            return tuple(parts)
    except:
        pass
    return None


def get_yes_no(prompt, default=True):
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    while True:
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        if response == '':
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def get_color_input(prompt, default_color):
    """Get color input from user."""
    default_str = f"{default_color[0]},{default_color[1]},{default_color[2]}"
    while True:
        response = input(f"{prompt} (R,G,B) [{default_str}]: ").strip()
        if response == '':
            return default_color
        color = parse_color(response)
        if color:
            return color
        print("Invalid color format. Use: R,G,B (e.g., 255,0,0 for red)")


def get_number_input(prompt, default_value, min_val=1, max_val=1000):
    """Get number input from user."""
    while True:
        response = input(f"{prompt} [{default_value}]: ").strip()
        if response == '':
            return default_value
        try:
            value = int(response)
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("Please enter a valid number")


def configure_advanced():
    """Interactive configuration wizard for advanced users."""
    print("\n" + "=" * 60)
    print("ADVANCED CONFIGURATION")
    print("=" * 60)
    print("\nCustomize your wallpaper settings.")
    print("Press Enter to accept default values shown in [brackets]\n")

    config = DEFAULT_CONFIG.copy()

    # Background
    print("--- Background ---")
    config['background_color'] = get_color_input(
        "Background color", DEFAULT_CONFIG['background_color'])

    # Grid
    print("\n--- Grid ---")
    config['show_grid'] = get_yes_no("Show grid?", True)
    if config['show_grid']:
        config['grid_color'] = get_color_input(
            "Grid color", DEFAULT_CONFIG['grid_color'])
        config['grid_spacing'] = get_number_input(
            "Grid spacing (pixels)", DEFAULT_CONFIG['grid_spacing'], 10, 500)

    # Circle
    print("\n--- Aspect Ratio Circle ---")
    config['show_circle'] = get_yes_no("Show aspect ratio circle?", True)

    # Border
    print("\n--- Border ---")
    config['show_border'] = get_yes_no("Show border?", True)
    if config['show_border']:
        config['border_color'] = get_color_input(
            "Border color", DEFAULT_CONFIG['border_color'])
        config['border_width'] = get_number_input(
            "Border width (pixels)", DEFAULT_CONFIG['border_width'], 1, 20)

    # Text
    print("\n--- Text ---")
    config['show_center_text'] = get_yes_no("Show center hostname text?", True)
    if config['show_center_text']:
        config['text_color'] = get_color_input(
            "Center text color", DEFAULT_CONFIG['text_color'])
        config['font_size'] = get_number_input(
            "Font size", DEFAULT_CONFIG['font_size'], 20, 500)

    config['show_corner_text'] = get_yes_no("Show corner hostname labels?", True)
    if config['show_corner_text']:
        config['corner_text_color'] = get_color_input(
            "Corner text color", DEFAULT_CONFIG['corner_text_color'])

    print("\n" + "=" * 60)
    print("Configuration complete!")
    print("=" * 60 + "\n")

    return config


def get_hostname():
    """Get the computer's hostname."""
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Error getting hostname: {e}")
        return "UNKNOWN-PC"


def get_screen_resolution():
    """Get the primary monitor's screen resolution with DPI awareness."""
    # Method 1: Try Windows API with DPI awareness (most accurate)
    try:
        # Set process to be DPI aware to get true resolution
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()  # Fallback for older Windows
            except:
                pass

        # Get the actual screen resolution
        width = ctypes.windll.user32.GetSystemMetrics(0)  # SM_CXSCREEN
        height = ctypes.windll.user32.GetSystemMetrics(1)  # SM_CYSCREEN

        if width > 0 and height > 0:
            print(f"Detected resolution (DPI-aware): {width}x{height}")
            return width, height
    except Exception as e:
        print(f"Warning: DPI-aware detection failed ({e})")

    # Method 2: Try screeninfo library as fallback
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        if monitors:
            primary = monitors[0]
            print(f"Detected resolution (screeninfo): {primary.width}x{primary.height}")
            return primary.width, primary.height
    except Exception as e:
        print(f"Warning: screeninfo detection failed ({e})")

    # Method 3: Fallback to common resolution
    print("Warning: Could not detect screen resolution. Using fallback 1920x1080.")
    return 1920, 1080


def create_wallpaper_image(hostname, width, height, config=None):
    """
    Create the wallpaper image with hostname, grid, and border.

    Args:
        hostname: The hostname text to display
        width: Image width in pixels
        height: Image height in pixels
        config: Configuration dictionary (uses DEFAULT_CONFIG if None)

    Returns:
        PIL Image object
    """
    if config is None:
        config = DEFAULT_CONFIG

    # Create base image with configured background
    img = Image.new('RGB', (width, height), color=config['background_color'])
    draw = ImageDraw.Draw(img)

    # Draw grid (vertical and horizontal lines)
    if config['show_grid']:
        print(f"Drawing grid with {config['grid_spacing']}px spacing...")
        for x in range(0, width, config['grid_spacing']):
            draw.line([(x, 0), (x, height)], fill=config['grid_color'], width=1)
        for y in range(0, height, config['grid_spacing']):
            draw.line([(0, y), (width, y)], fill=config['grid_color'], width=1)

    # Draw large circle for aspect ratio verification
    if config['show_circle']:
        print("Drawing aspect ratio circle...")
        center_x = width // 2
        center_y = height // 2

        # Calculate radius to fit exactly within screen (perfect circle, not oval)
        # Use the smaller dimension (height or width) to ensure circle fits
        max_radius = min(width, height) // 2

        if config['show_grid']:
            # Round radius down to nearest grid spacing multiple for clean alignment
            radius = (max_radius // config['grid_spacing']) * config['grid_spacing']
        else:
            radius = max_radius

        circle_bbox = [
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ]
        # Circle is twice as thick as grid lines for better visibility
        draw.ellipse(circle_bbox, outline=config['grid_color'], width=2)

    # Draw border around display boundaries
    if config['show_border']:
        print(f"Drawing {config['border_width']}px border...")
        for i in range(config['border_width']):
            draw.rectangle(
                [(i, i), (width - 1 - i, height - 1 - i)],
                outline=config['border_color'],
                width=1
            )

    # Draw hostname text
    if config['show_center_text'] or config['show_corner_text']:
        print(f"Drawing hostname: {hostname}")
        font_size = config['font_size']

        # Load fonts with helper function
        def load_font(size):
            """Try to load a TrueType font at the given size."""
            try:
                return ImageFont.truetype("arial.ttf", size)
            except:
                try:
                    return ImageFont.truetype("arialbd.ttf", size)
                except:
                    try:
                        return ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", size)
                    except:
                        return ImageFont.load_default()

        # Draw center text with auto-scaling
        if config['show_center_text']:
            # Start with desired font size
            current_font_size = font_size
            font_large = load_font(current_font_size)

            # Get text dimensions
            bbox = draw.textbbox((0, 0), hostname, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Auto-scale down if text is too wide or too tall
            # Leave 10% margin (5% on each side)
            max_width = int(width * 0.90)
            max_height = int(height * 0.90)

            while (text_width > max_width or text_height > max_height) and current_font_size > 20:
                # Reduce font size
                current_font_size = int(current_font_size * 0.9)
                font_large = load_font(current_font_size)

                # Recalculate dimensions
                bbox = draw.textbbox((0, 0), hostname, font=font_large)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

            if current_font_size < font_size:
                print(f"Auto-scaled text from {font_size}pt to {current_font_size}pt to fit screen")

            # Calculate centered position
            x = (width - text_width) // 2
            y = (height - text_height) // 2

            # Draw the hostname text (center)
            draw.text((x, y), hostname, fill=config['text_color'], font=font_large)

        # Load small font for corners (fixed at 60pt regardless of center text size)
        font_small = load_font(60)

        # Draw corner labels
        if config['show_corner_text']:
            padding_top = 20  # Padding from top edges
            padding_side = 20  # Padding from side edges
            padding_bottom = 80  # Extra padding from bottom to avoid Windows taskbar

            # Get small text dimensions
            bbox_small = draw.textbbox((0, 0), hostname, font=font_small)
            small_width = bbox_small[2] - bbox_small[0]
            small_height = bbox_small[3] - bbox_small[1]

            # Top-left corner
            draw.text((padding_side, padding_top), hostname, fill=config['corner_text_color'], font=font_small)

            # Top-right corner
            draw.text((width - small_width - padding_side, padding_top), hostname, fill=config['corner_text_color'], font=font_small)

            # Bottom-left corner (raised to avoid taskbar)
            draw.text((padding_side, height - small_height - padding_bottom), hostname, fill=config['corner_text_color'], font=font_small)

            # Bottom-right corner (raised to avoid taskbar)
            draw.text((width - small_width - padding_side, height - small_height - padding_bottom), hostname, fill=config['corner_text_color'], font=font_small)

    return img


def save_wallpaper(img):
    """
    Save the wallpaper image to AppData directory.

    Args:
        img: PIL Image object to save

    Returns:
        Full path to saved wallpaper file
    """
    # Save to AppData\Roaming directory
    appdata_path = os.environ.get('APPDATA', os.path.expanduser('~'))
    wallpaper_path = os.path.join(appdata_path, 'hostname_wallpaper.bmp')

    print(f"Saving wallpaper to: {wallpaper_path}")
    img.save(wallpaper_path, 'BMP')

    return wallpaper_path


def set_wallpaper(image_path):
    """
    Set the Windows desktop wallpaper.

    Args:
        image_path: Full path to the wallpaper image file
    """
    print("Setting desktop wallpaper...")

    # Convert to absolute path
    abs_path = os.path.abspath(image_path)

    # Windows API constants
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    try:
        # Call Windows API to set wallpaper
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            abs_path,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )

        if result:
            print("Desktop wallpaper set successfully!")
        else:
            print("Failed to set wallpaper. You may need to set it manually.")
            print(f"Wallpaper file location: {abs_path}")
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        print(f"You can manually set the wallpaper from: {abs_path}")


def main():
    """Main application entry point."""
    print("=" * 60)
    print(f"Spy - Machine Identity Wallpaper Generator v{__version__}")
    print("=" * 60)

    # Mode selection
    print("\nSelect mode:")
    print("  [1] Quick (use default settings)")
    print("  [2] Advanced (customize colors and features)")

    mode = input("\nEnter choice [1]: ").strip()

    if mode == '2':
        config = configure_advanced()
    else:
        config = DEFAULT_CONFIG
        print("\nUsing default configuration...")

    # Step 1: Get hostname
    hostname = get_hostname()
    print(f"\nHostname: {hostname}")

    # Step 2: Get screen resolution
    width, height = get_screen_resolution()
    print(f"Screen Resolution: {width}x{height}")

    # Step 3: Create wallpaper image
    print(f"\nGenerating wallpaper image...")
    img = create_wallpaper_image(hostname, width, height, config)

    # Step 4: Save wallpaper
    wallpaper_path = save_wallpaper(img)

    # Step 5: Set as desktop wallpaper
    set_wallpaper(wallpaper_path)

    print("\n" + "=" * 60)
    print("Done! Your desktop wallpaper has been updated.")
    print("=" * 60)

    # Keep console open if run directly (not from command line)
    if len(sys.argv) == 1:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
