import json
from jsondiff import diff
data = open(r'jsonowy.json')

data = json.load(data)


set1 = data["artists"]
print(set1)

# set1 = data
#
set2 = [{'artist_name': 'CHOPPA TEE', 'artist_id': '12iGnI7m6kxA8LpEQ1xdiJ', 'artist_index': 91}, {'artist_name': 'Ash Bash Tha Rapper', 'artist_id': '4GHSsO2bndtYIfy8js9hUN', 'artist_index': 370}]
#
print(set2)

difference = diff(set1, set2)
if difference:
    print('Roznica')
else:
    print('Brak roznic')