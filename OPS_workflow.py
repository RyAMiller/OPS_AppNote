#!/usr/bin/env python3

import sys
import urllib.request
import urllib.parse
import json
import pprint
import requests
import csv
from urllib.parse import urlparse
from SPARQLWrapper import SPARQLWrapper, XML
import xml.dom.minidom 

def sparqlQ (concept):
	sparql = SPARQLWrapper("http://sparql.wikipathways.org/")
	sparql.setQuery("""
		PREFIX wp:      <http://vocabularies.wikipathways.org/wp#> 
		PREFIX wprdf:   <http://rdf.wikipathways.org/>
		PREFIX dc:      <http://purl.org/dc/elements/1.1/> 
		PREFIX dcterms: <http://purl.org/dc/terms/>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT distinct ?label
		WHERE { 
		  <""" + concept + """> rdfs:label ?label 
		}
	""")
	sparql.setReturnFormat(XML)
	results = sparql.query().convert()
	print(concept)

	litList = results.getElementsByTagName("literal")
	if (litList) :
		lit1 = litList[0]
		print (lit1.firstChild.wholeText)
		sparqlRes = lit1.firstChild.wholeText
		return sparqlRes
	else : 
		sparqlRes = 'NA'
		return sparqlRes
		 

OPS_api = 'df2facbe3d5cee743dc500a1589e53bf'
ops_ID = '0a081d11'
inputPWID = input('enter your pathway Id to get interactions: ')

apiID = '&app_id=' + ops_ID + '&app_key=' + OPS_api
apiFormat = '&_format=json'
f = open('getInteractionsOutput.csv', 'w')
pathwayId = 'WP' + inputPWID
queryType = 'pathway/getInteractions?uri=http%3A%2F%2Fidentifiers.org%2Fwikipathways%2F' + pathwayId
url = 'https://beta.openphacts.org/2.2/' + queryType + apiID + apiFormat

print (url + '\n')
f.write(url + '\n\n')

json_obj = requests.get(url)
json_obj.raise_for_status()
data = json_obj.json()

i = 0

if isinstance(data['result']['primaryTopic']['latest_version'], (list)):
	for value in data['result']['primaryTopic']['latest_version'][0]['hasPart']:
		i = i + 1
		interactCount = i
		jsonvalue = json.dumps(value)
		loadedValue = json.loads(jsonvalue)
		print ('interaction\t' + value['_about'])
		f.write('interaction\t' + value['_about'] + '\n')
		print ('int type\t' + value['type'])
		f.write('int type\t' + value['type'] + '\n')

		if isinstance(loadedValue['source'], (list)):
			for values in loadedValue['source']:
				url2bencoded = values['_about']
				sparqlRes = sparqlQ(url2bencoded)
				print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
				print ('source\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
				f.write('source\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
		else:
			url2bencoded = value['source']['_about']
			sparqlRes = sparqlQ(url2bencoded)
			print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
			print ('source\t' + value['source']['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
			f.write('source\t' + value['source']['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )

		if isinstance(loadedValue['target'], (list)):
			for values in loadedValue['target']:
				url2bencoded = values['_about']
				sparqlRes = sparqlQ(url2bencoded)
				print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
				print ('target\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n\n'  )
				f.write('target\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n\n' )
		else:
			url2bencoded = value['target']['_about']
			sparqlRes = sparqlQ(url2bencoded)
			print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
			print ('target\t' + value['target']['_about'] + '\taliasIDs\t' + sparqlRes + '\n\n' )
			f.write('target\t' + value['target']['_about'] + '\taliasIDs\t' + sparqlRes + '\n\n' )				

else:
	for value in data['result']['primaryTopic']['latest_version']['hasPart']:

		i = i + 1
		interactCount = i
		jsonvalue = json.dumps(value)
		loadedValue = json.loads(jsonvalue)
		print ('interaction\t' + value['_about'])
		f.write('interaction\t' + value['_about'] + '\n')
		print ('int type\t' + value['type'])
		f.write('int type\t' + value['type'] + '\n')

		print(loadedValue)
		try:
			if isinstance(loadedValue['source'], (list)):
				for values in loadedValue['source']:
					url2bencoded = values['_about']
					sparqlRes = sparqlQ(url2bencoded)
					print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
					print ('source\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
					f.write('source\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
		except KeyError:
			pass	
				
		else:
			url2bencoded = value['source']['_about']
			sparqlRes = sparqlQ(url2bencoded)
			print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
			print ('source\t' + value['source']['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
			f.write('source\t' + value['source']['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
		try:
			if isinstance(loadedValue['target'], (list)):
				for values in loadedValue['target']:
					url2bencoded = values['_about']
					sparqlRes = sparqlQ(url2bencoded)
					print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
					print ('target\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n' )
					f.write('target\t' + values['_about'] + '\taliasIDs\t' + sparqlRes + '\n\n' )
		except KeyError:
			pass	
					
		else:
			url2bencoded = value['target']['_about']

			sparqlRes = sparqlQ(url2bencoded)
			print (sparqlRes, "xxxxxxxxxxxxxxxxxxxxxxxx")
			print ('target\t' + value['target']['_about'] + '\taliasIDs\t' + sparqlRes + '\n\n' )
			f.write('target\t' + value['target']['_about'] + '\taliasIDs\t' + sparqlRes + '\n\n' )

print ('PW ID\t',inputPWID)
f.write('PW ID\t' + inputPWID + '\n')
print ('interactions for the pathway\t{}'.format(interactCount) + '\n')
f.write('interactions for the pathway\t{}'.format(interactCount))        
f.close()
