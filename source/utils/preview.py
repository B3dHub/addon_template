import os
import re

from bpy.utils import previews


def enum_previews(self, context):
    """EnumProperty callback"""
    directory = os.path.join(os.path.dirname(__file__), "../../previews")
    pcoll = preview_collections["previews"]

    if directory == pcoll.previews_dir:
        return pcoll.previews

    enum_items = []
    if os.path.exists(directory):
        for i, name in enumerate(fn for fn in os.listdir(directory) if fn.lower().endswith(".png")):
            filepath = os.path.join(directory, name)
            thumb = pcoll.get(name) or pcoll.load(name, filepath, "IMAGE")
            item_name = re.sub(r"\d+ ", "", name).replace(".png", "")
            enum_items.append((item_name, item_name, "", thumb.icon_id, i))

    pcoll.previews = enum_items
    pcoll.previews_dir = directory
    return pcoll.previews


# We can store multiple preview collections here,
# however in this example we only store "main"
preview_collections = {}


def register():
    # Example Previews
    pcoll = previews.new()
    pcoll.previews_dir = ""
    pcoll.previews = ()
    preview_collections["previews"] = pcoll


def unregister():
    for pcoll in preview_collections.values():
        previews.remove(pcoll)

    preview_collections.clear()
