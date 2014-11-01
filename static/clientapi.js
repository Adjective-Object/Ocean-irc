(function() {
  var typingArea;

  typingArea = $("textarea");

  $(document).ready(function() {
    typingArea.autosize();
    $(document).keypress(function(e) {
      switch (e.keyCode) {
        case 9:
        case 67:
        case 99:
          return $("body").toggleClass("sidebarhidden");
        case 13:
          e.preventDefault();
          e.stopPropagation();
          if (typingArea.is(":focus")) {
            console.log("...");
            sendMessage(typingArea.text);
            return typingArea.text = "";
          } else {
            return typingArea.focus();
          }
          break;
        default:
          return console.log("unknown keycode", e.keyCode);
      }
    });
    return $.ajax("./api/connect/104.236.63.94/oceanman/", {
      type: "GET",
      dataType: "html",
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log(textStatus);
      },
      success: function(data, textStatus, jqXHR) {
        return console.log(data);
      }
    });
  });

  sendMessage(function(str) {
    return $.get(function() {
      return "./api/connect/";
    });
  });

}).call(this);
