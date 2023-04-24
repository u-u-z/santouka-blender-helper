# SPDX-License-Identifier: GPL-2.0-or-later

from . import (
    ui,
    operators,
)
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
)
from bpy.types import PropertyGroup
import bpy
import math


class SceneProperties(PropertyGroup):
    use_alignxy_face_area: BoolProperty(
        name="Face Areas",
        description="Normalize normals proportional to face areas",
        default=False,
    )

    export_format: EnumProperty(
        name="Format",
        description="Format type to export to",
        items=(
            ('OBJ', "OBJ", ""),
            ('PLY', "PLY", ""),
            ('STL', "STL", ""),
            ('X3D', "X3D", ""),
        ),
        default='STL',
    )
    use_export_texture: BoolProperty(
        name="Copy Textures",
        description="Copy textures on export to the output path",
        default=False,
    )
    use_apply_scale: BoolProperty(
        name="Apply Scale",
        description="Apply scene scale setting on export",
        default=False,
    )
    use_data_layers: BoolProperty(
        name="Data Layers",
        description=(
            "Export normals, UVs, vertex colors and materials for formats that support it "
            "significantly increasing file size"
        ),
    )
    export_path: StringProperty(
        name="Export Directory",
        description="Path to directory where the files are created",
        default="//",
        maxlen=1024,
        subtype="DIR_PATH",
    )
    thickness_min: FloatProperty(
        name="Thickness",
        description="Minimum thickness",
        subtype='DISTANCE',
        default=0.001,  # 1mm
        min=0.0,
        max=10.0,
    )
    threshold_zero: FloatProperty(
        name="Threshold",
        description="Limit for checking zero area/length",
        default=0.0001,
        precision=5,
        min=0.0,
        max=0.2,
    )
    angle_distort: FloatProperty(
        name="Angle",
        description="Limit for checking distorted faces",
        subtype='ANGLE',
        default=math.radians(45.0),
        min=0.0,
        max=math.radians(180.0),
    )
    angle_sharp: FloatProperty(
        name="Angle",
        subtype='ANGLE',
        default=math.radians(160.0),
        min=0.0,
        max=math.radians(180.0),
    )
    angle_overhang: FloatProperty(
        name="Angle",
        subtype='ANGLE',
        default=math.radians(45.0),
        min=0.0,
        max=math.radians(90.0),
    )


classes = (
    SceneProperties,

    ui.VIEW3D_PT_print3d_stk_analyze,
    ui.VIEW3D_PT_print3d_stk_cleanup,
    ui.VIEW3D_PT_print3d_stk_transform,
    ui.VIEW3D_PT_print3d_stk_export,

    operators.MESH_OT_print3d_stk_info_volume,
    operators.MESH_OT_print3d_stk_info_area,
    operators.MESH_OT_print3d_stk_check_degenerate,
    operators.MESH_OT_print3d_stk_check_distorted,
    operators.MESH_OT_print3d_stk_check_solid,
    operators.MESH_OT_print3d_stk_check_intersections,
    operators.MESH_OT_print3d_stk_check_thick,
    operators.MESH_OT_print3d_stk_check_sharp,
    operators.MESH_OT_print3d_stk_check_overhang,
    operators.MESH_OT_print3d_stk_check_all,
    operators.MESH_OT_print3d_stk_clean_distorted,
    # operators.MESH_OT_print3d_stk_clean_thin,
    operators.MESH_OT_print3d_stk_clean_non_manifold,
    operators.MESH_OT_print3d_stk_select_report,
    operators.MESH_OT_print3d_stk_scale_to_volume,
    operators.MESH_OT_print3d_stk_scale_to_bounds,
    operators.MESH_OT_print3d_stk_align_to_xy,
    operators.MESH_OT_print3d_stk_export,
)


def in_side_addon_register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.print_3d = PointerProperty(type=SceneProperties)


def in_side_addon_unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.print_3d
