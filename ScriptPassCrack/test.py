import requests

x = requests.get('https://w3schools.com')
print(float(x.elapsed.total_seconds()))