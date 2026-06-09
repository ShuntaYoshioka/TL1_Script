import bpy

# Blenderに登録するアドオンの情報
bl_info = {
    "name": "レベルエディタ",  
    "author": "Shunta Yoshioka",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}

def draw_menu_manual(self, context):
    self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')

class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):

        self.layout.operator("wm.url_open_preset", 
                             text="Manual", icon='HELP')

    def submenu(self, context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# 登録するクラスのリスト
classes = (
    TOPBAR_MT_my_menu,
)

def register():
    # クラスの登録
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタ（アドオン）が有効化されました.")

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタ（アドオン）が無効化されました.")
    
# テスト実行用コード
if __name__ == "__main__":
    register()