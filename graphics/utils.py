import bpy

def getDpiFactor():
    return getDpi() / 72

def getDpi():
    systemPreferences = bpy.context.preferences.system
    retinaFactor = getattr(systemPreferences, "pixel_size", 1)
    return systemPreferences.dpi * retinaFactor
