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

def register():
    print("アドオンが有効化されました.")

def unregister():
    print("アドオンが無効化されました.")
    
# テスト実行用コード
if __name__ == "__main__":
    register()