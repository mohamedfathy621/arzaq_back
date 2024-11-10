import requests

url = 'http://127.0.0.1:8000/Rest/data/insert'  # Replace with your target URL
response = requests.post(url)

if response.status_code == 200:
    print("Success:", response.json())  # or response.text for non-JSON responses
else:
    print("Failed to retrieve data. Status code:", response.status_code)
