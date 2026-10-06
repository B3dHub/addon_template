import bpy
from bl_ui.utils import PresetPanel
from bpy.types import Panel

from ..ops.preset import PRESET_SUBDIR
from ..utils.addon import doc_url, package, tracker_url, version, version_str
from ..utils.icon import icons


class Addon:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Addon"

    def draw_list(self, layout, listtype_name, dataptr, propname, active_propname, rows=4):
        row = layout.row()
        row.scale_y = 1.2
        row.template_list(
            listtype_name,
            "",
            dataptr=dataptr,
            active_dataptr=dataptr,
            propname=propname,
            active_propname=active_propname,
            rows=rows,
            sort_lock=True,
        )
        col = row.column(align=True)
        col.scale_x = 1.1
        return col


# Preset popover for XX_PT_object_mode. Two ownership styles, both rendering the
# same PRESET_SUBDIR list:
#
# Panel-owned (active): the panel holds the preset_* attributes and inherits
# PresetPanel.draw, which renders the list and its add/remove rows.
#
# Menu-owned: uncomment draw() to render XX_MT_preset_menu's contents instead, so
# the menu owns the list and the preset_* attributes above become unused.
class XX_PT_test_presets(PresetPanel, Panel):
    bl_label = "Test Presets"
    preset_subdir = PRESET_SUBDIR
    preset_operator = "script.execute_preset"
    preset_add_operator = "xx.test_preset_add"

    # Menu-owned alternative.
    # def draw(self, context):
    #     layout = self.layout
    #     layout.emboss = "PULLDOWN_MENU"
    #     layout.operator_context = "EXEC_DEFAULT"
    #     layout.menu_contents("XX_MT_preset_menu")


class XX_PT_object_mode(Panel, Addon):
    bl_label = "Object Mode"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def draw_header_preset(self, context):
        XX_PT_test_presets.draw_panel_header(self.layout)

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = True

        prop = context.scene.test

        layout.prop(prop, "name")
        layout.template_icon_view(prop, "preview", show_labels=True, scale=6.0, scale_popup=6.0)
        layout.operator("xx.test")


class XX_PT_edit_mode(Panel, Addon):
    bl_label = "Edit Mode"

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False

        prop = context.scene.test

        layout.prop(prop, "name")
        layout.operator("xx.test")


class XX_PT_help(Panel, Addon):
    bl_label = f"Help - v{version_str}"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header_preset(self, context):
        self.layout.operator("preferences.addon_show", icon="PREFERENCES", emboss=False).module = package

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        if version >= (1, 0, 1):
            col.operator("xx.changelog", icon="RECOVER_LAST")
        col.operator("wm.url_open", text="Documentation", icon="HELP").url = doc_url
        col.operator("wm.url_open", text="Report a Bug", icon="URL").url = tracker_url
        col.operator(
            "wm.url_open", text="Superhive", icon_value=icons["SUPERHIVE"]
        ).url = "https://superhivemarket.com/products/addon"
        col.operator(
            "wm.url_open", text="Gumroad", icon_value=icons["GUMROAD"]
        ).url = "https://b3dhub.gumroad.com/l/addon"


classes = (
    XX_PT_test_presets,
    XX_PT_object_mode,
    XX_PT_edit_mode,
    XX_PT_help,
)


register, unregister = bpy.utils.register_classes_factory(classes)
