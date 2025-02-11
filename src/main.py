from src.textnode import TextNode, TextType


def main():
    text_node = TextNode("test", TextType.NORMAL_TEXT, "test")
    print(text_node)


if __name__ == "__main__":
    main()
