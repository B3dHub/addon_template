import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import PropertyGroup

from .preview import enum_previews


class XX_PG_test(PropertyGroup):

    name: StringProperty(default="Test")
    preview: EnumProperty(items=enum_previews)


classes = (XX_PG_test,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.test = bpy.props.PointerProperty(type=XX_PG_test)


def unregister():
    del bpy.types.Scene.test

    for cls in classes:
        bpy.utils.unregister_class(cls)
