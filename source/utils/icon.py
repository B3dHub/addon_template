import os

from bpy.utils import previews

preview_collections = {}
icons = {}


def load_icons_from_dir(pcoll, directory):
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(".png"):
            pcoll.load(os.path.splitext(entry.name)[0], entry.path, "IMAGE")
        elif entry.is_dir():
            load_icons_from_dir(pcoll, entry.path)


def register():
    if "icons" in preview_collections:
        unregister()

    pcoll = previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "../../icons")
    load_icons_from_dir(pcoll, icons_dir)
    icons.update({key: value.icon_id for key, value in pcoll.items()})
    preview_collections["icons"] = pcoll


def unregister():
    for pcoll in preview_collections.values():
        previews.remove(pcoll)

    preview_collections.clear()
