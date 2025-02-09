from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    NORMAL_TEXT = "normal_text"
    BOLD = "bold_text"
    ITALIC_TEXT = "italic_text"
    CODE_TEXT = "code_text"
    LINKS = "links"
    IMAGES = "images"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(self):
        match self.text_type:
            case TextType.NORMAL_TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC_TEXT:
                return LeafNode("i", self.text)
            case TextType.CODE_TEXT:
                return LeafNode("code", self.text)
            case TextType.LINKS:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGES:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError(f"Invalid text type {self.text_type}")
