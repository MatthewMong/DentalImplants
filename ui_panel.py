import bpy


class InfoPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Dental Implant"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if "Dental Implant" in obj.name:
            row1 = layout.row()
            row1.label(text="Active object is: " + obj.name)
            row2 = layout.row()
            row2.label(text="Orientation is: " + str(obj.rotation_euler[0]))
        elif "Mandible" in obj.name:
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
        obj=bpy.context.object
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