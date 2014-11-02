#special elems of the text
typingArea = $("textarea");
sideBar = $("#sidebar");
sideBarFocus = 0;
numChannels = $("#sidebar a").length

#init args
initChans = ["general", "mabois", "knurds"]

#data pulled from the server
autocompletes = [];
users = [];
channels = [];

window.ircapi_sendMessage = (str) ->
	return

$("#sidebar a").click (evt) ->
	evt.preventDefault()
	channel = this.hash.substring(1);

	window.location.hash = this.hash;
	$(".ticked").removeClasss(".ticked");
	this.addClass(".ticked");
	
joinChannel = (channame) ->
	$.ajax ("./api/join/"+channame+"/"),
	type: "GET"
	dataType: "json"
	error: (jqXHR, textStatus, errorThrown) ->
		console.log("error in getting userlist: ", errorThrown)
	success: (data, textStatus, jqXHR) ->
		$("#sidebar #publicChannels").after(
			$("<a href=\"##{channame}\">##{channame}</a>")
		);
		users.push(data)

# On Document Ready
$(document).ready ->
	#sending a "connect to server" message on connect
	$.ajax "./api/connect/104.236.63.94/oceanman/", 
		type: "GET"
		dataType: "html"
		error: (jqXHR, textStatus, errorThrown) ->
        	console.log(textStatus);
		success: (data, textStatus, jqXHR) ->
			console.log(data);
			#load users and autocompletes when connected
			loadAutoCompletes();
			(joinChannel(c) for c in initChans.reverse())
			channel = channels[0]


initialJoin = ->
	console.log("./api/userlist/"+channel+"/");
	joinChannel()
	$.ajax ("./api/join/"+channel+"/"),
		type: "GET"
		dataType: "json"
		error: (jqXHR, textStatus, errorThrown) ->
			console.log("error in getting userlist: ", errorThrown)
		success: (data, textStatus, jqXHR) ->
			this.users = data
			console.log(this.users)

loadAutoCompletes = ->
	$.ajax "./api/autocompletes",
		type: "GET"
		dataType: "json"
		error: (jqXHR, textStatus, errorThrown) ->
			console.log("error in getting autocompletes: ", errorThrown)
		success: (data, textStatus, jqXHR) ->
			this.autocompletes = data
			console.log(this.autocompletes)
