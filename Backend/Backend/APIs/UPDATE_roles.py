import requests
from GET_roles import fetch_roles
strapi_url = "http://localhost:1337"  # Assuming Strapi is running locally

# Using a custom registration token (adjust as needed)
api_token = "d8b23eef836c266894acef8b1cd911e933191c28d29c01f0e7d63a369ac151dffe33471a3368baae56a2692638a0054d0cdd275a18c7e9a19c6208fb0dfcad5749407f2b8cbf6a4899385636cbaa358fa07740b678be66a1557914fc103ff0d8a820042b03e9c138d7d18cb4a814e53aa0a1c340a10c670550b6f8a9ec8e3b8b"    

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# response = requests.get(f"{strapi_url}/api/users", headers=headers)
response = requests.get(f"{strapi_url}/api/users?filters[username][$eq]=newauthor", headers=headers)

print(response.json())



roles = fetch_roles()
print(roles)
