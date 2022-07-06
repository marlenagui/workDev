from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url="https://updloadfiles.vault.azure.net/", credential=credential)
secret = secret_client.get_secret("seb")

print(secret.name)
print(secret.value)