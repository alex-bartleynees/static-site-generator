from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if tag is None or children is None:
            raise ValueError("value cannot be None")
        self.tag = tag
        self.children = children
        self.props = props
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Must have tag")
        if self.children is None:
            raise ValueError("Must have children")

        childTags = ""

        for child in self.children:
            childTags += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{childTags}</{self.tag}>"

