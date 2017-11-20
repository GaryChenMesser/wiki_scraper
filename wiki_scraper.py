from urllib.request import urlopen
import re
import argparse
import os
import networkx as nx
from bs4 import BeautifulSoup

def wiki_scraping(start):
	ref = []
	html = urlopen("https://en.wikipedia.org/wiki/" + start)
	bsObj = BeautifulSoup(html)

	for link in bsObj.find("div", {"id": "bodyContent"}).findAll("a", href = re.compile("^(/wiki/)((?!:).)*$")):
		if 'href' in link.attrs:
			ref.append(link.attrs['href'])

	# turn '/wiki/xxx_xxx' into 'xxx_xxx' 
	for a in range(len(ref)):
		ref[a] = ref[a].split('/')[2]
	f = get_person(ref)
	return f

def get_person(ref):
	# remove the ref which is a single word or not begin with upper character
	for a in range(len(ref)):
		if a >= len(ref):
			break
		spl = ref[a].split('_')
		if len(spl) == 1:
			del ref[a]
			continue
		for b in range(len(spl)):
			if spl[b][0].islower():
				del ref[a]
				break
	# scrape in wiki to find "Personal details"
	person = []
	for a in range(len(ref)):
		if a >= 12:
			break
		#print(ref[a])
		#print(a)
		html = urlopen("https://en.wikipedia.org/wiki/" + ref[a])
		bsObj = BeautifulSoup(html)
		for link1 in bsObj.findAll("th", {"scope" : "row"}):
			if link1.string == 'Born':
				person.append(ref[a])
				break
	return person
	
def to_gdf(start, D, gdf_path):
	gdf_node = "nodedef->name VARCHAR,label VARCHAR"
	gdf_edge = "\nedgedef->node1 VARCHAR,node2 VARCHAR,weight DOUBLE"
	for n in D.nodes():
		if n == start:
			gdf_node = gdf_node + "\n{node},center".format(node = n)
		else:
			gdf_node = gdf_node + "\n{node},friend".format(node = n)
	print(D.nodes())
	print(gdf_node)
	for e in D.edges():
		gdf_edge = gdf_edge + "\n{node1},{node2},1.".format(node1 = e[0], node2 = e[1])

	with open(gdf_path, 'w') as gdf:
		gdf.write(gdf_node + gdf_edge)
	print('writing successfully!')
		
	
	
def main():
	parser = argparse.ArgumentParser(prog='wiki_scraper.py')
	parser.add_argument('--person', type=str, required = True)
	parser.add_argument('--steps', type=int, required = True)
	args = parser.parse_args()
	gdf_name = "{p}-{s}.gdf".format(p = args.person, s = str(args.steps))
	print(gdf_name)
	gdf_dir = 'output'
	if not os.path.exists(gdf_dir):
		os.makedirs(gdf_dir)
	gdf_path = os.path.join(gdf_dir, gdf_name)
	print(gdf_path)

	person = [args.person]
	D = nx.DiGraph()

	for step in range(args.steps):
		print('step = ', step)
		print('number of person is ', len(person))
		friend = []
		for start in person:
			print('start = ', start)
			f = wiki_scraping(start)
			print('f = ', f)
			D.add_edges_from([(start, i) for i in f])
			friend.extend(f)
		person = friend

	to_gdf(args.person, D, gdf_path)
	
	
if __name__ == '__main__':
	main()
