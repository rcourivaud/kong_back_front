import requests
import os

KONG_HOST_IP = os.environ.get("KONG_HOST_IP")
KONG_PORT = os.environ.get("KONG_PORT")
KEYCLOAK_HOST_IP = os.environ.get("KEYCLOAK_HOST_IP")
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT")

LOGSTASH_HOST = os.environ.get("LOGSTASH_HOST")
LOGSTASH_PORT = os.environ.get("LOGSTASH_PORT")

ENKI_API_SERVICE_ID = os.environ.get("ENKI_API_SERVICE_ID")

data = {
  'name': 'tcp-logstash',
  'config.host': LOGSTASH_HOST,
  'config.port': LOGSTASH_PORT,
  'config.tls': 'false'
}

response = requests.post(f'http://{KONG_HOST_IP}:{KONG_PORT}/services/{ENKI_API_SERVICE_ID}/plugins', data=data)
