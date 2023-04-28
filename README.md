<div align="center">
  <img src="docs/banner.svg"/>
  <h1>SANTOUKA BLENDER HELPER</h1>
  <p>A Blender plug-in, toolboxes, to helping 3D printing business studios</p>
</div>

<br/><br/><hr/>
## Useage (for User)

1. Download from release page: https://github.com/u-u-z/santouka-blender-helper/releases
2. Open Blender, go to `Edit` -> `Preferences` -> `Add-ons` -> `Install` -> select the downloaded zip file

## Environment (for Developer)

### Develop
- Blender 3.5.1
- Python 3.10.9
  - `Builtin Modules: bpy, bpy.data, bpy.ops, bpy.props, bpy.types, bpy.context, bpy.utils, bgl, gpu, blf, mathutils`
  - `Convenience Imports:   from mathutils import *; from math import *`
  - ` Convenience Variables: C = bpy.context, D = bpy.data`

About blender **type** support for code editor: `blender-stubs==3.10.27` in `requirements.txt` so u can:
```shell
$ pip -m venv venv
$ source ./venv/bin/activat
$ pip install -r requirements.txt
```
  
### Packaging for release
#### Pre-requisites
shell: `make`, `zip`
#### Packaging
Please use `make` (GNU Make 3.81) to package the add-on.
```shell
$ make

updating: satnouka-blender-helper/ (stored 0%)
updating: satnouka-blender-helper/main.py (deflated 69%)
updating: satnouka-blender-helper/mesh_helpers.py (deflated 64%)
updating: satnouka-blender-helper/ui.py (deflated 71%)
updating: satnouka-blender-helper/__init__.py (deflated 73%)
updating: satnouka-blender-helper/export.py (deflated 69%)
updating: satnouka-blender-helper/operators.py (deflated 76%)
updating: satnouka-blender-helper/report.py (deflated 19%)
Add-on already packaged, please see dist dir: ./dist/satnouka-blender-helper.zip
```

## More

### About icon items
please visit: https://docs.blender.org/api/current/bpy_types_enum_items/icon_items.html#rna-enum-icon-items