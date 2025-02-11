import unittest
from utilities import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_should_return_new_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT) 
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 3)

    def test_should_raise_error_when_no_matching_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.NORMAL_TEXT)
        with self.assertRaisesRegex(ValueError, "Unmatched delimiter '`' in text: This is text with a `code block word"):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_should_return_new_nodes_with_italic_demlimiter(self):
        node = TextNode("This is *italic* text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC_TEXT)

    def test_should_return_new_nodes_with_bold_demlimiter(self):
        node = TextNode("This is **bold** text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

   
class TestExtractMarkdownImages(unittest.TestCase):
    def test_should_return_tuple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(result[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_should_return_tuple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(result[1], ("to youtube", "https://www.youtube.com/@bootdotdev"))
