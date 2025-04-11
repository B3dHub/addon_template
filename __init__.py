bl_info = {
    "name": "Addon",
    "author": "Karan @b3dhub",
    "description": "Description",
    "blender": (3, 3, 0),
    "version": (0, 1, 0),
    "category": "Category",
    "location": "3D Viewport > Sidebar(N-Panel) > Addon",
    "support": "COMMUNITY",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://discord.gg/sdnHHZpWbT",
}


import bpy

from . import source


def register():
    source.register()


def unregister():
    source.unregister()
