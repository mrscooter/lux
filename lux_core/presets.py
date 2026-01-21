"""Preset definitions for G213 keyboard lighting."""

from enum import Enum


class PresetCategory(Enum):
    SPECIAL = "special"
    FLAG = "flag"
    COLOR = "color"


# Core preset definitions with aliases
# To add a new alias, just append to the "aliases" list
_PRESET_DEFINITIONS = [
    # Special
    {
        "aliases": ["magic-green", "i-am-hacker"],
        "category": PresetCategory.SPECIAL,
        "type": "solid",
        "color": "55ff12",
    },
    {
        "aliases": ["rainbow"],
        "category": PresetCategory.SPECIAL,
        "type": "regions",
        "colors": ["ff0000", "ff8000", "ffff00", "00ff00", "0000ff"],
    },

    # Flags
    {
        "aliases": ["Slovakia", "Slovensko", "slovakia", "slovensko"],
        "description": "Slovak flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["ffffff", "0000ff", "0000ff", "ff0000", "ff0000"],
    },
    {
        "aliases": ["USA", "Murica", "'Merica", "FREEDOM", "usa", "murica", "'merica", "freedom"],
        "description": "American flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["bf0a30", "ffffff", "002868", "ffffff", "bf0a30"],
    },
    {
        "aliases": ["Vatican", "Vaticano", "vatican", "vaticano"],
        "description": "Vatican flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["ffe135", "ffe135", "ffffff", "ffffff", "ffffff"],
    },
    {
        "aliases": ["Poland", "Polska", "poland", "polska"],
        "description": "Polish flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["ffffff", "ffffff", "ffffff", "dc143c", "dc143c"],
    },
    {
        "aliases": ["Croatia", "Hrvatska", "croatia", "hrvatska"],
        "description": "Croatian flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["ff0000", "ffffff", "ffffff", "ffffff", "171796"],
    },
    {
        "aliases": ["Bhutan", "འབྲུག་ཡུལ", "bhutan"],
        "description": "Bhutanese flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["ffd520", "ffd520", "ffd520", "ff4e12", "ff4e12"],
    },
    {
        "aliases": ["Mongolia", "Монгол", "ᠮᠣᠩᠭᠣᠯ", "mongolia"],
        "description": "Mongolian flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["c4272f", "015197", "015197", "015197", "c4272f"],
    },
    {
        "aliases": ["Uganda", "Natural-Obligations", "uganda", "natural-obligations"],
        "description": "Ugandan flag",
        "category": PresetCategory.FLAG,
        "type": "regions",
        "colors": ["000000", "fcdc04", "d90000", "000000", "fcdc04"],
    },

    # Royal colors
    {
        "aliases": ["royal-blue"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "4169e1",
    },
    {
        "aliases": ["emerald-green", "emerald"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "50c878",
    },
    {
        "aliases": ["bordeaux"],
        "description": "dark wine red",
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "800020",
    },
    {
        "aliases": ["royal-red"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "c41e3a",
    },
    {
        "aliases": ["royal-purple"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "7851a9",
    },
    {
        "aliases": ["gold"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "ffd700",
    },
    {
        "aliases": ["sapphire"],
        "description": "deep jewel blue",
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "0f52ba",
    },
    {
        "aliases": ["ruby"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "e0115f",
    },
    {
        "aliases": ["amethyst"],
        "description": "purple quartz",
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "9966cc",
    },
    {
        "aliases": ["ivory"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "fffff0",
    },
    {
        "aliases": ["burgundy"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "722f37",
    },
    {
        "aliases": ["navy"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "000080",
    },
    {
        "aliases": ["bronze"],
        "category": PresetCategory.COLOR,
        "type": "solid",
        "color": "cd7f32",
    },
]


def _build_presets():
    """Build PRESETS dict from definitions, expanding all aliases."""
    presets = {}
    for definition in _PRESET_DEFINITIONS:
        # Extract preset data (everything except aliases)
        preset_data = {k: v for k, v in definition.items() if k != "aliases"}
        # Register under each alias
        for alias in definition["aliases"]:
            presets[alias] = preset_data
    return presets


def get_preset_definitions():
    """Return raw preset definitions for listing with aliases grouped."""
    return _PRESET_DEFINITIONS


def get_presets_by_category(category: PresetCategory) -> list[dict]:
    """Return all preset definitions matching the given category."""
    return [p for p in _PRESET_DEFINITIONS if p.get("category") == category]


PRESETS = _build_presets()
