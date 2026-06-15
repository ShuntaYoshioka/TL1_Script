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


#オペレータ　頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました")

        #オペレーターの命令終了通知
        return {'FINISHED'}
    

class MYAFFON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description ="ICO球を生成します"
    bl_options = {'REGISTER', 'UNDO'}

    #メニューを実行したとき呼ばれる
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")

        return {'FINISHED'}

    

class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):

        self.layout.operator("wm.url_open_preset", 
                             text="Manual", icon='HELP')
        
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
             text=MYADDON_OT_stretch_vertex.bl_label)
        
        # ⭕ draw 関数の中に追記
        self.layout.operator(MYAFFON_OT_create_ico_sphere.bl_idname, 
                     text=MYAFFON_OT_create_ico_sphere.bl_label)

    def submenu(self, context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# 登録するクラスのリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYAFFON_OT_create_ico_sphere,
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