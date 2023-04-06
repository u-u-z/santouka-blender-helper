import bpy

bl_info = {
    "name": "山头火工具箱",
    "blender": (3, 3, 1),
    "category": "Object",
}

class MYADDON_PG_custom_properties(bpy.types.PropertyGroup):
    my_string: bpy.props.StringProperty(name="Test string")
    my_bool: bpy.props.BoolProperty(name="Test Bool")
    my_float: bpy.props.FloatProperty(name="Test Float")


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
#       self.report({'INFO'}, "Added a cube! ")
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

class SimpleAddonPanel2(bpy.types.Panel):
    bl_label = "山头火工具箱2"
    bl_idname = "OBJECT_PT_simple_addon_2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "山头火工具箱"
    
    def draw(self, context):
        layout = self.layout

class SimpleAddonPanel(bpy.types.Panel):
    bl_label = "山头火工具箱"
    bl_idname = "OBJECT_PT_simple_addon"
    bl_category = "山头火工具箱"
    
    bl_space_type = 'PROPERTIES' # 'VIEW_3D'
    bl_region_type = 'WINDOW' # 'UI'
    bl_context = 'object'

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text="基本操作", icon='WORLD_DATA')
        col.operator("object.add_cube")
        col.operator("object.undo_last")
        col.operator("object.move_to_zero")
        
        obj = context.object
        
        row = layout.row()
        row.label(text="Hello World", icon='WORLD_DATA')
        
        row = layout.row()
        row.prop(obj, "name")

class MYADDON_OT_modal_dialog(bpy.types.Operator):
    bl_idname = "myaddon.modal_dialog"
    bl_label = "My Addon Dialog"
    
    my_string: bpy.props.StringProperty(name="自定义属性")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "my_string")
        
        
class MYADDON_PT_show_dialog(bpy.types.Panel):
    bl_label = "My Addon"
    bl_idname = "MYADDON_PT_show_dialog"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My Addon'

    def draw(self, context):
        layout = self.layout
        layout.operator("myaddon.modal_dialog")
        
class MYADDON_PT_custom_panel(bpy.types.Panel):
    bl_label = "My Addon"
    bl_idname = "MYADDON_PT_custom_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        custom_props = scene.my_addon_custom_props
        layout.prop(custom_props, "my_string")
        layout.prop(custom_props, "my_bool")
        layout.prop(custom_props, "my_float")
        layout.operator("myaddon.modal_dialog")

def register():
    bpy.utils.register_class(MYADDON_PG_custom_properties)
    bpy.types.Scene.my_addon_custom_props = bpy.props.PointerProperty(type=MYADDON_PG_custom_properties)
    bpy.utils.register_class(MessageBox)
    bpy.utils.register_class(OBJECT_OT_add_cube)
    bpy.utils.register_class(OBJECT_OT_undo_last)
    bpy.utils.register_class(OBJECT_OT_move_to_zero)
    bpy.utils.register_class(SimpleAddonPanel)
    bpy.utils.register_class(MYADDON_PT_custom_panel)
    bpy.utils.register_class(MYADDON_OT_modal_dialog)
    bpy.utils.register_class(MYADDON_PT_show_dialog)

def unregister():
    bpy.utils.unregister_class(MessageBox)
    bpy.utils.unregister_class(OBJECT_OT_add_cube)
    bpy.utils.unregister_class(OBJECT_OT_undo_last)
    bpy.utils.unregister_class(OBJECT_OT_move_to_zero)
    bpy.utils.unregister_class(SimpleAddonPanel)
    del bpy.types.Scene.my_addon_custom_props
    bpy.utils.unregister_class(MYADDON_PG_custom_properties)
    bpy.utils.unregister_class(MYADDON_PT_custom_panel)
    bpy.utils.unregister_class(MYADDON_OT_modal_dialog)
    bpy.utils.unregister_class(MYADDON_PT_show_dialog)

if __name__ == "__main__":
    register()
    # unregister() #for