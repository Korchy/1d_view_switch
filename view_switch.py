# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_view_switch

import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from mathutils import Matrix

bl_info = {
    "name": "Viewswitch",
    "description": "Save and restore the 3D Viewport position",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Viewswitch",
    "doc_url": "https://github.com/Korchy/1d_view_switch",
    "tracker_url": "https://github.com/Korchy/1d_view_switch",
    "category": "All"
}


# MAIN CLASS

class Viewswitch:

    _stored_viewport_position = None
    _viewport_attributes = [
        'is_perspective', 'show_sync_view', 'use_box_clip', 'view_distance', 'view_matrix', 'view_perspective'
    ]

    @classmethod
    def store_position(cls, context):
        # store current 3D Viewport position
        r3d = cls.get_r3d(context=context)
        copy_if_possible = lambda x: x.copy() if hasattr(x, 'copy') else x
        cls._stored_viewport_position = {
            attr: copy_if_possible(getattr(r3d, attr)) for attr in cls._viewport_attributes
        }
        print(cls._stored_viewport_position)

    @classmethod
    def restore_position(cls, context):
        # return to previously stored 3D Viewport position
        r3d = cls.get_r3d(context=context)
        stored_position_date = cls._stored_viewport_position if cls._stored_viewport_position else cls.default()
        for attr in cls._viewport_attributes:
            if attr in stored_position_date:
                setattr(r3d, attr, stored_position_date[attr])

    @staticmethod
    def get_r3d(context):
        # get region_3d from 3D Viewport area
        area = next((area for area in context.screen.areas if area.type == 'VIEW_3D'), None)
        if area:
            return area.spaces[0].region_3d

    @staticmethod
    def default():
        # return default 3D Viewport position (Num1)
        return {
            'view_matrix': Matrix(
                (
                    (1.0, -0.0, 0.0, -0.13593268394470215),
                    (0.0, -1.3435885648505064e-07, 1.0000001192092896, -0.03936590999364853),
                    (-0.0, -1.0000001192092896, -1.3435885648505064e-07, -0.9089528322219849),
                    (0.0, 0.0, 0.0, 1.0)
                )
            )
        }

    @staticmethod
    def ui(layout, context):
        # ui panel
        row = layout.row()
        row.operator(
            operator='viewswitch.store_viewport_position',
            icon='UNPINNED',
            text='Store'
        )
        row.operator(
            operator='viewswitch.restore_viewport_position',
            icon='FILE_PARENT',
            text='Restore'
        )


# OPERATORS

class Viewswitch_OT_store_viewport_position(Operator):
    bl_idname = 'viewswitch.store_viewport_position'
    bl_label = 'Store viewport position'
    bl_description = 'Store 3D Viewport position to memory'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        Viewswitch.store_position(
            context=context
        )
        return {'FINISHED'}


class Viewswitch_OT_restore_viewport_position(Operator):
    bl_idname = 'viewswitch.restore_viewport_position'
    bl_label = 'Restore viewport position'
    bl_description = 'Return to previously stored 3D Viewport position'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        Viewswitch.restore_position(
            context=context
        )
        return {'FINISHED'}


# PANELS

class Viewswitch_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Viewswitch'
    bl_category = '1D'

    def draw(self, context):
        Viewswitch.ui(
            layout=self.layout,
            context=context
        )


# KEYMAPS

class ViewswitchKeyMap:

    _keymaps = []

    @classmethod
    def register(cls, context):
        # add new key map
        if context.window_manager.keyconfigs.addon:
            keymap = context.window_manager.keyconfigs.addon.keymaps.new(name='Window')
            # add keys
            keymap_item = keymap.keymap_items.new(
                idname='viewswitch.store_viewport_position',
                type='NUMPAD_ASTERIX',
                value='PRESS'
            )
            cls._keymaps.append((keymap, keymap_item))
            keymap_item = keymap.keymap_items.new(
                idname='viewswitch.restore_viewport_position',
                type='NUMPAD_ASTERIX',
                value='PRESS',
                shift=True
            )
            cls._keymaps.append((keymap, keymap_item))

    @classmethod
    def unregister(cls):
        for keymap, keymap_item in cls._keymaps:
            keymap.keymap_items.remove(keymap_item)
        cls._keymaps.clear()


# REGISTER

def register(ui=True):
    register_class(Viewswitch_OT_store_viewport_position)
    register_class(Viewswitch_OT_restore_viewport_position)
    ViewswitchKeyMap.register(context=bpy.context)
    if ui:
        register_class(Viewswitch_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(Viewswitch_PT_panel)
    ViewswitchKeyMap.unregister()
    unregister_class(Viewswitch_OT_restore_viewport_position)
    unregister_class(Viewswitch_OT_store_viewport_position)


if __name__ == "__main__":
    register()
