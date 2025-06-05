import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode

class TestHTMLNode(unittest.TestCase):
	def test_equal_nodes(self):
		node1 = HTMLNode("p", "Hello", None, {"class": "text"})
		node2 = HTMLNode("p", "Hello", None, {"class": "text"})
		self.assertEqual(node1, node2)

	def test_different_tag(self):
		node1 = HTMLNode("p", "Hello", None, {"class": "text"})
		node2 = HTMLNode("div", "Hello", None, {"class": "text"})
		self.assertNotEqual(node1, node2)

	def test_different_value(self):
		node1 = HTMLNode("p", "Hello", None, {"class": "text"})
		node2 = HTMLNode("p", "World", None, {"class": "text"})
		self.assertNotEqual(node1, node2)

	def test_different_props(self):
		node1 = HTMLNode("p", "Hello", None, {"class": "text"})
		node2 = HTMLNode("p", "Hello", None, {"id": "text"})
		self.assertNotEqual(node1, node2)

	def test_different_children(self):
		child1 = HTMLNode("span", "child", None, {})
		child2 = HTMLNode("span", "another child", None, {})
		node1 = HTMLNode("div", None, [child1], {})
		node2 = HTMLNode("div", None, [child2], {})
		self.assertNotEqual(node1, node2)

	def test_equal_with_none_children_and_props(self):
		node1 = HTMLNode("p", "text", None, None)
		node2 = HTMLNode("p", "text", None, None)
		self.assertEqual(node1, node2)

	def test_not_equal_to_non_node(self):
		node = HTMLNode("p", "text", None, {})
		self.assertNotEqual(node, "not an HTMLNode")

	def test_single_attribute(self):
		node = HTMLNode(props={"class": "button"})
		self.assertEqual(node.props_to_html(), ' class="button"')

	def test_multiple_attributes(self):
		node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
		result = node.props_to_html()
		# Order isn't guaranteed unless explicitly sorted
		self.assertIn('href="https://example.com"', result)
		self.assertIn('target="_blank"', result)
		self.assertEqual(len(result.strip().split()), 2)  # Two attributes

	def test_empty_props(self):
		node = HTMLNode(props={})
		self.assertEqual(node.props_to_html(), '')

	def test_none_props(self):
		node = HTMLNode(props=None)
		self.assertEqual(node.props_to_html(), '')

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

	def test_text(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_text_bold(self):
		node = TextNode("Bold text", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "Bold text")

	def test_text_italic(self):
		node = TextNode("Italic text", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "Italic text")

	def test_text_code(self):
		node = TextNode("code()", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "code()")

	def test_text_link(self):
		node = TextNode("Click me", TextType.LINK, "https://example.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "Click me")
		self.assertEqual(html_node.props, {"href": "https://example.com"})

	def test_unknown_type_raises(self):
		node = TextNode("Unknown", "weird")
		with self.assertRaises(ValueError):
			text_node_to_html_node(node)

if __name__ == "__main__":
	unittest.main()
