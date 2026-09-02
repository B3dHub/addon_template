from . import lists, menus, panels


def register():
    lists.register()
    menus.register()
    panels.register()


def unregister():
    lists.unregister()
    menus.unregister()
    panels.unregister()
