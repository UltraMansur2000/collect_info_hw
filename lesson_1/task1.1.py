import requests
from pprint import pprint
username = 'UltraMansur2000'
url = f'https://api.github.com/users/{username}/repos'
data = requests.get(url)
with open('repos.json', 'wb') as f:
    f.writelines(data)
    print('Repos loaded successfully')
pprint(data.json())
