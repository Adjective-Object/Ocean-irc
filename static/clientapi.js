(function() {
  var activeChannel, autocompletes, fetchMessages, handleLinkClick, initChans, joinChannel, loadAutoCompletes, messages, numChannels, setActiveChannel, sideBar, sideBarFocus, typingArea, users;

  typingArea = $("textarea");

  sideBar = $("#sidebar");

  sideBarFocus = 0;

  numChannels = $("#sidebar a").length;

  initChans = ["general", "mabois", "knurds"];

  messages = {};

  autocompletes = [];

  users = [];

  activeChannel = "";

  window.ircapi_sendMessage = function(str) {};

  setActiveChannel = function(chan) {
    activeChannel = chan;
    window.location.hash = "#" + chan;
    $(".ticked").removeClass("ticked");
    return $("#sidebar a[href='#" + chan + "']").addClass("ticked");
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
        if (window.location.hash === void 0) {
          setActiveChannel(channame);
        } else if (window.location.hash === ("#" + channame)) {
          setActiveChannel(channame);
        }
        messages[channame] = [];
        return users.push(data["users"]);
      }
    });
  };

  fetchMessages = function() {
    return $.ajax("./api/getMessages", {
      type: "GET",
      dataType: "json",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("error in getting userlist: ", errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        var msg, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          msg = data[_i];
          messages[msg["channel"]].push(msg);
          if (msg["channel"] === activeChannel) {
            _results.push(buildMsg(msg));
          } else {
            _results.push(void 0);
          }
        }
        return _results;
      }
    });
  };

  $(document).ready(function() {
    return $.ajax("./api/connect/104.236.63.94/oceanman/", {
      type: "GET",
      dataType: "html",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log(textStatus);
      },
      success: function(data, textStatus, jqXHR) {
        var c, _i, _len, _ref;
        console.log(data);
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
