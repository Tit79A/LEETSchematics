import os
import cgi
import shutil
from urllib.parse import urlparse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from libraries import JSONToLEET, LEETToJSON, GlobalTools, NBTSchematicsTools
from werkzeug.utils import secure_filename


class LSRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsedURL = (urlparse(self.path).path)[1:].split("/")
        if parsedURL[0] == "api":
            if len(parsedURL) >= 2:
                if parsedURL[1] == "ltj":
                    self.respond(bytes(str(LEETToJSON.LTJManager(parsedURL[2:])), "utf-8"))
                elif parsedURL[1] == "jtl":
                    self.respond(bytes(str(JSONToLEET.JTLManager(parsedURL[2:])), "utf-8"))
                elif parsedURL[1] == "download":
                    if len(parsedURL) >= 3:
                        if GlobalTools.checkToken(parsedURL[2]):
                            try:
                                NBTSchematicsTools.generateSchematicFromBlocksFile("../output/json/" + secure_filename(parsedURL[2]) + ".json", "../output/schematic/")
                                with open("../output/schematic/" + secure_filename(parsedURL[2]) + ".schematic", 'rb') as f:
                                    self.send_response(200)
                                    self.send_header("Content-Type", 'application/octet-stream')
                                    self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(secure_filename(parsedURL[2] + ".schematic")))
                                    fs = os.fstat(f.fileno())
                                    self.send_header("Content-Length", str(fs.st_size))
                                    self.end_headers()
                                    shutil.copyfileobj(f, self.wfile)
                            except:
                                self.respond(bytes("Unable to generate the file, please try again.", "utf-8"))
                        else:
                            self.respond(bytes("No construction is linked to this token.", "utf-8"))
                    else:
                        self.respond(bytes("You must provide a token.", "utf-8"))
                else:
                    self.respond(bytes("Error : Invalid argument(s).", "utf-8"))
            else:
                self.respond(bytes("Error : Missing argument(s).", "utf-8"))
        else:
            super().do_GET()
    
    
    def do_POST(self):
        parsedURL = (urlparse(self.path).path)[1:].split("/")
        if parsedURL[0] == "api":
            if len(parsedURL) >= 2:
                if parsedURL[1] == "upload":
                    length = int(self.headers['content-length'])
                    if length < 5000000:
                        form = cgi.FieldStorage(
                            fp=self.rfile,
                            headers=self.headers,
                            environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type']}
                        )
                        filename = str(form['file'].filename)
                        if filename.endswith(".schematic"):
                            data = form['file'].file.read()
                            token = GlobalTools.generateToken()
                            open("../output/schematic/" + token + ".schematic", "wb").write(data)
                            try:
                                NBTSchematicsTools.readBlocksFromSchematicFile("../output/schematic/" + token + ".schematic", "../output/json/")
                                self.respond(bytes("The construction has been successfully uploaded, its token is: <font color='red'>" + token + "</font>", "utf-8"))
                            except:
                                self.respond(bytes("The loading of the build failed. If this does not work after several attempts, the file may be incompatible.", "utf-8"))
                        else:
                            self.respond(bytes("Sorry, I only accept files with the \".schematic\" extension.", "utf-8"))
                    else:
                        self.respond(bytes("This file is too big. Please select another one.", "utf-8"))
                else:
                    self.respond(bytes("Error : Invalid argument(s).", "utf-8"))
            else:
                self.respond(bytes("Error : Missing argument(s).", "utf-8"))
        else:
            self.respond(bytes("Error : POST requests are not handled here.", "utf-8"))
            
    
    def respond(self, response):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response) 


httpd = HTTPServer(("127.0.0.1", 80), LSRequestHandler)
os.chdir("www")
GlobalTools.makeNeededDirectories()
print("HTTP server started !")
httpd.serve_forever()