import bpy
from bl_operators.presets import AddPresetBase
from bpy.types import Operator

# Add/remove operator. preset_menu names the class AddPresetBase stamps with the
# active preset's name (bl_label); a Menu or the PresetPanel both work.
# Preset folder shared by the operator, panel and menu: AddPresetBase writes here
# and Menu.draw_preset reads here, so all three must agree.
PRESET_SUBDIR = "test_presets"


class XX_OT_test_preset_add(AddPresetBase, Operator):
    bl_label = "Add Preset"
    bl_idname = "xx.test_preset_add"
    preset_menu = "XX_MT_preset_menu"
    preset_subdir = PRESET_SUBDIR
    preset_defines = [
        "prop = bpy.context.scene.test",
    ]
    preset_values = [
        "prop",
    ]


classes = (XX_OT_test_preset_add,)


register, unregister = bpy.utils.register_classes_factory(classes)
