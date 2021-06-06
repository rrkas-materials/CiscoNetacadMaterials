var preload, canvasXML, mediaXML;
var folderId;
var canvasXMLSrc, mediaXMLSrc;
var canvasWidth = 600;
var canvasHeight = 400;
var htmlSlideCount = 0;
var lastslide = 0;

function init() {
    // delete the Flash object
    try{
        document.getElementsByTagName("Object")[1].data = ""
    }catch(e){}
    runtime = "html";
    path = document.getElementsByTagName("Title")[0].innerHTML
    if(path.includes(" ")){
        path = path.split(" ")[0]
    }
    mediaXMLSrc = "media_" + path + ".xml";
    canvasXMLSrc = "media_" + path + "_canvas.xml";
    loadHTMLVersion();
}

function loadHTMLVersion() {
    var newImage = new Image();
    newImage.src = '../../../common/images/preloader.gif';
    newImage.onload = function() {
        var img = document.createElement('img');
        img.src = '../../../common/images/preloader.gif';
        img.id = 'preloader';
        img.alt = 'Loading...';
        img.style.position = 'absolute';
        img.style.top = '50%';
        img.style.left = '50%';
        document.body.appendChild(img);
        document.body.setAttribute("spellcheck", "false");
        //loadTemplate();
        loadScript("../../../common/scripts/jquery-2.2.4.min.js", jqueryLoaded);
    };
}

function jqueryLoaded() {
    $("body").append('<div id="htmlMedia"><canvas id="canvas" width="' + canvasWidth + '" height="' + canvasHeight + '" ></canvas></div>')
    loadScript("../../../common/scripts/createJS_bundle_060.min.js", loadTemplate);
    try {
        if (parent.parent.jquery) $.noConflict();
    } catch (e) {
        // do nothing
    }
}

//To load template files
function loadTemplate() {
    var templateFile;
    //For Deployment
    //tF = "../../../common/scripts/templates_base_min.js";
    //For Developement
    templateFile = "../../../common/scripts/templates_base_dev.js";

    var url = location.href;
    var mediaPath = url.split("index.html")[0];

    var langPath = getUrlVars()['lang'];
    if (langPath) {
        //select the language folder
        mediaPath = mediaPath.replace("trans_1", langPath);
    };
    
    var manifest = [{ id: "mediaXML", src: mediaXMLSrc },
        { id: "canvasXML", src: canvasXMLSrc },
        { id: "templateFile", src: templateFile }
    ];

    preload = new createjs.LoadQueue(false);
    preload.addEventListener("fileload", hLoaded);
    preload.addEventListener("error", hError);
    preload.addEventListener("complete", hComplete);
    preload.loadManifest(manifest);
}

function hLoaded(event) {
    switch (event.item.type) {
        case createjs.LoadQueue.IMAGE:
            break;
        case createjs.LoadQueue.JAVASCRIPT:
            document.body.appendChild(event.result);
            break;
        case createjs.LoadQueue.XML:
            if (event.item.id == "mediaXML") mediaXML = event.result;
            if (event.item.id == "canvasXML") canvasXML = event.result;
            break;
    }
}

function hComplete(event) {
    preload = null;
    initiateTemplate();
}

function setSlide(index) {
    if (typeof slideViewChange == 'function') slideViewChange(btnArray[index - 1], index - 1);
    btnArray[lastslide].hide();
    btnArray[index - 1].show();
    lastslide = index - 1;
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
    try {
        var url = window.parent.parent.location.href;
        var parts = url.split("#")[0].replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m, key, value) {
            vars[key] = value;
        });
    } catch (e) {
        // do nothing
    }
    return vars;
}