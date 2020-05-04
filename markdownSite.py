#!/usr/bin/python3

# This script builds a html document from a html template and markdown files with json metadata.
# Call the script with -h to see help/documentation.

import re
import os
import sys
import json
import markdown
import optparse


def openFile(file):
	with open(file, 'r') as openedFile:
		return openedFile.read()

def writeFile(file, content):
	try:
		with open(file, 'w') as writeFile: # write the file.
			writeFile.write(content) # write content to file.
	except FileNotFoundError:
		os.makedirs(os.path.dirname(file)) # make all the missing directories.
		with open(file, 'w') as writeFile: # write the file.
			writeFile.write(content) # write content to file.
	except:
		print('An unexpected error occurred while trying to write a file. Exiting...')
		sys.exit(-1)

def formatStyles(stylesheets, backRef):
	output = ''
	# Generate Styles
	for stylesheet in stylesheets:
		output += '<link rel="stylesheet" type="text/css" href="{}styles/{}">\n'.format(backRef, stylesheet)
	return output

def formatScripts(scripts, backRef):
	output = ''
	# Generate Scripts
	for script in scripts:
		output += '<script type="text/javascript" src="{}scripts/{}"></script>\n'.format(backRef, script)
	return output

def formatNavigation(siteMap):
	output = ''
	template = '<li><a href="{}">{}</a></li>\n'
	for links in siteMap:
		for link in siteMap[links]:
			#print(links+'/'+link)
			f, ext = os.path.splitext(link)
			if f == 'index' and links == '':
				output += template.format('/'+os.path.join(links,link.replace('.md','.html')), 'Home')
			elif f == 'index':
				head, tail = os.path.split(os.path.join(links,link))
				#print('here', f, head.split('/')[-1])
				output += template.format('/'+os.path.join(head,tail.replace('.md','.html')), head.split('/')[-1].title() )
			else:
				output += template.format('/'+os.path.join(links,link.replace('.md','.html')), f.title() )
	return output

def parseMd2Html(md):
	# parse the markdown into html
	return markdown.markdown(md, extensions=['codehilite','meta'])

def generateHtmlDoc(template, title, backRef, styles, scripts, navigation, pageContent):
	# print out the template with placeholders replaced.
	return template.format(
		title=title,
		backRef=backRef,
		styles=styles,
		scripts=scripts,
		navigation=navigation,
		pageContent=pageContent
	)

def writeHtmlDoc(template, options, navigation, file, backRef):
	# Generate the page specified.
	md = openFile(os.path.join(options.root_dir, options.input_dir, file))
	meta = json.loads(openFile(os.path.join(options.root_dir, options.input_dir, file.replace('.md','.json'))))
	writeFile(
		  os.path.join(options.root_dir, options.output_dir, file.replace('.md','.html'))
		, generateHtmlDoc(template
			, meta["title"]+options.suffix
			, backRef
			, formatStyles(meta["styles"], backRef)
			, formatScripts(meta["scripts"], backRef)
			, navigation
			, parseMd2Html(md)
		)
	)

def main():
	# handle command line options and args
	version = "%prog 1.0"
	usage = "usage: %prog site_root_dir"
	description = "Generates html pages from markdown files."
	parser = optparse.OptionParser(version=version, usage=usage, description=description)
	parser.add_option("-v", "--verbose", action="store_false", dest="verbose", default=False, help="When enabled the html will also be output to stdout. (Default: False)")
	parser.add_option("-t", "--template", dest="template", default="master_template.html", help="Specify the master page template that each html page will be built off of. (Default: master_template.html)")
	parser.add_option("-r", "--root_dir", dest="root_dir", default="./", help="Specify the root directory of the site files. (Default: ./)")
	parser.add_option("-i", "--input_dir", dest="input_dir", default="docs_md/", help="Specify the directory of markdown files. (Default: docs_md)")
	parser.add_option("-o", "--output_dir", dest="output_dir", default="docs/", help="Specify the output directory for the html files. (Default: docs)")
	parser.add_option("-s", "--single_file", dest="single_file", default="", help="Just generate a single file from the --input_dir. May be removed in the future.")
	parser.add_option("-S", "--site_suffix", dest="suffix", default=" | Hexpowered", help="Set a default site suffix in the title of every page. (Default: ' | Hexpowered')")
	parser.add_option("-P", "--site_prefix", dest="prefix", default="", help="Set a default site prefix in the title of every page. (Default: none not fully implemented.)")
	(options, args) = parser.parse_args()

	# Load html document template.
	template = openFile(os.path.join(options.root_dir,options.template))


	# Generating a single page isn't really supported at this point since
	# adding the navigation part of the page requires traversing the whole site.
	# I would need to cache the site structure between runs to allow for
	# small changes to just one page while keeping the navigation updated.
	if options.single_file != '': # If only running a single file. Then Generate a single file.
		writeHtmlDoc(template, options, options.single_file)
	else: # Otherwise, walk through the input directory and build the site page by page.
		# Build site map for navigation.
		siteMap = {}

		# walk through input dir and build the site map.
		for root, dirs, files in os.walk(os.path.join(options.root_dir,options.input_dir)):
			for file in files:
				f, ext = os.path.splitext(file) # Get extension of the file.
				if ext == '.md': # If the file is a markdown file (.md) add it to the list.
					thisRoot = re.sub(os.path.join(options.root_dir,options.input_dir), '', os.path.join(root))
					thisPage = re.sub(os.path.join(options.root_dir,options.input_dir), '', os.path.join(root,file))

					# Make sure key exists in sitemap.
					# Either way add it to the sitemap.
					try:
						# Add page to sitemap.
						siteMap[thisRoot].append(file)
					except KeyError:
						siteMap[thisRoot] = [file]

		# Generate Site Navigation
		navigation = formatNavigation(siteMap)

		# Generate each page.
		for folder in siteMap:
			for page in siteMap[folder]:
				backRef = '../' * os.path.join(folder,page).count(os.sep)
				print('Generating html for:', os.path.join(folder,page)) # Log the file we're generating.
				writeHtmlDoc(template, options, navigation, os.path.join(folder,page), backRef)

main() # Start script.
