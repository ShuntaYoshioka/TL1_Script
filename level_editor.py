import bpy
import math
import bpy_extras

import gpu
import gpu_extras.batch

import copy

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
    

class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
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
         self.write_and_print(file, indent + object.type)
         trans, rot, scale = object.matrix_local.decompose()
         #回転をQuterionからEulerに変換
         rot = rot.to_euler()
         #ラジアンから度数法に変換
         rot.x = math.degrees(rot.x)
         rot.y = math.degrees(rot.y)
         rot.z = math.degrees(rot.z)
         #トランスフォーム情報の表示
         self.write_and_print(file,indent +"T %f %f %f " % (trans.x, trans.y, trans.z))
         self.write_and_print(file,indent +"R %f %f %f " % (rot.x, rot.y, rot.z))
         self.write_and_print(file,indent +"S %f %f %f " % (scale.x, scale.y, scale.z))
         #カスタムプロパティ
         if "file_name" in object:
             self.write_and_print(file,indent + "N %s" % object["file_name"])
         self.write_and_print(file, indent + 'END')
         self.write_and_print(file, '')

         #子ノードへ進む
         for child in object.children:
             self.parse_scene_recursive(file, child,level + 1)
            

#パネル　クラス名
class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    #サブメニュー
    def draw(self,context):
        #パネルに項目を追加
        if "file_name" in context.object:
            self.layout.prop(context.object, '[file_name]', text=self.bl_label)
        else:
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)

        
    
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName追加"
    bl_description = "['fila_name']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        #['file_name']カスタムプロパティを追加
        context.object["file_name"] = ""

        return {"FINISHED"}

    

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


#こらいだー描画
class DrawCollider:
    #びょうがバンドル
    handle = None
    #3Dビューに登録する描画関数
    def draw_collider():
        #頂点データ
        vertices = {"pos":[]}
        #インデックスデータ
        indices = []

        #各頂点のオブジェクト中心からのオフセット
        offsets = [
            [-0.5,-0.5,-0.5],#左下前
            [+0.5,-0.5,-0.5],#右下前
            [-0.5,+0.5,-0.5],#左上前
            [+0.5,+0.5,-0.5],#右上前
            [-0.5,-0.5,+0.5],#左下奥
            [+0.5,-0.5,+0.5],#右下奥
            [-0.5,+0.5,+0.5],#左上億
            [+0.5,+0.5,+0.5],#右上奥
        ]

        #立方体のx,y,z方向サイズ
        size = [2,2,2]

        #現在sceneのオブジェクトリストを走査
        for object in bpy.context.scene.objects:
            #追加前の頂点数
            start = len(vertices["pos"])

            #Boxの8頂点分回す
            for offset in offsets:
                #オブジェクトの中心座標をコピー
                pos = copy.copy(object.location)
                #中心点を基準に各頂点ごとにずらす
                pos[0]+=offset[0]*size[0]
                pos[1]+=offset[1]*size[1]
                pos[2]+=offset[2]*size[2]
                #頂点データリストに座標を追加
                vertices['pos'].append(pos)
                
            #前面を構成する辺の頂点インデックス
            indices.append([start+0,start+1])
            indices.append([start+2,start+3])
            indices.append([start+0,start+2])
            indices.append([start+1,start+3])
            #奥面を構成する辺の頂点インデックス
            indices.append([start+4,start+5])
            indices.append([start+6,start+7])
            indices.append([start+4,start+6])
            indices.append([start+5,start+7])
            #手前と奥を繋ぐ辺の頂点インデックス
            indices.append([start+0,start+4])
            indices.append([start+1,start+5])
            indices.append([start+2,start+6])
            indices.append([start+3,start+7])
                


        #ビルドインのシェーダー取得
        shader = gpu.shader.from_builtin("UNIFORM_COLOR")

        batch = gpu_extras.batch.batch_for_shader(shader, "LINES", vertices,indices = indices)

        #シェーダーのパラメータ設定
        color = {0.5,1.0,1.0,1.0}
        shader.bind()
        shader.uniform_float("color",color)
        #描画
        batch.draw(shader)



# 登録するクラスのリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
)

def register():
    # クラスの登録
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    #3Dビューに描画関数を追加
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW")


    print("レベルエディタ（アドオン）が有効化されました.")

def unregister():
    #メニューから項目を排除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle,"WINDOW")


    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタ（アドオン）が無効化されました.")
    
# テスト実行用コード
if __name__ == "__main__":
    register()