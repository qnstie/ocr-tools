# This script assumes, that in the current directories there are files with JSON results of the Google Vision OCR output.
# They can be obtained by manual OCR at https://cloud.google.com/vision/docs/drag-and-drop
# API is accessible at https://vision.googleapis.com/v1/images:annotate
# The script processess all .json files sorted by name and outputs a series of test files wth the text output, 
# trying to post-process some most obvious formatting mistakes. 
#
# @qnstie, 2020


import os
import json
import re

directory = '.'
MIN_CONFIDENCE_BLOCK = 0.75

def main():
	combined_out = open("combined.txt", "w")
	file_count = 0
	for file_name in sorted(os.listdir(directory)):
		if file_name.endswith(".json"):
			with open(file_name) as f:
				data = json.load(f)
				f.close()
				txt = ocr_json_to_text(data)
				txt = correct_spaces(txt)
				print("\n\n\n**** PAGE %d (file %s) %s" % (file_count, file_name, txt))

				outf = open(file_name + ".txt", "w")
				outf.write(txt)
				outf.close

				if	file_count > 0:
					combined_out.write("\n\n\n");
				file_count += 1
				combined_out.write("**** PAGE %d (file %s)" % (file_count, file_name));
				combined_out.write(txt);
			continue
		else:
			continue
	combined_out.close()


def ocr_json_to_text(data):
	txt = ""

	for page in data["fullTextAnnotation"]["pages"]:
		for block in page["blocks"]:
			if block["blockType"] == "TEXT" and block["confidence"] > MIN_CONFIDENCE_BLOCK:
				txt = txt + "\n"
				for paragraph in block["paragraphs"]:
					txt = txt + "\n"
					word_count = 0
					for word in paragraph["words"]:
						w = ""
						if word_count > 0:
							txt += " "
						word_count += 1
						for symbol in word["symbols"]:
							w = w + symbol["text"]
						txt = txt + w

	return txt

pat1 = re.compile(r'\s([\.,:;]\s)')       # '  .  ' to '. '
pat2 = re.compile(r'\s(\')\s')            # 'a ' la' to 'a'la '
pat3 = re.compile(r'(\s\()\s')            # ' ( ' to ' ('
pat4 = re.compile(r'\s(\)\s)')            # ' ) ' to ') '
pat5 = re.compile(r'([,.;:])\s([,.;:])')  # '. :' to '.:'


def correct_spaces(txt):
	txt = pat1.sub('\\1', txt)
	txt = pat2.sub('\\1', txt)
	txt = pat3.sub('\\1', txt)
	txt = pat4.sub('\\1', txt)
	txt = pat5.sub('\\1\\2', txt)
	return txt


if __name__ == '__main__':
	main()