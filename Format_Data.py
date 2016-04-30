import json
import csv
import sys
from pprint import pprint

i = 0
j = 0
adj = []
flag = 1
file = []

file = sys.argv

with open(file[1]) as f:
	     data = json.load(f)
	     # commit[i] = data;
	     # i = i + 1
	     


while(i < len(data)):
	
	if(flag):
		adj.append([]) 	

	flag = 0

 	while(j < len(data[i])):
 		
 		if(data[i][j]["status"] != "deleted"):
 			
 			# print(str(i) + " " + str(j) + " " + str(k))
 			flag = 1
 			adj[i].append(data[i][j]["filename"])
 		
 		j = j + 1

 	i = i + 1
	j = 0

i = 0
j = 0

pprint(adj)


with open('abc.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    while(i < len(adj)):
    	wr.writerow(adj[i])
    	i = i + 1
 		
		 

# while(i < len(data)):
# 	while(j < len(data[i])):
# 		if(data[i][j]["status"] != "deleted"):
# 			adj[data[i][j]["filename"]] = {}
# 		else:
# 			adj[data[i][j]["filename"]] = 0
# 		j = j + 1

# 	i = i + 1

# i = 0
# j = 0

# while(i < len(data)):
# 	while(j < len(data[i])):
		
# 		if(adj[data[i][j]["filename"]] != 0):	
# 			adj[data[i][j]["filename"]][data[i][j]["sha"]] = 1
		
# 		j = j + 1

# 	i = i + 1

