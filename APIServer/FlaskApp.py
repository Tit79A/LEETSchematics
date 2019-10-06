import os
import io
from flask import Flask, send_from_directory, send_file, request
from libraries import JSONToLEET, LEETToJSON, GlobalTools, NBTSchematicsTools
from werkzeug.utils import secure_filename


static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'www')
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5000000


os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'www'))
GlobalTools.makeNeededDirectories()


@app.route('/', methods=['GET'])
def serveIndex():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serveStaticFile(path):
    return send_from_directory(static_file_dir, path)


@app.route('/api/', defaults={'path': ''}, methods=['GET'])
@app.route('/api/<path:path>', methods=['GET'])
def apiGET(path):
    parsedURL = path.split("/")
    if len(parsedURL) >= 1:
        if parsedURL[0] == "ltj":
            return LEETToJSON.LTJManager(parsedURL[1:])
        elif parsedURL[0] == "jtl":
            return JSONToLEET.JTLManager(parsedURL[1:])
        elif parsedURL[0] == "download":
            if len(parsedURL) >= 2:
                if GlobalTools.checkToken(parsedURL[1]):
                    try:
                        NBTSchematicsTools.generateSchematicFromBlocksFile("../output/json/" + secure_filename(parsedURL[1]) + ".json", "../output/schematic/")
                        with open("../output/schematic/" + secure_filename(parsedURL[1]) + ".schematic", 'rb') as f:
                            return send_file(io.BytesIO(f.read()), attachment_filename = secure_filename(parsedURL[1]) + ".schematic", mimetype = "application/octet-stream")
                    except:
                        return "Unable to generate the file, please try again."
                else:
                    return "No construction is linked to this token."
            else:
                return "You must provide a token."
        else:
            return "Error : Invalid argument(s)."
    else:
        return "Error : Missing argument(s)."


@app.route('/api/', defaults={'path': ''}, methods=['POST'])
@app.route('/api/<path:path>', methods=['POST'])
def apiPOST(path):
    parsedURL = path.split("/")
    if len(parsedURL) >= 1:
        if parsedURL[0] == "upload":
            if 'file' in request.files:
                file = request.files['file']
                if file.filename != '':
                    if (file.filename).endswith(".schematic"):
                        token = GlobalTools.generateToken()
                        file.save("../output/schematic/" + token + ".schematic")
                        try:
                            NBTSchematicsTools.readBlocksFromSchematicFile("../output/schematic/" + token + ".schematic", "../output/json/")
                            return "The construction has been successfully uploaded, its token is: <font color='red'>" + token + "</font>"
                        except:
                            return "The loading of the build failed. If this does not work after several attempts, the file may be incompatible."
                    else:
                        return "Sorry, I only accept files with the \".schematic\" extension."
                else:
                    return "There is no selected file"
            else:
                return "There is no selected file"
        else:
            return "Error : Invalid argument(s)."
    else:
        return "Error : Missing argument(s)."