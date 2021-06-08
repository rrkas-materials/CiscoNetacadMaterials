var netacad = function() {
  var view = window;
  var hostname = view.location.hostname;
  while (view) {
    if (typeof view.netacad === "object") {
      return view.netacad;
    }
    try {
      if (view == view.parent || view.parent.location.hostname != hostname) {
        break;
      }
    } catch (e) {
      break;
    }
    view = view.parent;
  }
  return null;
}();

var override = {};
var pageType = null;
var pageSize = null;
var pageNewAnim = null;

function Page(element) {
  this.element = element;
  this.document = this.element.ownerDocument;
  this.view = this.document.defaultView;
  this.type = override.pageType || this.TEXT_ON_RIGHT;
  this.size = override.pageSize || this.PAGE_SIZE;
  this.anim = override.pageNewAnim || this.PAGE_NEW_ANIM;
  
  if (this.document.documentElement.getAttribute("dir") == "rtl") {
    if (this.type == this.TEXT_ON_RIGHT) {
      this.type = this.TEXT_ON_LEFT;
    } else if (this.type == this.TEXT_ON_LEFT) {
      this.type = this.TEXT_ON_RIGHT;
    }
  }
  pageType = this.type;
  pageSize = this.size;
  pageNewAnim = this.anim;
  this.mediaWidth = null;
  this.textMinWidth = null;
  this.textMaxWidth = null;
  this.mediaContainer = document.getElementById("media-container");
  this.textContainer = document.getElementById("text-container");
  this.textContainer.setAttribute("role", "region");
  this.mediaDescription = document.getElementById("media-description");
  this.mediaDescription.tabIndex = 0;
  this.text = document.getElementById('text').getElementsByTagName('h1');
  this.text[0].tabIndex = 0;
  this.textDiv = document.getElementById('text').getElementsByTagName('div');
  this.textDiv[0].tabIndex = 0;
  this.textHandle = this.document.getElementById("text-handle");
  this.view.addEventListener("load", this);
  this.view.addEventListener("resize", this);
  //this.textHandle.addEventListener("mousedown", this);
  this.textHandle.addEventListener("click", this);
  this.textHandle.addEventListener("touchstart", this);
  $(this.element).addClass(this.type);
  this.update();
  if (netacad) {
    var width = netacad.settings.get(netacad.settings.TEXTWIDTH_KEY);
    if (width) {
      this.setTextWidth(width);
    }
  }
};

Page.prototype.TEXT_ON_RIGHT = "text-on-right";
Page.prototype.TEXT_ON_LEFT = "text-on-left";
Page.prototype.FULL_MEDIA = "full-media";
Page.prototype.PAGE_SIZE = "680*490";
Page.prototype.PAGE_NEW_ANIM = "false";

Page.prototype.handleEvent = function(event) {
  if (event.type == "load" || event.type == "resize") {
    this.update();
  } else if (event.type == "mousedown") {
    this.handleMouseDown(event);
  } else if (event.type == "click") {
   this.handleMouseDown2(event);
  } else if (event.type == "touchstart") {
    this.handleTouchStart(event);
  }
};

Page.prototype.handleMouseDown2 = function(event) {
 var that = this;
 that.toggle();
}

Page.prototype.handleMouseDown = function(event) {

  if (event.button > 1) {
    return;
  }

  var that = this;
  var moved = false;
  var threshold = 4;
  var screenX = event.screenX;
  var textWidth = this.getTextWidth();
  var frame = document.getElementById("media");

  function handleMouseMove(event) {
    var deltaX = (screenX - event.screenX);
    if (Math.abs(deltaX) > threshold) {
      if (that.type == that.TEXT_ON_RIGHT) {
        that.setTextWidth(textWidth + deltaX);
      } else if (that.type == that.TEXT_ON_LEFT) {
        that.setTextWidth(textWidth - deltaX);
      }
      moved = true;
    }
    event.stopPropagation();
    event.preventDefault();
  }

  function handleMouseUp(event) {
    if (!moved) {
      that.toggle();
    }
    window.removeEventListener("mouseup", handleMouseUp, true);
    window.removeEventListener("mousemove", handleMouseMove, true);
    try {
      window.parent.removeEventListener("mouseup", handleMouseUp, true);
      window.parent.removeEventListener("mousemove", handleMouseMove, true);
    } catch (e) {
      // do nothing
    }
    frame.contentWindow.removeEventListener("mouseup", handleMouseUp, true);
    frame.contentWindow.removeEventListener("mousemove", handleMouseMove, true);
    event.stopPropagation();
    event.preventDefault();
  }

  window.addEventListener("mouseup", handleMouseUp, true);
  window.addEventListener("mousemove", handleMouseMove, true);
  try {
    window.parent.addEventListener("mouseup", handleMouseUp, true);
    window.parent.addEventListener("mousemove", handleMouseMove, true);
  } catch (e) {
    // do nothing
  }
  frame.contentWindow.addEventListener("mouseup", handleMouseUp, true);
  frame.contentWindow.addEventListener("mousemove", handleMouseMove, true);
  event.stopPropagation();
  event.preventDefault();

};

Page.prototype.handleTouchStart = function(event) {

  var that = this;
  var moved = false;
  var threshold = 8;
  var anchor = event.changedTouches[0];
  var identifier = anchor.identifier;
  var screenX = anchor.screenX;
  var textWidth = this.getTextWidth();
  
  function handleTouchMove(event) {
    for (var i = 0; i < event.changedTouches.length; i++) {
      var touch = event.changedTouches[i];
      if (touch.identifier == identifier) {
        var deltaX = screenX - touch.screenX;
        if (Math.abs(deltaX) > threshold) {
          if (that.type == that.TEXT_ON_RIGHT) {
            that.setTextWidth(textWidth + deltaX);
          } else if (that.type == that.TEXT_ON_LEFT) {
            that.setTextWidth(textWidth - deltaX);
          }
          moved = true;
        }
        event.stopPropagation();
        event.preventDefault();
        break;
      }
    }
  }

  function handleTouchEnd(event) {
    for (var i = 0; i < event.changedTouches.length; i++) {
      var touch = event.changedTouches[i];
      if (touch.identifier == identifier) {
        if (!moved) {
          that.toggle();
        }
        window.removeEventListener("touchend", handleTouchEnd, true);
        window.removeEventListener("touchcancel", handleTouchEnd, true);
        window.removeEventListener("touchmove", handleTouchMove, true);
        event.stopPropagation();
        event.preventDefault();
        break;
      }
    }
  }

  window.addEventListener("touchend", handleTouchEnd, true);
  window.addEventListener("touchcancel", handleTouchEnd, true);
  window.addEventListener("touchmove", handleTouchMove, true);
  event.stopPropagation();
  event.preventDefault();

};

Page.prototype.toggle = function(event) {
  if ($(this.textContainer).hasClass("open")) {
    this.setTextWidth(this.textMinWidth);
  } else {
    this.setTextWidth(this.textMaxWidth);
  }
};

Page.prototype.update = function() {
  if (this.type == this.FULL_MEDIA) {
    this.mediaContainer.style.removeProperty("width");
    this.textContainer.style.removeProperty("width");
    this.textContainer.style.removeProperty("min-width");
    this.textContainer.style.removeProperty("max-width");
  } else {
    var ratio = 680 / 490;
    var availableWidth = document.body.clientWidth;
    var availableHeight = document.body.clientHeight;
    this.mediaWidth = Math.round(availableHeight * ratio);
    this.textMinWidth = Math.round(availableWidth - this.mediaWidth);
    this.textMaxWidth = Math.round((this.mediaWidth / 2) + this.textMinWidth);
    this.mediaContainer.style.setProperty("width", this.mediaWidth + "px");
    this.textContainer.style.setProperty("min-width", this.textMinWidth + "px");
    this.textContainer.style.setProperty("max-width", this.textMaxWidth + "px");
    var textWidth = this.getTextWidth();
    if (textWidth > this.textMaxWidth) {
      this.setTextWidth(this.textMaxWidth);
    }
    if (textWidth < this.textMinWidth) {
      this.setTextWidth(this.textMinWidth);
    }
  }
};

Page.prototype.getTextWidth = function() {
  return parseInt(this.textContainer.style.getPropertyValue("width")) || this.textMinWidth;
};

Page.prototype.setTextWidth = function(value) {
  if (this.type == this.FULL_MEDIA) {
    return;
  }
  var width = value;
  width = Math.min(width, this.textMaxWidth);
  width = Math.max(width, this.textMinWidth);
  if (width > this.textMinWidth) {
    $(this.textContainer).addClass("open");
    this.textContainer.style.setProperty("width", width + "px");
    if (netacad) {
      netacad.settings.set(netacad.settings.TEXTWIDTH_KEY, width);
    }
  } else {
    this.textContainer.style.removeProperty("width");
    $(this.textContainer).removeClass("open");
    if (netacad) {
      netacad.settings.remove(netacad.settings.TEXTWIDTH_KEY);
    }
  }
};

var Highlighter = new function() {

  function Mark(index, lastIndex) {
    this.index = Math.min(index, lastIndex);
    this.lastIndex = Math.max(index, lastIndex);
  }

  Mark.prototype.overlapsWith = function(mark) {
    return (
      (this.index <= mark.index && mark.index <= this.lastIndex) ||
      (this.index <= mark.lastIndex && mark.lastIndex <= this.lastIndex)
    );
  };

  Mark.prototype.compareWith = function(mark) {
    if (this.index < mark.index) {
      return -1;
    }
    if (this.index > mark.index) {
      return 1;
    }
    return 0;
  };

  function Marks() {
    this.list = [];
  }

  Marks.prototype.add = function(newMark) {
    var overlaps = this.getOverlaps(newMark);
    while (overlaps.length) {
      var mark = overlaps.pop();
      newMark.index = Math.min(mark.index, newMark.index);
      newMark.lastIndex = Math.max(mark.lastIndex, newMark.lastIndex);
      this.remove(mark);
    }
    this.list.push(newMark);
  };

  Marks.prototype.getOverlaps = function(newMark) {
    var overlaps = [];
    this.each(function(mark) {
      if (newMark.overlapsWith(mark)) {
        overlaps.push(mark);
      }
    });
    return overlaps;
  };

  Marks.prototype.remove = function(mark) {
    var index = this.list.indexOf(mark);
    if (index >= 0) {
      this.list.splice(index, 1);
    }
  };

  Marks.prototype.each = function(callback) {
    for (var i = 0; i < this.list.length; i++) {
      callback(this.list[i]);
    }
  };

  Marks.prototype.sort = function() {
    this.list.sort(function(a, b) {
      return a.compareWith(b);
    });
  };

  function initialize() {
    var terms = getSearchTerms(window.location.search.substring(1));
    if (!terms.length) {
      return;
    }
    var nodes = getTextNodes(document.getElementById("text-container"));
    while (nodes.length) {
      highlight(terms, nodes.pop());
    }
  }

  function getSearchTerms(search) {
    var terms = [];
    var pairs = search.split("&");
    while (pairs.length) {
      var pair = pairs.shift().split("=");
      var key = "";
      var value = "";
      if (pair.length > 0) {
        key = decodeURIComponent(pair[0].replace(/\+/g, "%20"));
      }
      if (pair.length > 1) {
        value = decodeURIComponent(pair[1].replace(/\+/g, "%20")).trim();
      }
      if (key == "q" && value.length) {
        terms = terms.concat(value.split(/\s+/));
      }
    }
    return terms;
  }

  function isValidTextNode(node) {
    return (
      node instanceof Node &&
      node.nodeType == 3 &&
      node.parentNode
    );
  }

  function isValidElement(node) {
    return (
      node instanceof Node &&
      node.nodeType == 1 &&
      node.hasChildNodes() &&
      node.nodeName.toLowerCase() != "style" &&
      node.nodeName.toLowerCase() != "script"
    );
  }

  function getTextNodes(node) {
    var list = [];
    if (isValidTextNode(node)) {
      list.push(node);
    } else if (isValidElement(node)) {
      var child = node.firstChild;
      while (child) {
        list = list.concat(getTextNodes(child));
        child = child.nextSibling;
      }
    }
    return list;
  }

  function escapeRegExp(s){
    return s.replace(/([.*+?^${}()|\[\]\/\\])/g, "\\$1");
  }

  function highlight(terms, node) {
    var marks = new Marks();
    var text = node.nodeValue;
    for (var i = 0; i < terms.length; i++) {
      var result;
      var regex = new RegExp(escapeRegExp(terms[i]), "gi");
      while ((result = regex.exec(text)) !== null) {
        marks.add(new Mark(result.index, regex.lastIndex));
      }
    }
    marks.sort();
    var cursor = 0;
    var fragment = document.createDocumentFragment();
    marks.each(function(mark) {
      if (cursor < mark.index) {
        fragment.appendChild(document.createTextNode(text.slice(cursor, mark.index)));
      }
      var span = document.createElement("span");
      span.setAttribute("class", "highlight");
      span.appendChild(document.createTextNode(text.slice(mark.index, mark.lastIndex)));
      fragment.appendChild(span);
      cursor = mark.lastIndex;
    });
    if (cursor > 0) {
      if (cursor < text.length) {
        fragment.appendChild(document.createTextNode(text.slice(cursor)));
      }
      node.parentNode.replaceChild(fragment, node);
    }
  }

  window.addEventListener("DOMContentLoaded", initialize, false);

}();

window.onload = function() {
  permission.check(function(success) {
    if (success) {
      var page = new Page(document.documentElement);
      var frame = document.getElementById("media");
      if (netacad && netacad.settings.get(netacad.settings.TRANSCRIPT_KEY)) {
        $(document.documentElement).addClass('transcript');
      } else {
        frame.setAttribute('src', 'media/index.html');
      }
    } else {
      var login = document.getElementById('login');
      while (document.body.hasChildNodes()) {
        document.body.removeChild(document.body.lastChild);
      }
      document.body.appendChild(login);
      $(document.documentElement).addClass('denied');
    }
  });
};

window.addEventListener('load', function() {
  $(document.documentElement).removeClass('loading');
});

window.addEventListener('DOMContentLoaded', function() {
  if (window.parent !== window) {
    var iframe = window.parent.document.getElementById('file_content');
    if (iframe) {
      if (media_transcript_file) {
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
          if (request.readyState === 4) {
            if (request.status === 200) {
              var div = document.createElement('div');
              div.setAttribute('id', 'mediaframedesc');
              div.setAttribute('class', 'screenreader-only');
              div.innerHTML = request.responseText;
              iframe.parentNode.insertBefore(div, iframe.nextSibling);
              iframe.setAttribute('aria-describedby', 'mediaframedesc');
            }
          }
        }
        request.open('GET', media_transcript_file, true);
        request.send();
      }
      iframe.style.height = '490px';
      iframe.style.minHeight = '490px';
    }
  }
});
function inIframe() {
    try {
        return window.self !== window.top;
    } catch (e) {
        return true;
    }
}
function mediaReady(media) {
  var active = null;
  var slide = media.getSlide();
  var length = media.getSlideCount();
  if (length > 1 && inIframe()==false) {
    var footer = document.createElement('div');
    footer.setAttribute('id', 'page-footer');
    var fieldset = document.createElement('fieldset');
    fieldset.setAttribute('id', 'page-slide-buttons');
    var legend = document.createElement('legend');
    legend.appendChild(document.createTextNode('Figures'));
    fieldset.appendChild(legend);
    var list = document.createElement('ol');
    for (var i = 1; i <= length; i++) {
      var item = document.createElement('li');
      var button = document.createElement('button');
      button.setAttribute('title', 'Figure ' + i);
      button.setAttribute('value', i);
      button.addEventListener('click', function(event) {
        var index = parseInt(event.target.value);
        media.setSlide(index);
        active.removeAttribute('class');
        active = event.target;
        active.setAttribute('class', 'active');
      }, false);
      if (slide == i) {
        button.setAttribute('class', 'active');
        active = button;
      }
      button.appendChild(document.createTextNode(i));
      item.appendChild(button);
      list.appendChild(item);
    }
    fieldset.appendChild(list);
    footer.appendChild(fieldset);
    document.body.appendChild(footer);
    if (window.parent !== window) {
      var iframe = window.parent.document.getElementById('file_content');
      if (iframe) {
        iframe.style.height = '544px';
        iframe.style.minHeight = '544px';
      }
    }
  }
}

