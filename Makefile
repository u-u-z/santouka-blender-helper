.DEFAULT_GOAL := zip

.PHONY: zip

zip:
	@rm -rf dist
	@mkdir -p dist
	@zip -r dist/satnouka_tool_blender_addon.zip . -i *.py
	@echo "已生成插件，请查看 dist 目录: ./dist/satnouka_tool_blender_addon.zip"
