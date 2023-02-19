bl_info = {
    "name": "Fast Shape Creator",
    "author": "Stanislav Kolesnikov",
    "version": (1, 1, 1),
    "blender": (3, 4, 1),
    "location": "View 3D > Sidebar > FastTools",
    "description": "Create 3D shape from simple objects like circle and any 2D objects",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


import bpy
import bmesh
from  mathutils import Vector
from bpy.types import Panel, Operator
from bpy.props import FloatProperty

class WM_OT_Panel(Panel):
    bl_label = "Fast Shape Creator"
    bl_idname = "OBJECT_PT_fast_shape_creator_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FastTools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.popup_fast_shape_creator", text="Fast Shape Creator")
            
    
class WM_OT_popUp(Operator):
    """Create tube from the mesh"""
    bl_label = "Fast Shape Creator"
    bl_idname = "wm.popup_fast_shape_creator"
    bl_options = {'REGISTER','UNDO'}
    
    #Переменные которые появляются в окне обьявляються здесь
    heightZ: FloatProperty(name = "Height Z", default = .2)
    
    def execute(self, context):
        '''Create shape from flat objects'''
        if bpy.context.active_object and bpy.context.object.select_get():
        
            # Select the vertex you want to use for extrusion
            bop = bpy.ops
            bom = bop.mesh

            bop.object.mode_set(mode='EDIT')
            bom.select_mode(type='VERT')
            bom.select_all(action='SELECT')

            # Get the selected vertex and its local matrix
            obj = bpy.context.edit_object
            obd = obj.data
            bm = bmesh.from_edit_mesh(obd)

            vertex = [v for v in bm.verts if v.select][0]

            # Extrude the selected vertex upward
            local_z = obj.matrix_world.to_quaternion() @ Vector((0, 0, self.heightZ))        

            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": local_z})

            # Fill the holes
            bom.select_non_manifold()
            selected_verts = [v for v in bm.verts if v.select]

            if selected_verts is not None:
                bom.edge_face_add()
                
            bom.normals_make_consistent(inside=False)
            bop.object.mode_set(mode='OBJECT')
            obj.select_set(True)
            bm.free()
        else:
            assert not bpy.context.object.select_get() is not None, "Selecte the object!!!"
        
        return{'FINISHED'}

    
classes = [
    WM_OT_Panel,
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