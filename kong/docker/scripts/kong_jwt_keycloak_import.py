import requests
import os
# from dotenv import load_dotenv
# load_dotenv("../../.env")

KONG_HOST_IP = os.environ.get("KONG_HOST_IP")
KONG_PORT = os.environ.get("KONG_PORT")
KEYCLOAK_HOST_IP = os.environ.get("KEYCLOAK_HOST_IP")
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT")

BACKEND_URI = os.environ.get("BACKEND_URI")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

ENKI_API_SERVICE_ID = os.environ.get("ENKI_API_SERVICE_ID_JWT")

# Add Service for enki URL
data = {
    'name': ENKI_API_SERVICE_ID,
    'url': f'{BACKEND_URI}'
}
print(f'http://{KONG_HOST_IP}:{KONG_PORT}/services')
print(data)

response = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services', data=data)

print(response.json())

created_service_id = response.json()["id"]

# # Add routes path


data = {
    'service.id': f'{created_service_id}',
    'paths[]': '/enki-jwt',
}

_ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/{ENKI_API_SERVICE_ID}/routes', data=data)

# # Configure Jwt Kong Keycloak

data = {
  'name': 'jwt-keycloak',
  'config.allowed_iss': 'http://keycloak:8080/auth/realms/enki'
}

_ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/{created_service_id}/plugins', data=data)
