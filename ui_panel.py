import bpy
from math import pi
from mathutils import Vector
import math
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
        vector=(-1*x,y,-1*z)
        return(vector)
#        vec = Vector((x, y, z)).normalize()
#        return(vec.negate())
#        return((0,0,-1))
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
        return (euler/(2*pi))*360

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

    """
    Main Function for UI Panel
    """
    def draw(self, context):
        layout = self.layout
        obj = context.object
        if "Dental Implant" in obj.name:
            implants = [obj for obj in context.scene.objects if obj.name.startswith("Dental Implant")]
            row1 = layout.row()
            row1.label(text="Active object is: " + obj.name)
#            row2 = layout.row()
#            row2.label(text="X orientation is: " + str(InfoPanel.eulerToDegree(obj.rotation_euler[0])))
#            row3 = layout.row()
#            row3.label(text="Y orientation is: " + str(InfoPanel.eulerToDegree(obj.rotation_euler[1])))
#            row4 = layout.row()
#            row4.label(text="Z orientation is: " + str(InfoPanel.eulerToDegree(obj.rotation_euler[2])))
            row5 = layout.row()
            row5.label(text="X deviance is: " + str(abs(InfoPanel.eulerToDegree(obj.rotation_euler[0])-InfoPanel.average(implants, 0))))
            row6=layout.row()
            row6.label(text="Y deviance is: " + str(abs(InfoPanel.eulerToDegree(obj.rotation_euler[1])-InfoPanel.average(implants, 1))))
            row7=layout.row()
            row7.label(text="Z deviance is: " + str(abs(InfoPanel.eulerToDegree(obj.rotation_euler[2])-InfoPanel.average(implants, 2))))
            row8=layout.row()
            row8.label(text="depth: "+str(InfoPanel.distance_vec(obj.location,InfoPanel.distancecast(obj, context) )))
        layout.label(text="Appearance")
        row = layout.row(align=True)
        row.operator("object.simple_operator")
            
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
        obj=bpy.data.objects["Mandible"]
        mat = obj.active_material
        if mat.name == "Opaque":
            obj.active_material=bpy.data.materials["Translucent"]
        elif mat.name=="Translucent":
            obj.active_material=bpy.data.materials["Opaque"]
        return {'FINISHED'}

"""
Functions to add or remove to UI
"""
def register():
    print("new test")
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(InfoPanel)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(InfoPanel)


if __name__ == "__main__":
    register()