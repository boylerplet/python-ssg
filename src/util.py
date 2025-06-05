import re
from pprint import pprint # DEBUG
from functools import reduce
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from markdownblock import BlockType, block_to_block_type

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
	result_nodes = []
	for node in old_nodes:
		split = node.text.split(delimiter)
		# print(f"[SPLIT]: {split}") # DEBUG
		if len(split) == 1:
			result_nodes.append(node)
			continue

		for i, part in enumerate(split):
			if i % 2 != 0:
				result_nodes.append(TextNode(part, text_type))
			else:
				if part == "":
					continue
				result_nodes.append(TextNode(part, TextType.NORMAL))

	return result_nodes

def extract_markdown_images(text: str) -> list[tuple]:
	re_pattern = r"!\[(.*?)\]\((.*?)\)"
	matches = re.findall(re_pattern, text)
	return matches

def extract_markdown_links(text: str) -> list[tuple]:
	re_pattern = r"\[(.*?)\]\((.*?)\)"
	matches = re.findall(re_pattern, text)
	return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	sections = []
	for node in old_nodes:
		images = extract_markdown_images(node.text)
		if len(images) == 0:
			sections.append(node)
			continue

		current_text = node.text
		for i, (image_alt, image_link) in enumerate(images):
			# print(f"len(images): {len(images)}\n") # DEBUG
			[before, after] = current_text.split(f"![{image_alt}]({image_link})", 1)
			sections.append(TextNode(before, TextType.NORMAL))
			sections.append(TextNode(image_alt, TextType.IMAGE, image_link))
			current_text = after
			i += 1

			if i == len(images) and after != "":
				# print("last", after) # DEBUG
				sections.append(TextNode(after, TextType.NORMAL))

	return sections

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	sections = []
	for node in old_nodes:
		links = extract_markdown_links(node.text)
		if len(links) == 0:
			sections.append(node)
			continue

		current_text = node.text
		for i, (alt, link) in enumerate(links):
			[before, after] = current_text.split(f"[{alt}]({link})", 1)
			sections.append(TextNode(before, TextType.NORMAL))
			sections.append(TextNode(alt, TextType.LINK, link))
			current_text = after
			i += 1

			if i == len(links) and after != "":
				sections.append(TextNode(after, TextType.NORMAL))

	return sections

def compose(*functions):
	def composed(arg):
		return reduce(lambda acc, fn: fn(acc), reversed(functions), arg)
	return composed

def text_to_textnodes(text):
	initial_node = [TextNode(text, TextType.NORMAL)]
	pipeline = compose(
		lambda nodes: split_nodes_delimiter(nodes, "`", TextType.CODE),
		lambda nodes: split_nodes_delimiter(nodes, "_", TextType.ITALIC),
		lambda nodes: split_nodes_delimiter(nodes, "**", TextType.BOLD),
		split_nodes_link,
		split_nodes_image,
	)

	return pipeline(initial_node)

def markdown_to_blocks(markdown: str):
	blocks = list(
		filter(
			lambda x: x != '',
			map(
				lambda x: x.strip(),
				markdown.split('\n\n')
			)
		)
	)
	return blocks

def markdown_to_html_node(markdown: str):
	blocks = markdown_to_blocks(markdown)
	node_children = []

	for block in blocks:
		block_type = block_to_block_type(block)
		# print(f"[BLOCK]: {block}")

		# print(block_type)
		match (block_type):
			case BlockType.HEADING:
				re_heading_pattern = r"(#{1,6}) (.*)"
				match_heading = re.match(re_heading_pattern, block)
				if match_heading is None:
					raise Exception("Heading is not detected")

				heading_level, heading_text = match_heading.groups()
				heading_node = ParentNode(f"h{len(heading_level)}", [LeafNode(None, heading_text)])
				node_children.append(heading_node)


			case BlockType.CODE:
				codeblock_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, block.strip("```").strip("\n"))])])
				node_children.append(codeblock_node)

			case BlockType.QUOTE:
				lines = block.split('\n')
				quote_node = ParentNode("blockquote",
					map(
						lambda x: LeafNode(
							None,
							x.lstrip('> ') + '\n'
						),
						lines
					)
				)

				node_children.append(quote_node)

			case BlockType.UNORDERED_LIST:
				lines = block.split('\n')
				list_items = []

				list_items = map(
					lambda li_text:
						ParentNode(
							"li",
							map(
								lambda li_node:
									text_node_to_html_node(li_node),
									text_to_textnodes(li_text.lstrip('- '))
							)
						),
					lines
				)

				unordered_list_node = ParentNode("ul", list_items)
				node_children.append(unordered_list_node)

			case BlockType.ORDERED_LIST:
				lines = block.split('\n')
				list_items = []

				list_items = map(
					lambda li_text: ParentNode(
						"li",
						map(
							lambda li_node:
								text_node_to_html_node(li_node),
								text_to_textnodes(li_text.lstrip('0123456789. '))
						)
					),
					lines
				)

				ordered_list_node = ParentNode("ol", list_items)
				node_children.append(ordered_list_node)

			case BlockType.PARAGRAPH:
				nodes = list(
					map(
						lambda x:
							text_node_to_html_node(x),
							text_to_textnodes(block)
					)
				)

				paragraph_node = ParentNode("p", nodes)
				node_children.append(paragraph_node)

	node = ParentNode("div", node_children)
	return node
