bl_info = {
    "name": "Santouka Tools",
    "blender": (3, 5, 0),
    "category": "Object",
}

from . import stk_object_print3d_utils
from mathutils import Vector, Matrix
import bmesh
import bpy


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
        col.label(text=self.message, icon=self.icon)


def show_message_box(message):
    bpy.ops.message.message_box('INVOKE_DEFAULT', message=message)


class OBJECT_OT_move_to_zero(bpy.types.Operator):
    bl_idname = "object.move_to_zero"
    bl_label = "至原点"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "移动了 {selected_num} 个对象".format(
            selected_num=len(context.selected_objects))
        )
        if len(context.selected_objects) == 0:
            show_message_box("未选择任何对象，请先选择对象")
            return {'FINISHED'}
        else:
            for obj in context.selected_objects:
                obj.location = (0, 0, 0)
            return {'FINISHED'}


class OBJECT_OT_reset_origin_and_move_to_zero(bpy.types.Operator):
    bl_idname = "object.reset_origin_and_move_to_zero"
    bl_label = "至原点,并重置原点"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "移动了 {selected_num} 个对象".format(
            selected_num=len(context.selected_objects))
        )
        if len(context.selected_objects) == 0:
            show_message_box("未选择任何对象，请先选择对象")
            return {'FINISHED'}
        else:
            for obj in context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(
                    type='ORIGIN_GEOMETRY', center='BOUNDS')
                obj.location = (0, 0, 0)
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


class CreateObjectsProjectionToZZero(bpy.types.Operator):
    bl_idname = "object.create_object_projection"
    bl_label = "创建（z轴=0）XY面投影"

    def execute(self, context):
        selected_objects = context.selected_objects
        if len(selected_objects) == 0:
            show_message_box("没有选择任何对象")
            return {'FINISHED'}
        else:
            for obj in selected_objects:
                bpy.context.view_layer.objects.active = obj
                mesh_data = bpy.data.meshes.new("projection")
                projection_object = bpy.data.objects.new(
                    "projection", mesh_data)
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


class OBJECT_PT_SantoukaBusinessMeshBottom(bpy.types.Operator):
    bl_idname = "object.OBJECT_PT_SantoukaBusinessMeshBottom"
    bl_label = "创建底部（用于吸塑）"
    bl_description = "Create bottom mesh for vacuum forming"

    def execute(self, context):
        # get method from dependencies
        get_bounds = stk_object_print3d_utils.operators.get_bounds
        create_tmp_plane = stk_object_print3d_utils.operators.create_tmp_plane
        scale_object = stk_object_print3d_utils.operators.scale_object_110_non_standard
        clean_after_shrinkwraped = stk_object_print3d_utils.operators.clean_useless_verts_and_faces_after_shrinkwraped

        # get method for modifiers
        remesh_direct = modifiers.remesh_direct
        solidify_direct = modifiers.solidify_direct
        shrinkwrap_project_direct = modifiers.shrinkwrap_project_direct

        # business logic
        # selected_objects will same as "target_objects"
        selected_objects = context.selected_objects

        for selected_object in selected_objects:

            # get bounds of selected_object
            # for caculation plane size & postion for deploy
            selected_object_bounds = get_bounds(selected_object)

            # create plane by selected_object_bounds
            tmp_plane_x = selected_object_bounds[1] - selected_object_bounds[0]
            tmp_plane_y = selected_object_bounds[3] - selected_object_bounds[2]
            tmp_plane_top_z = selected_object_bounds[5]

            # if x,y is too small, then report warning
            if tmp_plane_x < 0.1 or tmp_plane_y < 0.1:
                self.report({'WARNING'}, "选择对象的宽度或高度过小")
                return {'FINISHED'}

            try:
                # create tmp_plane and scale to selected_object size
                # tmp_plane_not_scaled: tmp_plane without scale
                # tmp_plane: tmp_plane after scale
                # scale / resize plane to selected_object size
                # will use tmp_plane for remesh & shrinkwrap
                # plane need enough vertices & faces for shrinkwrap

                tmp_plane_not_scaled = create_tmp_plane(bpy)
                tmp_plane_object = scale_object(bpy, tmp_plane_not_scaled, {
                    'x': tmp_plane_x,
                    'y': tmp_plane_y,
                })

                # move plane_object to top of selected_object
                tmp_plane_object.location.z = tmp_plane_top_z + 5

                # remesh: tmp_plane -> tmp_plane_remeshed
                # for next shrinkwrap need more vertices & faces
                # TODO: remesh need more options (size) for user panel
                tmp_plane_object_remeshed = remesh_direct(
                    bpy,
                    tmp_plane_object
                )

                # shrinkwrap: tmp_plane_remeshed -> selected_object
                # made tmp_plane_remeshed fit selected_object(target_object)
                # TODO: shrinkwrap need more options for user panel
                tmp_plane_shrinkwraped_tuple = shrinkwrap_project_direct(
                    bpy, tmp_plane_object_remeshed, selected_object, )
                tmp_bottom_mesh = tmp_plane_shrinkwraped_tuple[0]
                # now tmp_bottom_mesh project on to the selected_object

                # move tmp_bottom_mesh mesh useless vertices to z = 0, and clean
                # useless vertices: the part of
                #   not shrinkwrap project on the selected_object part
                stash_tmp_bottom_object = clean_after_shrinkwraped(bpy, tmp_bottom_mesh)
                # this stash_bottom_object not solidify yet

                # solidify: add solid stash_tmp_bottom_object
                # TODO: solidify need tickness options for user panel
                #   default tickness is 0.7mm * 2
                solidified_object = solidify_direct(bpy, stash_tmp_bottom_object)
                # cuz it maybe have the bad faces, so need remesh again

                # remesh: solidified_object -> final_object
                # TODO: remesh need more options (size) for user panel
                final_object = remesh_direct(bpy, solidified_object)

            except:
                self.report({'ERROR'}, "底部 mesh 添加失败")
                return {'FINISHED'}

        return {'FINISHED'}


class SantoukaToolBoxPanel(bpy.types.Panel):
    bl_label = "山头火工具箱"
    bl_idname = "OBJECT_PT_simple_addon"
    bl_category = "山头火工具箱"

    bl_space_type = 'PROPERTIES'  # 'VIEW_3D'
    bl_region_type = 'WINDOW'  # 'UI'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="移动对象（请选择对象）", icon='OBJECT_DATA')
        col.operator("object.reset_origin_and_move_to_zero")
        col.operator("object.move_to_zero")

        col.label(text="投影", icon='LIGHT')
        col.operator("object.create_object_projection")

        col.label(text="减薄/增厚(正增负减)", icon='HOLDOUT_OFF')
        custom_props = context.scene.custom_props
        col.prop(custom_props, "thinning_float")
        col.operator("object.thinning_object")


def register():
    bpy.utils.register_class(CustomProperties)
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(
        type=CustomProperties)

    bpy.utils.register_class(MessageBox)
    bpy.utils.register_class(OBJECT_OT_move_to_zero)
    bpy.utils.register_class(OBJECT_OT_reset_origin_and_move_to_zero)
    bpy.utils.register_class(ThinningObject)
    bpy.utils.register_class(SantoukaToolBoxPanel)
    bpy.utils.register_class(CreateObjectsProjectionToZZero)

    # 3D-printing utils
    stk_object_print3d_utils.in_side_addon_register()


def unregister():
    bpy.utils.unregister_class(MessageBox)
    bpy.utils.unregister_class(OBJECT_OT_move_to_zero)
    bpy.utils.unregister_class(OBJECT_OT_reset_origin_and_move_to_zero)
    bpy.utils.unregister_class(ThinningObject)
    bpy.utils.unregister_class(SantoukaToolBoxPanel)
    del bpy.types.Scene.custom_props
    bpy.utils.unregister_class(CustomProperties)
    bpy.utils.unregister_class(CreateObjectsProjectionToZZero)

    # 3D-printing utils
    stk_object_print3d_utils.in_side_addon_unregister()


# if __name__ == "__main__":
#     register()
#     # unregister()
