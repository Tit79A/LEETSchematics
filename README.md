# LEETSchematics

**LEETSchematics** is a tool that allows you to work with "*.schematic*" files on a [LEET.CC](https://leet.cc) server. It is divided into two parts: a **MadCommands** script that runs on the game server and a **Python** program that processes data and requests.

**YouTube video:**

[![Download your LEET.CC server builds with LEETSchematics !](https://img.youtube.com/vi/dHNxzbpxYYY/mqdefault.jpg)](https://www.youtube.com/watch?v=dHNxzbpxYYY "Download your LEET.CC server builds with LEETSchematics !")

**It allows you to:**
- **Generate and download** a "*.schematic*" file from a construction on your server.
- **Share builds** between servers.
- **Import constructions** from "*.schematic*" files onto your server.

## How to use it

In order to be able to use this tool, you must have **MadCommands** plugin on your server. Then all you have to do is to copy all the commands in the [LEETSchematics.madcmd](LEETSchematics.madcmd) file to your server (directly or with the help of a [RCON tool](https://edroid.me/projects/rcon++/beta/)). You will find below some examples and you can use the command ```/ls help``` to see all the features.

(NOTE: you may need to increase the maximum processing time using the ```/cmd config proc-max-time <newMaxTime>``` command)

### ① Save your constructions
You want to convert one of your constructions into a "*.schematic*" file? Simply follow these steps:
 1. **Find** the construction that you want to download.
 2. Go to **the first corner** and type the command ```/ls save pos1```.
 3. Go to **the second corner** and use the command ```/ls save pos2```.
 4. **Type** ```/ls save go``` and wait for the end of the process.
 5. **Go** to the tool's web page ([click here](http://lwpdl.pythonanywhere.com/)).
 6. **Enter the token** you received from the server in the first field.
 7. **Click** on "*Download*" and you're done!

### ② Sharing between servers
You have a friend who would like to have your beautiful construction on his server? Simply follow these steps:
 1. **Find** the construction that you want to share.
 2. Go to **the first corner** and type the command ```/ls save pos1```.
 3. Go to **the second corner** and use the command ```/ls save pos2```.
 4. **Type** ```/ls save go``` and wait for the end of the process.
 5. **Send** the token to your friend.
 6. Your friend **must stand** at the place **and look** in the direction in which he wants the construction to appear.
 7. He just has to **type** ```/ls paste go <token>``` and wait for the build to appear.

### ③ Uploading a construction
You found a really cool build on Internet and you would like to have it on your server? Simply follow these steps:
 1. **Go** to the tool's web page ([click here](http://lwpdl.pythonanywhere.com/)).
 2. **Import** the file "*.schematic*" with the corresponding section.
 3. **Wait** until the import is finished and remember the token.
 4. **Go** to your server, **stand** at the place **and look** in the direction in which you want the construction to appear.
 5. Just **type** ```/ls paste go <token>``` and wait for the build to appear.

## Set up your own API server

You are an **advanced user** and you want to set up **your own API server**? Here are some important elements to consider. All the necessary files are located in the [APIServer](APIServer) folder.

### ① Prerequisites
In order for the API server to work properly, you must have **Python 3.6** installed on your machine. You must also install the **nbtschematic** module using the following command:
```
pip3 install nbtschematic
```
Your machine must also be **accessible on the Internet**.

### ② Configuration
In order to modify parameters on the API server, you will need to **edit the code**. For example, in order to make larger selections, you will need to **modify** the file [LEETToJSON.py](APIServer/libraries/LEETToJSON.py) at **line 7** and as follows:
```python
maxSize = <size>
```
You will also need to modify the **MadCommands code** on **line 1** to add the **API address** as follows:
```
let %apiURL% = \"<server adress>/api\"
```

### ③ Starting the server
The API server can work in **two different ways** depending on your needs:
- If you use the **Flask** framework, you can use the [FlaskApp.py](APIServer/FlaskApp.py) file.
- Otherwise, the [HTTPServer.py](APIServer/HTTPServer.py) code can be run directly **without any other installation**.

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.