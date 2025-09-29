import requests

BASE_URL = "http://127.0.0.1:8000/auth/register"

def test_success():
    data = {"username": "alice", "email": "alice@example.com", "age": 25}
    r = requests.post(BASE_URL, json=data)
    print("✅ Success case:")
    print(r.status_code, r.json())

def test_underage():
    data = {"username": "bob", "email": "bob@example.com", "age": 15}
    r = requests.post(BASE_URL, json=data)
    print("\n❌ Underage case:")
    print(r.status_code, r.json())

def test_invalid_user():
    data = {"username": 1234567, "email": "bob@example.com", "age": 35}
    r = requests.post(BASE_URL, json=data)
    print("\n❌ Invalid user case:")
    print(r.status_code, r.json())

def test_invalid_email():
    data = {"username": "bob", "email": "bobexample.com", "age": 35}
    r = requests.post(BASE_URL, json=data)
    print("\n❌ Invalid email case:")
    print(r.status_code, r.json())

def test_admin():
    data = {"username": "admin", "email": "admin@example.com", "age": 30}
    r = requests.post(BASE_URL, json=data)
    print("\n❌ Forbidden username case:")
    print(r.status_code, r.json())

def test_invalid_json():
    data = {"nouser": "bob", "email": "bob@example.com", "age": 35}
    r = requests.post(BASE_URL, json=data)
    print("\n❌ Invalid json case:")
    print(r.status_code, r.json())

if __name__ == "__main__":
    test_success()
    test_underage()
    test_invalid_user()
    test_invalid_email()
    test_admin()
    test_invalid_json()
