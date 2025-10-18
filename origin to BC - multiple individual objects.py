import bpy
import mathutils

def set_origin_to_bottom_center(obj: bpy.types.Object):
    """Move OBJ's origin to its bounding-box bottom-center without moving it in world space."""
    if obj.type != 'MESH':
        return

    if obj.data.users > 1:
        obj.data = obj.data.copy()

    bbox = [mathutils.Vector(corner) for corner in obj.bound_box]  
    min_z = min(v.z for v in bbox)
    avg_x = sum(v.x for v in bbox) / 8.0
    avg_y = sum(v.y for v in bbox) / 8.0
    p = mathutils.Vector((avg_x, avg_y, min_z))  

    # Skip if alreaady effectively there (optional tolerance)
    if p.length_squared == 0.0:
        return

    mesh = obj.data
    T_neg = mathutils.Matrix.Translation(-p)
    mesh.transform(T_neg)


    T_pos = mathutils.Matrix.Translation(p)
    obj.matrix_world = obj.matrix_world @ T_pos

# -------------------------------------------------------------------------

sel = list(bpy.context.selected_objects)
for ob in sel:
    set_origin_to_bottom_center(ob)


print(f"Adjusted origins for {len(sel)} selected object(s).")
