.DEFAULT_GOAL := zip

.PHONY: zip

zip:
	@mkdir -p dist
	@mkdir -p dist/satnouka-blender-helper
	@cp -r *.py dist/satnouka-blender-helper
	@cd dist && zip -r satnouka-blender-helper.zip satnouka-blender-helper
	@rm -rf dist/satnouka-blender-helper
	@echo "已生成插件，请查看 dist 目录: ./dist/satnouka-blender-helper.zip"

clean:
	@rm -rf dist 
	@rm .DS_Store
	@echo "已清理插件"
