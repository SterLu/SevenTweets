import requests

res = requests.get("http://localhost:5000/tweets/")
print("/tweets/")
print(res.status_code)
print(res.text)
print()

res = requests.post("http://localhost:5000/tweets/", json={"tweet": "New tweet text"})
print("/tweets/ (POST)")
print(res.status_code)
print(res.text)
print()


res = requests.post("http://localhost:5000/tweets/", json={"tweet": "Another new tweet text"})
print("/tweets/ (POST)")
print(res.status_code)
print(res.text)
print()


res = requests.post("http://localhost:5000/tweets/", json={"tweet": "One more new tweet text"})
print("/tweets/ (POST)")
print(res.status_code)
print(res.text)
print()


res = requests.get("http://localhost:5000/tweets/")
print("/tweets/")
print(res.status_code)
print(res.text)
print()


res = requests.delete("http://localhost:5000/tweets/", json={"id": "2"})
print("/tweets/ (DELETE id=2)")
print(res.status_code)
print(res.text)
print()


res = requests.get("http://localhost:5000/tweets/")
print("/tweets/")
print(res.status_code)
print(res.text)
print()


res = requests.delete("http://localhost:5000/tweets/", json={"id": "52"})
print("/tweets/ (DELETE id=52)")
print(res.status_code)
print(res.text)
print()

