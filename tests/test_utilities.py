import unittest
from src.utilities import extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_images, split_nodes_links, text_to_text_nodes
from src.textnode import TextNode, TextType

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

class TestSplitNodesImages(unittest.TestCase):
    def test_should_split_nodes_by_images(self):
        old_node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_images([old_node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "rick roll")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "obi wan")

    def test_should_return_nodes_when_no_images(self):
        old_node = TextNode(
                "This is text with no images",
                TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_images([old_node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no images")

    def test_should_handle_text_after_last_image(self):
        old_node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and text after image",
                TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_images([old_node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "rick roll")
        self.assertEqual(new_nodes[2].text, " and text after image")


class TestSplitNodesLinks(unittest.TestCase):
    def test_should_split_nodes_by_links(self):
        old_node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_links([old_node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "to youtube")

class TextToTextNodes(unittest.TestCase):
    def test_should_transform_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 10)

class MarkdownToBlocks(unittest.TestCase):
    def test_should_return_list_of_string(self):
        block = """# This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is the first list item in a list block
                * This is a list item
                * This is another list item"""

        result = markdown_to_blocks(block)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "# This is a heading")
        self.assertEqual(result[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
