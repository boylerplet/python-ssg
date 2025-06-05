import unittest

from markdownblock import *

class TestBlockToBlockType(unittest.TestCase):

	def test_heading(self):
		md = "# This is a heading"
		self.assertEqual(block_to_block_type(md), BlockType.HEADING)

	def test_code_block(self):
		md = "```python\nprint('Hello, world!')\n```"
		self.assertEqual(block_to_block_type(md), BlockType.CODE)

	def test_quote_block_single_line(self):
		md = "> This is a quote"
		self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

	def test_quote_block_multi_line(self):
		md = "> First line\n> Second line"
		self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

	def test_unordered_list_single(self):
		md = "- Item 1"
		self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

	def test_unordered_list_multi(self):
		md = "- Item 1\n- Item 2"
		self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

	def test_ordered_list_proper(self):
		md = "1. Item 1\n2. Item 2\n3. Item 3"
		self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

	def test_paragraph(self):
		md = "This is just a paragraph"
		self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()
