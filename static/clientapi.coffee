typingArea = $("textarea")

autocompletes = []
users = []

loadUsers = ->
	$.ajax "./api/userlist",
		type: "GET"
		dataType: "json"
		error: (jqXHR, textStatus, errorThrown) ->
			console.log("error in getting userlist: ", textStatus)
		success: (data, textStatus, jqXHR) ->
			this.users = data
			console.log(this.users)

loadAutoCompletes = ->
	$.ajax "./api/autocompletes",
		type: "GET"
		dataType: "json"
		error: (jqXHR, textStatus, errorThrown) ->
			console.log("error in getting autocompletes: ", textStatus)
		success: (data, textStatus, jqXHR) ->
			this.autocompletes = data
			console.log(this.autocompletes)

sendMessage = (str) ->
	return

# On Document Ready
$(document).ready ->
	typingArea.autosize();

	#keypresses that make it to the top level
	$(document).keypress (e) -> 
		switch e.keyCode
			when 9, 67, 99  #TAB or C or c
				$("body").toggleClass("sidebarhidden");
			when 13 #ENTER
				typingArea.focus();
			else
				console.log("unknown keycode", e.keyCode);

	#keypresses on the input box
	$("#inputbox").keypress (e)->
		e.stopPropagation();
		switch e.keyCode
			when 9  #TAB
				$("body").toggleClass("sidebarhidden");
				console.log("tab")
			when 13 #ENTER
				e.preventDefault();
				sendMessage(typingArea.text);
				$(typingArea).val("");
			when 27 #ESC
				console.log("esc");
				#switch focus from text bar to the sidebar
				$("body").removeClass("sidebarhidden");
				$("#sidebar").focus();
			else
				console.log(e.keyCode)

	#sending a "connect to server" message on connect
	$.ajax "./api/connect/104.236.63.94/oceanman/", 
		type: "GET"
		dataType: "html"
		error: (jqXHR, textStatus, errorThrown) ->
        	console.log(textStatus);
		success: (data, textStatus, jqXHR) ->
			console.log(data);
			loadUsers();
			loadAutoCompletes();