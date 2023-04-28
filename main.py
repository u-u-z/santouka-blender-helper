# SPDX-License-Identifier: GPL-2.0-or-later

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

from . import (
    ui,
    operators,
)


class SceneProperties(PropertyGroup):

    thinning_float: bpy.props.FloatProperty(name="减薄/增厚量")

    use_alignxy_face_area: BoolProperty(
        name="面的面积",
        description="Normalize normals proportional to face areas",
        default=False,
    )

    export_format: EnumProperty(
        name="格式",
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
        name="复制纹理",
        description="Copy textures on export to the output path",
        default=False,
    )
    use_apply_scale: BoolProperty(
        name="应用缩放",
        description="Apply scene scale setting on export",
        default=False,
    )
    use_data_layers: BoolProperty(
        name="数据层",
        description=(
            "Export normals, UVs, vertex colors and materials for formats that support it "
            "significantly increasing file size"
        ),
    )
    export_path: StringProperty(
        name="导出目录",
        description="Path to directory where the files are created",
        default="//",
        maxlen=1024,
        subtype="DIR_PATH",
    )
    thickness_min: FloatProperty(
        name="最小厚度",
        description="Minimum thickness",
        subtype='DISTANCE',
        default=0.001,  # 1mm
        min=0.0,
        max=10.0,
    )
    threshold_zero: FloatProperty(
        name="阈值",
        description="Limit for checking zero area/length",
        default=0.0001,
        precision=5,
        min=0.0,
        max=0.2,
    )
    angle_distort: FloatProperty(
        name="角度-失真",
        description="Limit for checking distorted faces",
        subtype='ANGLE',
        default=math.radians(45.0),
        min=0.0,
        max=math.radians(180.0),
    )
    angle_sharp: FloatProperty(
        name="角度-锐利",
        subtype='ANGLE',
        default=math.radians(160.0),
        min=0.0,
        max=math.radians(180.0),
    )
    angle_overhang: FloatProperty(
        name="角度-悬空",
        subtype='ANGLE',
        default=math.radians(45.0),
        min=0.0,
        max=math.radians(90.0),
    )


classes = (
    SceneProperties,

    ui.VIEW3D_PT_stk_tools_analyze,
    ui.VIEW3D_PT_stk_tools_cleanup,
    ui.VIEW3D_PT_stk_tools_transform,
    ui.VIEW3D_PT_stk_tools_export,
    ui.VIEW3D_PT_stk_tools_model_handle,

    # operators port from 3d print utils
    operators.MESH_OT_stk_tools_info_volume,
    operators.MESH_OT_stk_tools_info_area,
    operators.MESH_OT_stk_tools_check_degenerate,
    operators.MESH_OT_stk_tools_check_distorted,
    operators.MESH_OT_stk_tools_check_solid,
    operators.MESH_OT_stk_tools_check_intersections,
    operators.MESH_OT_stk_tools_check_thick,
    operators.MESH_OT_stk_tools_check_sharp,
    operators.MESH_OT_stk_tools_check_overhang,
    operators.MESH_OT_stk_tools_check_all,
    operators.MESH_OT_stk_tools_clean_distorted,
    # operators.MESH_OT_stk_tools_clean_thin,
    operators.MESH_OT_stk_tools_clean_non_manifold,
    operators.MESH_OT_stk_tools_select_report,
    operators.MESH_OT_stk_tools_scale_to_volume,
    operators.MESH_OT_stk_tools_scale_to_bounds,
    operators.MESH_OT_stk_tools_align_to_xy,
    operators.MESH_OT_stk_tools_export,

    # operators from the santouka business part
    operators.MessageBox,
    operators.OBJECT_OT_move_to_zero,
    operators.OBJECT_OT_reset_origin_and_move_to_zero,
    operators.OBJECT_PT_SantoukaBusinessMeshBottom,
    operators.ThinningObject,
    operators.CreateObjectsProjectionToZZero,
)


def addon_register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.stk_tools_props = PointerProperty(type=SceneProperties)


def addon_unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.stk_tools_props
