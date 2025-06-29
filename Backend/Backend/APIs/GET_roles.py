import requests


def fetch_roles():
    strapi_url = "http://localhost:1337"  # Assuming Strapi is running locally

    # Using Inspection API Token
    api_token = "8ca884275ad2f44df10430214d90977e28948bdbae26bc9d70ffb42b6a46f01af96db3321141b40a1edc8bd0233f298fb4424df7fde982f28f256b0fcccdc7b1366f8e12222774054516d3086d41425235bb7447e5a4ef3d1050caa4e3b9d7f3a8dff7a9eaaa70da336bd651fac7d37f3c24942b83614c7c580dd977dc82d29f" 

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(f"{strapi_url}/api/users-permissions/roles", headers=headers)

    if response.status_code == 200:
        print("Roles fetched successfully")
    else:
        print(f"Error: {response.status_code} - {response.text}")


    JSON = response.json()

    roles_dictionary = {}

    # Displaying the roles
    for role in JSON["roles"]:
        roles_dictionary.update({role['id']: role['name']})

    return roles_dictionary    
    
    