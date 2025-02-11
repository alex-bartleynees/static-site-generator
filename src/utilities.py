from typing import List, Tuple
from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

        count = node.text.count(delimiter)
        if count % 2 != 0:  
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        
        split_text = node.text.split(delimiter)
        for text in split_text:
            if text and not is_delimited_text(text, node.text, delimiter):
                new_nodes.append(TextNode(text=text, text_type=TextType.NORMAL_TEXT))
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
                new_nodes.append(TextNode(text=parts[0], text_type=TextType.NORMAL_TEXT))

            new_nodes.append(TextNode(text=image_alt, text_type=TextType.IMAGES, url=image_link))

            if len(parts) > 1:
                remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(text=remaining_text, text_type=TextType.NORMAL_TEXT))
    
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
                new_nodes.append(TextNode(text=parts[0], text_type=TextType.NORMAL_TEXT))

            new_nodes.append(TextNode(text=link_text, text_type=TextType.LINKS, url=link_url))

            if len(parts) > 1:
                remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(text=remaining_text, text_type=TextType.NORMAL_TEXT))
   
    return new_nodes

def text_to_text_nodes(text: str):
    base_node = TextNode(text=text, text_type=TextType.NORMAL_TEXT)
    new_nodes = split_nodes_links(split_nodes_images(split_nodes_delimiter(split_nodes_delimiter(
        split_nodes_delimiter([base_node], "**", TextType.BOLD), 
        "*", TextType.ITALIC_TEXT), "`", TextType.CODE_TEXT)))

    return new_nodes


    
