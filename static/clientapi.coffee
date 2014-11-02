#special elems of the text
typingArea = $("textarea");
sideBar = $("#sidebar");
sideBarFocus = 0;
numChannels = $("#sidebar a").length

#init args
initChans = ["general", "knurds", "mabois", "urmum"];
messages = {};

#data pulled from the server
autocompletes = [];
channels = {};
activeChannel = ""

me = "oceanman"

window.ircapi_sendMessage = (message) ->
    d = {};
    d["usr"] = me["username"];
    d["msg"] = message;
    d["channel"] = activeChannel;
    d["timestamp"] = Date.now();

    
    buildMsg(d);
    messages["##{activeChannel}"].push(d);

    pushMessageToServer(message, activeChannel)

setActiveChannel = (chan) ->
    activeChannel = chan;
    window.location.hash = "##{chan}";
    $(".ticked").removeClass("ticked");
    $("#sidebar a[href='##{chan}']").addClass("ticked");

    $("#topic").text("##{chan} :: " + channels["##{chan}"]["topic"]);
    $("#chatcontents").empty();
    console.log(chan, messages);
    populateChatBuffer(messages["##{chan}"]);
    
    $("#sidebar a[href='##{chan}']").removeAttr("data-notif");


populateChatBuffer = (msgs) ->
    for msg in msgs
        buildMsg(msg);

handleLinkClick = (evt) ->
    setActiveChannel(this.hash.substring(1));
    evt.preventDefault();

joinChannel = (channame) ->
    $.ajax ("./api/join/"+channame+"/"),
        type: "GET"
        dataType: "json"
        error: (jqXHR, textStatus, errorThrown) ->
            console.log("error in joining channel: ", errorThrown)
        success: (data, textStatus, jqXHR) ->
            if (data["private"])
                $("<a href=\"##{channame}\">##{channame}</a>").insertAfter(
                    $("#sidebar #privateChannels")).click(handleLinkClick);
            else
                $("<a href=\"##{channame}\">##{channame}</a>").insertAfter(
                    $("#sidebar #publicChannels")).click(handleLinkClick);

            messages["##{channame}"] = [];
            channels["##{channame}"] = data;
            console.log(channels);

            if (window.location.hash == undefined)
                setActiveChannel(channame); 
            else if (window.location.hash == "##{channame}")
                setActiveChannel(channame)

buildMsg = (msg) ->
    c = $("#chatcontents");

    scroll = c.scrollTop() + c.height() >= c.get(0).scrollHeight;
    icon = "./static/imgdump/placeholder.gif";
    n = $("<section class='post' sender='#{msg['usr']}'>"+
            "<img src='#{icon}'/>"+
            "<section class='name'>#{msg['usr']}</section>"+
            "<section class='timestamp'>#{msg['timestamp']}</section>"+
            "<section class='body'></section>"+
        "</section>");
    obj = $(".body",n)
    obj.text(msg['msg']).html();
    obj.html(obj.html().replace(/\n/g,'<br/>'));
    c.append(n);
    if scroll
        c.scrollTop(c.get(0).scrollHeight)

fetchMessages = ->
    $.ajax ("./api/getMessages"),
        type: "GET"
        dataType: "json"
        error: (jqXHR, textStatus, errorThrown) ->
            console.log("error in getting messages: ", errorThrown)
        success: (data, textStatus, jqXHR) ->
            for msg in data
                messages[msg["channel"]].push(msg)
                if (msg["channel"].substring(1) == activeChannel)
                    buildMsg(msg)
                else
                    ln = $("#sidebar a[href='#{(msg["channel"])}']");
                    dval = ln.attr("data-notif");
                    if dval == undefined
                        ln.attr("data-notif", 1);
                    else
                        ln.attr("data-notif", parseInt(dval)+1);

pushMessageToServer = (message, channel) ->
    $.ajax ("./api/pushMessage/#{channel}"),
        type: "POST"
        dataType: "json"
        data: {"message": message}
        error: (jqXHR, textStatus, errorThrown) ->
            console.log("error in getting messages: ", errorThrown)
        success: (data, textStatus, jqXHR) ->
            console.log("posted, cool");


# On Document Ready
$(document).ready ->
    #sending a "connect to server" message on connect
    $.ajax "./api/connect/104.236.63.94/oceanman/oceanman/", 
        type: "GET"
        dataType: "html"
        error: (jqXHR, textStatus, errorThrown) ->
            console.log(textStatus);
        success: (data, textStatus, jqXHR) ->
            me = data
            #load users and autocompletes when connected
            loadAutoCompletes();
            (joinChannel(c) for c in initChans.reverse())
            initChans.reverse();

            setInterval(fetchMessages, 100);

loadAutoCompletes = ->
    $.ajax "./api/autocompletes",
        type: "GET"
        dataType: "json"
        error: (jqXHR, textStatus, errorThrown) ->
            console.log("error in getting autocompletes: ", errorThrown)
        success: (data, textStatus, jqXHR) ->
            this.autocompletes = data
            console.log(this.autocompletes)
