#
# Author Sharan Agrawal
#

import json
import sys


i = 0
reco = ""
rule_split = []
# commit = []

# commit = sys.argv

with open("COMMIT_SAMPLE.json") as f:
    data = json.load(f)

f.close()

# print(len(data[0]))

while(i < len(data[0])):

    file = data[0][i]['filename']
    # print(file)
    searchfile = open("rules.txt", "r")

    for line in searchfile:

        rule_split = line.split('==>', 1)
        # print(rule_split[0])
        # print(file)

        if (rule_split[0].find(file)) != -1:

            # print(rule_split[0])
            reco += line

    searchfile.close()
    i = i + 1
    # print(i)


print(reco)
