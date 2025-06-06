from textnode import TextType, TextNode

class HTMLNode():
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag      = tag
		self.value    = value
		self.children = children
		self.props    = props

	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self):
		attr_string = ""
		if self.props is not None:
			for key, value in self.props.items():
				attr_string += f" {key}=\"{value}\""

		return attr_string

	def __eq__(self, other):
		if not isinstance(other, HTMLNode):
			return False

		if (self.tag      == other.tag      and
			self.value    == other.value    and
			self.children == other.children and
			self.props    == other.props):
			return True
		return False

	def __repr__(self):
		class_string = f"HTMLNode(\n{self.tag},\n{self.value},\n{self.children},\n{self.props},\n)"
		return class_string

class LeafNode(HTMLNode):
	def __init__(self, tag = None, value = None, props = None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		html_string = ""

		# Case with no value
		if self.value is None:
			if self.tag != "img" and self.tag != "a":
				raise ValueError(f"All leaf nodes must have a value at <{self.tag}>{self.value}</{self.tag}>")

		# Case with text node
		if self.tag is None:
			html_string = f"{self.value}"
		else:
			if self.tag == "img":
				# Image
				html_string = f"<{self.tag}{self.props_to_html()}></{self.tag}>"
			else:
				# Normal case
				html_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

		return html_string

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		html_string = ""

		# Case with no tag
		if self.tag is None:
			print(self)
			raise ValueError("All parent nodes must have a tag")

		# Case with no childrent
		if self.children is None:
			print(self)
			raise ValueError("All parent nodes must have a child")

		# Normal case
		children_string = ""
		for node in self.children:
			children_string += node.to_html()

		html_string = f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"

		return html_string


def text_node_to_html_node(text_node):
	match(text_node.text_type):
		case TextType.NORMAL:
			return LeafNode(None, text_node.text.replace('\n', ' '))
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})

		case _:
			raise ValueError("Invalid Text Type {}".format(text_node.text_type))



