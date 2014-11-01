typingArea = $("textarea")

$(document).ready ->
	typingArea.autosize();

	#bind global keys
	$(document).keypress (e) -> 
		switch e.keyCode
			when 9, 67, 99  #TAB or C or c
				$("body").toggleClass("sidebarhidden");
			when 13 #ENTER
				e.preventDefault();
				e.stopPropagation();
				if typingArea.is(":focus")
					console.log("...");
					sendMessage(typingArea.text);
					typingArea.text = "";
				else
					typingArea.focus();
			else
				console.log("unknown keycode", e.keyCode);				


	$.ajax "./api/connect/104.236.63.94/oceanman/", 
		type: "GET"
		dataType: "html"
		error: (jqXHR, textStatus, errorThrown) ->
        	console.log(textStatus);
		success: (data, textStatus, jqXHR) ->
			console.log(data);

sendMessage (str) ->
	$.get -> "./api/connect/"