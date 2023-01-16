/*
var ws = new WebSocket("ws://156.255.1.217:3000");

ws.onopen = function() {
    ws.send('update')
};

ws.onmessage = function (evt) { 
    var received_msg = evt.data;
    if(received_msg == "username or password not found ..."){
        alert(received_msg)
    }
    else if(received_msg == "you loged in ..."){
        console.log("login")
        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;
        document.cookie = "username="+username;
        document.cookie = "password="+password;
    }
    else if(received_msg == "hello"){
        console.log(received_msg)
    }
    else{
        document.getElementById("main").innerHTML = received_msg;
    }
};
*/


window.onbeforeunload = closingCode;
function closingCode(){
    ws.close();
    return null;
}