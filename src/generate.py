from pathlib import Path
import shutil

def copy_static():
    current_path = Path(__file__).parent.resolve()
    new_path = f"{current_path.parent}/public"
    public_path = Path(new_path)
    if public_path.exists():
        shutil.rmtree(new_path)
    public_path.mkdir()
    copy_files(Path(f"{current_path.parent}/static"), public_path)

def copy_files(folder_path: Path, public_path: Path):
    folder = Path(folder_path)
    files = folder.glob("*")
    for file in files:
        if file.is_file():
            shutil.copy(file, public_path)
        elif file.is_dir():
            new_folder_path = Path(f"{public_path}/{file.parts[-1]}")
            new_folder_path.mkdir()
            copy_files(file, new_folder_path)


