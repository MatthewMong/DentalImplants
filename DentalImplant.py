import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import os 
from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator 


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )
    def add_object(self, context):
        scale_x = self.scale.x
        scale_y = self.scale.y
#       get dental implant stl from local files, this should be changed to a proper file within the module
        bpy.ops.import_mesh.stl(filepath=r"C:\Users\ascar\Downloads\dental-implant-9.snapshot.1\Tornillo_imp.STL")
        obj = bpy.context.object
#       set name of object
        obj.name="Dental Implant"
#       set object origin to the geometry origin
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        scene=bpy.context.scene
#       translate implant to the 3d cursor
        obj.matrix_world.translation = scene.cursor.location
        bpy.context.scene.transform_orientation_slots[1].type = 'LOCAL'

    def execute(self, context):

        OBJECT_OT_add_object.add_object(self, context)
        
        return {'FINISHED'}
    
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="add Dental Implant",
        icon='PLUGIN')
        

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="add Dental Implant",
        icon='PLUGIN')