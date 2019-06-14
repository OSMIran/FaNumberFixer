#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Converting English digits [1234567890] and also Arabic digits [٤٥٦] into their equivalents in Perisan encoding [۴۵۶].

import re,fileinput,sys,os,datetime
import xml.etree.ElementTree as ET
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/modules")
import persian
import pytz


os.system('cls')

logfile = open(os.path.dirname(os.path.realpath(__file__))+"/log.txt", 'ab')
now = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
currentdatetime = now.strftime("%Y-%m-%d_%H-%M-%S")
logchangesfile = open(os.path.dirname(os.path.realpath(__file__))+"/logs/Changes_"+currentdatetime+".html", 'wb')
logchangesfile.write(b"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<title>OSM FaNumberFixer Changes Result</title>
<meta charset="utf-8">
<style>
#changestbl{font-family:"Trebuchet MS",Arial,Helvetica,sans-serif;border-collapse:collapse;width:100%}#changestbl td,#changestbl th{border:1px solid #ddd;padding:8px}#changestbl tr:nth-child(even){background-color:#f2f2f2}#changestbl tr:hover{background-color:#ddd}#changestbl th{padding-top:12px;padding-bottom:12px;text-align:center;background-color:#4caf50;color:#fff}#changestbl td{text-align:center}
</style>
<script>function closeOnLoad(n){var o=window.open(n,"connectWindow","width=600,height=400,scrollbars=yes");return setTimeout(function(){o.close()},1e3),!1}</script>
</head>
<body>
<div align="center" dir="auto" style="white-space:pre;line-height: 11pt;"><h3>{{info}}</h3></div>
<table id="changestbl">
<tr><th>#</th><th>ID</th><th>Old Name</th><th>New Name</th><th>Open In Editor</th></tr>
""")

def log(text):
	print(text)
	text = str(text)
	text = now.strftime("%Y-%m-%d %H:%M:%S")+":   "+text+"\n"
	text = text.encode('utf8')
	logfile.write(text)

def logchanges(n,id,oldname,newname):
	n=str(n)
	josm=id.replace("node/","n").replace("way/","w").replace("relation/","r").encode('utf-8')
	iD=id.replace("node/","node=").replace("way/","way=").replace("relation/","relation=").encode('utf-8')
	logchangesfile.write(b"""<tr><td>%s</td><td><a href='https://www.openstreetmap.org/%s/history'>%s</a></td><td>%s</td><td>%s</td><td><a href='https://openstreetmap.org/edit?editor=id&zoom=17&%s' target='_blank'>iD</a> | <a href='#%s' onclick='javascript:closeOnLoad("http://127.0.0.1:8111/load_object?new_layer=true&objects=%s");'>JOSM</a></td></tr> """% (n.encode('utf-8'),id.encode('utf-8'),id.encode('utf-8'),oldname.encode('utf-8'),newname.encode('utf-8'),iD,josm,josm)+b"\n")
		
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
					logchanges(counter,"node/"+node.attrib['id'],name,v_fixed)
			else:
				log ("    Warning: id:"+node.attrib['id']+"  name:'"+name+"' did not matched in accepted_chars , it didn't get touched")
info = str(counter) + " node With "+str(issuecounter)+" Issue Fixed.  ("+str(ar_numbers)+" Arabic Numbers - "+str(en_numbers)+" English Numbers)"


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
					logchanges(counter,"way/"+way.attrib['id'],name,v_fixed)
			else:
				log ("    Warning: id:"+way.attrib['id']+"  name:'"+name+"' did not matched in accepted_chars , it didn't get touched")
info = info + "\n" + str(counter) + " way With "+str(issuecounter)+" Issue Fixed.  ("+str(ar_numbers)+" Arabic Numbers - "+str(en_numbers)+" English Numbers)"


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
				# log("    id:"+relation.attrib['id']+"  name:'"+name+"' matched in ignore_list , it didn't get touched")
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
					# logchanges(counter,"relation/"+relation.attrib['id'],name,v_fixed)
			# else:
				# log ("    Warning: id:"+relation.attrib['id']+"  name:'"+name+"' did not matched in accepted_chars , it didn't get touched")
# info = info + "\n" + str(counter) + " Relation With "+str(issuecounter)+" Issue Fixed.  ("+str(ar_numbers)+" Arabic Numbers - "+str(en_numbers)+" English Numbers)"

log (info)
log ("")
log ("* Writing to output file")
tree.write('output.osm',encoding="UTF-8")
log("------------------------------------------------------------------------------------------")
log ("* Closing files")
logfile.close
logchangesfile.write(b"""</table></body>
</html>""")
logchangesfile.close
info = info + "\n Changeset: 		| Date: "+now.strftime("%Y/%m/%d %H:%M:%S")+" IRST"
info = info.replace("\n","\n<br>")
with open(os.path.dirname(os.path.realpath(__file__))+"/logs/Changes_"+currentdatetime+".html", "rb") as logchangesfile:
	newText=logchangesfile.read().replace(b'{{info}}', info.encode('utf8'))
 
with open(os.path.dirname(os.path.realpath(__file__))+"/logs/Changes_"+currentdatetime+".html", "wb") as logchangesfile:
	logchangesfile.write(newText)
log ("* Done.")

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

