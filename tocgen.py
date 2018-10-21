import os
import re
import sys

REGEX_MARKDOWN_HEADER = re.compile(r'(#+) ?(.+)\n?')
REGEX_TAG_START = re.compile(r'<!--ts-->', re.IGNORECASE)
REGEX_TAG_END = re.compile(r'<!--te-->', re.IGNORECASE)

def is_markdown_file(file_path):
	return file_path[-3:].lower() == '.md'

def get_filenames(path, selector_lambda=None):
	# By default we select everything
	if selector_lambda == None:
		selector_lambda = lambda path : True

	files = []
	for root, directories, filenames in os.walk(path):
		for filename in filenames:
			if selector_lambda(filename):
				files.append(os.path.join(root, filename))

	return files;

def get_link_tag(header, link_tags_found):
	result = ''
	for c in header.lower():
		if c.isalnum():
			result += c
		elif c == ' ' or c == '-':
			result += '-'
		# else it's punctuation so we drop it.
		
	if result not in link_tags_found:
		link_tags_found[result] = 0
	else:
		link_tags_found[result] += 1
		result += '-' + str(link_tags_found[result])
	
	return '(#' + result + ')'

def generate_toc_lines(file_lines):
	toc = []
	link_tags_found = {}
	
	for line in file_lines:
		match = REGEX_MARKDOWN_HEADER.match(line)
		if match:
			# add spaces based on sub-level, add [Header], then figure out what the git link is for that header and add it
			toc_entry = '    ' * (len(match.group(1)) - 1) + '* [' + match.group(2) + ']' + get_link_tag(match.group(2), link_tags_found)
			toc.append(toc_entry + '\n')
	
	return toc
			
		

# Returns indexes in the strings where tag starts and where it finishes.
# Returns -1, -1 if tag not found
def find_tags(file_lines):
	current = 0
	for line in file_lines:
		if REGEX_TAG_START.match(line):
			for i in range(current + 1, len(file_lines)):
				if REGEX_TAG_END.match(file_lines[i]):
					return current, i
			# If we get here we didn't find a matching tag so just move on.
			return -1, -1
		
		current += 1
		
	return -1, -1

def main():
	md_files = get_filenames(sys.argv[1], is_markdown_file)
	
	for file in md_files:
		lines = []
		with open(file, 'r') as file_handle:
			lines = file_handle.readlines()
		
		start, end = find_tags(lines)
		
		if start != -1: # Found tags
			del lines[start+1:end] # Remove anything in between the tags (eg. the table of contents)
			
			toc_lines = generate_toc_lines(lines)
			
			with open(file, 'w') as write_handle:
				for i in range(0, start + 1):
					write_handle.write(lines[i])
				
				for line in toc_lines:
					write_handle.write(line)
					
				for i in range(start + 1, len(lines)):
					write_handle.write(lines[i])
					
if __name__ == "__main__":
	main()
