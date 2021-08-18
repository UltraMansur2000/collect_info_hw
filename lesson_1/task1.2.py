# 56829ce125285ef58295fb0fa05d98b952bf7d4b3cabb751e8bbc848f3eec65dff414d960fc20a17d9558
# 491651788
import requests

groups = []
params = {'user_id': '491651788',
          'v': '5.131',
          'access_token': '56829ce125285ef58295fb0fa05d98b952bf7d4b3cabb751e8bbc848f3eec65dff414d960fc20a17d9558',
          'extended': '1'}
url = 'https://api.vk.com/method/groups.get'
data = requests.get(url, params=params).json()
for i in data.get('response').get('items'):
    groups.append(f'{i.get("name")}\n')
with open('groups.txt', 'w', encoding='utf-8') as f:
    f.writelines(groups)
