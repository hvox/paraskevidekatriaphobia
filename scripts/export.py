import bpy
from math import log
from pathlib import Path

meshes = {}
for obj in bpy.data.objects:
    if obj.type != "MESH":
        continue
    meshes[obj.name.lower()] = obj.data

binary = bytearray()
for name in [
    "engineer",
    "engineer glasses",
    "engineer hair",
    "engineer head",
    "spider",
    "spider leg",
    "chicken",
    "printer",
    "portal",
    "basement",
    "drill",
    "cube",
]:
    mesh = meshes[name]

    x_max = max(abs(v.co.x) for v in mesh.vertices)
    y_max = max(abs(v.co.y) for v in mesh.vertices)
    z_max = max(abs(v.co.z) for v in mesh.vertices)
    power = int(log(max(x_max, y_max, z_max) / 127) / log(0.9))
    scale = 0.9**power

    color = mesh.materials[0].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:]
    print(f" {name.capitalize()} : v={len(mesh.vertices)} f={len(mesh.polygons)} x={scale*127:.3f} {color=}")
    binary.extend(round((x**0.5) * 255) for x in color[0:3])
    binary.append(mesh.polygons[0].use_smooth)
    binary.append(power)
    binary.append(len(mesh.vertices))
    for v in mesh.vertices:
        binary.extend([round(x / scale) + 128 for x in v.co])
    binary.append(len(mesh.polygons))
    for poly in mesh.polygons:
        assert poly.loop_total == 4
        for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
            binary.append(mesh.loops[loop_index].vertex_index)

path = Path("models.bin").resolve()
print(path)
path.write_bytes(binary)
