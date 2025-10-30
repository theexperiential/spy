"""
Creates a simple googly eyes icon for the Spy application
Generates multiple sizes for proper Windows Explorer display
"""
from PIL import Image, ImageDraw

def create_icon_at_size(size):
    """Create a googly eyes icon at a specific size"""
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)

    # Dark gray background circle
    bg_color = (43, 43, 43, 255)  # Same as app background
    padding = max(2, size // 25)
    draw.ellipse([padding, padding, size-padding, size-padding], fill=bg_color)

    # Scale eye parameters based on size
    eye_spacing = size // 4
    eye_y = size // 2 - size // 13
    eye_left_x = size // 2 - eye_spacing // 2
    eye_right_x = size // 2 + eye_spacing // 2
    eye_radius = size // 5

    # Draw left eye (white)
    draw.ellipse([
        eye_left_x - eye_radius,
        eye_y - eye_radius,
        eye_left_x + eye_radius,
        eye_y + eye_radius
    ], fill='white')

    # Draw right eye (white)
    draw.ellipse([
        eye_right_x - eye_radius,
        eye_y - eye_radius,
        eye_right_x + eye_radius,
        eye_y + eye_radius
    ], fill='white')

    # Draw left pupil (black, slightly off-center for googly effect)
    pupil_radius = eye_radius // 2.5
    pupil_offset_x = eye_radius // 5
    pupil_offset_y = eye_radius // 3
    draw.ellipse([
        eye_left_x - pupil_radius + pupil_offset_x,
        eye_y - pupil_radius + pupil_offset_y,
        eye_left_x + pupil_radius + pupil_offset_x,
        eye_y + pupil_radius + pupil_offset_y
    ], fill='black')

    # Draw right pupil (black, slightly off-center for googly effect)
    draw.ellipse([
        eye_right_x - pupil_radius - pupil_offset_x // 2,
        eye_y - pupil_radius + pupil_offset_y // 2,
        eye_right_x + pupil_radius - pupil_offset_x // 2,
        eye_y + pupil_radius + pupil_offset_y // 2
    ], fill='black')

    return img

# Create icons at multiple sizes
print("Creating icons at multiple sizes...")
sizes = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]
icons = []

for size in sizes:
    icon = create_icon_at_size(size)
    icons.append(icon)
    print(f"  Created {size}x{size}")

# Save the largest as PNG preview
icons[-1].save('spy_icon.png', 'PNG')
print("\nCreated spy_icon.png (256x256 preview)")

# Save as ICO with all sizes embedded
icons[-1].save('spy_icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
print("Created spy_icon.ico (multi-resolution)")
print("\nIcon files created successfully!")
print("Icon includes sizes: 16, 20, 24, 32, 40, 48, 64, 96, 128, 256")
