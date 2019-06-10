#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Converting English digits [1234567890] and also Arabic digits [٤٥٦] into their equivalents in Perisan encoding [۴۵۶].

import re,fileinput,sys,os,datetime
import xml.etree.ElementTree as ET
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/modules")
import persian
import pytz

debugging = True

os.system('cls')

def log(text):
	print(text)
	text = str(text)
	if debugging == True:
		now = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
		with open(os.path.dirname(os.path.realpath(__file__))+"/log.txt", 'ab') as file:
			text = now.strftime("%Y-%m-%d %H:%M:%S")+":   "+text+"\n"
			text = text.encode('utf8')
			file.write(text)

log("* Loading File")
tree = ET.parse('input.osm')		#Source input file name
root = tree.getroot()
log("* File loaded, Fixing.")

counter = 0
issuecounter = 0
ar_numbers = 0
en_numbers = 0
# if the name has one of the following accepted_chars (allowed chars) apply the fixes. doing so to avoid editing names which are not farsi.
accepted_chars = ['ا','آ','ب','پ','ت','ث','ج','چ','ح','خ','د','ذ','ر','ز','ژ','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ک','گ','ل','م','ن','و','ه','ی','1','2','3','4','5','6','7','8','9','۰','۱','۲','۳','۴','۵','۶','۷','۸','۹','٤','٥','٦']
# do not edit names which have one of this characters in them.
ignore_list = ['ك','ي','ى','أ','إ','ة','ؤ','ئ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
log("Working on Nodes:")
for node in root.findall('node'):
	for tag in node.findall('tag'):
		k = tag.attrib['k']
		if k=='name':
			name = tag.attrib['v']
			if any(char in name for char in ignore_list):
				log("    id:"+node.attrib['id']+"  name:'"+name+"' matched in ignore_list , it didn't get touched")
				continue
			if any(char in name for char in accepted_chars):
				temp = tag.attrib['v']
				v_fixed=persian.convert_ar_numbers(name)
				if temp != v_fixed:
					ar_numbers = ar_numbers+1
					issuecounter = issuecounter+1
					temp = v_fixed
				v_fixed=persian.convert_en_numbers(v_fixed)
				if temp != v_fixed:
					en_numbers = en_numbers+1
					issuecounter = issuecounter+1
					temp = v_fixed
				if v_fixed != name:
					counter=counter+1
					tag.attrib['v'] = v_fixed
					node.set('action', 'modify')
			else:
				log ("    Warning: id:"+node.attrib['id']+"  name:'"+name+"' did not matched in accepted_chars , it didn't get touched")
log (str(counter) + " node With "+str(issuecounter)+" Issue Fixed.  ("+str(ar_numbers)+" Arabic Numbers - "+str(en_numbers)+" English Numbers)")



counter = 0
issuecounter = 0
ar_numbers = 0
en_numbers = 0
log("Working on Ways:")
for way in root.findall('way'):
	for tag in way.findall('tag'):
		k = tag.attrib['k']
		if k=='name':
			name = tag.attrib['v']
			if any(char in name for char in ignore_list):
				log("    id:"+way.attrib['id']+"  name:'"+name+"' matched in ignore_list , it didn't get touched")
				continue
			if any(char in name for char in accepted_chars):
				temp = tag.attrib['v']
				v_fixed=persian.convert_ar_numbers(name)
				if temp != v_fixed:
					ar_numbers = ar_numbers+1
					issuecounter = issuecounter+1
					temp = v_fixed
				v_fixed=persian.convert_en_numbers(v_fixed)
				if temp != v_fixed:
					en_numbers = en_numbers+1
					issuecounter = issuecounter+1
					temp = v_fixed
				if v_fixed != name:
					counter=counter+1
					tag.attrib['v'] = v_fixed
					way.set('action', 'modify')
			else:
				log ("    Warning: id:"+way.attrib['id']+"  name:'"+name+"' did not matched in accepted_chars , it didn't get touched")
log (str(counter) + " way With "+str(issuecounter)+" Issue Fixed.  ("+str(ar_numbers)+" Arabic Numbers - "+str(en_numbers)+" English Numbers)")



# counter = 0
# issuecounter = 0
# ar_numbers = 0
# en_numbers = 0
# log("Working on Relations:")
# for relation in root.findall('relation'):
	# for tag in relation.findall('tag'):
		# k = tag.attrib['k']
		# if k=='name':
			# name = tag.attrib['v']
			# if any(char in name for char in ignore_list):
				# log("    id:"+node.attrib['id']+"  name:'"+name+"' matched in ignore_list , it didn't get touched")
				# continue
			# if any(char in name for char in accepted_chars):
				# temp = tag.attrib['v']
				# v_fixed=persian.convert_ar_numbers(name)
				# if temp != v_fixed:
					# ar_numbers = ar_numbers+1
					# issuecounter = issuecounter+1
					# temp = v_fixed
				# v_fixed=persian.convert_en_numbers(v_fixed)
				# if temp != v_fixed:
					# en_numbers = en_numbers+1
					# issuecounter = issuecounter+1
					# temp = v_fixed
				# if v_fixed != name:
					# counter=counter+1
					# tag.attrib['v'] = v_fixed
					# relation.set('action', 'modify')
			# else:
				# log ("    Warning: id:"+node.attrib['id']+"  name:'"+name+"' did not matched in accepted_chars , it didn't get touched")
# log (str(counter) + " Relation With "+str(issuecounter)+" Issue Fixed.  ("+str(ar_numbers)+" Arabic Numbers - "+str(en_numbers)+" English Numbers)")

log ("")
log ("* Writing to output file")
tree.write('output.osm',encoding="UTF-8")
log ("* Done.")


log("------------------------------------------------------------------------------------------")



#comment:
'''
[out:xml][timeout:180];
{{geocodeArea:iran}}->.searchArea;
(
  node["name"!~"[a-z]+"]["name"!~"[A-Z]+"]["name"~"[0-9]|٦|٥|٤|ي|ك"](area.searchArea);
  way["name"!~"[a-z]+"]["name"!~"[A-Z]+"]["name"~"[0-9]|٦|٥|٤|ي|ك"](area.searchArea);
 );
(._;>;);
out meta;
'''

