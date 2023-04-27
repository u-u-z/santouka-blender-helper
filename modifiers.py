import bpy
from typing import Tuple


def remesh_direct(blender_py_lib: bpy,
                  target_object: bpy.types.Object,
                  mode='VOXEL',
                  voxel_size=0.3,
                  modifier_name='TMP_REMESH_MODIFIER'
                  ) -> bpy.types.Object:

    remesh_modifier: bpy.types.Modifier = target_object.modifiers.new(
        name=modifier_name, type='REMESH')
    remesh_modifier.mode = mode
    remesh_modifier.voxel_size = voxel_size
    blender_py_lib.ops.object.modifier_apply(
        {"object": target_object}, modifier=modifier_name)
    return target_object


def solidify_direct(blender_py_lib: bpy,
                    target_object: bpy.types.Object,
                    thickness=0.7,
                    modifier_name='TMP_SOLIDIFY_MODIFIER'
                    ) -> bpy.types.Object:
    solidify_modifier = target_object.modifiers.new(
        name=modifier_name, type='SOLIDIFY')
    solidify_modifier.thickness = thickness
    solidify_modifier.offset = 0.0
    blender_py_lib.context.view_layer.update()
    blender_py_lib.ops.object.modifier_apply(
        {"object": target_object}, modifier=modifier_name)
    return target_object


def decimate_direct(blender_py_lib: bpy,
                    target_object: bpy.types.Object,
                    ratio=0.5,
                    modifier_name='TMP_DECIMATE_MODIFIER'
                    ) -> bpy.types.Object:
    decimate_modifier = target_object.modifiers.new(
        name=modifier_name, type='DECIMATE')
    decimate_modifier.ratio = ratio
    blender_py_lib.context.view_layer.update()
    blender_py_lib.ops.object.modifier_apply(
        {"object": target_object}, modifier=modifier_name)
    return target_object


def shrinkwrap_project_direct(
        blender_py_lib: bpy,
        source_object: bpy.types.Object,
        target_object: bpy.types.Object,
        options: dict = {
            'wrap_method': 'PROJECT',
            'use_negative_direction': True,
            'use_positive_direction': False,
            'project_limit': 0,
            'use_project_z': True
        },
        modifier_name='TMP_SHRINKWRAP_MODIFIER',

) -> Tuple[bpy.types.Object, bpy.types.Object]:
    shrinkwrap_modifier = source_object.modifiers.new(
        name=modifier_name, type='SHRINKWRAP')

    shrinkwrap_modifier.target = target_object
    shrinkwrap_modifier.wrap_method = options['wrap_method']
    shrinkwrap_modifier.use_negative_direction = options['use_negative_direction']
    shrinkwrap_modifier.use_positive_direction = options['use_positive_direction']
    shrinkwrap_modifier.project_limit = options['project_limit']
    shrinkwrap_modifier.use_project_z = options['use_project_z']

    blender_py_lib.context.view_layer.update()
    blender_py_lib.ops.object.modifier_apply(
        {"object": source_object}, modifier=modifier_name)
    return (source_object, target_object)
