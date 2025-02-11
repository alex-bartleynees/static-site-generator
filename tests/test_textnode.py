import unittest

from src.leafnode import LeafNode
from src.textnode import TextNode, TextType


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

    def test_text_node_to_html_node(self):
        node = TextNode("test", TextType.NORMAL_TEXT)
        expected_result = LeafNode(None, "test")
        result = node.text_node_to_html_node()
        self.assertEqual(result, expected_result)

    def test_text_node_to_html_node_invalid(self):
        node = TextNode("test", "silly")
        with self.assertRaisesRegex(ValueError, "Invalid text type silly"):
            node.text_node_to_html_node()
        
        


if __name__ == "__main__":
    unittest.main()
