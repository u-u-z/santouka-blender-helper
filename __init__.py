import bpy
import bmesh
from mathutils import Vector, Matrix


bl_info = {
    "name": "山头火工具箱",
    "blender": (3, 3, 1),
    "category": "Object",
}

class CustomProperties(bpy.types.PropertyGroup):    
    thinning_float: bpy.props.FloatProperty(name="减薄/增厚量")

class MessageBox(bpy.types.Operator):
    icon: bpy.props.StringProperty(name="Icon", default="ERROR")
    message: bpy.props.StringProperty(name="Message", default="")
    
    bl_idname = "message.message_box"
    bl_label = "提示"
    
    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text=self.message, icon=self.icon) # 
        
def show_message_box(message):
    bpy.ops.message.message_box('INVOKE_DEFAULT', message=message)

class OBJECT_OT_add_cube(bpy.types.Operator):
    bl_idname = "object.add_cube"
    bl_label = "增加方体"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # self.report({'INFO'}, "Added a cube! ")
        show_message_box("Added a cube! ")
        bpy.ops.mesh.primitive_cube_add()
        return {'FINISHED'}
class OBJECT_OT_move_to_zero(bpy.types.Operator):
    bl_idname = "object.move_to_zero"
    bl_label = "移动原点"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = context.selected_objects
        if len(selected_objects) == 0:
            show_message_box("没有选择任何对象")
            return {'FINISHED'}
        else:
            for obj in selected_objects:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                obj.location = (0, 0, 0)
                return {'FINISHED'}
class OBJECT_OT_undo_last(bpy.types.Operator):
    bl_idname = "object.undo_last"
    bl_label = "Undo Lasts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.ed.undo()
        return {'FINISHED'}


class ThinningObject(bpy.types.Operator):
    bl_idname = "object.thinning_object"
    bl_label = "减小/增加 模型厚度（双平行面）"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        if len(selected_objects) == 0:
            show_message_box("没有选择任何对象")
            return {'FINISHED'}
        else:
            for obj in selected_objects:
                thinning_float = context.scene.custom_props.thinning_float
                self.report({'INFO'}, "减薄/增厚量: " + str(thinning_float))
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.select_mode(type="FACE")
                bpy.ops.transform.shrink_fatten(
                    value=thinning_float, 
                    use_even_offset=False, 
                    mirror=True, 
                    use_proportional_edit=True, 
                    proportional_edit_falloff='SMOOTH', 
                    proportional_size=0.909091, 
                    use_proportional_connected=False, 
                    use_proportional_projected=False, 
                    snap=False,
                    release_confirm=True
                )
                bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class CreateObjectsProjectionToZ(bpy.types.Operator):
    bl_idname = "object.create_object_projection"
    bl_label = "创建投影"

    def execute(self, context):
        selected_objects = context.selected_objects
        if len(selected_objects) == 0:
            show_message_box("没有选择任何对象")
            return {'FINISHED'}
        else:
            for obj in selected_objects:
                bpy.context.view_layer.objects.active = obj
                mesh_data = bpy.data.meshes.new("projection")
                projection_object = bpy.data.objects.new("projection", mesh_data)
                scene = bpy.context.scene
                scene.collection.objects.link(projection_object)
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                bm.transform(obj.matrix_world)
                matrix_proj = Matrix()
                matrix_proj[0][0] = 1
                matrix_proj[1][1] = 1
                matrix_proj[2][2] = 0
                for v in bm.verts:
                    v.co = matrix_proj @ v.co
                bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
                bm.to_mesh(mesh_data)
                bm.free()

class SimpleAddonPanel(bpy.types.Panel):
    bl_label = "山头火工具箱"
    bl_idname = "OBJECT_PT_simple_addon"
    bl_category = "山头火工具箱"
    
    bl_space_type = 'PROPERTIES' # 'VIEW_3D'
    bl_region_type = 'WINDOW' # 'UI'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        #
        col = layout.column()
        col.label(text="基本操作", icon='WORLD_DATA')
        col.operator("object.add_cube")
        col.operator("object.undo_last")
        col.operator("object.move_to_zero")
        col.operator("object.create_object_projection")

        col.label(text="减薄/增厚(正增负减)", icon='WORLD_DATA')
        custom_props = context.scene.custom_props
        col.prop(custom_props, "thinning_float")
        col.operator("object.thinning_object")  

def register():
    bpy.utils.register_class(CustomProperties)
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomProperties)
    bpy.utils.register_class(MessageBox)
    bpy.utils.register_class(OBJECT_OT_add_cube)
    bpy.utils.register_class(OBJECT_OT_undo_last)
    bpy.utils.register_class(OBJECT_OT_move_to_zero)
    bpy.utils.register_class(ThinningObject)
    bpy.utils.register_class(SimpleAddonPanel)
    bpy.utils.register_class(CreateObjectsProjectionToZ)

def unregister():
    bpy.utils.unregister_class(MessageBox)
    bpy.utils.unregister_class(OBJECT_OT_add_cube)
    bpy.utils.unregister_class(OBJECT_OT_undo_last)
    bpy.utils.unregister_class(OBJECT_OT_move_to_zero)
    bpy.utils.unregister_class(ThinningObject)
    bpy.utils.unregister_class(SimpleAddonPanel)
    del bpy.types.Scene.custom_props
    bpy.utils.unregister_class(CustomProperties)
    bpy.utils.unregister_class(CreateObjectsProjectionToZ)
                               
if __name__ == "__main__":
    register()
    #unregister() #for