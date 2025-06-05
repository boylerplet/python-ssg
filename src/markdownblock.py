import re
from pprint import pprint # DEBUG
from enum import Enum

class BlockType(Enum):
	PARAGRAPH      = 1
	HEADING        = 2
	CODE           = 3
	QUOTE          = 4
	UNORDERED_LIST = 5
	ORDERED_LIST   = 6

def block_to_block_type(markdown_block: str):
	# HEADING
	re_heading_pattern = r"#{1,6} (.*)"
	match_heading = re.match(re_heading_pattern, markdown_block)
	if match_heading is not None:
		return BlockType.HEADING

	# CODEBLOCK
	re_codeblock_pattern = r"```(.|\n)*```"
	match_codeblock = re.match(re_codeblock_pattern, markdown_block)
	if match_codeblock is not None:
		# print("[DEBUG]: CODE BLOCK TYPE") # DEBUG
		return BlockType.CODE

	# QUOTE BLOCK
	re_quote_block_pattern = r"> (.*)(\n> .*)*"
	match_quoute_block = re.match(re_quote_block_pattern, markdown_block)
	if match_quoute_block is not None:
		# print("[DEBUG]: QUOTE BLOCK TYPE") # DEBUG
		return BlockType.QUOTE

	# UNORDERED LIST
	re_unordered_list_pattern = r"- (.*)(\n- .*)*"
	match_unordered_list_block = re.match(re_unordered_list_pattern, markdown_block)
	if match_unordered_list_block is not None:
		# print("[DEBUG]: UNORDERED LIST TYPE") # DEBUG
		return BlockType.UNORDERED_LIST

	# ORDERED LIST
	re_quote_block_pattern = r"(\d+)\. .*"
	mapped = list(map(lambda x: re.match(re_quote_block_pattern, x), markdown_block.split('\n')))

	lc = 1
	for match in mapped:
		# print(f"[DEBUG]: match    = {match}") # DEBUG
		if match == None:
			# print("[ERROR]: All lines in list do not match pattern")
			break

		list_num = match.groups()[0]
		# print(f"[DEBUG]: list_num = {list_num}")            # DEBUG
		# print(f"[DEBUG]: lc       = {lc}")                  # DEBUG
		# print(f"[DEBUG]: lc == ln = {lc == int(list_num)}") # DEBUG
		if lc == int(list_num):
			lc += 1
			continue
		else:
			# print("[ERROR]: Line numbers not sequential")
			break

	# print(f"[DEBUG]: len_mapped = {len(mapped)}") # DEBUG
	# print(f"[DEBUG]: lc         = {lc}")          # DEBUG
	if lc == (len(mapped) + 1):
		# print("[DEBUG]: ORDERED LIST TYPE") # DEBUG
		return BlockType.ORDERED_LIST

	return BlockType.PARAGRAPH

