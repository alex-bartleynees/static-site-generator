import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_all_properties(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT, "test.com")
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.ITALIC_TEXT)
        self.assertEqual(node.url, "test.com")

    def test_url_is_none_when_empty(self):
        node = TextNode("test", TextType.ITALIC_TEXT)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
