from src.textnode import TextNode
from src.texttype import TextType


def main():
    text_node = TextNode("test", TextType.TEXT, "test")
    print(text_node)


if __name__ == "__main__":
    main()
