import requests
from GET_roles import fetch_roles
strapi_url = "http://localhost:1337"  # Assuming Strapi is running locally

# Using a custom registration token (adjust as needed)
api_token = "d8b23eef836c266894acef8b1cd911e933191c28d29c01f0e7d63a369ac151dffe33471a3368baae56a2692638a0054d0cdd275a18c7e9a19c6208fb0dfcad5749407f2b8cbf6a4899385636cbaa358fa07740b678be66a1557914fc103ff0d8a820042b03e9c138d7d18cb4a814e53aa0a1c340a10c670550b6f8a9ec8e3b8b"    

roles = fetch_roles()
print(roles)


# New user details (example for Author)
user_data = {
    "username": "ThisIsTestMail",
    "email": "TestMail1234@example.com",
    "password": "Pass123"
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Step 1: Register the user
response = requests.post(f"{strapi_url}/api/auth/local/register", json=user_data, headers=headers)

if response.status_code == 200:
    print("User registered successfully:", response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
    
# Step 2: Assign role to the user
if response.status_code == 200:
    user_id = response.json()["user"]["id"]  # Extract user ID
    assign_role_url = f"{strapi_url}/users-permissions/users/{user_id}"

    # Data to update the user role (role 3 is for Author, change as needed)
    update_data = {
        "role": 3  # Role ID for Author
    }

    response_update = requests.put(assign_role_url, json=update_data, headers=headers)

    if response_update.status_code == 200:
        print("Role assigned successfully:", response_update.json())
    else:
        print(f"Error assigning role: {response_update.status_code} - {response_update.text}")
else:
    print(f"User registration failed: {response.status_code} - {response.text}")
