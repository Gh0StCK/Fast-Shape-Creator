bl_info = {
    "name": "Fast Tube Creator",
    "author": "Stanislav Kolesnikov",
    "version": (1, 0, 9),
    "blender": (3, 4, 1),
    "location": "View 3D > Sidebar > FastTools",
    "description": "This add-on helps you quickly create a tube from a mesh, such as a plane or other simple 2D objects.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy
from bpy.types import Operator, Panel
from bpy.props import FloatProperty


class MyPanel(Panel):
    bl_label = "Fast Tube Creator"
    bl_idname = "OBJECT_PT_fast_tube_creator_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FastTools"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.popup_fast_tube_creator", text="Fast Tube Creator")    

class WM_OT_popUp(Operator):
    """Create tube from the mesh"""
    bl_label = "Fast Tube Creator"
    bl_idname = "wm.popup_fast_tube_creator"
    bl_options = {'REGISTER','UNDO'}
    
    #Переменные которые появляются в окне обьявляються здесь
    depth: FloatProperty(name = "Depth (mm)", default = 60)
    
    def execute(self, context):
        
        obj = bpy.context.active_object
        
        #Errors
        assert obj is not None, "No object selected!!!"
        assert bpy.context.object.select_get(), "Object has not selected!!!"
        
        if obj.type == 'MESH':
            bpy.ops.object.convert(target='CURVE')        
        
        curve = obj.data
        
        curve.bevel_mode = 'ROUND'

        d = self.depth
        
        curve.bevel_depth = d/1000

        bpy.ops.object.convert(target='MESH')
        
        obj = None 
        
        return{'FINISHED'}
    
classes = [
    MyPanel,
    WM_OT_popUp
]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)

def unregister():
    for cl in reversed(classes):
        bpy.utils.register_class(cl)

if __name__ == "__main__":
    register()
