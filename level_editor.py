import bpy
import math
import bpy_extras

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
    

class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description ="ICO球を生成します"
    bl_options = {'REGISTER', 'UNDO'}

    #メニューを実行したとき呼ばれる
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")

        return {'FINISHED'}
    

class  MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
     bl_idname = "myaddon.myaddon_ot_export_scene"
     bl_label = "scene出力"
     bl_description ="scene情報をExportします"


        # 出力するファイルの拡張子
     filename_ext = ".scene"

     def export(self):
        """ファイルに出力"""

        print("scene情報出力開始... %r " % self.filepath)

        with open(self.filepath, "wt") as file:
            
            self.write_and_print(file, "SCENE")
            
            for object in bpy.context.scene.objects:
             
             if(object.parent):
                 continue
             
             self.parse_scene_recursive(file, object,0)

             if object.parent:
                print("Parent:" + object.parent.name)
             print()


     def execute(self, context):
        print(" scene情報をExportします")

        #ファイル出力
        self.export()



        print(bpy.context.scene.objects)

        print("scene情報をExportしました")
        self.report({'INFO'}, "scene情報をExportしました")

        return {'FINISHED'}

     def write_and_print(self,file,str):
        print(str)

        file.write(str)
        file.write('\n')

     def parse_scene_recursive(self, file,object, level):
         

         #深さ分インデントする
         indent = ''
         for i in range(level):
             indent += "\t"


         #オブジェクト名書き込み
         self.write_and_print(file, indent + object.type + " - " + object.name)
         trans, rot, scale = object.matrix_local.decompose()
         #回転をQuterionからEulerに変換
         rot = rot.to_euler()
         #ラジアンから度数法に変換
         rot.x = math.degrees(rot.x)
         rot.y = math.degrees(rot.y)
         rot.z = math.degrees(rot.z)
         #トランスフォーム情報の表示
         self.write_and_print(file,indent +"Trans(%f,%f,%f)" % (trans.x, trans.y, trans.z))
         self.write_and_print(file,indent +"Rot(%f,%f,%f)" % (rot.x, rot.y, rot.z))
         self.write_and_print(file,indent + "Scale(%f,%f,%f)" % (scale.x, scale.y, scale.z))
         self.write_and_print(file, '')

         #子ノードへ進む
         for child in object.children:
             self.parse_scene_recursive(file, child,level + 1)
            


     
    


    

class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):

        self.layout.operator("wm.url_open_preset", 
                             text="Manual", icon='HELP')
        
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
             text=MYADDON_OT_stretch_vertex.bl_label)
        
        #draw 関数の中に追記
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, 
                     text=MYADDON_OT_create_ico_sphere.bl_label)
        
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,
                     text=MYADDON_OT_export_scene.bl_label)

    def submenu(self, context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# 登録するクラスのリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
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