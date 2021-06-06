/**
 * Namespace for the NetAcad library.
 */
var netacad = new function() {

  if (!window || !Object || !Object.create) {
    throw new Error("unsupported");
  }

  function getObjectByName(name) {
    var current = window;
    var parts = name.split('.');
    for (var part; part = parts.shift();) {
      if (current[part]) {
        current = current[part];
      } else {
        return null;
      }
    }
    if (current === window) {
      return null;
    }
    return current;
  }

  this.provide = function(name) {
    if (getObjectByName(name)) {
      throw new Error('"' + name + '" already provided.');
    }
    var current = window;
    var parts = name.split('.');
    for (var part; part = parts.shift();) {
      current[part] = current[part] || {};
      current = current[part];
    }
  };

  this.extend = function(Subclass, Superclass) {
    Subclass.prototype = Object.create(Superclass.prototype || Superclass, {
      constructor: {
        value: Subclass,
        writable: true,
        configurable: true,
        enumerable: false
      }
    });
  };

  this.merge = function() {
    var result = {};
    for (var i = 0; i < arguments.length; i++) {
      var source = Object(arguments[i]);
      var keys = Object.keys(source);
      while (keys.length) {
        var key = keys.shift();
        var desc = Object.getOwnPropertyDescriptor(source, key);
        if (desc !== undefined && desc.enumerable) {
          result[key] = source[key];
        }
      }
    }
    return result;
  };

}();


/**
 * netacad.console
 */
netacad.console = new function() {
  this.log = function(message) {
    var list = document.getElementById("console");
    var item = document.createElement("li");
    item.appendChild(document.createTextNode(message));
    list.appendChild(item);
    list.scrollTop = list.scrollHeight - list.clientHeight;
  };
}();


/**
 * netacad.environment
 */
netacad.environment = new function() {
  var prod = (window.location.hostname == "static-course-assets.s3.amazonaws.com");
  var trunk = (window.location.pathname.indexOf("/trunk/") >= 0);
  this.isProd = function() {
    return prod;
  };
  this.hasTrunk = function() {
    return trunk;
  };
}();


/**
 * Namespace for DOM related utilities.
 */
netacad.provide("netacad.dom");

netacad.dom.empty = function(node) {
  while (node.hasChildNodes()) {
    node.removeChild(node.lastChild);
  }
  return node;
};


/**
 * netacad.events
 */
netacad.provide("netacad.events");


/**
 * netacad.events.createEvent
 */
netacad.events.createEvent = function(type) {
  var event = document.createEvent("Event");
  event.initEvent(type, true, true);
  return event;
};


/**
 * netacad.events.EventDispatcher
 * @constructor
 */
netacad.events.EventDispatcher = function() {
  this.listeners = {};
};

netacad.events.EventDispatcher.prototype.addEventListener = function(type, listener) {
  if (!type || !listener) {
    return;
  }
  this.removeEventListener(type, listener);
  if (!(type in this.listeners)) {
    this.listeners[type] = [];
  }
  this.listeners[type].push(listener);
};

netacad.events.EventDispatcher.prototype.removeEventListener = function(type, listener) {
  if (!type || !listener || !(type in this.listeners)) {
    return;
  }
  var listeners = this.listeners[type];
  var index = listeners.indexOf(listener);
  if (index >= 0) {
    listeners.splice(index, 1);
  }
  if (listeners.length == 0) {
    delete listeners[type];
  }
};

netacad.events.EventDispatcher.prototype.dispatchEvent = function(event) {
  if (!event || !event.type || !(event.type in this.listeners)) {
    return;
  }
  var listeners = this.listeners[event.type];
  for (var i = 0; i < listeners.length; i++) {
    var listener = listeners[i];
    if (listener instanceof Function) {
      listener.call(this);
    } else if (listener.handleEvent) {
      listener.handleEvent(event);
    }
  }
};


/**
 * netacad.lang
 */
netacad.lang = new function() {

  var map = {};

  this.set = function(name, value) {
    map[name] = value;
  };

  this.get = function(name) {
    return map[name] || "";
  };

  this.has = function(name) {
    return !!map[name];
  };

}();


/**
 * Namespace for networking related utilities.
 */
netacad.provide("netacad.net");


/**
 * netacad.net.URL
 * @constructor
 * @param {string} url The URL string.
 */
netacad.net.URL = function(url) {

  this.components = netacad.net.URL.regex.exec(url);

  this.scheme = this.components[2];
  this.authority = this.components[4];
  this.path = this.components[5];
  this.query = this.components[7];
  this.fragment = this.components[9];

  this.parameters = {};
  if (this.query) {
    var pairs = this.query.split('&');
    for (var i = 0; i < pairs.length; i++) {
      var pair = pairs[i].split('=');
      var name = decodeURIComponent(pair[0]);
      var value = (pair.length > 1)? decodeURIComponent(pair[1]): null;
      this.parameters[name] = value;
    }
  }

};


/**
 * From RFC 3986 appendix B
 * @const
 */
netacad.net.URL.regex = /^(([^:\/?#]+):)?(\/\/([^\/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?/;
//                        12             3    4           5       6  7        8 9


/**
 * @param {boolean} include_query Flag to include query or not.
 * @param {boolean} include_fragment Flag to include fragment or not.
 * @return {string} The recomposed URL.
 */
netacad.net.URL.prototype.recompose = function(include_query, include_fragment) {
  var result = '';
  if (this.components[1]) {
    result += this.scheme;
    result += ':';
  }
  if (this.components[3]) {
    result += '//';
    result += this.authority;
  }
  if (this.components[5]) {
    result += this.path;
  }
  if (this.components[6] && include_query) {
    result += '?';
    result += this.query;
  }
  if (this.components[8] && include_fragment) {
    result += '#';
    result += this.fragment;
  }
  return result;
};


/**
 * @param {string} name The query name.
 * @return {string} The value associated with the query name.
 */
netacad.net.URL.prototype.get = function(name) {
  return this.parameters[name];
};


/**
 * @param {string} name The query name.
 * @return {boolean} Returns true if the URL has the named parameter.
 */
netacad.net.URL.prototype.contains = function(name) {
  return (name in this.parameters);
};


/**
 * netacad.config
 */
netacad.config = {};

/**
 * netacad.configLoader
 */
netacad.configLoader = function(callback) {
  var url = '../netacad.config.json';
  if (netacad.environment.hasTrunk()) {
    url = '../' + url;
  }
  var request = new XMLHttpRequest();
  try {
    request.onreadystatechange = function() {
      if (request.readyState == 4) {
        if (request.status == 200) {
          try {
            var config = JSON.parse(request.responseText);
            netacad.config = netacad.merge(netacad.config, config);
          } catch (e) {
            console.warn("unable to parse " + url);
          } finally {
            callback();
          }
        } else {
          callback();
        }
      }
    };
    request.open("GET", url, true);
    request.send();
  } catch (e) {
    callback();
  }
};


/**
 * netacad.settings
 * TODO: listen to storage events and dispatch change events
 */
netacad.settings = new function() {

  var prefix = "";

  this.BACKGROUND_KEY = "background";
  this.BOOKMARKS_KEY = "bookmarks";
  this.RECENT_KEY = "recent";
  this.RETURN_KEY = "return";
  this.TRANSCRIPT_KEY = "transcript";
  this.TEXTWIDTH_KEY = "textwidth";

  this.DEVELOPER_KEY = "developer";
  this.DEVELOPER_PSEUDOLOCALIZATION_KEY = "developer/pseudolocalization";

  this.get = function(name) {
    var key = prefix + "/" + name;
    try {
      return JSON.parse(localStorage.getItem(key));
    } catch (error) {
      console.warn("unable to get local storage");
    }
    return null;
  };

  this.set = function(name, value) {
    var key = prefix + "/" + name;
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.warn("unable to set local storage");
    }
  };

  this.remove = function(name) {
    var key = prefix + "/" + name;
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.warn("unable to remove local storage");
    }
  };

  this.clear = function() {
    var keys = [];
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (key.indexOf(prefix + "/") == 0) {
          keys.push(key);
        }
      }
      while (keys.length) {
        var key = keys.pop();
        localStorage.removeItem(key);
      }
    } catch (error) {
      console.warn("unable to clear local storage");
    }
  };
  
  this.init = function(id) {

    prefix = id;

    var queryKeys = {};
    queryKeys["dev"] = this.DEVELOPER_KEY;
    queryKeys["bg"] = this.BACKGROUND_KEY;
    queryKeys["r"] = this.RETURN_KEY;

    var url = new netacad.net.URL(window.location.href);
    if (url.query) {
      for (var queryKey in queryKeys) {
        if (url.contains(queryKey)) {
          var storageKey = queryKeys[queryKey];
          var storageValue = url.get(queryKey);
          if (queryKey == "dev") {
            storageValue = (storageValue == "true");
          }
          this.set(storageKey, storageValue);
        }
      }
      window.location.replace(url.recompose(false, true));
    }

  };

}();


/**
 * netacad.search
 * TODO: search by TI
 */
netacad.provide("netacad.search");

/**
 * TODO: international word boundaries
 * Unicode Standard Annex #29
 * Unicode Text Segmentation
 * Word Boundary Rules
 * <http://www.unicode.org/reports/tr29/#Word_Boundaries>
 */
netacad.search.getWords = function(text) {
  // 2000 - 206F General Punctuation
  // 0000 - 001F C0 Controls and Basic Latin: C0 controls
  // 0020 - 002F C0 Controls and Basic Latin: ASCII Punctuation and symbols
  // 003A - 0040 C0 Controls and Basic Latin: ASCII Punctuation and symbols
  // 005B - 0060 C0 Controls and Basic Latin: ASCII Punctuation and symbols
  // 007B - 007E C0 Controls and Basic Latin: ASCII Punctuation and symbols
  // 007F        C0 Controls and Basic Latin: Control character
  // 0080 - 009F C1 Controls and Latin-1 Supplement: C1 controls
  // 00A0 - 00BF C1 Controls and Latin-1 Supplement: Latin-1 punctuation and symbols
  // FE50 - FE6F Small Form Variants
  // 2E00 - 2E7F Supplemental Punctuation
  text = text.toLowerCase();
  text = text.replace(/[\u2000-\u206F,\u0000-\u001F,\u0020-\u002F,\u003A-\u0040,\u005B-\u0060,\u007B-\u007E,\u007F,\u0080-\u009F,\u00A0-\u00BF,\uFE50-\uFE6F,\u2E00-\u2E7F]/g, " ");
  text = text.trim();
  return text.split(/\s+/);
};

netacad.search.intersect = function(a, b){
  var result = [];
  for (var i = 0; i < a.length; i++) {
      for (var j = 0; j < b.length; j++) {
          if (a[i] == b[j]) {
              result.push(a[i]);
              break;
          }
      }
  }
  return result;
};


/**
 * netacad.search.SearchEngine
 */
netacad.search.SearchEngine = function(url) {
  this.url = url;
  this.list = [];
  this.map = {};
};

netacad.search.SearchEngine.prototype.index = function(id, text) {
  var index = list.indexOf(id);
  if (index < 0) {
    index = this.list.push(id) - 1;
  }
  var words = netacad.search.getWords(text);
  for (var i = 0; i < words.length; i++) {
    var word = words[i];
    if (word) {
      if (!this.map[word]) {
        this.map[word] = [];
      }
      if (this.map[word].indexOf(index) < 0) {
        this.map[word].push(index);
      }
    }
  }
};

netacad.search.SearchEngine.prototype.toJSON = function() {
  return JSON.stringify({list: this.list, map: this.map});
};

netacad.search.SearchEngine.prototype.fromJSON = function(s) {
  var o = null;
  try {
    o = JSON.parse(s);
  } catch (error) {
    console.warn("unable to parse");
  }
  if (o && o.list && o.map) {
    this.list = o.list;
    this.map = o.map;
  }
};

netacad.search.SearchEngine.prototype.load = function(callback) {
  var that = this;
  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      if (request.status == 200) {
        that.fromJSON(request.responseText);
      }
      callback();
    }
  };
  request.open("GET", this.url, true);
  request.send();
};

netacad.search.SearchEngine.prototype.listWords = function() {
  var result = [];
  for (var word in this.map) {
    result.push(word);
  }
  return result.sort();
};

netacad.search.SearchEngine.prototype.find = function(words) {
  var result = null;
  for (var i = 0; i < words.length; i++) {
    var word = words[i];
    if (word) {
      if (this.map[word]) {
        if (result) {
          result = netacad.search.intersect(result, this.map[word]);
        } else {
          result = this.map[word];
        }
      } else {
        result = [];
        break;
      }
    }
  }
  return result || [];
};


/**
 * netacad.models
 */
netacad.provide("netacad.models");


/**
 * netacad.models.Item
 * @constructor
 */
netacad.models.Item = function(li, title) {
  netacad.events.EventDispatcher.call(this);
  this.li = li;
  this.title = title;
  this.parent = null;
  this.children = [];
  this.firstChild = null;
  this.lastChild = null;
  this.previousSibling = null;
  this.nextSibling = null;
  this.type = "Item";
  if (this.li) {
    netacad.models.Item.map[this.li] = this;
  }
};

netacad.models.Item.map = {};
netacad.extend(netacad.models.Item, netacad.events.EventDispatcher);

netacad.models.Item.prototype.toString = function() {
  return this.li + " " + this.title;
};

netacad.models.Item.prototype.appendChild = function(child) {
  if (!this.firstChild) {
    this.firstChild = child;
  }
  this.children.push(child);
  child.parent = this;
  if (this.lastChild) {
    this.lastChild.nextSibling = child;
    child.previousSibling = this.lastChild;
  }
  this.lastChild = child;
};

netacad.models.Item.prototype.getFirst = function(item) {
  if (item.firstChild) {
    return this.getFirst(item.firstChild);
  }
  return item;
};

netacad.models.Item.prototype.getLast = function(item) {
  if (item.lastChild) {
    return this.getLast(item.lastChild);
  }
  return item;
};


/**
 * netacad.models.Course
 * @constructor
 * 
 * TODO: add Recent Pages and Bookmarks to the model
 * 
 */
netacad.models.Course = function(li, lang, title) {
  netacad.models.Item.call(this, li, title);
  this.lang = lang;
  this.type = "Course";
  this.current = null;
  this.search = null;
  window.addEventListener("hashchange", this);
};

netacad.extend(netacad.models.Course, netacad.models.Item);

netacad.models.Course.prototype.handleEvent = function(event) {
  if (event.type == "hashchange") {
    this.update();
  }
};

netacad.models.Course.prototype.update = function() {
  var hash = window.location.hash.substring(1); // remove "#"
  if (hash) {
    var item = netacad.models.Item.map[hash];
    if (item && item != this.current) {
      this.setCurrent(item);
    }
  }
};

netacad.models.Course.prototype.appendChild = function(child) {
  if (child instanceof netacad.models.Module) {
    netacad.models.Item.prototype.appendChild.call(this, child);
  }
};

netacad.models.Course.prototype.getCurrent = function() {
  return this.current;
};

netacad.models.Course.prototype.setCurrent = function(item, search) {
  this.current = item;
  this.search = search;
  window.location.hash = this.current? this.current.li: "";
  this.dispatchEvent(netacad.events.createEvent("change"));
};

netacad.models.Course.prototype.getFirst = function(item) {
  if (item.firstChild) {
    return this.getFirst(item.firstChild);
  }
  return item;
};

netacad.models.Course.prototype.getLast = function(item) {
  if (item.lastChild) {
    return this.getLast(item.lastChild);
  }
  return item;
};

netacad.models.Course.prototype.getNext = function(item) {
  if (item == null) {
    return null;
  }
  if (item.nextSibling) {
    return this.getFirst(item.nextSibling);
  } else {
    return this.getNext(item.parent);
  }
};

netacad.models.Course.prototype.getPrevious = function(item) {
  if (item == null) {
    return null;
  }
  if (item.previousSibling) {
    return this.getLast(item.previousSibling);
  } else {
    return this.getPrevious(item.parent);
  }
};


/**
 * netacad.models.Module
 * @constructor
 */
netacad.models.Module = function(li, title) {
  netacad.models.Item.call(this, li, title);
  this.type = "Module";
};

netacad.extend(netacad.models.Module, netacad.models.Item);

netacad.models.Module.prototype.appendChild = function(child) {
  if (child instanceof netacad.models.Section) {
    netacad.models.Item.prototype.appendChild.call(this, child);
  }
};


/**
 * netacad.models.Section
 * @constructor
 */
netacad.models.Section = function(li, title) {
  netacad.models.Item.call(this, li, title);
  this.type = "Section";
};

netacad.extend(netacad.models.Section, netacad.models.Item);

netacad.models.Section.prototype.appendChild = function(child) {
  if (child instanceof netacad.models.Topic) {
    netacad.models.Item.prototype.appendChild.call(this, child);
  }
};


/**
 * netacad.models.Topic
 * @constructor
 */
netacad.models.Topic = function(li, title) {
  netacad.models.Item.call(this, li, title);
  this.type = "Topic";
};

netacad.extend(netacad.models.Topic, netacad.models.Item);

netacad.models.Topic.prototype.appendChild = function(child) {
  if (child instanceof netacad.models.Page) {
    netacad.models.Item.prototype.appendChild.call(this, child);
  }
};


/**
 * netacad.models.Page
 * @constructor
 */
netacad.models.Page = function(li, title, pageType, activityType, activitySubtype) {
  netacad.models.Item.call(this, li, title);
  this.type = "Page";
  this.pageType = pageType;
  this.activityType = activityType;
  this.activitySubtype = activitySubtype;
  this.url = null;
  if (this.li) {
    this.url = "course/module" + this.li.split(".")[0] + "/" + this.li + "/" + this.li + ".html";
  }
};

netacad.extend(netacad.models.Page, netacad.models.Item);

netacad.models.Page.prototype.appendChild = function(child) {
  // netacad.models.Item.prototype.appendChild.call(this, child);
};


/**
 * netacad.models.Background
 * @constructor
 */
netacad.models.Background = function() {
  netacad.events.EventDispatcher.call(this);
  this.current = null;
  this.setBackground(netacad.settings.get(netacad.settings.BACKGROUND_KEY));
};

netacad.extend(netacad.models.Background, netacad.events.EventDispatcher);

netacad.models.Background.prototype.backgrounds = [

  "bg-0",
  "bg-1",
  "bg-2",
  "bg-3",

  "bg-4",
  "bg-5",
  "bg-6",
  "bg-7",

  "bg-8",
  "bg-9",
  "bg-10",
  "bg-11"

];

netacad.models.Background.prototype.setBackground = function(ident) {
  if (ident && this.current != ident) {
    var index = this.backgrounds.indexOf(ident);
    if (index >= 0) {
      this.current = this.backgrounds[index];
      netacad.settings.set(netacad.settings.BACKGROUND_KEY, this.current);
      this.dispatchEvent(netacad.events.createEvent("change"));
    } else {
      console.warn("invalid background identifier");
    }
  }
};

netacad.models.Background.prototype.getBackground = function() {
  return this.current;
};

netacad.models.Background.prototype.getBackgrounds = function() {
  return this.backgrounds;
};


/**
 * netacad.models.DeveloperTools
 * @constructor
 */
netacad.models.DeveloperTools = function() {
  netacad.events.EventDispatcher.call(this);
  if (!netacad.settings.get(netacad.settings.DEVELOPER_KEY)) {
    netacad.settings.remove(netacad.settings.DEVELOPER_PSEUDOLOCALIZATION_KEY);
    netacad.settings.remove(netacad.settings.DEVELOPER_KEY);
  }
};

netacad.extend(netacad.models.DeveloperTools, netacad.events.EventDispatcher);

netacad.models.DeveloperTools.prototype.disable = function() {
  netacad.settings.remove(netacad.settings.DEVELOPER_PSEUDOLOCALIZATION_KEY);
  netacad.settings.remove(netacad.settings.DEVELOPER_KEY);
  window.location.reload();
};

netacad.models.DeveloperTools.prototype.clearLocalStorage = function() {
  netacad.settings.clear();
  var url = new netacad.net.URL(window.location.href);
  window.location.replace(url.recompose(false, false));
};

netacad.models.DeveloperTools.prototype.clearBackground = function() {
  netacad.settings.remove(netacad.settings.BACKGROUND_KEY);
  var url = new netacad.net.URL(window.location.href);
  window.location.replace(url.recompose(false, false));
};

netacad.models.DeveloperTools.prototype.setPseudolocalization = function(value) {
  if (netacad.settings.get(netacad.settings.DEVELOPER_PSEUDOLOCALIZATION_KEY) != value) {
    netacad.settings.set(netacad.settings.DEVELOPER_PSEUDOLOCALIZATION_KEY, value);
    window.location.reload();
  }
};

netacad.models.DeveloperTools.prototype.getPseudolocalization = function() {
  return !!netacad.settings.get(netacad.settings.DEVELOPER_PSEUDOLOCALIZATION_KEY);
};


/**
 * netacad.views
 */
netacad.provide("netacad.views");


/**
 * netacad.views.View
 * @constructor
 */
netacad.views.View = function(model, element) {
  this.model = model;
  this.element = element;
  if (this.element) {
    this.document = this.element.ownerDocument;
  }
  if (this.document) {
    this.view = this.document.defaultView;
  }
};

/** @abstract */
netacad.views.View.prototype.build = function() {
  throw new Error("abstract method not implemented");
};

/** @abstract */
netacad.views.View.prototype.destroy = function() {
  throw new Error("abstract method not implemented");
};

netacad.views.View.prototype.buildItemList = function(items, message) {
  // <ul class="items">...</ul> 
  var ul = this.document.createElement("ul");
  ul.setAttribute("class", "items");
  if (items && items.length) {
    var fragment = document.createDocumentFragment();
    for (var i = 0; i < items.length; i++) {
      var item = netacad.models.Item.map[items[i]] || items[i]; // TODO: a bit tenuous
      if (item) {
        /*
         * <li>
         *   <a href="#{item.li}>
         *     <div class="item-header">{type} {item.li}</div>
         *     <div class="item-title">{item.title}</div>
         *   </a>
         * </li>
         */
        var li = this.document.createElement("li");
        var anchor = netacad.components.Gestures.enable(this.document.createElement("a"));
        anchor.addEventListener("click", this);
        anchor.addEventListener("dblclick", this);
        anchor.addEventListener("tap", this);
        anchor.addEventListener("double-tap", this);
        anchor.setAttribute("href", "#" + item.li);
        anchor.setAttribute("class", item.type);
        if (item instanceof netacad.models.Page) {
          var thumb = this.document.createElement("img");
          thumb.setAttribute("class", "item-thumb");
          thumb.setAttribute("src", "course/module" + item.li.split(".")[0] + "/" + item.li + "/media/media_" + item.li + "_thumb.jpg");
          thumb.setAttribute("alt", netacad.lang.get("PageThumbnail").replace("#", item.li));
          thumb.setAttribute("aria-hidden", "true");
          anchor.appendChild(thumb);
        }
        var header = this.document.createElement("div");
        header.setAttribute("class", "item-header");
        header.appendChild(this.document.createTextNode(netacad.lang.get(item.type).replace("#", item.li)));
        anchor.appendChild(header);
        var title = this.document.createElement("div");
        title.setAttribute("class", "item-title");
        title.appendChild(this.document.createTextNode(item.title));
        anchor.appendChild(title);
        li.appendChild(anchor);
        fragment.appendChild(li);
      }
    }
    ul.appendChild(fragment);
  } else if (message) {
    var li = this.document.createElement("li");
    li.setAttribute("class", "message");
    li.appendChild(this.document.createTextNode(message));
    ul.appendChild(li);
  }
  return ul;
};

netacad.views.View.prototype.destroyItemList = function(list) {
  if (list && list.querySelectorAll) {
    var anchors = list.querySelectorAll("a");
    for (var i = 0; i < anchors.length; i++) {
      var anchor = anchors[i];
      anchor.removeEventListener("click", this);
      anchor.removeEventListener("dblclick", this);
      anchor.removeEventListener("tap", this);
      anchor.removeEventListener("double-tap", this);
    }
    if (list.parentNode) {
      list.parentNode.removeChild(list);
    }
  }
};


/**
 * netacad.views.ContentView
 * @constructor
 */
netacad.views.ContentView = function(model, element) {

  netacad.views.View.call(this, model, element);

  var width = 1024;
  var height = 768;
  
  var top = 65;
  var right = 10;
  var bottom = 101;
  var left = 10;

  var border = 2;
  var header = 54;
  var footer = 54;

  this.outerWidthOffset = left + right;
  this.outerHeightOffset = top + bottom;
  this.innerWidthOffset = border + border;
  this.innerHeightOffset = border + header + footer + border;
  
  this.minWidth = width - this.outerWidthOffset; // 1004
  this.minHeight = height - this.outerHeightOffset; // 602
  this.ratioWidth = left / this.outerWidthOffset;
  this.ratioHeight = top / this.outerHeightOffset;
  this.ratio = (this.minWidth - this.innerWidthOffset) / (this.minHeight - this.innerHeightOffset); // 1000 / 490

  this.document.body.style.setProperty("min-width", this.minWidth + "px");
  this.document.body.style.setProperty("min-height", this.minHeight + "px");
  this.view.addEventListener("load", this);
  this.view.addEventListener("resize", this);

  // adjust map, too
  this.map = this.document.getElementById("map");

  this.update();

};

netacad.extend(netacad.views.ContentView, netacad.views.View);

netacad.views.ContentView.prototype.handleEvent = function(event) {
  if (event.type == "load" || event.type == "resize") {
    this.update();
  }
};

netacad.views.ContentView.prototype.update = function() {

  var isRTL = this.document.documentElement.getAttribute("dir") == "rtl";

  // get available size
  this.document.documentElement.style.setProperty("overflow", "hidden"); // without scrollbars
  var width = this.document.documentElement.clientWidth - (this.outerWidthOffset + this.innerWidthOffset);
  var height = this.document.documentElement.clientHeight - (this.outerHeightOffset + this.innerHeightOffset);

  // constrain to aspect ratio
  if ((width / height) > this.ratio) {
    width = Math.round(height * this.ratio);
  } else {
    height = Math.round(width / this.ratio);
  }

  // constrain to minimum size
  width = Math.max(width, this.minWidth - this.innerWidthOffset);
  height = Math.max(height, this.minHeight - this.innerHeightOffset);

  width = width + this.innerWidthOffset;
  height = height + this.innerHeightOffset;

  // set position
  var x = Math.round((this.document.documentElement.clientWidth - width) * this.ratioWidth);
  var y = Math.round((this.document.documentElement.clientHeight - height) * this.ratioHeight);
  this.document.documentElement.style.removeProperty("overflow"); // allow scrolling again

  // apply position and size
  this.element.style.setProperty("position", "absolute");
  if (isRTL) {
    this.element.style.removeProperty("left");
    this.element.style.setProperty("right", Math.max(x, 0) + "px");
  } else {
    this.element.style.removeProperty("right");
    this.element.style.setProperty("left", Math.max(x, 0) + "px");
  }
  this.element.style.setProperty("top", Math.max(y, 0) + "px");
  this.element.style.setProperty("width", Math.max(width, 0) + "px");
  this.element.style.setProperty("height", Math.max(height, 0) + "px");

  // adjust map, too
  this.map.style.removeProperty("top");
  this.map.style.removeProperty("height");
  this.map.style.setProperty("position", "absolute");
  if (isRTL) {
    this.map.style.removeProperty("left");
    this.map.style.setProperty("right", Math.max(x, 0) + "px");
  } else {
    this.map.style.removeProperty("right");
    this.map.style.setProperty("left", Math.max(x, 0) + "px");
  }
  this.map.style.setProperty("width", Math.max(width, 0) + "px");
  if (this.map.clientHeight > this.minHeight) {
    this.map.style.setProperty("top", Math.max(y, 0) + "px");
    this.map.style.setProperty("height", Math.max(height, 0) + "px");
  }

};


/**
 * netacad.views.CourseMapView
 * @constructor
 * @augments View
 */
netacad.views.CourseMapView = function(model, element) {

  netacad.views.View.call(this, model, element);

  this.modulesMap = this.document.getElementById("map-modules");
  this.sectionsMap = this.document.getElementById("map-sections");
  this.topicsMap = this.document.getElementById("map-topics");
  this.pagesMap = this.document.getElementById("map-pages");

  this.modulesScrollPane = new netacad.components.ScrollPane(this.modulesMap.querySelector(".scroll-pane"));
  this.sectionsScrollPane = new netacad.components.ScrollPane(this.sectionsMap.querySelector(".scroll-pane"));
  this.topicsScrollPane = new netacad.components.ScrollPane(this.topicsMap.querySelector(".scroll-pane"));
  this.pagesScrollPane = new netacad.components.ScrollPane(this.pagesMap.querySelector(".scroll-pane"));
  
  this.modulesContent = this.modulesScrollPane.content;
  this.sectionsContent = this.sectionsScrollPane.content;
  this.topicsContent = this.topicsScrollPane.content;
  this.pagesContent = this.pagesScrollPane.content;

  this.currentCourse = null;
  this.currentModule = null;
  this.currentSection = null;
  this.currentTopic = null;
  this.currentPage = null;

  this.model.addEventListener("change", this);
  this.build();
  this.update();

};

netacad.extend(netacad.views.CourseMapView, netacad.views.View);

netacad.views.CourseMapView.prototype.build = function() {
  this.buildModulesMap(this.model);
  this.destroySectionsMap();
  this.destroyTopicsMap();
  this.destroyPagesMap();
};

netacad.views.CourseMapView.prototype.buildModulesMap = function(course) {
  if (course == this.currentCourse) {
    return;
  }
  this.modulesMap.setAttribute("aria-busy", true);
  this.destroyModulesMap();
  this.modulesContent.appendChild(this.buildModulesList(course.children));
  this.modulesScrollPane.reset();
  this.currentCourse = course;
  this.modulesMap.removeAttribute("aria-busy");
};

netacad.views.CourseMapView.prototype.destroyModulesMap = function() {
  this.destroy(this.modulesContent);
  this.modulesScrollPane.reset();
  this.currentModule = null;
};

netacad.views.CourseMapView.prototype.buildModulesList = function(modules) {
  return this.buildItemList(modules);
};

netacad.views.CourseMapView.prototype.buildSectionsMap = function(module) {
  if (module == this.currentModule) {
    return;
  }
  this.sectionsMap.setAttribute("aria-busy", true);
  this.destroySectionsMap();
  this.sectionsContent.appendChild(this.buildSectionsList(module.children));
  this.sectionsScrollPane.reset();
  this.currentModule = module;
  this.sectionsMap.removeAttribute("aria-busy");
};

netacad.views.CourseMapView.prototype.destroySectionsMap = function() {
  this.destroy(this.sectionsContent);
  this.sectionsScrollPane.reset();
  this.currentModule = null;
};

netacad.views.CourseMapView.prototype.buildSectionsList = function(sections) {
  return this.buildItemList(sections);
};

netacad.views.CourseMapView.prototype.buildTopicsMap = function(section) {
  if (section == this.currentSection) {
    return;
  }
  this.topicsMap.setAttribute("aria-busy", true);
  this.destroyTopicsMap();
  this.topicsContent.appendChild(this.buildTopicsList(section.children));
  this.topicsScrollPane.reset();
  this.currentSection = section;
  this.topicsMap.removeAttribute("aria-busy");
};

netacad.views.CourseMapView.prototype.destroyTopicsMap = function() {
  this.destroy(this.topicsContent);
  this.topicsScrollPane.reset();
  this.currentSection = null;
};

netacad.views.CourseMapView.prototype.buildTopicsList = function(topics) {
  return this.buildItemList(topics);
};

netacad.views.CourseMapView.prototype.buildPagesMap = function(topic) {
  if (topic == this.currentTopic) {
    return;
  }
  this.pagesMap.setAttribute("aria-busy", true);
  this.destroyPagesMap();
  this.pagesContent.appendChild(this.buildPagesList(topic.children));
  this.pagesScrollPane.reset();
  this.currentTopic = topic;
  this.pagesMap.removeAttribute("aria-busy");
};

netacad.views.CourseMapView.prototype.destroyPagesMap = function() {
  this.destroy(this.pagesContent);
  this.pagesScrollPane.reset();
  this.currentTopic = null;
};

netacad.views.CourseMapView.prototype.buildPagesList = function(pages) {
  return this.buildItemList(pages);
};

netacad.views.CourseMapView.prototype.destroy = function(content) {
  var anchors = content.querySelectorAll("a");
  for (var i = 0; i < anchors.length; i++) {
    var anchor = anchors[i];
    anchor.removeEventListener("click", this);
    anchor.removeEventListener("dblclick", this);
    anchor.removeEventListener("tap", this);
    anchor.removeEventListener("double-tap", this);
  }
  while (content.hasChildNodes()) {
    content.removeChild(content.lastChild);
  }
};

netacad.views.CourseMapView.prototype.handleEvent = function(event) {
  if (event.type == "click" || event.type == "tap") {
    this.handleClick(event);
  } else if (event.type == "dblclick" || event.type == "double-tap") {
    this.handleDoubleClick(event);
  } else if (event.type == "change") {
    this.update();
  }
};

netacad.views.CourseMapView.prototype.handleClick = function(event) {
  if (event.currentTarget instanceof HTMLAnchorElement) {
    var anchor = event.currentTarget;
    var href = anchor.getAttribute("href");
    var id = href.substring(1); // remove "#"
    var item = netacad.models.Item.map[id];
    this.model.setCurrent(item);
    event.stopPropagation();
    event.preventDefault();
  }
};

netacad.views.CourseMapView.prototype.handleDoubleClick = function(event) {
  if (event.currentTarget instanceof HTMLAnchorElement) {
    var anchor = event.currentTarget;
    var href = anchor.getAttribute("href");
    var id = href.substring(1); // remove "#"
    var item = netacad.models.Item.map[id];
    this.model.setCurrent(this.model.getFirst(item));
    event.stopPropagation();
    event.preventDefault();
  }
};

netacad.views.CourseMapView.prototype.update = function() {
  var active = !!(document.querySelector("#container.active") || document.querySelector(".overlay.active"));
  this.modulesMap.setAttribute("aria-live", active? "off": "polite");
  this.sectionsMap.setAttribute("aria-live", active? "off": "polite");
  this.topicsMap.setAttribute("aria-live", active? "off": "polite");
  this.pagesMap.setAttribute("aria-live", active? "off": "polite");
  $('a.selected', this.element).removeClass('selected');
  var item = this.model.getCurrent();
  if (item instanceof netacad.models.Module) {
    this.buildModulesMap(item.parent);
    this.buildSectionsMap(item);
    this.destroyTopicsMap();
    this.destroyPagesMap();
    if (!active) {
      this.sectionsContent.focus();
    }
  } else if (item instanceof netacad.models.Section) {
    this.buildModulesMap(item.parent.parent);
    this.buildSectionsMap(item.parent);
    this.buildTopicsMap(item);
    this.destroyPagesMap();
    if (!active) {
      this.topicsContent.focus();
    }
  } else if (item instanceof netacad.models.Topic) {
    this.buildModulesMap(item.parent.parent.parent);
    this.buildSectionsMap(item.parent.parent);
    this.buildTopicsMap(item.parent);
    this.buildPagesMap(item);
    if (!active) {
      this.pagesContent.focus();
    }
  } else if (item instanceof netacad.models.Page) {
    this.buildModulesMap(item.parent.parent.parent.parent);
    this.buildSectionsMap(item.parent.parent.parent);
    this.buildTopicsMap(item.parent.parent);
    this.buildPagesMap(item.parent);
  }
  while (item) {
    $('a[href="#' + item.li + '"]', this.element).addClass('selected');
    item = item.parent;
  }
};

netacad.views.CourseMapView.prototype.setARIALive = function(value) {
  this.modulesMap.setAttribute("aria-live", value? "polite": "off");
  this.sectionsMap.setAttribute("aria-live", value? "polite": "off");
  this.topicsMap.setAttribute("aria-live", value? "polite": "off");
  this.pagesMap.setAttribute("aria-live", value? "polite": "off");
};


/**
 * netacad.views.Overlay
 */
netacad.views.Overlay = function(model, element) {
  netacad.views.View.call(this, model, element);
  this.closeButton = this.element.querySelector(".overlay-close-button");
  this.closeButton.addEventListener("click", this);
};

netacad.extend(netacad.views.Overlay, netacad.views.View);

netacad.views.Overlay.prototype.handleEvent = function(event) {
  if (event.type == "click") {
    if (event.target == this.closeButton) {
      this.close();
      event.stopPropagation();
    }
  }  
};

netacad.views.Overlay.prototype.open = function() {
  $(".overlay.active").removeClass("active");
  $(this.element).addClass("active");
  this.element.setAttribute("aria-hidden", "false");
  this.element.focus();
  this.document.addEventListener("focus", this, true);
  this.document.addEventListener("keydown", this, true);
};

netacad.views.Overlay.prototype.close = function() {
  this.document.removeEventListener("focus", this, true);
  this.document.removeEventListener("keydown", this, true);
  $(".overlay.active").removeClass("active");
  this.element.setAttribute("aria-hidden", "true");
  var menuButton = this.document.querySelector(".menu-button.active");
  if (menuButton) {
    $(menuButton).removeClass("active");
    menuButton.focus();
  }
};


/**
 * netacad.views.filters
 */
netacad.provide("netacad.views.filters");

netacad.views.filters.showAll = function(item) {
  return true;
};

netacad.views.filters.showPacketTracer = function(item) {
  if (item instanceof netacad.models.Page) {
    return (item.pageType == "Activity" && item.activityType == "Packet Tracer");
  } else if (item.children) {
    for (var i = 0; i < item.children.length; i++) {
      if (netacad.views.filters.showPacketTracer(item.children[i])) {
        return true;
      }
    }
    return false;
  }
};

netacad.views.filters.showLabs = function(item) {
  if (item instanceof netacad.models.Page) {
    return (item.pageType == "Activity" && item.activityType == "Lab");
  } else if (item.children) {
    for (var i = 0; i < item.children.length; i++) {
      if (netacad.views.filters.showLabs(item.children[i])) {
        return true;
      }
    }
    return false;
  }
};

netacad.views.filters.showVideos = function(item) {
  if (item instanceof netacad.models.Page) {
    return (item.pageType == "Activity" && item.activityType == "Other" && item.activitySubtype == "Flash PnC");
  } else if (item.children) {
    for (var i = 0; i < item.children.length; i++) {
      if (netacad.views.filters.showVideos(item.children[i])) {
        return true;
      }
    }
    return false;
  }
};

/**
 * netacad.views.CourseIndexView
 * @constructor
 */ 
netacad.views.CourseIndexView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  var that = this;
  this.scrollPane = new netacad.components.ScrollPane(this.element.querySelector(".scroll-pane"));
  this.content = this.scrollPane.content;
  this.indexCourseButton = this.document.getElementById("index-course");
  this.indexPacketTracerButton = this.document.getElementById("index-packet-tracer");
  this.indexLabButton = this.document.getElementById("index-lab");
  this.indexVideoButton = this.document.getElementById("index-video");
  this.indexCourseButton.addEventListener("click", function() {
    $("#course-index-buttons .active").removeClass("active");
    $("#index-course").addClass("active");
    that.build(netacad.views.filters.showAll);
  });
  this.indexPacketTracerButton.addEventListener("click", function() {
    $("#course-index-buttons .active").removeClass("active");
    $("#index-packet-tracer").addClass("active");
    that.build(netacad.views.filters.showPacketTracer);
  });
  this.indexLabButton.addEventListener("click", function() {
    $("#course-index-buttons .active").removeClass("active");
    $("#index-lab").addClass("active");
    that.build(netacad.views.filters.showLabs);
  });
  this.indexVideoButton.addEventListener("click", function() {
    $("#course-index-buttons .active").removeClass("active");
    $("#index-video").addClass("active");
    that.build(netacad.views.filters.showVideos);
  });
  this.model.addEventListener("change", this);
  this.element.addEventListener("click", this);
  this.element.addEventListener("tap", this);
  $("#course-index-buttons .active").removeClass("active");
  $("#index-course").addClass("active");
};

netacad.extend(netacad.views.CourseIndexView, netacad.views.Overlay);

netacad.views.CourseIndexView.prototype.open = function() {
  netacad.views.Overlay.prototype.open.call(this);
  if (!this.content.hasChildNodes()) {
    $("#course-index-buttons .active").removeClass("active");
    $("#index-course").addClass("active");
    this.build(netacad.views.filters.showAll);
  }
  if (typeof ga !== "undefined") {
    ga("set", "page", "/" + this.model.li + "/" + this.model.lang + "/course-index");
    ga("send", "pageview");
  }
};

netacad.views.CourseIndexView.prototype.close = function() {
  netacad.views.Overlay.prototype.close.call(this);
  this.destroy();
};

netacad.views.CourseIndexView.prototype.build = function(filter) {
  this.element.setAttribute("aria-busy", true);
  this.destroy();
  this.content.appendChild(this.buildModuleList(this.model.children, filter));
  this.scrollPane.reset();
  this.content.focus();
  this.element.removeAttribute("aria-busy");
};

netacad.views.CourseIndexView.prototype.destroy = function() {
  netacad.dom.empty(this.content);
  this.scrollPane.update();
};

netacad.views.CourseIndexView.prototype.buildModuleList = function(modules, filter) {
  var empty = true;
  var fragment = this.document.createDocumentFragment();
  for (var i = 0; i < modules.length; i++) {
    var module = modules[i];
    if (module && filter(module)) {
       // <h1>Module 1<br/>Module Title</h1>
       var h1 = this.document.createElement("h1");
       h1.appendChild(this.document.createTextNode(netacad.lang.get("Module").replace("#", module.li)));
       h1.appendChild(this.document.createElement("br"));
       h1.appendChild(this.document.createTextNode(module.title));
       fragment.appendChild(h1);
       fragment.appendChild(this.buildSectionList(module.children, filter));
       empty = false;
    }
  }
  if (empty) {
    var p = this.document.createElement("p");
    p.setAttribute("class", "message");
    p.appendChild(this.document.createTextNode(netacad.lang.get("NoItems")));
    fragment.appendChild(p);
  }
  return fragment;
};

netacad.views.CourseIndexView.prototype.buildSectionList = function(sections, filter) {
  var fragment = this.document.createDocumentFragment();
  for (var i = 0; i < sections.length; i++) {
    // <h2>1.2 Section Title</h2>
    var section = sections[i];
    if (section && filter(section)) {
      var h2 = this.document.createElement("h2");
      h2.appendChild(this.document.createTextNode(section.li + " " + section.title));
      fragment.appendChild(h2);
      fragment.appendChild(this.buildTopicList(section.children, filter));
    }
  }
  return fragment;
};

netacad.views.CourseIndexView.prototype.buildTopicList = function(topics, filter) {
  var fragment = this.document.createDocumentFragment();
  for (var i = 0; i < topics.length; i++) {
    // <h3>1.2.3 Topic Title</h3>
    var topic = topics[i];
    if (topic && filter(topic)) {
      var h3 = this.document.createElement("h3");
      h3.appendChild(this.document.createTextNode(topic.li + " " + topic.title));
      fragment.appendChild(h3);
      fragment.appendChild(this.buildPageList(topic.children, filter));
    }
  }
  return fragment;
};

netacad.views.CourseIndexView.prototype.buildPageList = function(pages, filter) {
  var fragment = this.document.createDocumentFragment();
  for (var i = 0; i < pages.length; i++) {
    // <h4><a class="page-title" href="#1.2.3.4>1.2.3.4 Page Title</a></h4>
    var page = pages[i];
    if (page && filter(page)) {
      var h4 = this.document.createElement("h4");
      var anchor = netacad.components.Gestures.enable(this.document.createElement("a"));
      anchor.setAttribute("class", "page-title");
      anchor.setAttribute("href", "#" + page.li);
      anchor.appendChild(this.document.createTextNode(page.li + " " + page.title));
      h4.appendChild(anchor);
      fragment.appendChild(h4);
    }
  }
  return fragment;
};

netacad.views.CourseIndexView.prototype.handleEvent = function(event) {
  netacad.views.Overlay.prototype.handleEvent.call(this, event);
  if (event.type == "click" || event.type == "tap") {
    if (event.target instanceof HTMLAnchorElement) {
      var anchor = event.target;
      var href = anchor.getAttribute("href");
      var id = href.substring(1); // remove "#"
      var item = netacad.models.Item.map[id];
      this.model.setCurrent(item);
      event.stopPropagation();
      event.preventDefault();
    }
  } else if (event.type == "change") {
    // TODO: mark course index? scroll to current page?
  }
};


/**
 * netacad.views.RecentPagesView
 * @constructor
 */
netacad.views.RecentPagesView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  this.MAX = 10;
  this.pages = [];
  var data = netacad.settings.get(netacad.settings.RECENT_KEY);
  if (data instanceof Array) {
    // TODO: map to actual Items
    this.pages = data;
  }
  this.scrollPane = new netacad.components.ScrollPane(this.element.querySelector(".scroll-pane"));
  this.content = this.scrollPane.content;
  this.model.addEventListener("change", this);
  this.setRecent(this.model.getCurrent());
  this.build();
};

netacad.extend(netacad.views.RecentPagesView, netacad.views.Overlay);

netacad.views.RecentPagesView.prototype.open = function() {
  netacad.views.Overlay.prototype.open.call(this);
  this.scrollPane.update();
  if (typeof ga !== "undefined") {
    ga("set", "page", "/" + this.model.li + "/" + this.model.lang + "/recent-pages");
    ga("send", "pageview");
  }
};

netacad.views.RecentPagesView.prototype.build = function() {
  this.element.setAttribute("aria-busy", true);
  this.destroy();
  this.content.appendChild(this.buildItemList(this.pages, netacad.lang.get("NoRecentPages")));
  this.scrollPane.update();
  this.element.removeAttribute("aria-busy");
};

netacad.views.RecentPagesView.prototype.destroy = function() {
  this.destroyItemList(this.content.firstChild);
  this.scrollPane.update();
};

netacad.views.RecentPagesView.prototype.handleEvent = function(event) {
  netacad.views.Overlay.prototype.handleEvent.call(this, event);
  if (event.type == "change") {
    this.setRecent(this.model.getCurrent());
    this.build();
  } else if (event.type == "click" || event.type == "tap") {
    if (event.currentTarget instanceof HTMLAnchorElement) {
      var anchor = event.currentTarget;
      var href = anchor.getAttribute("href");
      var id = href.substring(1); // remove "#"
      var item = netacad.models.Item.map[id];
      this.model.setCurrent(item);
      event.stopPropagation();
      event.preventDefault();
    }
  }
};

netacad.views.RecentPagesView.prototype.setRecent = function(item) {
  // only track Pages
  if (item instanceof netacad.models.Page) {
    // if it's already in the list
    var li = item.li;
    var index = this.pages.indexOf(li);
    if (index >= 0) {
      // then remove if from the list
      this.pages.splice(index, 1);
    }
    var length = this.pages.unshift(li);
    // only keep so many in the list
    if (length > this.MAX) {
      this.pages.splice(this.MAX, 1);
    }
    netacad.settings.set(netacad.settings.RECENT_KEY, this.pages);
  }
};


/**
 * netacad.views.BookmarksView
 * @constructor
 * TODO: Make bookmarks a property of Page objects.
 */
netacad.views.BookmarksView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  this.pages = [];
  var data = netacad.settings.get(netacad.settings.BOOKMARKS_KEY);
  if (data instanceof Array) {
    // TODO: map to actual Items
    this.pages = data;
  }
  this.scrollPane = new netacad.components.ScrollPane(this.element.querySelector(".scroll-pane"));
  this.content = this.scrollPane.content;
  this.button = this.document.getElementById("page-menu-bookmark-button");
  this.button.addEventListener("click", this);
  this.model.addEventListener("change", this);
  this.build();
};

netacad.extend(netacad.views.BookmarksView, netacad.views.Overlay);

netacad.views.BookmarksView.prototype.open = function() {
  netacad.views.Overlay.prototype.open.call(this);
  this.scrollPane.update();
  if (typeof ga !== "undefined") {
    ga("set", "page", "/" + this.model.li + "/" + this.model.lang + "/bookmarks");
    ga("send", "pageview");
  }
};

netacad.views.BookmarksView.prototype.build = function() {
  this.element.setAttribute("aria-busy", true);
  this.destroy();
  this.content.appendChild(this.buildItemList(this.pages, netacad.lang.get("NoBookmarks")));
  this.scrollPane.update();
  this.element.removeAttribute("aria-busy");
};

netacad.views.BookmarksView.prototype.destroy = function() {
  this.destroyItemList(this.content.firstChild);
  this.scrollPane.update();
};

netacad.views.BookmarksView.prototype.handleEvent = function(event) {
  netacad.views.Overlay.prototype.handleEvent.call(this, event);
  if (event.type == "change") {
    this.checkBookmark(this.model.getCurrent());
  } else if (event.type == "click" || event.type == "tap") {
    if (event.target == this.button) {
      this.setBookmark(this.model.getCurrent());
      this.build();
    } else if (event.currentTarget instanceof HTMLAnchorElement) {
      var anchor = event.currentTarget;
      var href = anchor.getAttribute("href");
      var id = href.substring(1); // remove "#"
      var item = netacad.models.Item.map[id];
      this.model.setCurrent(item);
      event.stopPropagation();
      event.preventDefault();
    }
  }
};

netacad.views.BookmarksView.prototype.checkBookmark = function(item) {
  if (item instanceof netacad.models.Page) {
    if (this.pages.indexOf(item.li) >= 0) {
      $(this.button).addClass("selected");
    } else {
      $(this.button).removeClass("selected");
    }
  }
};

netacad.views.BookmarksView.prototype.setBookmark = function(item) {
  // only track Pages
  if (item instanceof netacad.models.Page) {
    // if it's already in the list
    var li = item.li;
    var index = this.pages.indexOf(li);
    if (index >= 0) {
      // then remove if from the list
      this.pages.splice(index, 1);
    } else {
      this.pages.unshift(li);
    }
    this.checkBookmark(item);
    netacad.settings.set(netacad.settings.BOOKMARKS_KEY, this.pages);
  }
};


/**
 * netacad.views.BackgroundView
 * @constructor
 */
netacad.views.BackgroundView = function(model, element) {
  netacad.views.View.call(this, model, element);
  this.model.addEventListener("change", this);
  this.update();
};

netacad.views.BackgroundView.prototype.handleEvent = function(event) {
  if (event.type == "change") {
    this.update();
  }  
};

netacad.views.BackgroundView.prototype.update = function() {
  var ident = this.model.getBackground();
  var backgrounds = this.model.getBackgrounds();
  for (var i = 0; i < backgrounds.length; i++) {
    var background = backgrounds[i];
    if (ident == background) {
      $(this.element).addClass(background);
    } else {
      $(this.element).removeClass(background);
    }
  }
};


/**
 * netacad.views.BackgroundsView
 * @constructor
 */
netacad.views.BackgroundsView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  this.scrollPane = new netacad.components.ScrollPane(this.element.querySelector(".scroll-pane"));
  this.content = this.scrollPane.content;
  this.build();
};

netacad.extend(netacad.views.BackgroundsView, netacad.views.Overlay);

netacad.views.BackgroundsView.prototype.open = function() {
  netacad.views.Overlay.prototype.open.call(this);
  this.scrollPane.update();
};

netacad.views.BackgroundsView.prototype.build = function() {
  this.element.setAttribute("aria-busy", true);
  this.destroy();
  var backgrounds = this.model.getBackgrounds();
  var list = this.document.createElement("ul");
  list.setAttribute("class", "backgrounds");
  var fragment = document.createDocumentFragment();
  for (var i = 0; i < backgrounds.length; i++) {
    /*
     * <li>
     *   <input type="image" value="ioe-bg-name" src="course/common/backgrounds/ioe-bg-name-S.jpg" alt="Background image #" aria-label="Background image #"/>
     * </li>
     */
    var background = backgrounds[i];
    var item = this.document.createElement("li");
    var input = this.document.createElement("input");
    input.addEventListener("click", this);
    input.setAttribute("type", "image");
    input.setAttribute("data-ident", background);
    input.setAttribute("src", "course/common/backgrounds/" + background + "-S.jpg");
    input.setAttribute("alt", netacad.lang.get("BackgroundImage") + " " + i);
    input.setAttribute("aria-label", netacad.lang.get("BackgroundImage") + " " + i);
    item.appendChild(input);
    fragment.appendChild(item);
  }
  list.appendChild(fragment);
  this.content.appendChild(list);
  this.scrollPane.update();
  this.element.removeAttribute("aria-busy");
};

netacad.views.BackgroundsView.prototype.destroy = function() {
  var images = this.content.querySelectorAll("img");
  for (var i = 0; i < images.length; i++) {
    images[i].removeEventListener("click", this);
  }
  netacad.dom.empty(this.content);
  this.scrollPane.update();
};

netacad.views.BackgroundsView.prototype.handleEvent = function(event) {
  netacad.views.Overlay.prototype.handleEvent.call(this, event);
  if (event.type == "click") {
    if (event.currentTarget instanceof HTMLInputElement) {
      var ident = event.currentTarget.getAttribute("data-ident");
      this.model.setBackground(ident);
      $('.overlay.active').removeClass('active');
      $('.menu-button.active').removeClass('active');
      event.stopPropagation();
      event.preventDefault();
    }
  }
};


/**
 * netacad.views.SearchView
 * @constructor
 */
netacad.views.SearchView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  this.searches = [];
  var modules = this.model.children;
  for (var i = 0; i < modules.length; i++) {
    var module = modules[i];
    if (module) {
      this.searches.push(new netacad.search.SearchEngine("course/module" + module.li + "/search.json"));
    }
  }
  this.input = this.document.getElementById("search-input");
  this.input.addEventListener("change", this);
  this.input.addEventListener("keyup", this);
  // show loading icon
  var that = this;
  $(this.element).addClass("loading");
  this.load(this.searches.slice(0), function() {
    // remove loading icon
    $(that.element).removeClass("loading");
  });
  this.scrollPane = new netacad.components.ScrollPane(this.element.querySelector(".scroll-pane"));
  this.content = this.scrollPane.content;
  this.build([], netacad.lang.get("EnterSearchTerms"));
};

netacad.extend(netacad.views.SearchView, netacad.views.Overlay);

netacad.views.SearchView.prototype.open = function() {
  netacad.views.Overlay.prototype.open.call(this);
  this.input.focus();
  if (typeof ga !== "undefined") {
    ga("set", "page", "/" + this.model.li + "/" + this.model.lang + "/search");
    ga("send", "pageview");
  }
};

netacad.views.SearchView.prototype.build = function(items, message) {
  this.element.setAttribute("aria-busy", true);
  this.destroy();
  this.content.appendChild(this.buildItemList(items, message));
  this.scrollPane.reset();
  this.element.removeAttribute("aria-busy");
};

netacad.views.SearchView.prototype.destroy = function() {
  this.destroyItemList(this.content.firstChild);
  this.scrollPane.reset();
};

netacad.views.SearchView.prototype.handleEvent = function(event) {
  netacad.views.Overlay.prototype.handleEvent.call(this, event);
  if (event.type == "change") {
    var text = event.target.value;
    if (!text) {
      this.build([], netacad.lang.get("EnterSearchTerms"));
    } else {
      this.find(netacad.search.getWords(text));
    }
  } else if (event.type == "keyup") {
    // some browsers (i.e. IE) do not trigger a
    // change event when the Enter key is pressed
    if (event.which == 13) { // Enter key
      event.target.blur();
      event.target.focus();
    }
    event.stopPropagation();
  } else if (event.type == "click") {
    if (event.currentTarget instanceof HTMLAnchorElement) {
      var anchor = event.currentTarget;
      var href = anchor.getAttribute("href");
      var id = href.substring(1); // remove "#"
      var item = netacad.models.Item.map[id];
      this.model.setCurrent(item, netacad.search.getWords(this.input.value));
      event.stopPropagation();
      event.preventDefault();
    }
  }
};

netacad.views.SearchView.prototype.load = function(searches, callback) {
  var that = this;
  var search = searches.shift();
  search.load(function() {
    if (searches.length) {
      that.load(searches, callback);
    } else {
      callback();
    }
  });
};

netacad.views.SearchView.prototype.find = function(words) {
  var items = [];
  for (var i = 0; i < this.searches.length; i++) {
    var search = this.searches[i];
    var results = search.find(words);
    for (var j = 0; j < results.length; j++) {
      var id = search.list[results[j]];
      var item = netacad.models.Item.map[id];
      if (item) {
        items.push(item);
      }
    }
  }
  this.build(items, netacad.lang.get("NoSearchResults"));
  return items;
};

netacad.views.SearchView.prototype.listWords = function() {
  var result = [];
  for (var i = 0; i < this.searches.length; i++) {
    result = result.concat(this.searches[i].listWords());
  }
  return result.sort();
};


/**
 * netacad.views.LanguagesView
 * @constructor
 */
netacad.views.LanguagesView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  this.scrollPane = new netacad.components.ScrollPane(this.element.querySelector(".scroll-pane"));
  this.content = this.scrollPane.content;
  this.build();
};

netacad.extend(netacad.views.LanguagesView, netacad.views.Overlay);

netacad.views.LanguagesView.prototype.open = function() {
  netacad.views.Overlay.prototype.open.call(this);
  this.scrollPane.update();
};

netacad.views.LanguagesView.prototype.build = function() {
  if (!netacad.config.languages) {
    return;
  }
  this.element.setAttribute("aria-busy", true);
  var anchors = this.element.querySelectorAll("a[data-lang]");
  for (var i = 0; i < anchors.length; i++) {
    var anchor = anchors[i];
    var lang = anchor.getAttribute("data-lang");
    if (netacad.config.languages.indexOf(lang) >= 0) {
      anchor.addEventListener("click", this);
    } else {
      anchor.parentNode.removeChild(anchor);
    }
  }
  this.scrollPane.update();
  this.element.removeAttribute("aria-busy");
};

netacad.views.LanguagesView.prototype.handleEvent = function(event) {
  netacad.views.Overlay.prototype.handleEvent.call(this, event);
  if (event.target != this.closeButton) {
    var anchor = event.target;
    var lang = anchor.getAttribute("data-lang");
    if(lang != null){
      var url = '../' + lang + '/index.html';
      if (netacad.environment.hasTrunk()) {
        url = '../../' + lang + '/trunk/';
      }
      var hash = window.location.hash;
      window.location.assign(url + hash);
      event.stopPropagation();
      event.preventDefault();
    }
  }
};


/**
 * netacad.views.HelpView
 */
netacad.views.HelpView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  var that = this;
  this.content = this.document.getElementById("help-content");
  this.document.getElementById("help-1").addEventListener("click", function() {
    $(".help-button.active").removeClass("active");
    $("#help-1").addClass("active");
    that.build("course/help/help1/index.html");
  });
  this.document.getElementById("help-2").addEventListener("click", function() {
    $(".help-button.active").removeClass("active");
    $("#help-2").addClass("active");
    that.build("course/help/help2/index.html");
  });
  this.document.getElementById("help-3").addEventListener("click", function() {
    $(".help-button.active").removeClass("active");
    $("#help-3").addClass("active");
    that.build("course/help/help3/index.html");
  });
  this.document.getElementById("help-4").addEventListener("click", function() {
    $(".help-button.active").removeClass("active");
    $("#help-4").addClass("active");
    that.build("course/help/help4/index.html");
  });
  this.document.getElementById("help-5").addEventListener("click", function() {
    $(".help-button.active").removeClass("active");
    $("#help-5").addClass("active");
    that.build("course/help/help5/index.html");
  });
};

netacad.extend(netacad.views.HelpView, netacad.views.Overlay);

netacad.views.HelpView.prototype.open = function() {
  netacad.views.Overlay.prototype.open.call(this);
  if (!this.content.hasChildNodes()) {
    $(".help-button.active").removeClass("active");
    $("#help-1").addClass("active");
    this.build("course/help/help1/index.html");
  }
  if (typeof ga !== "undefined") {
    ga("set", "page", "/" + this.model.li + "/" + this.model.lang + "/help");
    ga("send", "pageview");
  }
};

netacad.views.HelpView.prototype.close = function() {
  netacad.views.Overlay.prototype.close.call(this);
  netacad.dom.empty(this.content);
};

netacad.views.HelpView.prototype.build = function(url) {
  this.element.setAttribute("aria-busy", true);
  /*
   * <iframe src="url" title="help content" aria-label="help content"></iframe>
   */
  netacad.dom.empty(this.content);
  var frame = this.document.createElement('iframe');
  frame.setAttribute('src', url);
  frame.setAttribute('title', 'help content');
  frame.setAttribute('aria-label', 'help content');
  this.content.appendChild(frame);
  this.element.removeAttribute("aria-busy");
  this.content.focus();
};


/**
 * netacad.views.DeveloperToolsView
 * @constructor
 */
netacad.views.DeveloperToolsView = function(model, element) {
  netacad.views.Overlay.call(this, model, element);
  this.disableButton = this.document.getElementById("disable-developer-tools-button");
  this.enablePseudolocalizationButton = this.document.getElementById("enable-pseudolocalization-button");
  this.disablePseudolocalizationButton = this.document.getElementById("disable-pseudolocalization-button");
  this.clearBackgroundButton = this.document.getElementById("clear-background-button");
  this.clearButton = this.document.getElementById("clear-local-storage-button");
  this.model.addEventListener("change", this);
  this.disableButton.addEventListener("click", this);
  this.enablePseudolocalizationButton.addEventListener("click", this);
  this.disablePseudolocalizationButton.addEventListener("click", this);
  this.clearBackgroundButton.addEventListener("click", this);
  this.clearButton.addEventListener("click", this);
  this.update();
};

netacad.extend(netacad.views.DeveloperToolsView, netacad.views.Overlay);

netacad.views.DeveloperToolsView.prototype.handleEvent = function(event) {
  netacad.views.Overlay.prototype.handleEvent.call(this, event);
  if (event.type == "change") {
    this.update();
  } else if (event.type == "click") {
    if (event.target == this.disableButton) {
      this.model.disable();
    } else if (event.target == this.enablePseudolocalizationButton) {
      this.model.setPseudolocalization(true);
    } else if (event.target == this.disablePseudolocalizationButton) {
      this.model.setPseudolocalization(false);
    } else if (event.target == this.clearBackgroundButton) {
      this.model.clearBackground();
    } else if (event.target == this.clearButton) {
      this.model.clearLocalStorage();
    }
  }
};

netacad.views.DeveloperToolsView.prototype.update = function() {
  if (this.model.getPseudolocalization()) {
    this.disablePseudolocalizationButton.style.removeProperty("display");
    this.enablePseudolocalizationButton.style.setProperty("display", "none");
  } else {
    this.enablePseudolocalizationButton.style.removeProperty("display");
    this.disablePseudolocalizationButton.style.setProperty("display", "none");
  }
};


/**
 * netacad.views.PageView
 * @constructor
 */
netacad.views.PageView = function(model, element) {
  netacad.views.View.call(this, model, element);
  this.content = this.document.getElementById("content");
  this.container = this.document.getElementById("container");
  this.header = this.document.getElementById("page-header");
  this.footer = this.document.getElementById("page-footer");
  this.pageContent = this.document.getElementById("page-content");
  this.slideButtons = this.document.getElementById("page-slide-buttons");
  this.closeButton = this.document.getElementById("page-menu-close-button");
  this.transcriptButton = this.document.getElementById("page-menu-transcript-button");
  this.nextButton = this.document.getElementById("page-menu-next-button");
  this.previousButton = this.document.getElementById("page-menu-previous-button");
  this.previousButton.addEventListener("click", this);
  this.nextButton.addEventListener("click", this);
  this.closeButton.addEventListener("click", this);
  this.transcriptButton.addEventListener("click", this);
  this.model.addEventListener("change", this);
  this.update(this.model.getCurrent());
};

netacad.extend(netacad.views.PageView, netacad.views.View);

netacad.views.PageView.prototype.build = function() {
  // TODO: build page view
};

netacad.views.PageView.prototype.handleEvent = function(event) {
  if (event.type == "change") {
    this.update(this.model.getCurrent(), this.model.search);
  } else if (event.type == "click") {
    if (event.target == this.nextButton) {
      this.next();
    } else if (event.target == this.previousButton) {
      this.previous();
    } else if (event.target == this.closeButton) {
      this.close();
    } else if (event.target == this.transcriptButton) {
      this.setTranscript(!this.getTranscript());
    }
  } else if (event.type == "focus") {
    if (!this.element.contains(event.target)) {
      event.stopPropagation();
      this.element.focus();
    }
  } else if (event.type == "keydown") {
    if (event.keyCode == 27) { // Escape Key
      if (!this.document.querySelector(".overlay.active")) {
        this.close();
      }
    }
  }
};

netacad.views.PageView.prototype.update = function(page, search) {
  
  if (page instanceof netacad.models.Page) {

    this.container.setAttribute("aria-busy", true);

    var pageCrumb = this.document.getElementById("breadcrumbs-page");
    var pageCrumbLI = this.document.getElementById("breadcrumbs-page-li");
    var pageCrumbTitle = this.document.getElementById("breadcrumbs-page-title");
    netacad.dom.empty(pageCrumbLI);
    netacad.dom.empty(pageCrumbTitle);
    pageCrumb.setAttribute("href", "#" + page.li);
    pageCrumbLI.appendChild(this.document.createTextNode(page.li));
    
    var topic = page.parent;
    var topicCrumb = this.document.getElementById("breadcrumbs-topic");
    var topicCrumbLI = this.document.getElementById("breadcrumbs-topic-li");
    var topicCrumbTitle = this.document.getElementById("breadcrumbs-topic-title");
    netacad.dom.empty(topicCrumbLI);
    netacad.dom.empty(topicCrumbTitle);
    topicCrumb.setAttribute("href", "#" + topic.li);
    topicCrumbLI.appendChild(this.document.createTextNode(topic.li));
    
    var section = topic.parent;
    var sectionCrumb = this.document.getElementById("breadcrumbs-section");
    var sectionCrumbLI = this.document.getElementById("breadcrumbs-section-li");
    var sectionCrumbTitle = this.document.getElementById("breadcrumbs-section-title");
    netacad.dom.empty(sectionCrumbLI);
    netacad.dom.empty(sectionCrumbTitle);
    sectionCrumb.setAttribute("href", "#" + section.li);
    sectionCrumbLI.appendChild(this.document.createTextNode(section.li));
    
    var module = section.parent;
    var moduleCrumb = this.document.getElementById("breadcrumbs-module");
    var moduleCrumbLI = this.document.getElementById("breadcrumbs-module-li");
    var moduleCrumbTitle = this.document.getElementById("breadcrumbs-module-title");
    netacad.dom.empty(moduleCrumbLI);
    netacad.dom.empty(moduleCrumbTitle);
    moduleCrumb.setAttribute("href", "#" + module.li);
    moduleCrumbLI.appendChild(this.document.createTextNode(netacad.lang.get("Module").replace("#", module.li)));

    var totalBreadCrumbLength = page.title.length+topic.title.length+section.title.length+module.title.length;
    if(totalBreadCrumbLength > 200){
      pageCrumbTitle.appendChild(this.document.createTextNode(truncate(page.title)));
      topicCrumbTitle.appendChild(this.document.createTextNode(truncate(topic.title)));
      sectionCrumbTitle.appendChild(this.document.createTextNode(truncate(section.title)));
      moduleCrumbTitle.appendChild(this.document.createTextNode(truncate(module.title)));
    }else{
      pageCrumbTitle.appendChild(this.document.createTextNode(page.title));
      topicCrumbTitle.appendChild(this.document.createTextNode(topic.title));
      sectionCrumbTitle.appendChild(this.document.createTextNode(section.title));
      moduleCrumbTitle.appendChild(this.document.createTextNode(module.title));
    }
    function truncate(t){
      if(t.length >56){
        t = t.substring(0,56);
        t = t.substring(0,t.lastIndexOf(" "))
        return (t + "...");
      }
      return t;
    }

    netacad.dom.empty(this.slideButtons);

    // the iframe is removed and rebuilt to keep the iframe
    // in sync with menu when the back button is used
    /*
     * <iframe id="frame" src="url"></iframe>
     */
    netacad.dom.empty(this.pageContent);
    var frame = this.document.createElement('iframe');
    frame.setAttribute('id', 'frame');
    frame.setAttribute('title', netacad.lang.get('Page').replace("#", page.li));
    var url = page.url;
    if (search) {
      url += '?q=' + encodeURIComponent(search.join(" "));
    }
    frame.setAttribute('src', url);
    this.pageContent.appendChild(frame);
    this.previousButton.disabled = this.isFirst(page);
    this.nextButton.disabled = this.isLast(page);
    if (!$(this.container).hasClass("active")) {
   	  this.document.addEventListener("focus", this, true);
   	  this.document.addEventListener("keydown", this, true);
      $(this.container).addClass("active");
      this.container.focus();
    }
    this.checkTranscript();
    if (typeof ga !== "undefined") {
      ga("set", "page", "/" + this.model.li + "/" + this.model.lang + "/module" + module.li);
      ga("send", "pageview");
    }

    this.container.removeAttribute("aria-busy");

  } else {
    this.close();
  }
  $(".overlay.active").removeClass("active");
  $(".menu-button.active").removeClass("active");

};

netacad.views.PageView.prototype.checkTranscript = function() {
  if (this.getTranscript()) {
    $(this.transcriptButton).addClass("selected");
  } else {
    $(this.transcriptButton).removeClass("selected");
  }
};

netacad.views.PageView.prototype.getTranscript = function(value) {
  return netacad.settings.get(netacad.settings.TRANSCRIPT_KEY);
};

netacad.views.PageView.prototype.setTranscript = function(value) {
  if (value != netacad.settings.get(netacad.settings.TRANSCRIPT_KEY)) {
    netacad.settings.set(netacad.settings.TRANSCRIPT_KEY, value);
    this.update(this.model.getCurrent());
  }
};

netacad.views.PageView.prototype.updateSlideButtons = function(index) {
  $("#page-slide-buttons .active").removeClass("active");
  $("#page-slide-buttons button[value='" + index + "']").addClass("active");
};

netacad.views.PageView.prototype.setMedia = function(media) {
  var that = this;
  // TODO: remove listeners
  netacad.dom.empty(this.slideButtons);
  var length = media.getSlideCount();
  if (length > 1) {
    var fieldset = this.document.createElement('fieldset');
    var list = this.document.createElement("ol");
    for (var i = 1; i <= length; i++) {
      /*
       * <li>
       *   <button value="#">#</button>
       * </li>
       */
      var item = this.document.createElement("li");
      var button = this.document.createElement("button");
      button.setAttribute("title", netacad.lang.get("Figure").replace("#", i));
      button.setAttribute("value", i);
      button.addEventListener("click", function(event) {
        var index = parseInt(event.target.value);
        media.setSlide(index);
        that.updateSlideButtons(index);
      }, false);
      button.appendChild(this.document.createTextNode(i));
      item.appendChild(button);
      list.appendChild(item);
    }
    var legend = this.document.createElement("legend");
    legend.appendChild(this.document.createTextNode(netacad.lang.get("Figures")));
    fieldset.appendChild(legend);
    fieldset.appendChild(list);
    this.slideButtons.appendChild(fieldset);
    this.updateSlideButtons(media.getSlide());
  }
};

netacad.views.PageView.prototype.isFirst = function(page) {
  return (page == this.model.getFirst(this.model));
};

netacad.views.PageView.prototype.isLast = function(page) {
  return (page == this.model.getLast(this.model));
};

netacad.views.PageView.prototype.next = function() {
  this.model.setCurrent(this.model.getNext(this.model.getCurrent()));
};

netacad.views.PageView.prototype.previous = function() {
  this.model.setCurrent(this.model.getPrevious(this.model.getCurrent()));
};

netacad.views.PageView.prototype.close = function() {
  this.document.removeEventListener("focus", this, true);
  this.document.removeEventListener("keydown", this, true);
  $(this.container).removeClass("active");
  netacad.dom.empty(this.pageContent);
  var selectedPage = document.querySelector(".selected.Page");
  if (selectedPage) {
    selectedPage.focus();
  }
};


/**
 * netacad.views.SplashView
 * @constructor
 */
netacad.views.SplashView = function(model, element, callback) {
  netacad.views.View.call(this, model, element);
  var that = this;
  this.callback = callback;
  this.element.setAttribute("aria-busy", true);
  $(this.element).addClass("loading");
  this.load("course/common/backgrounds/lang.json", function() {
    $(that.element).removeClass("loading");
    that.element.removeAttribute("aria-busy");
  });
  if (this.model.getBackground()) {
    if (this.callback) {
      this.callback();
    }
  } else {
    $(this.document.documentElement).addClass("splash");
    this.document.getElementById("login").setAttribute('aria-hidden', true);
    this.document.getElementById("splash").setAttribute('aria-hidden', false);
    this.document.getElementById("main").setAttribute('aria-hidden', true);
    this.build();
  }
};

netacad.extend(netacad.views.SplashView, netacad.views.View);

netacad.views.SplashView.prototype.load = function(url, callback) {
  var that = this;
  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      if (request.status == 200) {
        that.fromJSON(request.responseText);
      }
      callback();
    }
  };
  request.open("GET", url, true);
  request.send();
};

netacad.views.SplashView.prototype.fromJSON = function(s) {
  var o = null;
  try {
    o = JSON.parse(s);
  } catch (error) {
    console.warn("unable to parse");
  }
  if (o) {
    for (var k in o) {
      var e = this.document.getElementById(k + "-text");
      if (e) {
        netacad.dom.empty(e);
        e.appendChild(this.document.createTextNode(o[k]));
      }
    }
  }
};

netacad.views.SplashView.prototype.build = function() {
  var images = this.element.querySelectorAll("input");
  for (var i = 0; i < images.length; i++) {
    var image = images[i];
    image.addEventListener("click", this);
  }
};

netacad.views.SplashView.prototype.handleEvent = function(event) {
  if (event.type == "click") {
    if (event.target instanceof HTMLInputElement) {
      this.model.setBackground(event.target.id);
      $(this.document.documentElement).removeClass("splash");
      this.document.getElementById("login").setAttribute('aria-hidden', true);
      this.document.getElementById("splash").setAttribute('aria-hidden', true);
      this.document.getElementById("main").setAttribute('aria-hidden', false);
      event.stopPropagation();
      event.preventDefault();
      if (this.callback) {
        this.callback();
      }
    }
  }
};


/**
 * netacad.components
 */
netacad.provide("netacad.components");

/**
 * netacad.components.Component
 * @constructor
 */
netacad.components.Component = function(element) {

  if (element) {
    Object.defineProperty(this, "element", {
      value: element,
      writable: false,
      configurable: true
    });
    Object.defineProperty(element, "component", {
      value: this,
      writable: false,
      configurable: true
    });
  }

  if (this.element) {
    this.document = this.element.ownerDocument;
  }

  if (this.document) {
    this.view = this.document.defaultView;
  }

};


/**
 * netacad.components.Gestures
 * @constructor
 */
netacad.components.Gestures = function(element) {
  netacad.components.Component.call(this, element);
  this.identifier = null;
  this.screenX = null;
  this.screenY = null; 
  this.lastTap = Number.NEGATIVE_INFINITY;
  this.touchMoveFlag = false;
  this.doubleTapFlag = false;
  this.addListeners();
};

netacad.extend(netacad.components.Gestures, netacad.components.Component);

netacad.components.Gestures.prototype.MOVE_THRESHOLD = 10;
netacad.components.Gestures.prototype.DOUBLE_TAP_THRESHOLD = 500;
netacad.components.Gestures.prototype.LONG_PRESS_THRESHOLD = 1000;

netacad.components.Gestures.enable = function(element) {
  new netacad.components.Gestures(element);
  return element;
};

netacad.components.Gestures.disable = function(element) {
  element.component.removeListeners();
  delete element.component;
  return element;
};

netacad.components.Gestures.prototype.addListeners = function() {
  this.element.addEventListener("touchstart", this);
};

netacad.components.Gestures.prototype.removeListeners = function() {
  this.element.removeEventListener("touchstart", this);
};

netacad.components.Gestures.prototype.handleEvent = function(event) {
  if (event.type == "touchstart") {
    this.handleTouchStart(event);
  } else if (event.type == "touchmove") {
    this.handleTouchMove(event);
  } else if (event.type == "touchend" || event.type == "touchcancel") {
    this.handleTouchEnd(event);
  }
};

netacad.components.Gestures.prototype.handleTouchStart = function(event) {
  var anchor = event.changedTouches[0];
  this.identifier = anchor.identifier;
  this.screenX = anchor.screenX;
  this.screenY = anchor.screenY;
  this.doubleTapFlag = false;
  this.view.addEventListener("touchmove", this, true);
  this.view.addEventListener("touchend", this, true);
  this.view.addEventListener("touchcancel", this, true);
  var now = Date.now();
  if (now - this.lastTap < this.DOUBLE_TAP_THRESHOLD) {
    this.doubleTapFlag = true;
  }
  this.lastTap = now;
};

netacad.components.Gestures.prototype.handleTouchMove = function(event) {
  for (var i = 0; i < event.changedTouches.length; i++) {
    var touch = event.changedTouches[i];
    if (touch.identifier == this.identifier) {
      var deltaX = Math.abs(this.screenX - touch.screenX);
      var deltaY = Math.abs(this.screenY - touch.screenY);
      if (deltaX * deltaX + deltaY * deltaY > this.MOVE_THRESHOLD * this.MOVE_THRESHOLD) {
         this.touchMoveFlag = true;
      }
      break;
    }
  }
};

netacad.components.Gestures.prototype.handleTouchEnd = function(event) {
  for (var i = 0; i < event.changedTouches.length; i++) {
    var touch = event.changedTouches[i];
    if (touch.identifier == this.identifier) {
      this.view.removeEventListener("touchmove", this, true);
      this.view.removeEventListener("touchend", this, true);
      this.view.removeEventListener("touchcancel", this, true);
      if (!this.touchMoveFlag) {
        this.element.dispatchEvent(netacad.events.createEvent("tap"));
        if (this.doubleTapFlag) {
          this.element.dispatchEvent(netacad.events.createEvent("double-tap"));
          this.doubleTapFlag = false;
        }
      }
      this.touchMoveFlag = false;
      this.identifier = null;
      this.screenX = null;
      this.screenY = null;
      break;
    }
  }
};


/**
 * netacad.components.ScrollPane
 * @constructor
 */
netacad.components.ScrollPane = function(element) {

  netacad.components.Component.call(this, element);

  var that = this;
  
  this.scrollMin = 0;
  this.scrollMax = 0;
  this.scrollDelta = 12;
  this.wheelDelta = 2 * this.scrollDelta;
  this.delay = Math.round(1000 / 24);
  this.moved = false;

  this.content = element.querySelector(".scroll-pane-content");
  this.upButton = element.querySelector(".scroll-pane-up-button");
  this.downButton = element.querySelector(".scroll-pane-down-button");

  this.content.addEventListener('scroll', function(event) {
    that.update();
  });

  this.upButton.addEventListener("mousedown", function(event) {

    if (event.button > 1) {
      return;
    }

    var intervalID = window.setInterval(function() {
      that.scroll(that.scrollDelta);
    }, that.delay);

    function mouseHandler(event) {
      window.clearInterval(intervalID);
      window.removeEventListener("mouseup", mouseHandler, true);
      event.stopPropagation();
      event.preventDefault();
    }

    window.addEventListener("mouseup", mouseHandler, true);
    event.stopPropagation();
    event.preventDefault();
    that.scroll(that.scrollDelta);

  }, false);

  this.downButton.addEventListener("mousedown", function(event) {

    if (event.button > 1) {
      return;
    }

    var intervalID = window.setInterval(function() {
      that.scroll(-that.scrollDelta);
    }, that.delay);

    function mouseHandler(event) {
      window.clearInterval(intervalID);
      window.removeEventListener("mouseup", mouseHandler, true);
      event.stopPropagation();
      event.preventDefault();
    }

    window.addEventListener("mouseup", mouseHandler, true);
    event.stopPropagation();
    event.preventDefault();
    that.scroll(-that.scrollDelta);

  }, false);

  this.upButton.addEventListener("touchstart", function(event) {

    var anchor = event.changedTouches[0];
    var identifier = anchor.identifier;
    var intervalID = window.setInterval(function() {
      that.scroll(that.scrollDelta);
    }, that.delay);

    function touchHandler(event) {
      for (var i = 0; i < event.changedTouches.length; i++) {
        var touch = event.changedTouches[i];
        if (touch.identifier == identifier) {
          window.clearInterval(intervalID);
          window.removeEventListener("touchend", touchHandler, true);
          window.removeEventListener("touchcancel", touchHandler, true);
          event.stopPropagation();
          event.preventDefault();
          break;
        }
      }
    }

    window.addEventListener("touchend", touchHandler, true);
    window.addEventListener("touchcancel", touchHandler, true);

    that.scroll(that.scrollDelta);
    event.stopPropagation();
    event.preventDefault();

  }, false);

  this.downButton.addEventListener("touchstart", function(event) {

    var anchor = event.changedTouches[0];
    var intervalID = window.setInterval(function() {
      that.scroll(-that.scrollDelta);
    }, that.delay);

    function touchHandler(event) {
      for (var i = 0; i < event.changedTouches.length; i++) {
        var touch = event.changedTouches[i];
        if (touch.identifier == anchor.identifier) {
          window.clearInterval(intervalID);
          window.removeEventListener("touchend", touchHandler, true);
          window.removeEventListener("touchcancel", touchHandler, true);
          event.stopPropagation();
          event.preventDefault();
          break;
        }
      }
    }

    window.addEventListener("touchend", touchHandler, true);
    window.addEventListener("touchcancel", touchHandler, true);
    event.stopPropagation();
    event.preventDefault();
    that.scroll(-that.scrollDelta);

  }, false);

  this.content.addEventListener("mousedown", function(event){

    if (that.scrollMax == 0 || event.button > 1) {
      return;
    }

    var screenY = event.screenY;
    var scrollTop = that.content.scrollTop;
    that.moved = false;

    function mouseMoveHandler(event) {
      if (Math.abs(screenY - event.screenY) > that.scrollDelta) {
        that.content.scrollTop = scrollTop + (screenY - event.screenY);
        event.stopPropagation();
        event.preventDefault();
        that.moved = true;
      }
    }

    function mouseUpHandler(event) {
      window.removeEventListener("mousemove", mouseMoveHandler, true);
      window.removeEventListener("mouseup", mouseUpHandler, true);
      event.stopPropagation();
      event.preventDefault();
    }

    window.addEventListener("mousemove", mouseMoveHandler, true);
    window.addEventListener("mouseup", mouseUpHandler, true);
    event.stopPropagation();
    event.preventDefault();

  }, false);

  this.content.addEventListener("touchstart", function(event) {

    if (that.scrollMax == 0) {
      return;
    }

    var anchor = event.changedTouches[0];
    // some browsers (i.e. Safari) reuse the Touch objects,
    // so store the Touch's current properties
    var identifier = anchor.identifier;
    var screenY = anchor.screenY;
    var scrollTop = that.content.scrollTop;

    function touchMoveHandler(event) {
      for (var i = 0; i < event.changedTouches.length; i++) {
        var touch = event.changedTouches[i];
        if (touch.identifier == identifier) {
          if (Math.abs(screenY - touch.screenY) > that.scrollDelta) {
            that.content.scrollTop = scrollTop + (screenY - touch.screenY);
          }
          event.stopPropagation();
          event.preventDefault();
          break;
        }
      }
    }

    function touchEndHandler(event) {
      for (var i = 0; i < event.changedTouches.length; i++) {
        var touch = event.changedTouches[i];
        if (touch.identifier == identifier) {
          window.removeEventListener("touchmove", touchMoveHandler, true);
          window.removeEventListener("touchend", touchEndHandler, true);
          window.removeEventListener("touchcancel", touchEndHandler, true);
          event.stopPropagation();
          event.preventDefault();
          break;
        }
      }
    }

    window.addEventListener("touchmove", touchMoveHandler, true);
    window.addEventListener("touchend", touchEndHandler, true);
    window.addEventListener("touchcancel", touchEndHandler, true);
    event.stopPropagation();
    event.preventDefault();

  }, false);

  this.content.addEventListener("wheel", this);
  this.content.addEventListener("click", this, true);

  window.addEventListener("load", this);
  window.addEventListener("resize", this);

  this.update();

};

netacad.extend(netacad.components.ScrollPane, netacad.components.Component);

netacad.components.ScrollPane.prototype.handleEvent = function(event) {
  if (event.type == "load" || event.type == "resize") {
    this.update();
  } else if (event.type == "wheel") {
    this.handleWheel(event);
  } else if (event.type == "click") {
    if (this.moved) {
      // consume extraneous click
      event.stopPropagation();
      event.preventDefault();
      this.moved = false;
    }
  }
};

netacad.components.ScrollPane.prototype.scroll = function(delta) {
  this.content.scrollTop -= delta;
};

netacad.components.ScrollPane.prototype.update = function() {
  // allow for rounding errors when zooming
  this.scrollMax = Math.max(this.content.scrollHeight - this.content.clientHeight - 1, 0);
  this.upButton.disabled = (this.content.scrollTop <= this.scrollMin);
  this.downButton.disabled = (this.content.scrollTop >= this.scrollMax);
};

netacad.components.ScrollPane.prototype.reset = function() {
  this.content.scrollTop = 0;
  this.update();
};

netacad.components.ScrollPane.prototype.handleWheel = function(event) {
  if (event.deltaY < 0) {
    this.scroll(this.wheelDelta);
  } else {
    this.scroll(-this.wheelDelta);
  }
  if (this.content.scrollTop > this.scrollMin && this.content.scrollTop < this.scrollMax) {
    event.stopPropagation();
    event.preventDefault();
  }
};


// Google Analytics
if (netacad.environment.isProd()) {
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-54968464-1', 'auto');
  ga('require', 'displayfeatures');
}
