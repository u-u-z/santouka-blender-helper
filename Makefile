.DEFAULT_GOAL := zip

.PHONY: zip

zip:
	@rm -rf dist
	@mkdir -p dist
	@mkdir -p dist/santouka-blender-helper
	@cp -r *.py dist/santouka-blender-helper
	@cd dist && zip -r "santouka-blender-helper.zip" santouka-blender-helper
	@SUM=$$(shasum "./dist/santouka-blender-helper.zip" | cut -c 1-10) && echo "File sum: $$SUM"; \
	mv "./dist/santouka-blender-helper.zip" "./dist/santouka-blender-helper-$$SUM.zip"
	@rm -rf dist/santouka-blender-helper
	@echo "已生成插件，请查看 dist 目录: ./dist"

clean:
	@rm -rf dist 
	@rm -f .DS_Store
	@echo "已清理插件"
