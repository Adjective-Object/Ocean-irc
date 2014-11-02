(function() {
  var autocompletes, channels, initChans, initialJoin, joinChannel, loadAutoCompletes, numChannels, sideBar, sideBarFocus, typingArea, users;

  typingArea = $("textarea");

  sideBar = $("#sidebar");

  sideBarFocus = 0;

  numChannels = $("#sidebar a").length;

  initChans = ["general", "mabois", "knurds"];

  autocompletes = [];

  users = [];

  channels = [];

  window.ircapi_sendMessage = function(str) {};

  $("#sidebar a").click(function(evt) {
    var channel;
    evt.preventDefault();
    channel = this.hash.substring(1);
    window.location.hash = this.hash;
    $(".ticked").removeClasss(".ticked");
    return this.addClass(".ticked");
  });

  joinChannel = function(channame) {
    return $.ajax("./api/join/" + channame + "/", {
      type: "GET",
      dataType: "json",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("error in getting userlist: ", errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        $("#sidebar #publicChannels").after($("<a href=\"#" + channame + "\">#" + channame + "</a>"));
        return users.push(data);
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
        var c, channel, _i, _len, _ref;
        console.log(data);
        loadAutoCompletes();
        _ref = initChans.reverse();
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          c = _ref[_i];
          joinChannel(c);
        }
        return channel = channels[0];
      }
    });
  });

  initialJoin = function() {
    console.log("./api/userlist/" + channel + "/");
    joinChannel();
    return $.ajax("./api/join/" + channel + "/", {
      type: "GET",
      dataType: "json",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("error in getting userlist: ", errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        this.users = data;
        return console.log(this.users);
      }
    });
  };

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
