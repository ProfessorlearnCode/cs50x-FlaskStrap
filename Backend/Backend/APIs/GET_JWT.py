import requests


strapi_url = "http://localhost:1337"


# User login details
login_data = {
    "identifier": "JohnDoe",  # This can be username or email
    "password": "12341234"
}


# Login the user
login_response = requests.post(f"{strapi_url}/api/auth/local", json=login_data)

if login_response.status_code == 200:
    login_info = login_response.json()
    jwt = login_info['jwt']  # Extracting the JWT from the response
    print("User logged in successfully. JWT:", jwt)
else:
    print(f"Error: {login_response.status_code} - {login_response.text}")
