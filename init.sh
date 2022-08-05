cd /home/sepenet/uploadFiles
. bin/activate

export AZURE_CLIENT_ID="def8c7be-99f3-49ca-99f3-746bad04a203"
export AZURE_CLIENT_SECRET="cDY8Q~GpO6jLhWBDNoAYMz~xFNYOp2RQYPgCDbLS"
export AZURE_TENANT_ID="b1d48f7c-fcc5-4713-8c1e-bcfb9952c5ba"
export KEY_VAULT_NAME=updloadfiles
export FLASK_APP=uploadFiles.py
export FLASK_ENV=development
export  AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=sebuploadfiles;AccountKey=EBaqI0KJuRr/560P3wxqU8GpnklTFnNanswFdFsFazJOWgY8f5PE5rG3Yggg4prlDjPEnCVt3T4R+AStEG7X8A==;EndpointSuffix=core.windows.net"
export AZURE_STORAGE_ACCOUNT=sebuploadfiles
export AZURE_STORAGE_ACCESS_KEY=ZROxUZZXU6UM2LdMCRuhb9UMPXoZ0I+P71fvNmLkdA9LJ8dMSfktWszHLbxCSmNRITioPAEb3i2E+AStwRUN4A==

flask run --host=0.0.0.0

# git config user.email "sebastine@pe-net.fr"
# git config user.name "Sebastien Penet"
# git branch -M main
# git remote add origin https://github.com/marlenagui/uploadFiles.git
# git push -u origin main

kubectl create secret generic azure-secret --from-literal azurestorageaccountname=sebuploadfiles --from-literal azurestorageaccountkey="ZROxUZZXU6UM2LdMCRuhb9UMPXoZ0I+P71fvNmLkdA9LJ8dMSfktWszHLbxCSmNRITioPAEb3i2E+AStwRUN4A==" --type=Opaque