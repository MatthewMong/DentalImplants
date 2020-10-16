bl_info = {
    "name": "Dental Implants",
    "author": "Matthew Mong",
    "version": (0, 1),
    "blender": (2, 90, 1),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Dental Implants",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import os 
from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator 

"""
Main Class for importing Dental Implant Mesh
"""
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

"""
Main Class for Importing Mandible
Note: uses built in blender file browser
"""
class OT_TestOpenFilebrowser(Operator, ImportHelper): 
    bl_idname = "io.importobj"  
    bl_label = "Import Mandible"
    location = ""
    filter_glob: StringProperty( 
        default='*.stl', 
        options={'HIDDEN'} 
    ) 
    
    some_boolean: BoolProperty( 
        name='Do a thing', 
        description='Do a thing with the file you\'ve selected', 
        default=True, 
    ) 
    """
    Import Mandible STL and apply materials for transparency options
    """
    def add_mandible(self, context):
        bpy.ops.import_mesh.stl(filepath=self.location)
        obj = bpy.context.object
        obj.name="Mandible" 
        mat = bpy.data.materials.new(name="Translucent")
#        last number in array defines alpha which is how we control transparency
        mat.diffuse_color = (1,1,1,0.2) 
        obj.data.materials.append(mat)
        obj.active_material = mat
        mat2 = bpy.data.materials.new(name="Opaque")
        mat2.diffuse_color = (1,1,1,1) 
        
    """
    Driver function for class, opens file browser (limited to STL files)
    triggers add_mandible function and frames mandible
    Note: sometimes the frame will swap back if you tab through layouts im not sure why
    """
    def execute(self, context): 
        """Do something with the selected file(s).""" 
        filename, extension = os.path.splitext(self.filepath)
        print('Selected file:', self.filepath)
        self.location=self.filepath
        print(self.location)
        OT_TestOpenFilebrowser.add_mandible(self, context)
        bpy.ops.view3d.localview(frame_selected=True)
        return {'FINISHED'} 

"""
Some Helper functions, mostly button operators
"""
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="add Dental Implant",
        icon='PLUGIN')

def add_mandible_button(self, context):
    self.layout.operator(
        OT_TestOpenFilebrowser.bl_idname,
        text="add Mandible",
        icon='PLUGIN')

# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://github.com/MatthewMong/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "DentalImplants"),
    )
    return url_manual_prefix, url_manual_mapping


"""
Boilerplate add and remove buttons
"""
def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(OT_TestOpenFilebrowser)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)
    bpy.types.VIEW3D_MT_mesh_add.append(add_mandible_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_mandible_button)



if __name__ == "__main__":
    register()
