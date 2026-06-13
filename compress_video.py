import argparse
from PIL import Image

FRAME_WIDTH = 32
FRAME_HEIGHT = 8
FRAME_BYTE_SIZE = 96


# -----------------------------
# RGB → 3-bit (R,G,B threshold)
# -----------------------------
def rgb_to_3bit(rgb):
    r, g, b = rgb
    return ((r > 127) << 2) | ((g > 127) << 1) | (b > 127)


# -----------------------------
# Serpentine column mapping
# -----------------------------
def serpentine_order(pixels, width, height):
    """
    Convert row-major pixel list into serpentine column-major order:
    - col 0: top → bottom
    - col 1: bottom → top
    - col 2: top → bottom
    ...
    """

    # rebuild 2D grid
    grid = []
    it = iter(pixels)

    for y in range(height):
        row = []
        for x in range(width):
            row.append(next(it))
        grid.append(row)

    ordered = []

    for x in range(width):
        col = [grid[y][x] for y in range(height)]

        if x % 2 == 1:
            col.reverse()

        ordered.extend(col)

    return ordered


# -----------------------------
# Pack 3-bit values into bytes
# -----------------------------
def pack_3bit_pixels(pixels):
    buffer = 0
    bits = 0
    out = []

    for p in pixels:
        buffer = (buffer << 3) | (p & 0b111)
        bits += 3

        while bits >= 8:
            bits -= 8
            out.append((buffer >> bits) & 0xFF)

    if bits > 0:
        out.append((buffer << (8 - bits)) & 0xFF)

    return out


# -----------------------------
# Extract frames from PNG
# -----------------------------
def extract_frames(img, frame_count):
    """
    Layout:
    row 0 = separator (ignored)
    then repeating:
        8 rows frame
        1 row separator
    """

    frames = []
    y = 1  # skip top separator

    for _ in range(frame_count):
        frame = []

        for row in range(FRAME_HEIGHT):
            for x in range(FRAME_WIDTH):
                frame.append(img.getpixel((x, y + row)))

        frames.append(frame)
        y += FRAME_HEIGHT + 1

    return frames


# -----------------------------
# Main conversion pipeline
# -----------------------------
def generate_cpp(input_png, output_h, frame_rate, frame_count):
    img = Image.open(input_png).convert("RGB")

    frames = extract_frames(img, frame_count)

    output_frames = []

    for frame in frames:

        # 1. RGB → 3-bit
        encoded = [rgb_to_3bit(p) for p in frame]

        # 2. Apply serpentine wiring correction
        encoded = serpentine_order(encoded, FRAME_WIDTH, FRAME_HEIGHT)

        # 3. Pack into bytes
        packed = pack_3bit_pixels(encoded)

        # 4. Ensure 96 bytes
        packed = (packed + [0] * FRAME_BYTE_SIZE)[:FRAME_BYTE_SIZE]

        output_frames.append(packed)

    # -------------------------
    # Write C++ header
    # -------------------------
    with open(output_h, "w") as f:
        f.write("#pragma once\n")
        f.write("#include <avr/pgmspace.h>\n\n")

        f.write(f"const uint8_t NUM_FRAMES PROGMEM = {len(output_frames)};\n")
        f.write(f"const uint8_t FRAME_RATE PROGMEM = {frame_rate};\n\n")

        f.write("const byte FRAMES[][96] PROGMEM = {\n")

        for i, frame in enumerate(output_frames):
            f.write("  {")
            f.write(",".join(f"B{b:08b}" for b in frame))
            f.write("}")

            if i != len(output_frames) - 1:
                f.write(",")

            f.write("\n")

        f.write("};\n")


# -----------------------------
# CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="PNG → AVR LED matrix video encoder")

    parser.add_argument("input_png", help="Input PNG path")
    parser.add_argument("output_h", help="Output C++ header path")
    parser.add_argument("frame_count", type=int, help="Number of frames")
    parser.add_argument("frame_rate", type=int, help="Frame rate (FPS)")

    args = parser.parse_args()

    generate_cpp(
        input_png=args.input_png,
        output_h=args.output_h,
        frame_rate=args.frame_rate,
        frame_count=args.frame_count
    )


if __name__ == "__main__":
    main()
