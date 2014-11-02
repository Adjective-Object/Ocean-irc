(function() {
  var BACKTICK, DOWN, ENTER, ESC, J, K, TAB, UP, autocompletes, loadAutoCompletes, loadUsers, numChannels, sendMessage, shiftSidebarFocus, sideBar, sideBarFocus, typingArea, users;

  ENTER = 13;

  TAB = 9;

  ESC = 27;

  BACKTICK = 192;

  UP = 38;

  DOWN = 40;

  J = 74;

  K = 75;

  typingArea = $("textarea");

  sideBar = $("#sidebar");

  sideBarFocus = 0;

  numChannels = $("#sidebar a").length;

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

  shiftSidebarFocus = function(index) {
    sideBarFocus = (numChannels + sideBarFocus + index) % numChannels;
    return $("#sidebar a:nth-of-type(" + (sideBarFocus + 1) + ")").focus();
  };

  $(document).ready(function() {
    typingArea.autosize();
    $(document).keydown(function(e) {
      switch (e.keyCode) {
        case BACKTICK:
          return $("body").toggleClass("sidebarhidden");
        case ENTER:
          return typingArea.focu1s();
        default:
          return console.log("uk body", e.keyCode);
      }
    });
    typingArea.keydown(function(e) {
      e.stopPropagation();
      switch (e.keyCode) {
        case BACKTICK:
          $("body").toggleClass("sidebarhidden");
          return shiftSidebarFocus(0);
        case TAB:
          e.preventDefault();
          $("body").removeClass("sidebarhidden");
          shiftSidebarFocus(0);
          return console.log("tab");
        case ENTER:
          e.preventDefault();
          sendMessage(typingArea.text);
          return $(typingArea).val("");
        case ESC:
          console.log("esc");
          $("body").removeClass("sidebarhidden");
          return shiftSidebarFocus(0);
        default:
          return console.log("uk textbox", e.keyCode);
      }
    });
    sideBar.keydown(function(e) {
      e.stopPropagation();
      e.preventDefault;
      switch (e.keyCode) {
        case TAB:
          e.preventDefault();
          return shiftSidebarFocus(1);
        case ENTER:
          return sideBar.focus();
        case UP:
        case K:
          return shiftSidebarFocus(-1);
        case DOWN:
        case J:
          return shiftSidebarFocus(1);
        default:
          return console.log("uk inputbox", e.keyCode);
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
