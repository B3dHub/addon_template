from typing import List

import bpy
from bpy.types import UILayout

addon_keymaps = []


def get_keymap_items(idname: str) -> List[bpy.types.KeyMapItem]:
    """Get all keymap items that match the given idname.

    Args:
        idname (str): The idname of the keymap item.

    Returns:
        List[bpy.types.KeyMapItem]: Returns a list of keymap items that match the given idname.
    """
    matching_keymap_items = []
    kc = bpy.context.window_manager.keyconfigs.user
    for addon_km in addon_keymaps:
        km = kc.keymaps[addon_km.name].active()
        matching_keymap_items.extend(kmi for kmi in km.keymap_items if kmi.idname == idname)
    return matching_keymap_items


def convert_keymap_item_to_string(keymap_item: bpy.types.KeyMapItem) -> str:
    """Convert a keymap item to a string.

    Args:
        keymap_item (bpy.types.KeyMapItem): The keymap item to convert.

    Returns:
        str: Returns the keymap item as a string.
    """
    text = keymap_item.to_string(compact=True)

    if keymap_item.map_type == "KEYBOARD":
        return " + ".join(text.split(" "))
    elif keymap_item.map_type == "MOUSE":
        *split, last = text.split(" ")
        split.append(f"{UILayout.enum_item_name(keymap_item, 'value', keymap_item.value)} ({last})")
        return " + ".join(split)


def register():
    kc = bpy.context.window_manager.keyconfigs.addon

    if kc is not None:
        # 3D View
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        addon_keymaps.append(km)
        # km.keymap_items.new("xx.test", type="LEFTMOUSE", value="CLICK", shift=False, ctrl=False, alt=False, head=True)


def unregister():
    kc = bpy.context.window_manager.keyconfigs.addon

    if kc is not None:
        for km in addon_keymaps:
            kc.keymaps.remove(km)

    addon_keymaps.clear()
