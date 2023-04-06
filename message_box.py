import bpy

class MessageBox(bpy.types.Operator):

    """
    This operator displays a message box
    """

    bl_idname = "message.message_box"
    bl_label = ""

    message: bpy.props.StringProperty(name="Message", default="")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text=self.message, icon='ERROR')
        
def show_message_box(message):
    bpy.ops.message.message_box('INVOKE_DEFAULT', message=message)

def register():
    bpy.utils.register_class(MessageBox)