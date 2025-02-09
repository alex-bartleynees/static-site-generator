import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_create_node_tag_is_not_optional(self):
        with self.assertRaisesRegex(ValueError, "value cannot be None"):  
            ParentNode(None, "p", {"class": "test"})

    def test_create_node_children_is_not_optional(self):
        with self.assertRaisesRegex(ValueError, "value cannot be None"):  
            ParentNode("p", None, {"class": "test"})

    def test_create_node_props_should_be_optional(self):
        node = ParentNode("p", "b")
        self.assertEqual(node.props, None)

    def test_to_html_should_raise_value_error_when_no_tag(self):
        node = ParentNode("p", "b")
        node.tag = None
        with self.assertRaisesRegex(ValueError, "Must have tag"):
            node.to_html()

    def test_to_html_should_raise_value_error_when_children_is_missing_value(self):
        node = ParentNode("p", "b")
        node.children = None
        with self.assertRaisesRegex(ValueError, "Must have children"):
            node.to_html()

    def test_to_html_should_render_html_with_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")])
        result = node.to_html()
        self.assertEqual(result, '<p><b>Bold text</b></p>')

    def test_to_html_should_render_html_with__multiple_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text")
                                ])
        result = node.to_html()
        self.assertEqual(result, '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_should_handle_nested_parent_nodes(self):
        parent_node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text")
                                ])
        node = ParentNode("div", [parent_node])

        result = node.to_html()

        self.assertEqual(result, '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>')

