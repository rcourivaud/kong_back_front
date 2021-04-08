import requests
import os

# from dotenv import load_dotenv
# load_dotenv("../../.env")

KONG_HOST_IP = os.environ.get("KONG_HOST_IP")
KONG_PORT = os.environ.get("KONG_PORT")
KEYCLOAK_HOST_IP = os.environ.get("KEYCLOAK_HOST_IP")
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT")
IS_PROD = os.environ.get("PROD") == "true"

BACKEND_URI = os.environ.get("BACKEND_URI")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REALM_NAME = "enki"

print(CLIENT_SECRET)

ENKI_API_SERVICE_ID = os.environ.get("ENKI_API_SERVICE_ID")

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
    'paths[]': '/enki',
}

_ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/{ENKI_API_SERVICE_ID}/routes', data=data)

# # Configure OIDC Plugin

introspection_url = f"https://{KEYCLOAK_HOST_IP}/auth/realms/{REALM_NAME}/protocol/openid-connect/token/introspect" \
    if IS_PROD else f'http://{KEYCLOAK_HOST_IP}:{KEYCLOAK_PORT}/auth/realms/{REALM_NAME}/protocol/openid-connect/token/introspect'
discovery_url = f"https://{KEYCLOAK_HOST_IP}/auth/realms/{REALM_NAME}/.well-known/openid-configuration"\
    if IS_PROD else f'http://{KEYCLOAK_HOST_IP}:{KEYCLOAK_PORT}/auth/realms/{REALM_NAME}/.well-known/openid-configuration'

print(introspection_url)
print(discovery_url)
data = {
    'name': 'oidc',
    'config.client_id': f'{CLIENT_ID}',
    'config.client_secret': f'{CLIENT_SECRET}',
    'config.realm': f'{REALM_NAME}',
    'config.bearer_only': 'true',
    'config.introspection_endpoint':introspection_url,
    'config.discovery':discovery_url
}

_ = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/{created_service_id}/plugins', data=data)
