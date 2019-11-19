'''
Copyright (C) 2016 Jacques Lucke
mail@jlucke.com

Created by Jacques Lucke

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''



bl_info = {
    "name":        "Code Autocomplete",
    "description": "Autocompletion, templates and addon development tools for the text editor.",
    "author":      "Jacques Lucke",
    "version":     (2, 0, 0),
    "blender":     (2, 80, 0),
    "location":    "Text Editor",
    "category":    "Development"
    }



# load and reload submodules
##################################

# append jedi package path to make 'import jedi' available
import os, sys
sys.path.append(os.path.join(__path__[0], "jedi"))

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())



# register
##################################

import bpy

addon_keymaps = []
def register_keymaps():
    global addon_keymaps
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name = "Text", space_type = "TEXT_EDITOR")
    kmi = km.keymap_items.new("code_autocomplete.select_whole_string", type = "Y", value = "PRESS", ctrl = True)
    kmi = km.keymap_items.new("wm.call_menu", type = "SPACE", value = "PRESS", ctrl = True)
    kmi.properties.name = "code_autocomplete_insert_template_menu"
    kmi = km.keymap_items.new("wm.call_menu", type = "TAB", value = "PRESS", ctrl = True)
    kmi.properties.name = "code_autocomplete_select_text_block"
    addon_keymaps.append(km)

def unregister_keymaps():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

from . addon_development import AddonDevelopmentSceneProperties
from . quick_operators import register_menus, unregister_menus
from . code_templates.base import draw_template_menu


classes = (
    # code_autocomplete_insert_template_menu,
    # code_autocomplete.build_script,
    # code_autocomplete.correct_whitespaces,
    # code_autocomplete.convert_addon_indentation,
    # SolveWhitespaceInconsistency,
    # SelectWholeString,
    # ConvertFileIndentation,
    SelectTextBlockMenu,
    OpenTextBlock,
    CompletionProviders ,
    ContextBoxProperties,
    DescriptionBoxProperties,
    AddonPreferences,
    TextBlock,
    Provider,
    Completion,
    JediCompletion,
    JediCompletionProvider,
    OperatorCompletion,
    ParameterCompletion,
    OperatorCompletionProvider,
    WordCompletion,
    WordCompletionProvider,
    BlockEvent,
    AutocompleteHandler,
    ContextUI,
    ActiveTextArea,
    AddonDeveloperPanel,
    AddonFilesPanel,
    SetDirectoryVisibility,
    RunAddon,
    RestartBlender,
    NewFile,
    NewDirectory,
    FileMenuOpener,
    OpenFile,
    OpenExternalFileBrowser,
    RenameFile,
    DeleteFile,
    SaveFiles,
    ExportAddon,
    ConvertAddonIndentation,
    FindExistingAddon,
    MakeAddonNameValid,
    CreateNewAddon,
    AddonDevelopmentSceneProperties,
    TextBox,
    ListItem,
    ListBox,
    Rectangle,
)

def register():
    for i in classes:
        bpy.utils.register_class(i)
    register_keymaps()
    register_menus()
    bpy.types.TEXT_MT_templates.append(draw_template_menu)
    bpy.types.Scene.addon_development: bpy.props.PointerProperty(name = "Addon Development", type = AddonDevelopmentSceneProperties)

    print("Registered Code Autocomplete with {} modules.".format(len(modules)))

def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
    unregister_keymaps()
    unregister_menus()
    bpy.types.TEXT_MT_templates.remove(draw_template_menu)

    print("Unregistered Code Autocomplete")
