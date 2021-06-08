if (typeof(jQuery) == "undefined") {
    var iframeBody = document.getElementsByTagName("body");
    try { 
      if(parent.parent.jQuery)
      {
      	window.jQuery = function (selector) { return parent.parent.jQuery(selector, iframeBody); };
           window.$ = window.jQuery;
      }
    } catch (e) {
      // do nothing
    }
}	

function loadScript(url, callback){
    var script = document.createElement("script")
    script.type = "text/javascript";

    if (script.readyState){  //IE
        script.onreadystatechange = function(){
            if (script.readyState == "loaded" ||
                    script.readyState == "complete"){
                script.onreadystatechange = null;
		if(callback != null){
                	callback();
		}
            }
        };
    } else {  //Others
        script.onload = function(){
            if(callback != null){
                	callback();
		}
        };
    }
    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}



