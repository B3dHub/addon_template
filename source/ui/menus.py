import os

import bpy
from bpy.types import Menu

from ..ops.preset import PRESET_SUBDIR

# Preset list, used standalone or embedded by XX_PT_test_presets. Specifying
# preset_add_operator lets it render the add/remove rows; the operator's
# preset_menu names this class. Shipped presets are not on preset_paths, so they
# are listed explicitly before the user's own.


PRESET_DIR = os.path.join(os.path.dirname(__file__), "../../presets")


def operator_preset(layout, menu: bpy.types.Menu, *, filepath: str, text: str, icon: str = "NONE"):
    """Add a built-in preset entry that executes filepath, relative to presets/."""
    result = layout.operator("script.execute_preset", text=text, icon=icon)
    result.filepath = f"{PRESET_DIR}/{filepath}"
    result.menu_idname = menu


class XX_MT_preset_menu(Menu):
    bl_label = "Presets"
    preset_subdir = PRESET_SUBDIR
    preset_operator = "script.execute_preset"
    preset_add_operator = "xx.test_preset_add"

    def draw(self, context):
        layout = self.layout.column()
        operator_preset(
            layout,
            self.bl_idname,
            filepath="example.py",
            text="Example",
            icon="PRESET",
        )
        layout.separator()
        self.draw_preset(context)


classes = (XX_MT_preset_menu,)


register, unregister = bpy.utils.register_classes_factory(classes)
