import bpy
from bpy.types import UIList


class XX_UL_demo_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(text="List")


classes = (XX_UL_demo_list,)


register, unregister = bpy.utils.register_classes_factory(classes)
