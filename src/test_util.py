import unittest
from htmlnode import HTMLNode
from textnode import TextType, TextNode
from util import *

class TestSplitNodeDelimiter(unittest.TestCase):

	def test_basic_split(self):
		nodes = [TextNode("This is *bold* text", TextType.NORMAL)]
		result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
		self.assertEqual(len(result), 3)
		self.assertEqual(result[0].text, "This is ")
		self.assertEqual(result[0].text_type, TextType.NORMAL)
		self.assertEqual(result[1].text, "bold")
		self.assertEqual(result[1].text_type, TextType.BOLD)
		self.assertEqual(result[2].text, " text")
		self.assertEqual(result[2].text_type, TextType.NORMAL)

	def test_multiple_splits(self):
		nodes = [TextNode("A *bold* and *strong* case", TextType.NORMAL)]
		result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
		self.assertEqual(len(result), 5)
		self.assertEqual(result[1].text, "bold")
		self.assertEqual(result[3].text, "strong")

	def test_no_delimiter(self):
		nodes = [TextNode("No formatting here", TextType.NORMAL)]
		result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].text, "No formatting here")
		self.assertEqual(result[0].text_type, TextType.NORMAL)

	def test_odd_number_of_delimiters(self):
		nodes = [TextNode("Unmatched *bold start", TextType.NORMAL)]
		result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].text_type, TextType.NORMAL)
		self.assertEqual(result[1].text_type, TextType.BOLD)  # Treats as formatted even without closing

	def test_multiple_nodes(self):
		nodes = [
			TextNode("One **bold**", TextType.NORMAL),
			TextNode(" and **another**", TextType.NORMAL)
		]
		result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
		self.assertEqual(len(result), 4)
		self.assertEqual(result[1].text, "bold")
		self.assertEqual(result[3].text, "another")
	
class TestExtractMarkdownImages(unittest.TestCase):

	def test_single_image(self):
		text = "Here is an image ![cat](http://cat.com/cat.png)"
		result = extract_markdown_images(text)
		self.assertEqual(result, [("cat", "http://cat.com/cat.png")])

	def test_multiple_images(self):
		text = "![dog](http://dog.png) and ![bird](http://bird.png)"
		result = extract_markdown_images(text)
		self.assertEqual(result, [
			("dog", "http://dog.png"),
			("bird", "http://bird.png")
		])

	def test_image_with_spaces(self):
		text = "Image: ![a dog photo](https://x.com/photo.png)"
		result = extract_markdown_images(text)
		self.assertEqual(result, [("a dog photo", "https://x.com/photo.png")])

	def test_no_images(self):
		text = "This text has no markdown images."
		result = extract_markdown_images(text)
		self.assertEqual(result, [])

	def test_image_with_nested_brackets(self):
		text = "Broken ![alt [bracket]](https://x.com)"
		result = extract_markdown_images(text)
		self.assertEqual(result, [("alt [bracket]", "https://x.com")])

class TestSplitNodesImages(unittest.TestCase):

	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.NORMAL,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.NORMAL),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.NORMAL),
				TextNode(
					"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
		)

	def test_split_images_middle(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another",
			TextType.NORMAL,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.NORMAL),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another", TextType.NORMAL),
			],
			new_nodes,
		)

class TestSplitNodesLinks(unittest.TestCase):

	def test_split_links(self):
		node = TextNode(
			"This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
			TextType.NORMAL,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.NORMAL),
				TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.NORMAL),
				TextNode(
					"second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
		)

	def test_split_links_middle(self):
		node = TextNode(
			"This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another",
			TextType.NORMAL,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.NORMAL),
				TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another", TextType.NORMAL),
			],
			new_nodes,
		)

class TestTextToTextNodes(unittest.TestCase):

	def test_split(self):
		self.maxDiff = 1000
		input_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		nodes_actual = text_to_textnodes(input_text)
		nodes_expected = [
			TextNode("This is ", TextType.NORMAL),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.NORMAL),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.NORMAL),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.NORMAL),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.NORMAL),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		self.assertEqual(nodes_expected, nodes_actual)

class TestMarkdownToBlocks(unittest.TestCase):

	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)

class TestMarkdownToHTML(unittest.TestCase):
	
	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
		)

	def test_heading(self):
		md = """### Some heading"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h3>Some heading</h3></div>"
		)

	def test_quote(self):
		md = """
> Some quote
> Some other _line_ in the same quote
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><blockquote>Some quote\nSome other _line_ in the same quote\n</blockquote></div>"
		)

	def test_unordered_list(self):
		md = """
- Some quote
- Some other _line_ in the same quote
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>Some quote</li><li>Some other <i>line</i> in the same quote</li></ul></div>"
		)
	
	def test_ordered_list(self):
		md = """
1. Some quote
2. Some other _line_ in the same quote
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ol><li>Some quote</li><li>Some other <i>line</i> in the same quote</li></ol></div>"
		)

	def test_image(self):
		md = """ # Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>Tolkien Fan Club</h1><p><img src=\"/images/tolkien.png\" alt=\"JRR Tolkien sitting\"></img></p><p>Here's the deal, <b>I like Tolkien</b>.</p></div>"
		)

if __name__ == "__main__":
	unittest.main()
