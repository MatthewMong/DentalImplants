import bpy
from math import pi
from mathutils import Vector


class InfoPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Dental Implant"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    def distance_vec(point1: Vector, point2: Vector) -> float:
        return (point2 - point1).length
    
    def eulerToDegree(euler):
        euler=euler%(2*pi)
        if euler >pi:
            euler=euler-(2*pi)
        return (euler/(2*pi))*360
#        if euler >=pi:
#            euler=(pi)-euler
#        return ( (euler % (pi)) / (2 * pi) ) * 360
    def average(array, axis):
        sum = 0
        for obj in array:
            sum = sum + InfoPanel.eulerToDegree(obj.rotation_euler[axis])
        sum=sum/len(array)
        return sum
    
    
    def distancecast(obj, context):
#        find distance from implant to bottom of mandible, 
#        note that (0,0,-1) vector is temp until we can get orientation of implant
        scn = context.scene
        Flag = True
        location=obj.location
        print("break")
        result, location, normal, index, object, matrix=scn.ray_cast(context.window.view_layer,(location[0],location[1],location[2]),(0,0,-1))
        point1 = location
        point2 = location
        int=0
        if result is True:
            while result is True and (int<9):
                actuallocation=location
                result, location, normal, index, object, matrix=scn.ray_cast(context.window.view_layer,(location[0],location[1],location[2]-0.1),(0,0,-1))            
                int=int + 1
        return actuallocation

        
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
            row8.label(text="depth: "+str(InfoPanel.distance_vec(obj.location,InfoPanel.distancecast(obj, context))))
        layout.label(text="Appearance")
        row = layout.row(align=True)
        row.operator("object.simple_operator")
            
            
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

def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(InfoPanel)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(InfoPanel)


if __name__ == "__main__":
    register()