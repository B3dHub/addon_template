from . import preset, test


def register():
    preset.register()
    test.register()


def unregister():
    preset.unregister()
    test.unregister()
