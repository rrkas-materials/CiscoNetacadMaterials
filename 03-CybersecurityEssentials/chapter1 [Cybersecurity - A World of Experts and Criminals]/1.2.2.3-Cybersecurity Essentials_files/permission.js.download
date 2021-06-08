var permission = new function() {
  var currentURL = window.location.href;
  var courseID = currentURL.split("/")[3];
  function setSession() {
    var current = new Date();
    var expires = new Date(current.getTime());
    expires.setDate(expires.getDate() + 1);
    document.cookie = courseID+"=" + current.getDate() + "; expires=" + expires.toUTCString() + "; path=/" + courseID+"";
  }

  function checkSession(callback) {
    var re = new RegExp('\(?:(?:^|.*;\\s*)'+courseID+'\\s*\\=\\s*([^;]*).*$)|^.*$');
    var value = document.cookie.replace(re, "$1") || null;
    if (value == (new Date()).getDate()) {
      callback(true);
      return;
    }
    callback(false);
  }

  function setAuthAttemp(){
    var current = new Date();
    current.setTime(current.getTime() + (15 * 60 * 1000));
    document.cookie="name=auth_Attempted; expires=" + current.toUTCString() + ";";
  }
  function getAuthAttempt(){
    return (document.cookie && document.cookie.indexOf('auth_Attempted') != -1) 
  }

  function updateLoginLink(domain) {
    // 
  }
  function mapURL(url) {
    return null;
  }
	var urls = new Array();
	urls[0] = "https://www.netacad.com/portal/cors";
	urls[1] = "https://portal-cn.netacad.com/cors";
  urls[2] = "https://cu.netacad.com/portal/cors";
  urls[3] = "https://rni-test-portal.netacad.com/cors";
  urls[4] = "https://popga-portal.netacad.com/cors";
  urls[5] = "https://gni-prf.netacad.com/portal/cors";
  
  var i = 0;

  function checkHostname(callback) {
    // WEF courses - launched from canvas but logged in from OKTA rather than liferay so we can't do a standard test
    try{
    var r = netacad.settings.get(netacad.settings.RETURN_KEY);
    var url = new netacad.net.URL(r);
    console.log("check WEF: "+url)
     if(url.authority.indexOf("568933118")>= 0){
      //  if return to class URL is from the WEF academy then ok
      console.log("from Okta")
        callback(true)
        return
      }
    }catch(e){
      //
    }
    //   end WEF 
    testURL(function(success){
    if(success){
      callback(true);
    }else{
      if(i<=4){
        i++;
        checkHostname(function(success){
          if (success){
            callback(true);
          }else{
            callback(false);  
          }
        });
      }else{
        callback(false);
      }
    }
  }, urls, i);
  }
  function testURL(callback, urls,i){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(event) {
      if (request.readyState == XMLHttpRequest.DONE) {
      if(request.status == 200){
		callback(true);
      }else{
		callback(false);
      }
    }
    };
    request.withCredentials = "true";
    request.open("GET", urls[i], true);
        //permRequest.setRequestHeader("Accept",window.location.href);
    request.send();
  }

  this.check = function(callback) {
    if (window.location.hostname == "static-course-assets.s3.amazonaws.com") {
     checkSession(function(success) {
        if (success) {
          callback(true);
        } else {
          checkHostname(function(success) {
            if (success) {
              setSession();
              callback(true);
            } else {
              if(getAuthAttempt() == false){
                console.log("checked urls - no success - redirect");
                setAuthAttemp();
                //var tempHref = window.location.href;
                window.location.href = "https://www.netacad.com/portal/cors/user_login";
              }else{
                document.body.innerHTML = document.body.innerHTML.replace('<a href="http://netacad.com">netacad.com</a>', 'your class');
                callback(false);
              }
            }
          });
        }
      });
    } else {
      callback(true);
    }
  };
  
}();