#keycode defs
ENTER = 13;
TAB = 9
ESC = 27

UP = 38
DOWN = 40
J = 74
K = 75

#special elems of the text
typingArea = $("textarea");
sideBar = $("#sidebar");
sideBarFocus = 0;
numChannels = $("#sidebar a").length

#data pulled fro, the server
autocompletes = [];
users = [];


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

shiftSidebarFocus = (index) ->
	sideBarFocus = (numChannels + sideBarFocus + index) % numChannels
	$("#sidebar a:nth-of-type("+sideBarFocus+")").focus()


# On Document Ready
$(document).ready ->
	typingArea.autosize();

	#keypresses that make it to the top level
	$(document).keydown (e) -> 
		switch e.keyCode
			when TAB
				$("body").toggleClass("sidebarhidden");
			when ENTER #ENTER
				typingArea.focus();
			else
				console.log("uk body", e.keyCode);

	#keypresses on the input box
	typingArea.keydown (e)->
		e.stopPropagation();
		switch e.keyCode
			when TAB  #TAB
				e.preventDefault();
				$("body").removeClass("sidebarhidden");
				sideBar.focus();
				console.log("tab")
			when ENTER #ENTER
				e.preventDefault();
				sendMessage(typingArea.text);
				$(typingArea).val("");
			when ESC #ESC
				console.log("esc");
				#switch focus from text bar to the sidebar
				$("body").removeClass("sidebarhidden");
				sideBar.focus();
			else
				console.log("uk textbox", e.keyCode);


	#navigating in the sidebar
	sideBar.keydown (e) -> 
		e.stopPropagation();
		e.preventDefault
		switch e.keyCode
			when ENTER
				#TODO loading the right pane
				sideBar.focus()
			when UP, K
				shiftSidebarFocus(-1)
			when DOWN, J, TAB
				shiftSidebarFocus(1)
			else
				console.log("uk inputbox", e.keyCode);

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