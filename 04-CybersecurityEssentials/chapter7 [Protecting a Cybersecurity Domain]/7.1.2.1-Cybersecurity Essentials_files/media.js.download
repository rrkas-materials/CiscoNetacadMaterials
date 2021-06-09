/*

  FlashMedia

*/

function FlashMedia(element) {
  Media.call(this, element);
}

FlashMedia.prototype = new Media();
FlashMedia.prototype.constructor = FlashMedia;

FlashMedia.prototype.getSlideCount = function() {
  return this.element.getSlideCount();
};

FlashMedia.prototype.getSlide = function() {
  return this.element.getSlide();
};

FlashMedia.prototype.setSlide = function(index) {
  this.element.setSlide(index); 
};

/*

  HTMLMedia

*/

function HTMLMedia(element) {
  Media.call(this, element);
}

HTMLMedia.prototype = new Media();
HTMLMedia.prototype.constructor = HTMLMedia;

HTMLMedia.prototype.getSlideCount = function() {
  return htmlSlideCount;
};

HTMLMedia.prototype.getSlide = function() {
  return 1;
};

HTMLMedia.prototype.setSlide = function(index) {
   setSlide(index)
};

/*

  Media

*/

function Media(element) {
  this.element = element;
}

Media.prototype.getSlideCount = function() {
  throw new Error("abstract method not implemented");
};

Media.prototype.getSlide = function() {
  throw new Error("abstract method not implemented");
};

Media.prototype.setSlide = function(index) {
  throw new Error("abstract method not implemented");
};

Media.prototype.getPseudolocalize = function() {
  if (netacad) {
    return !!netacad.settings.get(netacad.settings.DEVELOPER_PSEUDOLOCALIZATION_KEY);
  }
  return false;
};

Media.prototype.ready = function() {
  var view = document.defaultView;
  var hostname = view.location.hostname;
  while (view) {
    if (typeof view.mediaReady === "function") {
      view.mediaReady(this);
    }
    try {
      if (view == view.parent || hostname != view.parent.location.hostname) {
        break;
      }
    } catch (e) {
      break;
    }
    view = view.parent;
  }
  return true;
};

var netacad = function() {
  var view = window;
  var hostname = view.location.hostname;
  while (view) {
    if (typeof view.netacad === "object" && view.netacad !== null) {
      return view.netacad;
    }
    try {
      if (view == view.parent || hostname != view.parent.location.hostname) {
        break;
      }
    } catch (e) {
      break;
    }
    view = view.parent;
  }
  return null;
}();
var media;
var element = document.getElementById("htmlMedia");
        media = new HTMLMedia(element);
        /*
swfobject.registerObject("flashObject", "9.0.0", false, function(event) {
  if (netacad && netacad.config.disableFlashMedia) {
    var element = document.getElementById("htmlMedia");
    media = new HTMLMedia(element);
  } else {
    if (event.success) {
      var mediaType = document.querySelector('[name="mediaType"]');
      if (mediaType && mediaType.value == "html") {
        var element = document.getElementById("htmlMedia");
        media = new HTMLMedia(element);
      } else {
        // hardcoded to always display HTML
        //var element = swfobject.getObjectById("flashObject");
       // media = new FlashMedia(element);
         var element = document.getElementById("htmlMedia");
        media = new HTMLMedia(element);
      }
    } else {
      var element = document.getElementById("htmlMedia");
      media = new HTMLMedia(element);
    }
  }
});
*/
