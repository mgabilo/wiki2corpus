#!/usr/bin/python3
# 2009, 2018 Michael Gabilondo

PERL_CMD='/usr/bin/perl'
PHP_CMD='/usr/bin/php'
SED_CMD='/bin/sed'


import os, sys
import xml.parsers.expat
import codecs
import xml
import pdb
import re
from subprocess import Popen
from subprocess import PIPE
from bz2 import BZ2File
from nltk.corpus import wordnet as nlwn
import codecs

garbage_line_re = re.compile(r'^\s*[#:*={}|!]')
garbage_line_re2 = re.compile(r'^\s*\[\[Image')
garbage_line_re3 = re.compile(r'^\s*\[\[[^]]+:[^]]+\]\]$')
garbage_line_re_list = [garbage_line_re, garbage_line_re2, garbage_line_re3]

intro_list_re = re.compile(r'((\. )|^)([A-Z]|"|\')[^.]+:$')

ref_end_re = re.compile(r'<ref>.*')
ref2_end_re = re.compile(r'<ref .*>$')
ref3_end_re = re.compile(r'<ref .*> \.$')

comment_start_re = re.compile(r'<!--.*')
comment_end_re = re.compile(r'.*?-->')
sentence_re = re.compile(r'^([A-Z]|").*[.?!"]$')

garbage_final = re.compile(r'[|{}<>&]|\[|\]')
def count_chars(line, char):
	n = 0
	for c in line:
		if c == char:
			n += 1
	
	return n

def final_filter(sentences):
	for line in sentences:
		if not garbage_final.search(line):
			if count_chars(line, '"') % 2 == 0:
				if sentence_re.search(line):
					yield line
					yield ''

# use only within sentence, not text chunk
sentence_comment_re = re.compile(r'<!--.*?-->')

SENT_BOUNDARY_CMD = ('%s sentence-boundary.pl -d HONORIFICS -i /dev/stdin -o /dev/stdout' % PERL_CMD).split()

URL_CMD = ('%s process_url.php' % PHP_CMD).split()

PRESPLIT_SED_CMD = ('%s -r -f presplit.sed' % SED_CMD).split()

quotes_re = re.compile(r'"(.*?)"')

pronouns = ['all', 'another', 'any', 'anybody', 'anyone', 'anything', \
		'both', 'each', 'either', 'everybody', 'everyone',\
		'everything', 'few', 'he', 'her', 'hers', 'herself', 'him', 'himself',\
		'his', 'I', 'i', 'it', 'its', 'itself', 'little', 'many', 'me', 'mine', \
		'more', 'most', 'much', 'myself', 'neither', 'nobody', \
		'none', 'nothing', 'one', 'one another', 'other', 'others', 'ours',\
		'ourselves', 'several', 'she', 'some', 'somebody', 'someone', 'something',\
		'that', 'theirs', 'them', 'themselves', 'these', 'they', 'this', 'those',\
		'us', 'we', 'what', 'whatever', 'which', 'whichever', 'who', 'whoever',\
		'whom', 'whomever', 'whose', 'you', 'yours', 'yourself', 'yourselves']

def is_missing_symchar(line, missing_check_chars):
	results = []

	for leftchar, rightchar in missing_check_chars:
		count = 0

		for c in line:
			# symmetric case
			if leftchar == rightchar:
				if leftchar == c and count == 0:
					count = 1
				elif leftchar == c and count == 1:
					count = 0

			else:
				# assymetric case
				if c == leftchar:
					count += 1
				elif c == rightchar:
					count -= 1

		if count != 0:
			results.append(True)
		else:
			results.append(False)
	return results

def remove_big_comment_sections(lines):
	in_comment = False
	new_lines = []

	for line in lines:
		if line.find('<!--') != -1 and line.find('-->') != -1:
			new_lines.append(line)
			continue

		if line.find('<!--') != -1 and not in_comment:
			in_comment = True
			continue

		elif line.find('-->') != -1 and in_comment:
			in_comment = False
			continue

		if not in_comment:
			new_lines.append(line)

	return new_lines

def remove_big_curly_sections(lines):
	in_curly = False
	new_lines = []

	for line_num, line in enumerate(lines):

		next_line = ''
		if line_num + 1 < len(lines):
			next_line = lines[line_num+1]

		if line.find('{{') != -1 and line.find('}}') != -1:
			new_lines.append(line)
			continue

		if line.startswith('{{') and line.endswith('|') and not in_curly:
			in_curly = True
			continue

		if line.startswith('{{') and next_line.startswith('|') and not in_curly:
			in_curly = True
			continue

		elif line.endswith('}}') and in_curly:
			in_curly = False
			continue

		if not in_curly:
			new_lines.append(line)

	return new_lines


def fix_italics_quotes(sentence):
	sentence = sentence.replace('""', '"')
	sentence = sentence.replace('"."', '."')

	quote_contents_list = quotes_re.findall(sentence)
	for quote_content in quote_contents_list:
		if len(quote_content.split()) != 1:
			continue
		if quote_content.lower() != quote_content:
			continue

		if quote_content in pronouns or len(nlwn.synsets(quote_content)) != 0:
			replace_source = '"' + quote_content + '"'
			sentence = sentence.replace(replace_source, quote_content)

	return sentence


def post_process_line(line):
	line = fix_italics_quotes(line)
	line = sentence_comment_re.sub('', line)
	line = ref_end_re.sub('', line)
	line = ref2_end_re.sub('', line)
	line = ref3_end_re.sub('', line)

	return line

def get_sentences(article_text):

	# get rid of block-wise garbage
	lines = [line.strip() for line in article_text.split('\n')]
	lines = remove_big_curly_sections(lines)
	lines = remove_big_comment_sections(lines)

	new_lines = []

	# get rid of line-wise garbage
	for line in lines:
		line = line.strip()

		filtered = False
		for garbage_line_re in garbage_line_re_list:
			if garbage_line_re.search(line):
				filtered = True

		line = intro_list_re.sub('.', line)

		if not filtered:
			new_lines.append(line)
	lines = new_lines

	# get rid of newlines and join the article as one long running line
	article_text = ' '.join(lines)

	# remove wiki markup and transform to plain text
	p1 = Popen(URL_CMD, stdin=PIPE, stdout=PIPE)
	p1.stdin.write(article_text.encode('utf-8'))
	p1.stdin.close()

	data = p1.stdout.read().decode('utf-8')
	p2 = Popen(PRESPLIT_SED_CMD, stdin=PIPE, stdout=PIPE)
	p2.stdin.write(data.encode('utf-8'))
	p2.stdin.close()
	data = p2.stdout.read().decode('utf-8')
	
	# split line by line after the article as been transformed to one long text
	# with no markup
	p3 = Popen(SENT_BOUNDARY_CMD, stdin=PIPE, stdout=PIPE)
	p3.stdin.write(data.encode('utf-8'))
	p3.stdin.close()
	stdout_data = p3.stdout.read()
	output = stdout_data.decode('utf-8', 'replace')

	sentences = []
	merge_next = False
	merge_txt = ''
	missing_check_chars = [ ('(', ')'), ('"', '"') ]

	for line in output.split('\n'):
		line = line.strip()
		if len(line) == 0: continue

		if merge_next:
			new_sentence = '%s%s\n' % (merge_txt, line)
			sentences.append(new_sentence)
			merge_next = False
			merge_txt = ''
			continue

		for boolval in is_missing_symchar(line, missing_check_chars):
			if boolval == True:
				merge_next = True
				merge_txt = line

		if not merge_next:
			sentences.append(line + '\n')


	new_sentences = []
	for line in sentences:
		new_sentences.append(post_process_line(line))
	sentences = new_sentences

	sentences = strip_comments(sentences)

	sentences = final_filter(sentences)

	return sentences

def strip_comments(sentences):
	in_comment = False
	new_sentences = []

	for sentence in sentences:
		if in_comment:
			if comment_end_re.search(sentence):
				sentence = comment_end_re.sub('', sentence)
				in_comment = False
				new_sentences.append(sentence)

		else:
			if comment_start_re.search(sentence):
				sentence = comment_start_re.sub('', sentence)
				in_comment = True
			new_sentences.append(sentence)

	for line in new_sentences:
		if len(line.strip()) > 0:
			yield line

class ParserHandler(object):
	def __init__(self):
		self.inpage = False
		self.intitle = False
		self.current_title = ''
		self.current_text = ''
	
	def start_element(self, name, attrs):
		if name == 'text':
			self.inpage = True

		if name == 'title':
			self.intitle = True

	def end_element(self, name):
		if name == 'text':

			if self.inpage and self.current_title and len(self.current_text) > 300:
				if not	self.current_title.startswith('User') and \
						self.current_title.lower().find('talk') == -1 and \
						self.current_title.find('ErrorArticle') == -1 and \
						self.current_title.find(':') == -1:

					sentences = get_sentences(self.current_text)
					sys.stdout.write('\n** Article: %s\n' % self.current_title)
					for s in sentences:
						sys.stdout.write('%s\n' % s.strip())

			self.inpage = False
			self.current_title = ''
			self.current_text = ''

		if name == 'title':
			self.intitle = False

	def char_data(self, data):
		if self.inpage:
			self.current_text += data

		elif self.intitle:
			self.current_title += data


wiki_corpus_file = ''
class read_xml(object):
	def __init__(self):
		self.re_initial = False
		self.filename = wiki_corpus_file
		self.fin = BZ2File(self.filename, 'r')

	def restart(self):
		self.re_initial = True

	def read(self, nbytes):

		# normally, if the parser throws an exception, it won't be able to keep
		# reading the file because it will be missing the proper headings. this
		# section is activated if self.restart() is called, and it inserts a
		# header into the read data artificially so the parser can continue.
		if self.re_initial:
			self.re_initial = False
			while True:
				line = self.fin.readline()
				if line.find('<text') != -1:
					break

			fin = open('wiki-header')
			s = '\n'.join([line for line in fin])
			fin.close()
			data = self.fin.read(nbytes - len(resend_str))
			if data:
				return resend_str + data
			else:
				return ''

		data = self.fin.read(nbytes)
		if not data:
			self.fin.close()
			raise IOError('EOF')
		return data

def main():
	global wiki_corpus_file
	wiki_corpus_file = sys.argv[2]
	file_type = sys.argv[1]

	if file_type == '-xmlbz2':

		fin_xml = read_xml()

		while 1:
			ph = ParserHandler()
			p = xml.parsers.expat.ParserCreate()

			p.StartElementHandler = ph.start_element
			p.EndElementHandler = ph.end_element
			p.CharacterDataHandler = ph.char_data
			try:
				p.ParseFile(fin_xml)
			except xml.parsers.expat.ExpatError as e:
				fin_xml.restart()
			except IOError as e:
				print(e)
				return

	elif file_type == '-plain':
		# a plain text file containing lines from within the <text> of
		# an article; used for testing
		article_text = open(wiki_corpus_file).read()
		sentences = get_sentences(article_text)
		for s in sentences:
			sys.stdout.write('%s\n' % s.strip())

if __name__ == "__main__":
	main()


