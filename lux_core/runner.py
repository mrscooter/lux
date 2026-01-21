"""Execution logic for g213-led commands."""

import subprocess


def run_g213_led(commands: list[str]) -> int:
    """Run g213-led with the given command arguments.

    Args:
        commands: List of command-line arguments for g213-led.

    Returns:
        Exit code from the g213-led process.
    """
    try:
        result = subprocess.run(
            ["g213-led"] + commands,
            check=False,
        )
        return result.returncode
    except FileNotFoundError:
        print("Error: g213-led not found. Please install it first.")
        return 1
