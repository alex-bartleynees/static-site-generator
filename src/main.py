from pathlib import Path
from src.generate import copy_static, generate_page


def main():
    copy_static()
    root_dir = Path(__file__).parents[1].resolve()
    from_path = f"{root_dir}/content/index.md"
    template_path = f"{root_dir}/template.html"
    dest_path = f"{root_dir}/public/index.html"
    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
