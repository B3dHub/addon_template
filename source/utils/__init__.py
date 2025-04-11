from . import icon, manual, prefs, preview, props


def register():
    icon.register()
    preview.register()
    props.register()
    manual.register()
    prefs.register()


def unregister():
    icon.unregister()
    preview.unregister()
    props.unregister()
    manual.unregister()
    prefs.unregister()
