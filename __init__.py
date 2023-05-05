from . import main

bl_info = {
    "name": "Santouka Tools",
    "blender": (3, 5, 0),
    "category": "Object",
    "author": "Santouka",
    "version": (0, 1, 2),
    "location": "3D Viewport > Object",
    "description": "A Blender plug-in, toolboxes, to helping 3D printing business studios",
    "warning": "",
    "doc_url": "https://github.com/u-u-z/santouka-blender-helper",
}


def register():
    main.addon_register()


def unregister():
    main.addon_unregister()

# For testing in Blender's Text Editor
# if __name__ == "__main__":
#     register()
#     # unregister()
