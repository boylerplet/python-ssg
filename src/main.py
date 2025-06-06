import os
import shutil
import re
from util import markdown_to_html_node

class Logger():
	def __init__(self, enabled = True):
		self.enabled = enabled

	def SUCCESS(self, message):
		if self.enabled:
			print(f"[SUCCESS]: {message}")
	def INFO(self, message):
		if self.enabled:
			print(f"[INFO]: {message}")
	def WARN(self, message):
		if self.enabled:
			print(f"[WARN]: {message}")
	def ERROR(self, message):
		if self.enabled:
			print(f"[ERROR]: {message}")
	def LOG(self, message):
		if self.enabled:
			print(f"[LOG]: {message}")
	def DEBUG(self, message):
		if self.enabled:
			print(f"[DEBUG]: {message}")

logger = Logger(enabled=True)

def remove_public():
	logger.INFO("Checking for public directory...")
	if os.path.exists('public'):
		logger.INFO("Removing public directory...")
		shutil.rmtree('public')
	os.mkdir('public')
	logger.INFO("Created new public directory...")

def copy_files_from_static(src_path = './static', dest_path = './public'):
	# Create dest if not exist
	if os.path.exists(dest_path) == False:
		os.mkdir(dest_path)

	if os.path.exists(src_path):
		ls = os.listdir(src_path)
		for i in ls:
			# FILE
			if os.path.isfile(os.path.join(src_path, i)):
				logger.INFO(f"Copy '{os.path.join(src_path, i)}' to '{os.path.join(dest_path, i)}'") 
				shutil.copy(os.path.join(src_path, i), os.path.join(dest_path, i))
			# DIR
			elif os.path.isdir(os.path.join(src_path, i)):
				copy_files_from_static(os.path.join(src_path, i), os.path.join(dest_path, i))

def extract_title(markdown: str):
	re_h1_pattern = r"# .*"
	matches = re.findall(re_h1_pattern, markdown)

	if len(matches) < 1:
		raise Exception("No H1 element in Markdown file")

	return matches[0].lstrip('# ')

def generate_page(from_path: str, template_path: str, dest_path: str):
	logger.INFO(f"Generaing page from '{from_path}' to '{dest_path}' using '{template_path}'")

	# Check destination exists
	dirs = '/'.join(dest_path.split('/')[:-1])
	if os.path.exists(dirs):
		logger.INFO(f"Dir Exists '{dirs}'")
	else:
		logger.INFO(f"Dir does not exist '{dirs}'")
		logger.INFO(f"Creating dir '{dirs}'...")
		os.makedirs(dirs)
		logger.INFO(f"Dir Created!!! '{dirs}'...")

	# Create file
	md_text = ""
	template_text = ""
	with open(from_path) as md:
		md_text = md.read()

	with open(template_path) as template:
		template_text = template.read()

	html_node = markdown_to_html_node(md_text)
	# print(html_node)
	html_text = html_node.to_html()

	page_title = extract_title(md_text)

	full_html = template_text.replace('{{ Title }}', page_title).replace('{{ Content }}', html_text)

	logger.INFO("Writing to file...")
	with open(dest_path, "w") as html_file:
		html_file.write(full_html)

	logger.SUCCESS(f"Completed generating HTML file at '{dest_path}' !!!")

def generate_pages_recursive(content_dir_path: str, template_path: str, dest_dir_path: str):
	content_dir_items = os.listdir(content_dir_path)

	for file in content_dir_items:
		# logger.DEBUG(f"Processing path '{content_dir_path}/{file}'")
		if os.path.isfile(os.path.join(content_dir_path, file)) and os.path.splitext(file)[1] == ".md":
			logger.INFO(f"FOUND .md file '{file}' at '{content_dir_path}'")
			generate_page(os.path.join(content_dir_path, file), template_path, os.path.join(dest_dir_path, os.path.splitext(file)[0] + ".html"))

		elif os.path.isdir(os.path.join(content_dir_path, file)):
			generate_pages_recursive(os.path.join(content_dir_path, file), template_path, os.path.join(dest_dir_path, file))

def main():
	remove_public()
	copy_files_from_static()

	generate_pages_recursive('./content', './template.html', './public')

main()
