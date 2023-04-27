from mathutils import Vector, Matrix
from typing import Tuple
import bpy
import bmesh


def create_tmp_plane(
        blender_py: bpy,
        options: dict = {
            "new_object_name": "TMP_PLANE",
            "size": 1.0,
            "enter_editmode": False,
            "align": 'WORLD',
            "location": (0, 0, 0),
        },

) -> bpy.types.Object:
    # create plane by bpy.ops.mesh.primitive_plane_add
    blender_py.ops.object.select_all(action='DESELECT')
    blender_py.ops.mesh.primitive_plane_add(
        size=options["size"],
        enter_editmode=options["enter_editmode"],
        align=options["align"],
        location=options["location"],
    )
    new_plane_object = blender_py.context.active_object
    new_plane_object.name = options["new_object_name"]
    return new_plane_object


def scale_object_110_non_standard(
    blender_py: bpy,
    target_object: bpy.types.Object,
    scale_resize: dict = {
        "x": None,
        "y": None,
    },
) -> bpy.types.Object:
    # scale object
    target_object.scale.x = scale_resize["x"] + (scale_resize["x"] * 0.1)
    target_object.scale.y = scale_resize["y"] + (scale_resize["y"] * 0.1)

    # apply scale
    blender_py.ops.object.select_all(action='DESELECT')
    target_object.select_set(True)
    blender_py.context.view_layer.objects.active = target_object
    blender_py.ops.object.transform_apply(
        location=False, rotation=False, scale=True)
    return target_object


def get_bounds(obj: bpy.types.Object) -> Tuple[float, float, float, float, float, float]:
    world_bounds = [obj.matrix_world @
                    Vector(bound) for bound in obj.bound_box]
    min_x = min(world_bounds, key=lambda b: b.x).x
    max_x = max(world_bounds, key=lambda b: b.x).x
    min_y = min(world_bounds, key=lambda b: b.y).y
    max_y = max(world_bounds, key=lambda b: b.y).y
    min_z = min(world_bounds, key=lambda b: b.z).z
    max_z = max(world_bounds, key=lambda b: b.z).z
    return min_x, max_x, min_y, max_y, min_z, max_z


def clean_useless_verts_and_faces_after_shrinkwraped(
        blender_py: bpy,
        target_object: bpy.types.Object,
        height_threshold: float
) -> bpy.types.Object:

    blender_py.ops.object.select_all(action='DESELECT')
    target_object.select_set(True)
    blender_py.context.view_layer.objects.active = target_object
    blender_py.ops.object.mode_set(mode='EDIT')
    target_object_mesh = bmesh.from_edit_mesh(target_object.data)
    world_matrix = target_object.matrix_world

    for v in target_object_mesh.verts:
        world_co = world_matrix @ v.co
        if world_co.z > height_threshold:
            world_co.z = -1
            v.co = world_matrix.inverted() @ world_co

    for f in target_object_mesh.faces:
        face_center_world = world_matrix @ f.calc_center_median()
        if face_center_world.z < 0:
            f.select_set(True)

    blender_py.ops.mesh.delete(type='FACE')
    bmesh.update_edit_mesh(target_object.data)
    blender_py.ops.object.mode_set(mode='OBJECT')

    return target_object
