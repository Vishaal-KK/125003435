import requests

'''
url = "http://20.244.56.144/test/register"
data = {
    "companyName": "gomart",
    "ownerName": "Vishal.KK",
    "rollNo": "125003435",
    "ownerEmail": "125003435@sastra.edu.in",
    "accessCode": "LGcHvG"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
'''

url = "http://20.244.56.144/test/auth"
data = {
    'companyName': 'gomart',
    'clientID': '036a8f48-69c3-4e2e-b537-ed4ba2d8003f',
    'clientSecret': 'RibsRSfQZyLVFPcN', 
    'ownerName': 'Vishal.KK', 
    'ownerEmail': '125003435@sastra.edu.in',
    'rollNo': '125003435'
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
