(function() {
  var activeChannel, autocompletes, buildMsg, channels, fetchMessages, handleLinkClick, initChans, joinChannel, loadAutoCompletes, me, messages, numChannels, populateChatBuffer, setActiveChannel, sideBar, sideBarFocus, typingArea;

  typingArea = $("textarea");

  sideBar = $("#sidebar");

  sideBarFocus = 0;

  numChannels = $("#sidebar a").length;

  initChans = ["general", "knurds", "mabois", "urmum"];

  messages = {};

  autocompletes = [];

  channels = {};

  activeChannel = "";

  me = "oceanman";

  window.ircapi_sendMessage = function(message) {
    var d;
    d = {};
    d["usr"] = me["usename"];
    d["msg"] = message;
    d["channel"] = activeChannel;
    d["timestamp"] = Date.now();
    buildMsg(d);
    return messages["#" + activeChannel].push(d);
  };

  setActiveChannel = function(chan) {
    activeChannel = chan;
    window.location.hash = "#" + chan;
    $(".ticked").removeClass("ticked");
    $("#sidebar a[href='#" + chan + "']").addClass("ticked");
    $("#topic").text(("#" + chan + " :: ") + channels["#" + chan]["topic"]);
    $("#chatcontents").empty();
    console.log(chan, messages);
    populateChatBuffer(messages["#" + chan]);
    return $("#sidebar a[href='#" + chan + "']").removeAttr("data-notif");
  };

  populateChatBuffer = function(msgs) {
    var msg, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = msgs.length; _i < _len; _i++) {
      msg = msgs[_i];
      _results.push(buildMsg(msg));
    }
    return _results;
  };

  handleLinkClick = function(evt) {
    setActiveChannel(this.hash.substring(1));
    return evt.preventDefault();
  };

  joinChannel = function(channame) {
    return $.ajax("./api/join/" + channame + "/", {
      type: "GET",
      dataType: "json",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("error in getting userlist: ", errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        if (data["private"]) {
          $("<a href=\"#" + channame + "\">#" + channame + "</a>").insertAfter($("#sidebar #privateChannels")).click(handleLinkClick);
        } else {
          $("<a href=\"#" + channame + "\">#" + channame + "</a>").insertAfter($("#sidebar #publicChannels")).click(handleLinkClick);
        }
        messages["#" + channame] = [];
        channels["#" + channame] = data;
        console.log(channels);
        if (window.location.hash === void 0) {
          return setActiveChannel(channame);
        } else if (window.location.hash === ("#" + channame)) {
          return setActiveChannel(channame);
        }
      }
    });
  };

  buildMsg = function(msg) {
    var c, icon, n, obj, scroll;
    c = $("#chatcontents");
    scroll = c.scrollTop() + c.height() >= c.get(0).scrollHeight;
    icon = "./static/imgdump/placeholder.gif";
    n = $(("<section class='post' sender='" + msg['usr'] + "'>") + ("<img src='" + icon + "'/>") + ("<section class='name'>" + msg['usr'] + "</section>") + ("<section class='timestamp'>" + msg['timestamp'] + "</section>") + "<section class='body'></section>" + "</section>");
    obj = $(".body", n);
    obj.text(msg['msg']).html();
    obj.html(obj.html().replace(/\n/g, '<br/>'));
    c.append(n);
    if (scroll) {
      return c.scrollTop(c.get(0).scrollHeight);
    }
  };

  fetchMessages = function() {
    return $.ajax("./api/getMessages", {
      type: "GET",
      dataType: "json",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("error in getting userlist: ", errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        var dval, ln, msg, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          msg = data[_i];
          messages[msg["channel"]].push(msg);
          if (msg["channel"].substring(1) === activeChannel) {
            _results.push(buildMsg(msg));
          } else {
            ln = $("#sidebar a[href='" + msg["channel"] + "']");
            dval = ln.attr("data-notif");
            if (dval === void 0) {
              _results.push(ln.attr("data-notif", 1));
            } else {
              _results.push(ln.attr("data-notif", parseInt(dval) + 1));
            }
          }
        }
        return _results;
      }
    });
  };

  $(document).ready(function() {
    return $.ajax("./api/connect/104.236.63.94/oceanman/oceanman/", {
      type: "GET",
      dataType: "html",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log(textStatus);
      },
      success: function(data, textStatus, jqXHR) {
        var c, _i, _len, _ref;
        me = data;
        loadAutoCompletes();
        _ref = initChans.reverse();
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          c = _ref[_i];
          joinChannel(c);
        }
        initChans.reverse();
        return setInterval(fetchMessages, 100);
      }
    });
  });

  loadAutoCompletes = function() {
    return $.ajax("./api/autocompletes", {
      type: "GET",
      dataType: "json",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("error in getting autocompletes: ", errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        this.autocompletes = data;
        return console.log(this.autocompletes);
      }
    });
  };

}).call(this);
