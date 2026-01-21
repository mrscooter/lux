"""CLI interface for lux."""

import argparse
import random
import sys
import time

from .presets import PRESETS, PresetCategory, get_preset_definitions, get_presets_by_category
from .runner import run_g213_led


def list_presets() -> None:
    """Print all available presets."""
    print("Available presets:")
    for preset in get_preset_definitions():
        names = ", ".join(preset["aliases"])
        description = preset.get("description", "")
        if description:
            print(f"  {names} - {description}")
        else:
            print(f"  {names}")


def is_valid_rgb(color: str) -> bool:
    """Check if string is a valid 6-character hex RGB code."""
    if len(color) != 6:
        return False
    try:
        int(color, 16)
        return True
    except ValueError:
        return False


def apply_rgb(color: str) -> int:
    """Apply a raw RGB color.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    if not is_valid_rgb(color):
        print(f"Error: Invalid RGB code '{color}'")
        print("Expected 6-character hex code, e.g. ff0000")
        return 1
    return run_g213_led(["-a", color])


def apply_preset_data(preset: dict) -> int:
    """Apply a preset from its data dict.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    if preset["type"] == "solid":
        return run_g213_led(["-a", preset["color"]])
    else:
        exit_code = 0
        for region, color in enumerate(preset["colors"], start=1):
            result = run_g213_led(["-r", str(region), color])
            if result != 0:
                exit_code = result
        return exit_code


def apply_preset(name: str) -> int:
    """Apply a preset by name.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    if name not in PRESETS:
        print(f"Error: Unknown preset '{name}'")
        print("Use --list to see available presets.")
        return 1

    return apply_preset_data(PRESETS[name])


def random_rgb() -> str:
    """Generate a random RGB hex color."""
    return f"{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"


def apply_random_zones(verbose: bool = False) -> int:
    """Apply random colors to each keyboard zone."""
    if verbose:
        print("Random zones mode:")
    exit_code = 0
    for region in range(1, 6):
        color = random_rgb()
        if verbose:
            print(f"  Zone {region}: #{color}")
        result = run_g213_led(["-r", str(region), color])
        if result != 0:
            exit_code = result
    return exit_code


def apply_gradient(left: str, right: str, verbose: bool = False) -> int:
    """Apply a gradient from left color to right color across zones.

    Args:
        left: Hex color for leftmost zone (zone 1)
        right: Hex color for rightmost zone (zone 5)
        verbose: Whether to print zone colors

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    left = left.lstrip("#")
    right = right.lstrip("#")

    if not is_valid_rgb(left):
        print(f"Error: Invalid left color '{left}'")
        return 1
    if not is_valid_rgb(right):
        print(f"Error: Invalid right color '{right}'")
        return 1

    c1 = [int(left[i:i+2], 16) for i in (0, 2, 4)]
    c2 = [int(right[i:i+2], 16) for i in (0, 2, 4)]

    if verbose:
        print(f"Gradient: #{left} -> #{right}")

    exit_code = 0
    for i in range(5):
        t = i / 4  # 0.0 to 1.0
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        color = f"{r:02x}{g:02x}{b:02x}"
        if verbose:
            print(f"  Zone {i + 1}: #{color}")
        result = run_g213_led(["-r", str(i + 1), color])
        if result != 0:
            exit_code = result
    return exit_code


def apply_random(category: str | None = None, verbose: bool = False) -> int:
    """Apply a random preset or effect.

    Args:
        category: Optional category to pick from ('flag', 'color', 'preset', or None for full random)
        verbose: Whether to print what's being applied

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    if category == "flag":
        presets = get_presets_by_category(PresetCategory.FLAG)
        chosen = random.choice(presets)
        if verbose:
            print(f"Random flag: {chosen['aliases'][0]}")
        return apply_preset_data(chosen)

    if category == "color":
        presets = get_presets_by_category(PresetCategory.COLOR)
        chosen = random.choice(presets)
        if verbose:
            print(f"Random color: {chosen['aliases'][0]}")
        return apply_preset_data(chosen)

    if category == "preset":
        presets = get_preset_definitions()
        chosen = random.choice(presets)
        if verbose:
            print(f"Random preset: {chosen['aliases'][0]}")
        return apply_preset_data(chosen)

    # Full random mode - pick something creative
    mode = random.choice(["preset", "random_rgb", "random_zones", "random_gradient"])

    if mode == "preset":
        presets = get_preset_definitions()
        chosen = random.choice(presets)
        if verbose:
            print(f"Random preset: {chosen['aliases'][0]}")
        return apply_preset_data(chosen)

    if mode == "random_rgb":
        color = random_rgb()
        if verbose:
            print(f"Random solid color: #{color}")
        return run_g213_led(["-a", color])

    if mode == "random_zones":
        return apply_random_zones(verbose)

    # random_gradient: smooth gradient between two random colors across zones
    if verbose:
        print("Random gradient:")
    c1 = [random.randint(0, 255) for _ in range(3)]
    c2 = [random.randint(0, 255) for _ in range(3)]
    exit_code = 0
    for i in range(5):
        t = i / 4  # 0.0 to 1.0
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        color = f"{r:02x}{g:02x}{b:02x}"
        if verbose:
            print(f"  Zone {i + 1}: #{color}")
        result = run_g213_led(["-r", str(i + 1), color])
        if result != 0:
            exit_code = result
    return exit_code


def rotate_presets(category: PresetCategory, interval: float, verbose: bool = False) -> int:
    """Rotate through presets of a given category.

    Runs indefinitely until interrupted with Ctrl+C.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    presets = get_presets_by_category(category)
    if not presets:
        print(f"Error: No presets found for category '{category.value}'")
        return 1

    if verbose:
        print(f"Rotating {len(presets)} {category.value} presets (interval: {interval}s)")
        print("Press Ctrl+C to stop")

    try:
        while True:
            for preset in presets:
                if verbose:
                    name = preset["aliases"][0]
                    print(f"  -> {name}")
                apply_preset_data(preset)
                time.sleep(interval)
    except KeyboardInterrupt:
        if verbose:
            print("\nStopped")
        return 0


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="lux",
        description="G213 keyboard lighting preset tool",
    )
    parser.add_argument(
        "preset",
        nargs="?",
        help="Name of preset to apply",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        dest="list_presets",
        help="List all available presets",
    )
    parser.add_argument(
        "--rgbhex", "-rh",
        metavar="RRGGBB",
        help="Apply a raw RGB hex color (e.g. ff0000)",
    )
    parser.add_argument(
        "--rotate", "-r",
        choices=["flags", "colors"],
        help="Rotate through presets of given category",
    )
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=5.0,
        metavar="SECONDS",
        help="Interval between rotations in seconds (default: 5)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output (show preset names during rotation)",
    )
    parser.add_argument(
        "--random", "-R",
        nargs="?",
        const="all",
        choices=["flag", "color", "preset", "all"],
        metavar="CATEGORY",
        help="Random mode: pick random flag/color/preset, or 'all' for surprise (default)",
    )
    parser.add_argument(
        "--gradient", "-g",
        nargs=2,
        metavar=("LEFT", "RIGHT"),
        help="Apply gradient from LEFT to RIGHT hex color across zones",
    )

    args = parser.parse_args()

    if args.list_presets:
        list_presets()
        return 0

    if args.rgbhex:
        return apply_rgb(args.rgbhex.lstrip("#"))

    if args.rotate:
        category = PresetCategory.FLAG if args.rotate == "flags" else PresetCategory.COLOR
        return rotate_presets(category, args.interval, args.verbose)

    if args.random:
        category = None if args.random == "all" else args.random
        return apply_random(category, args.verbose)

    if args.gradient:
        return apply_gradient(args.gradient[0], args.gradient[1], args.verbose)

    if args.preset is None:
        parser.print_help()
        return 1

    return apply_preset(args.preset)


if __name__ == "__main__":
    sys.exit(main())
