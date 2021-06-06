var preload,canvasXML,mediaXML;
var folderId;
var htmlSlideCount = 0;
var lastslide=0;
function init(isHtml)
{
	runtime = getUrlVars()["display"];
	if (runtime && runtime == "html") 
	{		
		loadHTMLVersion();			
	}
	else if(swfobject && !swfobject.hasFlashPlayerVersion("1"))
	{
		loadHTMLVersion();					
	}else if(isHtml){
		runtime = "html";
		loadHTMLVersion();
	}	
}

function loadHTMLVersion()
{
	var newImage=new Image();
		newImage.src='../../../common/images/preloader.gif';		
		newImage.onload=function()
		{	
			var img = document.createElement('img');
			img.src='../../../common/images/preloader.gif';
			img.id='preloader';			
			img.style.position='absolute';
			img.style.top='50%';
			img.style.left='50%';	
			document.body.appendChild(img);
			document.body.setAttribute("spellcheck","false");
			//loadTemplate();
			loadScript("../../../common/scripts/jquery-1.7.2.min.js", jqueryLoaded);		
		};	
}

function jqueryLoaded()
{
	folderId= $("[name = 'movie']")[0].value;

	//var runtime = getUrlVars()["display"];
	if (runtime && runtime == "html") {
		var _w = $("#canvas").attr("width");
		var _h = $("#canvas").attr("height");

		//$("#myId").remove();
		$("#flashObject").remove();
		$("#flashContent").append('<div id="htmlMedia"><canvas id="canvas" width="'+_w+'" height="'+_h+'" style="background-color:#ffffff"></canvas></div>')
	}

	loadScript("../../../common/scripts/createJS_bundle_060.min.js", loadTemplate);	
	
	if(parent.parent.jquery) $.noConflict();
}

//To load template files
function loadTemplate()
{
	var templateFile;	
	//For Deployment
	//tF = "../../../common/scripts/templates_base_min.js";
	//For Developement
	templateFile = "../../../common/scripts/templates_base_dev.js";
	
	var url=location.href;	
	var mediaPath = url.split("index.html")[0];
	
	var langPath = getUrlVars()['lang'];
	if(langPath)
	{
		//select the language folder
		mediaPath = mediaPath.replace("trans_1",langPath);		
	};
	//var folderId= document.getElementsByName("movie").item(0).value;
	//var folderId= $("[name = 'movie']")[0].value;
	var xmlPath = folderId.split(".swf")[0];
	var fileName = xmlPath;
	xmlPath = mediaPath+xmlPath;
	/*
	var url= document.getElementsByName("movie").item(0).value;
	var xmlPath = url.split(".swf")[0];
	//{id:"jquery", src:"../../../common/scripts/jquery-1.7.2.min.js"},
	*/
	var manifest = [{id:"mediaXML", src:xmlPath+'.xml'},
					{id:"canvasXML", src:fileName+'_canvas.xml'},
					{id:"templateFile", src:templateFile}];	
	
	preload = new createjs.LoadQueue(false);
	preload.addEventListener("fileload", hLoaded);
   	preload.addEventListener("error", hError);	
	preload.addEventListener("complete", hComplete);
	preload.loadManifest(manifest);	
}

function hLoaded(event) {
	switch (event.item.type){	
		case createjs.LoadQueue.IMAGE:
			break;	
		case createjs.LoadQueue.JAVASCRIPT:
			document.body.appendChild(event.result);
			break;		
		case createjs.LoadQueue.XML:
			if(event.item.id == "mediaXML") mediaXML = event.result;
			if(event.item.id == "canvasXML") canvasXML = event.result;
			break;	
	}
}

function hComplete(event)
{
	preload = null;
	initiateTemplate();	
}

function setSlide(index)
{
	if(typeof slideViewChange == 'function') slideViewChange(btnArray[index-1],index-1);
	btnArray[lastslide].hide();
	btnArray[index-1].show();
	lastslide=index-1;
}

function hError(event) {
	console.log("File loader failed");
	console.log(event);
	///alert("File loader failed "+event);
}

/********************************************************************************************************************************
														 Get URL Query
*********************************************************************************************************************************/
function getUrlVars() {
	var vars = {};
	var url = window.parent.parent.location.href;
	var parts = url.split("#")[0].replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
		vars[key] = value;
	});
	return vars;
}