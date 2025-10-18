import bpy
import mathutils

context = bpy.context
selected = context.selected_objects
active = context.view_layer.objects.active

if not selected or active not in selected or active.type != 'MESH':
    raise Exception("Select at least one mesh, and make sure the last selected (active) one is a mesh.")

bbox = [mathutils.Vector(corner) for corner in active.bound_box]
min_z = min(v.z for v in bbox)
avg_x = sum(v.x for v in bbox) / 8.0
avg_y = sum(v.y for v in bbox) / 8.0
bottom_center_local = mathutils.Vector((avg_x, avg_y, min_z))

target_world_pos = active.matrix_world @ bottom_center_local

for obj in selected:
    if obj.type != 'MESH':
        continue

    to_origin_local = obj.matrix_world.inverted() @ target_world_pos


    if obj.data.users > 1:
        obj.data = obj.data.copy()

    obj.data.transform(mathutils.Matrix.Translation(-to_origin_local))
    obj.matrix_world = obj.matrix_world @ mathutils.Matrix.Translation(to_origin_local)

print(f"Moved origins of {len(selected)} object(s) to bottom center of active object '{active.name}'.")
