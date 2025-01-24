import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_create_node_with_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        node = HTMLNode(props={"class": "button", "id": "button"})
        props_str = node.props_to_html()
        self.assertEqual(props_str, " class=button id=button")

    def test_eq(self):
        node = HTMLNode("div", "test", "p", {"class": "button"})
        node2 = HTMLNode("div", "test", "p", {"class": "button"})
        self.assertEqual(node, node2)

