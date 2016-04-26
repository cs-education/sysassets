from bs4 import BeautifulSoup
import urllib.request as url
import json

output_name = "headers.json"
man = "http://cs-education.github.io/sysassets/man_pages/html/"

request = url.Request(man, headers={'User-Agent': 'Magic Browser'})
response = url.urlopen(request)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

data = {}
syscall_paths = []
library_paths = []
for item in soup.findAll('li'):
	children = item.findChildren()
	for child in children:
		page = child.attrs['href'][:4]
		if page == 'man2' or page == 'man3':
			raw_call = child.attrs['href'][5:-7]
			data[raw_call] = []
			path = child.attrs['href'][5:]
			if page == 'man2':
				syscall_paths.append((path, raw_call))
			else:
				library_paths.append((path, raw_call))
		else:
			break

for path, raw_call in syscall_paths:
	link = man + "man2/" + path
	request = url.Request(link, headers={'User-Agent': 'Magic Browser'})
	try:
		response = url.urlopen(request)
	except:
		continue
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	tokens = soup.get_text().split('\n')
	for token in tokens:
		if token:
			subtokens = token.split()
			if len(subtokens) > 0:
				if subtokens[0] == '#define' or subtokens[0] == '#include':
					header = ' '.join(subtokens)
					if header not in data[raw_call]:
						if subtokens[0] == '#define':
							data[raw_call].insert(0, header)
						else:
							data[raw_call].append(header)

for path, raw_call in library_paths:
	link = man + "man3/" + path
	request = url.Request(link, headers={'User-Agent': 'Magic Browser'})
	try:
		response = url.urlopen(request)
	except:
		continue
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	tokens = soup.get_text().split('\n')
	for token in tokens:
		if token:
			subtokens = token.split()
			if len(subtokens) > 0:
				if subtokens[0] == 'DESCRIPTION':
					break
				if subtokens[0] == '#define' or subtokens[0] == '#include':
					header = ' '.join(subtokens)
					if header not in data[raw_call]:
						if subtokens[0] == '#define':
							data[raw_call].insert(0, header)
						else:
							data[raw_call].append(header)

with open(output_name, "w+") as output:
	output.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))