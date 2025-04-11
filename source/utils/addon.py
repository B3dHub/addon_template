import os
import time
from functools import wraps
from typing import Any, Callable

import bpy

from ... import __package__ as package
from ... import bl_info


def addon_path() -> str:
    """Get the path of the addon directory.

    Returns:
        str: Returns the path of the addon directory.
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def icon_value(icon_name: str) -> int:
    """Get the integer value of a Blender icon by its name.

    Args:
        icon_name: Name of the Blender icon.

    Returns:
        Integer value representing the icon.
    """
    return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[icon_name].value


def preferences() -> dict:
    """Get the preferences of the addon.

    Returns:
        dict: Returns the preferences of the addon.
    """
    return bpy.context.preferences.addons[package].preferences


def tag_redraw(area_type: str = "VIEW_3D", region_type: str = "UI"):
    for window in (w for wm in bpy.data.window_managers for w in wm.windows):
        for region in (
            r for area in window.screen.areas if area.type == area_type for r in area.regions if r.type == region_type
        ):
            region.tag_redraw()


def ui_update_timer() -> float | None:
    """Update the UI in the bpy.app.timers.

    Returns:
        float | None: Returns the input time if the update (redraw) is successful; returns None if a ReferenceError occurs.
    """
    try:
        tag_redraw()
    except ReferenceError:
        return None

    return 0.1


def timer(func: Callable) -> Callable:
    """Decorator to measure the time taken by a function to execute.

    Args:
        func: Function to be measured.

    Returns:
        Function: Returns the decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start: float = time.perf_counter()
        result: Any = func(*args, **kwargs)
        end: float = time.perf_counter()
        print(f"{func.__name__} took {end - start:.2f} seconds to execute.")

        return result

    return wrapper


version = bl_info["version"]
version_str = ".".join(map(str, bl_info["version"]))
