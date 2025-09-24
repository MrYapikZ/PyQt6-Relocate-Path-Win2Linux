import bpy
import re
import os

# Set to True for preview mode (no actual changes)
DRY_RUN = False


def relocate_lib(lib, new_path):
    abs_new = bpy.path.abspath(new_path)
    new_dir = os.path.dirname(abs_new)
    new_file = os.path.basename(abs_new)

    print(f"Relocating:\n  {lib.filepath}\n  -> {abs_new}")
    if DRY_RUN:
        return

    try:
        res = bpy.ops.library.relocate(
            library=lib.name,
            directory=new_dir + os.sep,
            filename=new_file,
        )
        print(f"  relocate result: {res}")
    except Exception as e:
        print(f"  relocate op failed, falling back to direct filepath set: {e}")
        lib.filepath = abs_new


# ---- main ----
changed = 0
for lib in bpy.data.libraries:
    old_path = lib.filepath

    m = re.match(r"([A-Za-z]):[\\/](.*)", old_path)
    if not m:
        print(f"Skipping (not a Windows drive path): {old_path}")
        continue

    drive = m.group(1).upper()
    rest = m.group(2).replace("\\", "/")
    new_path = f"/mnt/{drive}/{rest}"

    if bpy.path.abspath(old_path).replace("\\", "/") == bpy.path.abspath(new_path).replace("\\", "/"):
        print(f"Already correct: {old_path}")
        continue

    relocate_lib(lib, new_path)
    changed += 1

bpy.context.preferences.filepaths.use_relative_paths = True
bpy.ops.file.make_paths_relative()

reloaded = 0
for lib in bpy.data.libraries:
    try:
        lib.reload()
        print(f"Reloaded: {lib.filepath}")
        reloaded += 1
    except Exception as e:
        print(f"Could not reload {lib.filepath}: {e}")

print(f"Reloaded {reloaded} libraries.")

if not DRY_RUN and changed:
    #    bpy.ops.wm.save_mainfile()
    print(f"Saved .blend. Updated libraries: {changed}")
else:
    print("No changes saved (dry run or nothing to update).")
