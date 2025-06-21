import os
import shutil


def scaffold(manifest, target_dir=r"output\\final_project"):
    # 1. Clean and recreate the target dir
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    # 2. Create all folders
    for folder in manifest["folders"]:
        os.makedirs(os.path.join(target_dir, folder), exist_ok=True)

    # 3. Write all files
    for relpath, content in manifest["files"].items():
        fullpath = os.path.join(target_dir, relpath)
        # ensure parent dir exists
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        with open(fullpath, "w", encoding="utf-8") as f:
            f.write(content)

    # 4. Zip it up
    shutil.make_archive(target_dir, "zip", target_dir)
    print(f"Project scaffolded and zipped as {target_dir}.zip")
