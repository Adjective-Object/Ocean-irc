(function() {
  var BACKTICK, DOWN, ENTER, ESC, J, K, TAB, UP, autocompletes, currentusers, shiftSidebarFocus, sideBar, sideBarFocus, typingArea;

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

  autocompletes = [];

  currentusers = [];

  shiftSidebarFocus = function(index) {
    var numChannels;
    numChannels = $("#sidebar a").length;
    sideBarFocus = (numChannels + sideBarFocus + index) % numChannels;
    return $("#sidebar a:nth-of-type(" + (sideBarFocus + 1) + ")").focus();
  };

  $(document).ready(function() {
    $(document).keydown(function(e) {
      switch (e.keyCode) {
        case BACKTICK:
          return $("body").toggleClass("sidebarhidden");
        case ENTER:
          typingArea.focus();
          return e.preventDefault();
      }
    });
    typingArea.keydown(function(e) {
      e.stopPropagation();
      switch (e.keyCode) {
        case BACKTICK:
          e.preventDefault();
          $("body").toggleClass("sidebarhidden");
          if (!$("body").hasClass("sidebarhidden")) {
            return shiftSidebarFocus(0);
          }
          break;
        case TAB:
          e.preventDefault();
          $("body").removeClass("sidebarhidden");
          return shiftSidebarFocus(0);
        case ENTER:
          if (!e.shiftKey) {
            e.preventDefault();
            if (typingArea.val() !== "") {
              window.ircapi_sendMessage(typingArea.val());
              return $(typingArea).val("");
            }
          }
          break;
        case ESC:
          $("body").removeClass("sidebarhidden");
          return shiftSidebarFocus(0);
      }
    });
    sideBar.keydown(function(e) {
      e.stopPropagation();
      e.preventDefault();
      switch (e.keyCode) {
        case BACKTICK:
          $("body").addClass("sidebarhidden");
          return typingArea.focus();
        case TAB:
          return shiftSidebarFocus(1);
        case ENTER:
          return $(":focus").click();
        case UP:
        case K:
          return shiftSidebarFocus(-1);
        case DOWN:
        case J:
          return shiftSidebarFocus(1);
      }
    });
    sideBar.focusin(function(e) {
      return $("#sidebar").addClass("containsFocus");
    });
    return sideBar.focusout(function(e) {
      return $("#sidebar").removeClass("containsFocus");
    });
  });

}).call(this);
