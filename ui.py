# SPDX-License-Identifier: GPL-2.0-or-later

# Interface for this addon.


from bpy.types import Panel
import bmesh

from . import report


class View3DPrintPanelSTK:
    bl_category = "山头火工具箱：3D打印"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.mode in {'OBJECT', 'EDIT'}


class VIEW3D_PT_print3d_stk_analyze(View3DPrintPanelSTK, Panel):
    bl_idname = "VIEW3D_PT_print3d_stk_analyze"
    bl_category = "山头火工具箱：3D打印"
    bl_label = "分析"

    _type_to_icon = {
        bmesh.types.BMVert: 'VERTEXSEL',
        bmesh.types.BMEdge: 'EDGESEL',
        bmesh.types.BMFace: 'FACESEL',
    }

    def draw_report(self, context):
        layout = self.layout
        info = report.info()

        if info:
            is_edit = context.edit_object is not None

            layout.label(text="结果/报告")
            box = layout.box()
            col = box.column()

            for i, (text, data) in enumerate(info):
                if is_edit and data and data[1]:
                    bm_type, _bm_array = data
                    col.operator("mesh.print3d_stk_select_report", text=text,
                                 icon=self._type_to_icon[bm_type],).index = i
                else:
                    col.label(text=text)

    def draw(self, context):
        layout = self.layout

        print_3d = context.scene.print_3d

        # TODO, presets

        layout.label(text="统计")
        row = layout.row(align=True)
        row.operator("mesh.print3d_stk_info_volume", text="体积")
        row.operator("mesh.print3d_stk_info_area", text="面积")

        layout.label(text="检查")
        col = layout.column(align=True)
        col.operator("mesh.print3d_stk_check_solid", text="实体")
        col.operator("mesh.print3d_stk_check_intersect", text="交叉")
        row = col.row(align=True)
        row.operator("mesh.print3d_stk_check_degenerate", text="逆生成/损坏")
        row.prop(print_3d, "threshold_zero", text="")
        row = col.row(align=True)
        row.operator("mesh.print3d_stk_check_distort", text="扭曲/失真")
        row.prop(print_3d, "angle_distort", text="")
        row = col.row(align=True)
        row.operator("mesh.print3d_stk_check_thick", text="厚度")
        row.prop(print_3d, "thickness_min", text="")
        row = col.row(align=True)
        row.operator("mesh.print3d_stk_check_sharp", text="边缘锋利/尖锐")
        row.prop(print_3d, "angle_sharp", text="")
        row = col.row(align=True)
        row.operator("mesh.print3d_stk_check_overhang", text="外悬")
        row.prop(print_3d, "angle_overhang", text="")
        layout.operator("mesh.print3d_stk_check_all", text="检查所有")

        self.draw_report(context)


class VIEW3D_PT_print3d_stk_cleanup(View3DPrintPanelSTK, Panel):
    bl_label = "清理"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        print_3d = context.scene.print_3d

        row = layout.row(align=True)
        row.operator("mesh.print3d_stk_clean_distorted", text="扭曲/失真")
        row.prop(print_3d, "angle_distort", text="")
        layout.operator("mesh.print3d_stk_clean_non_manifold",
                        text="创建 Manifold")
        # XXX TODO
        # layout.operator("mesh.print3d_stk_clean_thin", text="Wall Thickness")


class VIEW3D_PT_print3d_stk_transform(View3DPrintPanelSTK, Panel):
    bl_label = "变换"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        print_3d = context.scene.print_3d

        layout.label(text="Scale To")
        row = layout.row(align=True)
        row.operator("mesh.print3d_stk_scale_to_volume", text="体积")
        row.operator("mesh.print3d_stk_scale_to_bounds", text="边界")
        row = layout.row(align=True)
        row.operator("mesh.print3d_stk_align_to_xy", text="对齐XY")
        row.prop(print_3d, "use_alignxy_face_area")


class VIEW3D_PT_print3d_stk_export(View3DPrintPanelSTK, Panel):
    bl_label = "导出"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        print_3d = context.scene.print_3d

        layout.prop(print_3d, "export_path", text="")
        layout.prop(print_3d, "export_format")

        col = layout.column()
        col.prop(print_3d, "use_apply_scale")
        col.prop(print_3d, "use_export_texture")
        sub = col.column()
        sub.active = print_3d.export_format != "STL"
        sub.prop(print_3d, "use_data_layers")

        layout.operator("mesh.print3d_stk_export",
                        text="导出", icon='EXPORT')
