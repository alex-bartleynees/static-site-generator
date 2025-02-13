import unittest
from src.blocktype import BlockType
from src.utilities import block_to_block_type, extract_markdown_images, extract_markdown_links, extract_title, markdown_to_blocks, markdown_to_html, split_nodes_delimiter, split_nodes_images, split_nodes_links, text_to_text_nodes
from src.textnode import TextNode 
from src.texttype import TextType

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_should_return_new_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE) 
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(len(new_nodes), 3)

    def test_should_raise_error_when_no_matching_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "Unmatched delimiter '`' in text: This is text with a `code block word"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_should_return_new_nodes_with_italic_demlimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_should_return_new_nodes_with_bold_demlimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
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
                TextType.TEXT,
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
                TextType.TEXT,
        )
        new_nodes = split_nodes_images([old_node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no images")

    def test_should_handle_text_after_last_image(self):
        old_node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and text after image",
                TextType.TEXT,
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
                TextType.TEXT,
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

class BlockToBlockType(unittest.TestCase):
    def test_should_return_block_type_paragraph(self):
        block = "# Heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_should_return_block_type_code(self):
        block = "```code () => {}```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_should_return_block_type_quote(self):
        block = "> This is the greatest quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_should_return_block_type_unordered_list(self):
        block = """- List item 1
                   - List item 2
        """
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_should_return_block_type_ordered_list(self):
        block = """1. List item 1
                   2. List item 2
        """
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_should_return_block_type_ordered_paragraph(self):
        block = "This is a paragraph" 
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

class MarkdownToHTML(unittest.TestCase):
    def test_convert_markdown_to_html(self):
        markdown = """
        # *Heading* 1
        ## **Heading** 2
        ### Heading 3
        #### Heading 4
        ##### Heading 5
        ###### Heading 6

        Test paragraph
        Test paragraph 2

        - Unordered list 1
        - Unordered list 2

        > This is a quote
        > This is another quote

        ```
        () => {}
        ```

        ```
        () => Hello World
        ```

        1. List item 1
        2. List item 2

        **bold**

        *italic*

        This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)

        This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)



        """

        html = markdown_to_html(markdown)
        print(html.to_html())
        self.assertEqual(html.to_html(), '''<body><h1><i>Heading</i> 1</h1><h2><b>Heading</b> 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6><div>Test paragraph</div><div>        Test paragraph 2</div><ul><li>Unordered list 1</li><li>Unordered list 2</li></ul><blockquote>This is a quote</blockquote><blockquote>This is another quote</blockquote><div><code>
        () => {}
        </code></div><div><code>
        () => Hello World
        </code></div><ol><li> List item 1</li><li> List item 2</li></ol><div><b>bold</b></div><div><i>italic</i></div><div>This is text with a link <a href="https://www.boot.dev">to boot dev</a> and <a href="https://www.youtube.com/@bootdotdev">to youtube</a></div><div>This is <b>text</b> with an <i>italic</i> word and a <code>code block</code> and an <img src="https://i.imgur.com/fJRm4Vk.jpeg" alt="obi wan image"></img> and a <a href="https://boot.dev">link</a></div><div></div></body>'''
)

    def test_extract_title(self):
        markdown = """
        # *Heading* 1
        ## **Heading** 2
        ### Heading 3
        #### Heading 4
        ##### Heading 5
        ###### Heading 6

        Test paragraph
        Test paragraph 2

        - Unordered list 1
        - Unordered list 2

        > This is a quote
        > This is another quote

        ```() => {}```
        ```() => Hello World```

        1. List item 1
        2. List item 2

        **bold**

        *italic*

        This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)

        This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
        """

        result = extract_title(markdown)

        self.assertEqual(result, "Heading 1")
