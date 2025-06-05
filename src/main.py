import os
import shutil
import re
from util import markdown_to_html_node
# Delete all contents of public
# Copy all files and subdirectories nested files from static to public
# log path of each file copied

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
	logger.INFO(f"Generaing page from {from_path} to {dest_path} using {template_path}")

	md_text = ""
	template_text = ""
	with open(from_path) as md:
		md_text = md.read()

	with open(template_path) as template:
		template_text = template.read()

	html_node = markdown_to_html_node(md_text)
	html_text = html_node.to_html()

	page_title = extract_title(md_text)

	full_html = template_text.replace('{{ Title }}', page_title).replace('{{ Content }}', html_text)

	logger.INFO("Writing to file...")
	with open(dest_path) as html_file:
		html_file.write(full_html)

	logger.SUCCESS("Completed!!!")

def main():
	remove_public()
	copy_files_from_static()

	generate_page('./content/index.md', './template.html', './public/index.html')

main()
