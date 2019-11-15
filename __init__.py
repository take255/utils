from bpy.types import Panel
import bpy

class panel(Panel):   
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category ='kia'
    bl_options = {'DEFAULT_CLOSED'}

icon = {
    'OBJECT':'OBJECT_DATA',
    'ADD':'ADD',
    'REMOVE':'REMOVE',
    'UP':'TRIA_UP_BAR',
    'DOWN':'TRIA_DOWN_BAR',
    'CANCEL':'CANCEL',
    'SELECT':'RESTRICT_SELECT_OFF',
    'BONE':"BONE_DATA"
    }

def activeObj(ob):
     bpy.context.view_layer.objects.active = ob

def getActiveObj():
    return bpy.context.active_object
    
def select(ob,state):
     ob.select_set(state=state)

#シングルオブジェクトの選択とアクティブ化。それ以外のオブジェクトの選択解除
def act(ob):
     deselectAll()
     select(ob,True)
     activeObj(ob)


def delete(ob):
     bpy.ops.object.select_all(action='DESELECT')
     select(ob,True)
     bpy.ops.object.delete()

#---------------------------------------------------------------------------------------
#ボーン関連 edit mode
#---------------------------------------------------------------------------------------
def get_selected_bones():
     #ポーズモードなら
     if current_mode() == 'POSE':
          return bpy.context.selected_pose_bones
     elif current_mode() == 'EDIT':
          return bpy.context.selected_bones
     elif current_mode() == 'OBJECT':
          return []

def get_active_bone():
     #ポーズモードなら
     if current_mode() == 'POSE':
          return bpy.context.active_pose_bone
     elif current_mode() == 'EDIT':
          return bpy.context.active_bone
     elif current_mode() == 'OBJECT':
          return []



#選択をすべて解除して最後のオブジェクトをアクティブにする
def multiSelection(objarray):
     if len(objarray) == 0:return
     deselectAll()
     for ob in objarray:
          select(ob,True)

     activeObj(objarray[0])

def deselectAll():
     bpy.ops.object.select_all(action='DESELECT')

def selectByName(obname,state):
    bpy.data.objects[obname].select_set(state=state)

def objectByName(obname):
    return bpy.data.objects[obname]

def showhide(ob,state):
     bpy.data.objects[ob.name].hide_viewport = state

def sceneLink(ob):
     bpy.context.scene.collection.objects.link(ob)

def sceneUnlink(ob):
     bpy.context.scene.collection.objects.unlink(ob)

#パブリッシュシーンをアクティブに
def sceneActive(fix_scene):
     scn = bpy.data.scenes[fix_scene]
     bpy.context.window.scene = scn
     return scn

def selected():
    return bpy.context.selected_objects

#UV meshデータを入れると新規UVを返す
def UV_new(mesh_data):
     return mesh_data.uv_layers.new()

#カーソルを原点に
def cursorOrigin():
     bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
     bpy.context.scene.cursor.location = (0,0,0)

def mirrorBoneXaxis():
     bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(True, False, False))


#マテリアル関連
#ノーマルマップイメージのカラースペース指定
def nmt_colorspace(node):
     node.image.colorspace_settings.name = 'Non-Color'


#マトリックスの掛け算
def m_mul(m0,m1):
     return m0 @ m1


#---------------------------------------------------------------------------------------
#モード
#---------------------------------------------------------------------------------------
def current_mode():
     return bpy.context.object.mode

def mode_e():
     bpy.ops.object.mode_set(mode = 'EDIT')

def mode_o():
     bpy.ops.object.mode_set(mode = 'OBJECT')

def mode_p():
     bpy.ops.object.mode_set(mode = 'POSE')


#---------------------------------------------------------------------------------------
#カーソル
#---------------------------------------------------------------------------------------
def init_cursor():
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)


#---------------------------------------------------------------------------------------
#リグのルートボーンを作成
#---------------------------------------------------------------------------------------
def rigroot():
    bpy.ops.object.mode_set(mode='EDIT')
    root = 'rig_root'
    amt = bpy.context.object  
    if root not in amt.data.edit_bones:
        rootbone = amt.data.edit_bones.new(root)
        rootbone.head = (0,0,0)
        rootbone.tail = (0,0,1)
    else:
        rootbone = amt.data.edit_bones[root]
    
    return rootbone

#---------------------------------------------------------------------------------------
#コレクション関連
#---------------------------------------------------------------------------------------
class collection:
     @classmethod
     def create( self , name ):          
          collection = bpy.context.scene.collection
          if name in [x.name for x in bpy.data.collections]:
               col = bpy.data.collections[name]
          else:
               col = bpy.data.collections.new(name)
               collection.children.link(col)
          return col

     @classmethod
     def get_active( self ):
          return bpy.context.view_layer.active_layer_collection 
     
     @classmethod
     def move_obj( self , ob , to_col):
          for col in ob.users_collection:
               col.objects.unlink(ob)
          to_col.objects.link(ob)
     
     @classmethod     
     def root(self):
          return bpy.context.scene.collection

     @classmethod     
     def children(self , col):
          pass

     @classmethod     
     def get_parent(self , col):
          result = []
          for c in bpy.data.collections:
               if col.name in c.children:
                    result.append(c)
          
          return result