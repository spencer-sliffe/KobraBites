def hex_to_rgba(hex_color, alpha=1.0):
    if (not hex_color): 
        return None
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')

    # Handle 3-digit hex format (e.g., #abc)
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])

    # Convert to RGB values
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {alpha})"
