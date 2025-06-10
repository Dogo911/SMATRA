import requests

payload = {
	"velocity":120,
	"speed": 99,
	"icon": "car",
}

response = requests.post("http://192.168.0.148:5050/update", json=payload)
print("Status: ", response.status_code)
print("Antwort: ", response.text)
