(function() {
  var autocompletes, loadAutoCompletes, loadUsers, sendMessage, typingArea, users;

  typingArea = $("textarea");

  autocompletes = [];

  users = [];

  loadUsers = function() {
    return $.ajax("./api/userlist", {
      type: "GET",
      dataType: "json",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("error in getting userlist: ", textStatus);
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
        return console.log("error in getting autocompletes: ", textStatus);
      },
      success: function(data, textStatus, jqXHR) {
        this.autocompletes = data;
        return console.log(this.autocompletes);
      }
    });
  };

  sendMessage = function(str) {};

  $(document).ready(function() {
    typingArea.autosize();
    $(document).keypress(function(e) {
      switch (e.keyCode) {
        case 9:
        case 67:
        case 99:
          return $("body").toggleClass("sidebarhidden");
        case 13:
          return typingArea.focus();
        default:
          return console.log("unknown keycode", e.keyCode);
      }
    });
    $("#inputbox").keypress(function(e) {
      e.stopPropagation();
      switch (e.keyCode) {
        case 9:
          $("body").toggleClass("sidebarhidden");
          return console.log("tab");
        case 13:
          e.preventDefault();
          sendMessage(typingArea.text);
          return $(typingArea).val("");
        case 27:
          console.log("esc");
          $("body").removeClass("sidebarhidden");
          return $("#sidebar").focus();
        default:
          return console.log(e.keyCode);
      }
    });
    return $.ajax("./api/connect/104.236.63.94/oceanman/", {
      type: "GET",
      dataType: "html",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log(textStatus);
      },
      success: function(data, textStatus, jqXHR) {
        console.log(data);
        loadUsers();
        return loadAutoCompletes();
      }
    });
  });

}).call(this);
