
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("Must have tag")
        if self.children is None:
            raise ValueError("Must have children")

        childTags = ""

        for child in self.children:
            childTags += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{childTags}</{self.tag}>"

    def props_to_html(self):
        props_str = ""
        if self.props is None:
            return props_str

        for (key, value) in self.props.items():
            props_str += f' {key}="{value}"'

        return props_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return (self.tag == other.tag and 
            self.value == other.value and 
            self.children == other.children and 
            self.props == other.props)
