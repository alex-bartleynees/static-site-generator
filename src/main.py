from pathlib import Path
from src.generate import copy_static, generate_page, generate_page_recursive


def main():
    copy_static()
    root_dir = Path(__file__).parents[1].resolve()
    from_path = f"{root_dir}/content"
    template_path = f"{root_dir}/template.html"
    dest_path = f"{root_dir}/public"
    generate_page_recursive(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
