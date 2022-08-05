from flask import Flask, render_template, jsonify, request, flash, url_for
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from werkzeug.utils import secure_filename
import os
import urllib.request
from datetime import datetime

#############################################################################################################################################
# Global variables
class glob(object):
    """global variables definition"""
    verbose = False
    uploadFolderLocal = ""
    uploadFolderContainer = "" 


#############################################################################################################################################
# Create the flask app and set parameters      
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024                         # Max length file 16GB 
app.secret_key='gmljrm,csdlfvnlerjhgoiajrome ldfnvmlkarjmoiazj'

ALLOWED_EXTENSIONS = set(['heic', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])       # Allowed extensions
   
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#############################################################################################################################################
# Keyvault init
#  a spn is required to provide the script access to the kv
# az ad sp create-for-rbac --name http://uploadFiles --skip-assignment 
#{
#  "appId": "def8c7be-99f3-49ca-99f3-746bad04a203",
#  "displayName": "http://uploadFiles",
#  "password": "cDY8Q~GpO6jLhWBDNoAYMz~xFNYOp2RQYPgCDbLS",
#  "tenant": "b1d48f7c-fcc5-4713-8c1e-bcfb9952c5ba"
#}
# policy need to be set on the kv for the SPN to access the secret
# az keyvault set-policy --name updloadfiles --spn $AZURE_CLIENT_ID --secret-permissions get  list 
# Then env variable need to be set 
#export AZURE_CLIENT_ID="def8c7be-99f3-49ca-99f3-746bad04a203"
#export AZURE_CLIENT_SECRET="cDY8Q~GpO6jLhWBDNoAYMz~xFNYOp2RQYPgCDbLS"
#export AZURE_TENANT_ID="b1d48f7c-fcc5-4713-8c1e-bcfb9952c5ba"
#export KEY_VAULT_NAME=uploadfiles
# TODO find an alternative to provide SPN ID, Secret, Tenant used to access the KV

keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KVUri, credential=credential)  

#############################################################################################################################################
# Storage account init
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


# Rendering the root page
@app.route('/')
def main():
    return render_template('index.html')
#############################################################################################################################################
# On root page post (aka continuer) the key is evaluated against keyvault secret. 
# if the key vault secret exist, it retrieves the value which is used target folder name to store the images.
# TODO Create the folder in the storage account instead of local directory
# TODO find an alternative to store the KV SPN ID, Secret and Tenant

@app.route('/uploadFiles', methods=['POST'])
def keyValidation():
    UPLOAD_FOLDER = '/mnt/images'                                        # set the root folder for images
    if request.method == 'POST':
        userKey = str(request.form.get('key')).lower()                     
        userFirstname = str(request.form.get('firstname')).lower()      # we get the user firstname, it corresponds in the form input name=firstname
        try: 
            retrieved_secret = secret_client.get_secret(userKey)        # we get the key, it corresponds in the form input name=key
        except Exception:
            flash("La clé n'existe pas...")
            return render_template("index.html", missing_key="La clé n'existe pas .... essaye encore :) ") 

        # Update the folder with the secret value of the key in the KV + firstname given on root page
        UPLOAD_FOLDER = UPLOAD_FOLDER + "/" + retrieved_secret.value + "/" + userFirstname  
        glob.uploadFolderContainer=retrieved_secret.value
        print(glob.uploadFolderContainer.lower())
        # create the local folder to temporarly store the images
        if not os.path.isdir(UPLOAD_FOLDER):
            try:
                print("create directory %s", UPLOAD_FOLDER)
                os.makedirs(UPLOAD_FOLDER)       # os.makedirs is used --> recursively create folders
            except OSError as error:
                return render_template('error.html', error_message="Impossible de créer le repertoire de dépot des images" + str(error))
        
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER                     # Set target folder for the dropzone 
        msg = 'La clé existe'    
    return render_template('uploadPage.html')

#############################################################################################################################################
# /upload API to load the images files in the target directory
# /upload is called from the /uploadFiles.html in the script section when file(s) are selected or dropped
# TODO upload in storage account instead of local folder

@app.route("/upload",methods=["POST","GET"])
def upload(): 
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
          
        if file and allowed_file(file.filename):
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        else:
           print('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
        msg = 'Success Uplaod'    
    return jsonify(msg)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)
