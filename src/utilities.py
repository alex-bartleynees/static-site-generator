from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
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


def is_delimited_text(text, original_text, delimiter):
    start_pos = original_text.find(text)
    if start_pos == -1:
        return False
        
    before_delimiter = original_text[start_pos - len(delimiter):start_pos] == delimiter
    after_delimiter = original_text[start_pos + len(text):start_pos + len(text) + len(delimiter)] == delimiter
    
    return before_delimiter and after_delimiter

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
