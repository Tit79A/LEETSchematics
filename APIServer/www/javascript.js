var infoBox = document.querySelector(".infoBox");
var closeButton = document.querySelector(".closeinfoBox");

function hideInfoBox() {
    infoBox.classList.toggle("showinfoBox", false);
	document.getElementById("infoBoxInnerText").innerHTML = '<span class="loadingText">Waiting<div class="loader"></div></span>';
}

function windowOnClick(event) {
    if (event.target === infoBox) {
        infoBox.classList.toggle("showinfoBox", false);
		document.getElementById("infoBoxInnerText").innerHTML = '<span class="loadingText">Waiting<div class="loader"></div></span>';
    }
}

closeButton.addEventListener("click", hideInfoBox);
window.addEventListener("click", windowOnClick);


function getFileNameByContentDisposition(contentDisposition){
    var regex = /filename[^;=\n]*=(UTF-8(['"]*))?(.*)/;
    var matches = regex.exec(contentDisposition);
    var filename;

    if (matches != null && matches[3]) { 
      filename = matches[3].replace(/['"]/g, '');
    }

    return decodeURI(filename);
}


function downloadSchematicByToken() {
	infoBox.classList.toggle("showinfoBox", true);
	
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "/api/download/" + document.getElementById("token").value);
	xhr.responseType = 'blob';
	xhr.timeout = 10000;
	xhr.onload = function(event){
		if (xhr.status != 200) {
			document.getElementById("infoBoxInnerText").innerHTML = "An error occurred while loading the data, please try again.";
		} else {
			if(xhr.getResponseHeader("Content-Type") == "application/octet-stream") {
				var blob = new Blob([this.response], {type: 'application/octet-stream'});
				let a = document.createElement("a");
				a.style = "display: none";
				document.body.appendChild(a);
				let url = window.URL.createObjectURL(blob);
				a.href = url;
				a.download = getFileNameByContentDisposition(xhr.getResponseHeader('Content-Disposition'));
				a.click();
				window.URL.revokeObjectURL(url);
				document.getElementById("infoBoxInnerText").innerHTML = "The file has been correctly downloaded!";
			} else {
				var blob = new Blob([this.response], {type: 'text/html'});
				var reader = new FileReader();
				reader.onload = function() {
					document.getElementById("infoBoxInnerText").innerHTML = reader.result;
				}
				reader.readAsText(blob);
			}
		}
	};
	xhr.send();
}

function sendSchematicFile() {
	infoBox.classList.toggle("showinfoBox", true);
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "/api/upload");
	xhr.timeout = 10000;
	xhr.onload = function(event){
		if (xhr.status != 200) {
			document.getElementById("infoBoxInnerText").innerHTML = "An error occurred while loading the data, please try again.";
		} else {
			document.getElementById("infoBoxInnerText").innerHTML = event.target.response;
		}
	};
	var formData = new FormData(document.getElementById("uploadForm")); 
	xhr.send(formData);
}