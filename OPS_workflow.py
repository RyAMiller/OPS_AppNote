#!/usr/bin/env python3

import sys
import urllib.request
import urllib.parse
#from urllib2 import urlopen
import json
import pprint
import requests
import csv
#import urllib2

#https://beta.openphacts.org/2.1/pathway/getInteractions?uri=http%3A%2F%2Fidentifiers.org%2Fwikipathways%2FWP1015&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf&_format=json
OPS_api = 'df2facbe3d5cee743dc500a1589e53bf'
ops_ID = '0a081d11'
inputPWID = input('enter your pathway Id to get interactions: ')

#OPS_api = 'df2facbe3d5cee743dc500a1589e53bf'
#ops_ID = '0a081d11'

apiID = '&app_id=' + ops_ID + '&app_key=' + OPS_api
apiFormat = '&_format=json'
f = open('getInteractionsF.txt', 'w')
f = open('getInteractionsF.csv', 'w')
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
				encodedUrl = urllib.parse.quote_plus(url2bencoded)
				url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"

				json_obj1 = requests.get(url1)
				if json_obj1.status_code != 200:
					continue
				json_obj1.raise_for_status()
				data1 = json_obj1.json()
				for targValues in data1['result']['items']['hasPart']:
					if targValues['_about'] == url2bencoded:
						print ('source\t' + values['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] )
						f.write('source\t' + values['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] + '\n')
					else: 
						print ('source\t' + values['_about'])
						f.write('source\t' + values['_about'] + '\n')


		else:
			url2bencoded = value['source']['_about']
			encodedUrl = urllib.parse.quote_plus(url2bencoded)
			url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"

			json_obj1 = requests.get(url1)
			if json_obj1.status_code != 200:
				continue
			json_obj1.raise_for_status()
			data1 = json_obj1.json()
			#for aliasList in data1['result']['primaryTopic']['exactMatch']:
			z = 0

			for targValues in data1['result']['items'][z]['hasPart']:
				j = 0
				if isinstance(data1['result']['items'][z]['hasPart'], (list)):
					if data1['result']['items'][z]['hasPart'][j]['_about'] == url2bencoded:
						
						for targIDs in data1['result']['items'][z]['hasPart'][j]:
							print ('source\t' + value['source']['_about'] + '\taliasIDs\t' + data1['result']['items'][z]['hasPart'][j-1]['exactMatch']['prefLabel_en'] )
							f.write('source\t' + value['source']['_about'] + '\taliasIDs\t' + data1['result']['items'][z]['hasPart'][j-1]['exactMatch']['prefLabel_en'] + '\n')
							j = j + 1
				else:

					print ('source\t' + value['source']['_about']  )
					f.write('source\t' + value['source']['_about']  + '\n')
				z = z + 1


		if isinstance(loadedValue['target'], (list)):
			for values in loadedValue['target']:
				url2bencoded = values['_about']
				encodedUrl = urllib.parse.quote_plus(url2bencoded)
				url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"

				json_obj1 = requests.get(url1)
				if json_obj1.status_code != 200:
					continue
				json_obj1.raise_for_status()
				data1 = json_obj1.json()
				#for aliasList in data1['result']['primaryTopic']['exactMatch']:
				for targValues in data1['result']['items']['hasPart'][0]:
					if targValues['_about'] == url2bencoded:
						print ('target\t' + values['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] )
						f.write('target\t' + values['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] + '\n')
					else: 
						print ('target\t' + values['_about'])
						f.write('target\t' + values['_about'] + '\n')

		else:
			url2bencoded = value['target']['_about']
			encodedUrl = urllib.parse.quote_plus(url2bencoded)
			url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"

			json_obj1 = requests.get(url1)
			if json_obj1.status_code != 200:
				continue
			json_obj1.raise_for_status()
			data1 = json_obj1.json()
			z = 0

			for targValues in data1['result']['items'][z]['hasPart']:
				if isinstance(data1['result']['items'][z]['hasPart'], (list)):
					j = 0
					if data1['result']['items'][z]['hasPart'][j]['_about'] == url2bencoded:
						
						for targIDs in data1['result']['items'][z]['hasPart'][j]:
							print ('target\t' + value['target']['_about'] + '\taliasIDs\t' + data1['result']['items'][z]['hasPart'][j-1]['exactMatch']['prefLabel_en'] )
							f.write('target\t' + value['target']['_about'] + '\taliasIDs\t' + data1['result']['items'][z]['hasPart'][j-1]['exactMatch']['prefLabel_en'] + '\n')
							j = j + 1
					else: 
						print ('target\t' + value['target']['_about'])
						f.write('target\t' + value['target']['_about'] + '\n')
						j = j + 1
				else:
					if data1['result']['items'][z]['hasPart']['_about'] == url2bencoded:
						
						for targIDs in ['result']['items'][z]['hasPart']:
							print ('target\t' + value['target']['_about'] + '\taliasIDs\t' + data1['result']['items'][z]['hasPart']['exactMatch']['prefLabel_en'] )
							f.write('target\t' + value['target']['_about'] + '\taliasIDs\t' + data1['result']['items'][z]['hasPart']['exactMatch']['prefLabel_en'] + '\n')
					else: 
						print ('target\t' + value['target']['_about'])
						f.write('target\t' + value['target']['_about'] + '\n')
				z = z + 1
				

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

		if isinstance(loadedValue['source'], (list)):
			for values in loadedValue['source']:
				url2bencoded = values['_about']
				encodedUrl = urllib.parse.quote_plus(url2bencoded)
				url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"

				json_obj1 = requests.get(url1)
				if json_obj1.status_code != 200:
					continue
				json_obj1.raise_for_status()
				data1 = json_obj.json()
				for targValues in data1['result']['items']['hasPart']:
					if targValues['_about'] == url2bencoded:
						print ('source\t' + values['_about'] +'\taliasIDs\t' + data1['result']['primaryTopic']['exactMatch'])
						f.write('source\t' + values['_about'] + '\taliasIDs\t' + data1['result']['primaryTopic']['exactMatch'] + '\n')
					else:
						print ('source\t' + values['_about'] )
						f.write('source\t' + values['_about'] + '\n')

				
		else:
			url2bencoded = value['source']['_about']
			encodedUrl = urllib.parse.quote_plus(url2bencoded)
			url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"

			json_obj1 = requests.get(url1)
			if json_obj1.status_code != 200:
				continue
			json_obj1.raise_for_status()
			data1 = json_obj1.json()
			#for aliasList in data1['result']['primaryTopic']['exactMatch']:
			for targValues in data1['result']['items']['hasPart']:
				if targValues['_about'] == url2bencoded:
					print ('source\t' + value['source']['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] )
					f.write('source\t' + value['source']['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] + '\n')
				else: 
					print ('source\t' + value['source']['_about'])
					f.write('source\t' + value['source']['_about'] + '\n')


		if isinstance(loadedValue['target'], (list)):
			for values in loadedValue['target']:
				url2bencoded = values['_about']
				encodedUrl = urllib.parse.quote_plus(url2bencoded)
				url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"

				json_obj1 = requests.get(url1)
				if json_obj1.status_code != 200:
					continue
				json_obj1.raise_for_status()
				data1 = json_obj1.json()

				for targValues in data1['result']['items']['hasPart']:
					if targValues['_about'] == url2bencoded:
						print ('target\t' + values['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] )
						f.write('target\t' + values['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] + '\n')
					else: 
						print ('target\t' + values['_about'])
						f.write('target\t' + values['_about'] + '\n')


		else:
			url2bencoded = value['target']['_about']
			encodedUrl = urllib.parse.quote_plus(url2bencoded)
			url1 = "https://beta.openphacts.org/2.2/pathways/byTarget?uri="+ encodedUrl +"&app_id=0a081d11&app_key=df2facbe3d5cee743dc500a1589e53bf"
			
			json_obj1 = requests.get(url1)
			if json_obj1.status_code != 200:
				continue
			json_obj1.raise_for_status()
			data1 = json_obj1.json()
			
			for targValues in data1['result']['items']['hasPart']:
				if targValues['_about'] == url2bencoded:
					print ('target\t' + value['target']['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] )
					f.write('target\t' + valus['target']['_about'] + '\taliasIDs\t' + data1['result']['items']['hasPart']['exactMatch']['prefLabel_en'] + '\n')
				else: 
					print ('target\t' + value['target']['_about'])
					f.write('target\t' + value['target']['_about'] + '\n')




print ('PW ID\t',inputPWID)
f.write('PW ID\t' + inputPWID + '\n')
print ('interactions for the pathway\t{}'.format(interactCount) + '\n')
f.write('interactions for the pathway\t{}'.format(interactCount))        
f.close()
