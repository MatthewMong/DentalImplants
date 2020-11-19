bl_info = {
    "name": "Dental Implants",
    "author": "Matthew Mong",
    "version": (0, 2),
    "blender": (2, 90, 1),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Dental Implants",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}
import bpy
import sys
from math import pi
from mathutils import Vector
import math
import bpy_extras.io_utils
import re
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import os 
from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
"""
Main UI component
Data->Properties->Object Properties->Dental Implant
"""
class InfoPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Dental Implant"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
#    Helper functions for the class
    """
    Convert from radians to unit vector, someone please look over this im bad at math
    """

    def euler_to_vector(obj):
        euler=obj.rotation_euler
        z=math.cos(euler[0])*math.cos(euler[1])
        y=math.sin(euler[0])*math.cos(euler[1])
        x=math.sin(euler[1])
        vector=(-1*x,-1*y,-1*z)
        print(vector)
        return(vector)

    """
    Calculates distance between two points which are represented as vectors
    Note: minimal inaccuracy due to fp math
    """
    def distance_vec(point1, point2) -> float:
        ret = "?"
        if (point1 is not None )and (point2 is not None):
            ret = (point2 - point1).length
        return ret
    """
    takes euler and returns degree
    Note: This specifically returns an angle that is =< 180 and will return 
    positive and negative numbers for orientation sake
    """
    def eulerToDegree(euler):
        euler=euler%(2*pi)
        if euler >pi:
            euler=euler-(2*pi)
        return str(round(((euler/(2*pi))*360),2))

    """
    Basic convenience function to calculate average of an array
    Note: we may want to ask Wong if she wants mean or median
    """
    def average(array, axis):
        sum = 0
        for obj in array:
            sum = sum + InfoPanel.eulerToDegree(obj.rotation_euler[axis])
        sum=sum/len(array)
        return sum
    
    """
    Get distance from center of implant to bottom of mandible
    Note: This is optimized for cpu usage instead of RAM
    Consistently send a ray cast down until an object is hit, and then send another ray cast
    repeat until no object is hit, we take the last raycast spot as the bottom of mandible
    
    Bug: returns 0 when object is being moved not sure why ye
    """
    def distancecast(obj, context):
#        find distance from implant to bottom of mandible, 
#        note that it currently lists depth of 2.64 because thats the bottom of the screw
        scn = context.scene
        Flag = True
        location=obj.location
        result, location, normal, index, object, matrix=scn.ray_cast(context.window.view_layer,(location[0],location[1],location[2]),InfoPanel.euler_to_vector(obj))
        actuallocation = location
        point1 = location
        point2 = location
        int=0
        if result is True:
#            the int < 10 is just to prevent an infinite loop/crash if theres a really nasty mandible
            while result is True and (int<10):
                try:
                    actuallocation=location
                    result, location, normal, index, object, matrix=scn.ray_cast(context.window.view_layer,(location[0],location[1],location[2]-0.1),InfoPanel.euler_to_vector(obj))            
                except:
                    print("error")
                int=int + 1
        if int <= 1:
            actuallocation = None
        return actuallocation
    
    def horizontal_distance(obj, context, implants):
        return_array=[]
        far = None
        name = None
        if len(implants)>1:
            location = obj.location
            for implant in implants:
                if implant is not obj:
                    imploc = implant.location
                    length = math.sqrt(((location[0]-imploc[0])**2)+((location[1]-imploc[1])**2)+((location[2]-imploc[2])**2))
                    return_array.append([implant.name, round(length,3)])
        else:
            return_array.append(["Nothing", 0])
        return return_array
    
    """
    Main Function for UI Panel
    """
    def draw(self, context):
        layout = self.layout
        layout.label(text="Active object is: " + context.active_object.name)
        brow = layout.row(align=True)
        brow.operator("object.simple_operator")
        brow3 = layout.row(align=True)
        brow3.operator("object.save")
        brow2 = layout.row(align=True)
        brow2.operator("object.duplicate")
        brow4= layout.row(align=True)
        brow4.operator("object.importtooth")
#        brow5 = layout.row(align = True)
#        brow5.operator("mesh.add_object")
#        if len([obj for obj in context.scene.objects if obj.name.startswith("Dental Implant")]) >0:
#            layout.row(align=True)
#            layout.operator("OBJECT_PT_select")

class ObjectSelectPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_select"
    bl_label = ""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Implant Orientations")

    def draw(self, context):
        implants = [obj for obj in context.scene.objects if obj.name.startswith("Dental Implant")]
        layout = self.layout
        obj = bpy.context.object
        for implant in implants:
            box = layout.box()
            box.prop(implant, "rotation_euler", text=implant.name)
            if "Dental Implant" in obj.name:
                box.label(text="Difference to current implant:")
                box.label(text="X:"+InfoPanel.eulerToDegree(implant.rotation_euler[0]-obj.rotation_euler[0])+" Y:"+InfoPanel.eulerToDegree(implant.rotation_euler[1]-obj.rotation_euler[1])+" Z:"+InfoPanel.eulerToDegree(implant.rotation_euler[2]-obj.rotation_euler[2]))
"""
Main Class for importing Dental Implant Mesh
"""
class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Dental Implant"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )
    def distance_vec(point1: Vector, point2: Vector) -> float:
        """Calculate distance between two points.""" 
        return (point2 - point1).length
    
    
    def add_object(self, context):
        distances=[]
        keystone=1024
        name=None
        scale_x = self.scale.x
        scale_y = self.scale.y
#       get dental implant stl from local files, this should be changed to a proper file within the module
#        bpy.ops.import_mesh.stl(filepath=r"C:\Users\ascar\OneDrive\Desktop\DentalImplants\Pipe.STL")
        bpy.ops.mesh.primitive_cylinder_add()
        obj = bpy.context.object
        obj.scale=(2,2,50)
#       set name of object
        obj.name="Dental Implant"
#       set object origin to the geometry origin
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        scene=bpy.context.scene
#       translate implant to the 3d cursor
        obj.matrix_world.translation = scene.cursor.location
        bpy.ops.transform.select_orientation(orientation='LOCAL')
        obj.constraints.new(type="SHRINKWRAP")
        for object in bpy.data.objects:
            if "Dental Implant" not in object.name:
                objloc=object.closest_point_on_mesh(scene.cursor.location)
                print(objloc)
                print(scene.cursor.location)
                dist=OBJECT_OT_add_object.distance_vec(objloc[1], scene.cursor.location)
                distances.append([object.name, dist])
        for pair in distances:
            if pair[1]<keystone:
                keystone=pair[1]
                name=pair[0]
        obj.constraints["Shrinkwrap"].target=bpy.data.objects[name]
        obj.constraints["Shrinkwrap"].shrinkwrap_type = 'PROJECT'
        obj.constraints["Shrinkwrap"].use_project_opposite=True
        obj.constraints["Shrinkwrap"].project_axis_space = 'WORLD'

        
        
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
        default='folder', 
        options={'HIDDEN'} 
    ) 
    
    some_boolean: BoolProperty( 
        name='Do a thing', 
        description='Do a thing with the file you\'ve selected', 
        default=True, 
    )
    
    def clean(self, context):
        for o in bpy.context.scene.objects:
            o.select_set(True)
        bpy.ops.object.delete()
    """
    Import Mandible STL and apply materials for transparency options
    """
    def add_mandible(self, context, mat, location):
        bpy.ops.import_mesh.stl(filepath=location)
        obj = bpy.context.selected_objects[0]
        obj.name="Mandible"
        obj.data.materials.append(mat)
        obj.active_material = mat
    def add_maxilla(self, context, mat, location):
        bpy.ops.import_mesh.stl(filepath=location)
        obj = bpy.context.selected_objects[0]
        obj.name="Maxilla"
        obj.data.materials.append(mat)
        obj.active_material = mat
    
    def add_resection(self, context, mat, location):
        bpy.ops.import_mesh.stl(filepath=location)
        obj = bpy.context.selected_objects[0]
        obj.name="Resection"
        obj.data.materials.append(mat)
        obj.active_material = mat
        
    """
    Driver function for class, opens file browser (limited to STL files)
    triggers add_mandible function and frames mandible
    Note: sometimes the frame will swap back if you tab through layouts im not sure why
    """
    def execute(self, context): 
        """Do something with the selected file(s)."""
        OT_TestOpenFilebrowser.clean(self, context)
        for material in bpy.data.materials:
            material.user_clear()
            bpy.data.materials.remove(material)
        mat = bpy.data.materials.new(name="Translucent")
#        last number in array defines alpha which is how we control transparency
        mat.diffuse_color = (1,1,1,0.8) 
        mat2 = bpy.data.materials.new(name="Opaque")
        mat2.diffuse_color = (1,1,1,1)  
        filename, extension = os.path.splitext(self.filepath)
        print('Selected file:', self.filepath)
        self.location=self.filepath
        for entry in os.scandir(self.location):
            if entry.is_file() and re.search("mandible",entry.name, re.IGNORECASE):
                OT_TestOpenFilebrowser.add_mandible(self, context, mat2, self.location+entry.name)
            elif entry.is_file() and re.search("resection",entry.name, re.IGNORECASE):
                OT_TestOpenFilebrowser.add_resection(self, context, mat, self.location+entry.name)
            elif entry.is_file() and re.search("maxilla",entry.name, re.IGNORECASE):
                OT_TestOpenFilebrowser.add_maxilla(self, context, mat2, self.location+entry.name)            
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.view3d.localview(frame_selected=True)
        return {'FINISHED'}             
"""
Transparency Button, right now it is hardcoded to mess with Mandible but should be changed to take 
a mesh of our choosing
Works by swapping the currently applied material to the mesh, note that the materials are defined on 
mandible mesh import
""" 
class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Change Transparency"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        objects = bpy.context.scene.objects
        for obj in objects:
            if "Dental Implant" not in obj.name:
                mat = obj.active_material
                if mat.name == "Opaque":
                    obj.active_material=bpy.data.materials["Translucent"]
                elif mat.name=="Translucent":
                    obj.active_material=bpy.data.materials["Opaque"]
        return {'FINISHED'}


class Duplicate(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.duplicate"
    bl_label = "Duplicate"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        if "Dental Implant" in obj.name:
                ob = obj.copy()
                bpy.context.collection.objects.link(ob)
                bpy.context.view_layer.objects.active = ob
                obj.select_set(False)
                
        return {'FINISHED'}

class Save(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Tooltip"""
    bl_idname = "object.save"
    bl_label = "Save"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        print(self.filepath)
        for object in bpy.context.view_layer.objects:
            if "Dental Implant" in object.name:
                object.select_set(state=True)
                bpy.context.view_layer.objects.active = object
        if self.filepath.endswith(".stl") is False:
            self.filepath=self.filepath+".stl"
        bpy.ops.export_mesh.stl(filepath=self.filepath,check_existing=True, use_selection=True)
        return {'FINISHED'}
    
class ImportTooth(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Tooltip"""
    bl_idname = "object.importtooth"
    bl_label = "Import Tooth"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.import_mesh.stl(filepath=self.filepath,filter_glob="*.stl")
        obj = bpy.context.selected_objects[0]
        obj.data.materials.append(bpy.data.materials.get("Opaque"))
        obj.active_material=bpy.data.materials.get("Opaque")
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        scene=bpy.context.scene
        obj.matrix_world.translation = scene.cursor.location
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
Functions to add or remove to UI
"""
def register():
    print("new test")
    bpy.utils.register_class(ObjectSelectPanel)
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(Duplicate)
    bpy.utils.register_class(Save)
    bpy.utils.register_class(ImportTooth)
    bpy.utils.register_class(InfoPanel)
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_class(OT_TestOpenFilebrowser)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_editor_menus.append(add_mandible_button)
    bpy.types.VIEW3D_MT_editor_menus.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(ObjectSelectPanel)
    bpy.utils.unregister_class(Duplicate)
    bpy.utils.unregister_class(Save)
    bpy.utils.unregister_class(ImportTooth)
    bpy.utils.unregister_class(InfoPanel)
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_editor_menus.remove(add_object_button)
    bpy.types.VIEW3D_MT_editor_menus.remove(add_mandible_button)


if __name__ == "__main__":
    register()