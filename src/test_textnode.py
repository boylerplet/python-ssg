import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_none(self):
		node = TextNode("This is a text node", TextType.LINK, "somestring")
		if node.text_type == TextType.LINK:
			self.assertNotEqual(node.url, None)

		node2 = TextNode("This is an image node", TextType.IMAGE, "somestring")
		if node2.text_type == TextType.IMAGE:
			self.assertNotEqual(node2.url, None)

	def test_textnode_not_equal_different_url(self):
		node1 = TextNode("hello", TextType.BOLD, "https://example.com")
		node2 = TextNode("hello", TextType.BOLD, None)
		self.assertNotEqual(node1, node2)

	def test_textnode_not_equal_different_text_type(self):
		node1 = TextNode("hello", TextType.BOLD, None)
		node2 = TextNode("hello", TextType.ITALIC, None)
		self.assertNotEqual(node1, node2)

	def test_textnode_not_equal_different_text(self):
		node1 = TextNode("hello", TextType.BOLD, None)
		node2 = TextNode("world", TextType.BOLD, None)
		self.assertNotEqual(node1, node2)

	def test_textnode_url_both_none_equal(self):
		node1 = TextNode("hello", TextType.BOLD, None)
		node2 = TextNode("hello", TextType.BOLD, None)
		self.assertEqual(node1, node2)

	def test_textnode_not_equal_type_mismatch(self):
		node = TextNode("hello", TextType.BOLD, None)
		not_a_node = "Not a TextNode"
		self.assertNotEqual(node, not_a_node)

if __name__ == "__main__":
	unittest.main()
