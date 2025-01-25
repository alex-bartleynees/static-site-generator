import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_create_node(self):
        node = LeafNode("p", "test", {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "test")
        self.assertDictEqual(node.props, {"class": "text"})

    def test_tohtml_should_raise_value_error_when_no_value(self):
        node = LeafNode("p", None, {"class": "text"})
        self.assertRaises(ValueError, node.to_html)

    def test_tohtml_should_return_value_as_raw_string_when_no_tag(self):
        node = LeafNode(None, "test", {"class": "button"})
        result = node.to_html()
        self.assertEqual(result, "test")

    def test_tohtml_should_render_html_with_props(self):
        node = LeafNode("p", "test", {"class": "button"})
        result = node.to_html()
        self.assertEqual(result, '<p class="button">test</p>')

    def test_tohtml_should_render_html_without_props(self):
        node = LeafNode("p", "test", None)
        result = node.to_html()
        self.assertEqual(result, '<p>test</p>')



