from typing import List, Tuple
from src.parentnode import ParentNode
from src.htmlnode import HTMLNode
from src.blocktype import BlockType
from src.textnode import TextNode
from src.texttype import TextType
import re


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        count = node.text.count(delimiter)
        if count % 2 != 0:  
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        
        split_text = node.text.split(delimiter)
        for text in split_text:
            if text and not is_delimited_text(text, node.text, delimiter):
                new_nodes.append(TextNode(text=text, text_type=TextType.TEXT))
            elif is_delimited_text(text, node.text, delimiter):
                new_nodes.append(TextNode(text=text, text_type=text_type))
            
    return new_nodes


def is_delimited_text(text: str, original_text: str, delimiter: str) -> bool:
    start_pos = original_text.find(text)
    if start_pos == -1:
        return False
        
    before_delimiter = original_text[start_pos - len(delimiter):start_pos] == delimiter
    after_delimiter = original_text[start_pos + len(text):start_pos + len(text) + len(delimiter)] == delimiter
    
    return before_delimiter and after_delimiter

def extract_markdown_images(text) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for image_alt, image_link in images:
            parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if parts[0]:
                new_nodes.append(TextNode(text=parts[0], text_type=TextType.TEXT))

            new_nodes.append(TextNode(text=image_alt, text_type=TextType.IMAGE, url=image_link))

            if len(parts) > 1:
                remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(text=remaining_text, text_type=TextType.TEXT))
    
    return new_nodes

def split_nodes_links(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for link_text, link_url in links:
            parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(text=parts[0], text_type=TextType.TEXT))

            new_nodes.append(TextNode(text=link_text, text_type=TextType.LINK, url=link_url))

            if len(parts) > 1:
                remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(text=remaining_text, text_type=TextType.TEXT))
   
    return new_nodes

def text_to_text_nodes(text: str) -> List[TextNode]:
    base_node = TextNode(text=text, text_type=TextType.TEXT)
    new_nodes = split_nodes_links(
    split_nodes_images(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [base_node], 
                        "**", TextType.BOLD
                    ),
                    "*", TextType.ITALIC
                ),
                "_", TextType.ITALIC  
            ),
            "`", TextType.CODE
        )
    )
)

    return new_nodes


def markdown_to_blocks(text: str) -> List[str]:
    blocks = text.split("\n\n")
    blocks = [block.strip() for block in blocks if block]

    return blocks
 
def block_to_block_type(block: str) -> BlockType:
    if re.match(r'^#{1,6}\s', block):
        return BlockType.HEADING
    if re.match(r'^```(?!`)[\s\S]*```(?!`)$', block):
        return BlockType.CODE
    if re.match(r'^>(?!>)\s', block):
        return BlockType.QUOTE
    if re.match(r'\s*[*-]\s.*(?:\n\s*[*-]\s.*)*', block):
        return BlockType.UNORDERED_LIST
    if re.match(r'^(\s*)(\d+\.\s+)(.*)', block) and validate_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def validate_ordered_list(text: str) -> bool:
    lines = text.strip().split('\n')
    expected_number = 1
    for line in lines:
        number = int(line.strip().split('.')[0])
        if number != expected_number:
            return False
        expected_number += 1
    return True

def markdown_to_html(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                text_nodes = text_to_text_nodes(block)
                html_nodes = [node.text_node_to_html_node() for node in text_nodes]
                parent_nodes.append(ParentNode("div", html_nodes))
            case BlockType.HEADING:
                parent_nodes = [*parent_nodes, *heading_block_to_html_nodes(block)] 
            case BlockType.PARAGRAPH:
                split_blocks = block.split("\n")
                for text in split_blocks:
                    text_nodes = text_to_text_nodes(text)
                    html_nodes = [node.text_node_to_html_node() for node in text_nodes]
                    parent_nodes.append(ParentNode("div", html_nodes))
            case BlockType.QUOTE:
                split_blocks = block.split("\n")
                for quote in split_blocks:
                    text_nodes = text_to_text_nodes(quote.strip(" > "))
                    html_nodes = [node.text_node_to_html_node() for node in text_nodes]
                    parent_nodes.append(ParentNode("blockquote", html_nodes))
            case BlockType.UNORDERED_LIST:
                split_blocks = block.split("\n")
                list_item_nodes = []
                for list_item in split_blocks:
                    stripped = list_item.lstrip()
                    if stripped.startswith('* '):
                        content = stripped[2:]  
                    elif stripped.startswith("- "):
                        content = stripped[2:]
                    else:
                        content = list_item
                    text_nodes = text_to_text_nodes(content)
                    html_nodes = [node.text_node_to_html_node() for node in text_nodes]
                    list_item_nodes.append(HTMLNode("li", children=html_nodes))
                parent_list_node = HTMLNode("ul", children=list_item_nodes)
                parent_nodes.append(parent_list_node)
            case BlockType.ORDERED_LIST:
                split_blocks = block.split("\n")
                list_item_nodes = []
                for list_item in split_blocks:
                    stripped = list_item.lstrip()
                    text_nodes = text_to_text_nodes(stripped[2:].strip())
                    html_nodes = [node.text_node_to_html_node() for node in text_nodes]
                    list_item_nodes.append(HTMLNode("li", children=html_nodes))
                parent_list_node = HTMLNode("ol", children=list_item_nodes)
                parent_nodes.append(parent_list_node)
                

    body_node = HTMLNode(tag="body", children=parent_nodes)
    return body_node

def heading_block_to_html_nodes(block: str) -> List[HTMLNode]:
    split_headings = block.split("\n")
    nodes = []
    for heading in split_headings:
        heading_number = heading.count("#")
        text_nodes = text_to_text_nodes(heading.strip(" # "))
        html_nodes = [node.text_node_to_html_node() for node in text_nodes]
        nodes.append(ParentNode(f"h{heading_number}", html_nodes))
    return nodes

def extract_title(markdown: str) -> str:
    match = re.search(r'^\s*#(?!#)\s+(.+)', markdown.strip())
    if match:
        cleaned_title = re.sub(r'\*{1,2}', '', match.group(1))
        return cleaned_title
    else:
        raise ValueError("Document must have a title")
