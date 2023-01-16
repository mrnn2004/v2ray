function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

let username = getCookie("username");
let password = getCookie("password");
if(username != "" && password != ""){
    var send_login_cookie = new WebSocket("ws://156.255.1.217:3000");
    send_login_cookie.onopen = function() {
        send_login_cookie.send("|+34>-)-*|" + username + "|<-->|" + password);
    };
    send_login_cookie.onmessage = function (evt) { 
        var received_msg = evt.data;
        if(received_msg == "username or password not found ..."){
            alert(received_msg);
            send_login_cookie.close();
        }
        else{
            document.getElementById("main").innerHTML = received_msg;
            send_login_cookie.close();
        }
    }
}


if(username == "" || password == ""){
    var send_login_input = new WebSocket("ws://156.255.1.217:3000");
    send_login_input.onmessage = function (evt) {
        var received_msg = evt.data;
        if(received_msg == "username or password not found ..."){
            alert(received_msg);
        }
        else{
            var username = document.getElementById("username").value;
            var password = document.getElementById("password").value;
            document.cookie = "username="+username;
            document.cookie = "password="+password;
            document.getElementById("main").innerHTML = received_msg;
            send_login_input.close();
        }
    };
    function login(){
        var user = document.getElementById("username").value;
        var pass = document.getElementById("password").value;
        send_login_input.send("|+34>-)-*|" + user + "|<-->|" + pass);
    }
    
}


function delete_user(env){
    let logedin_username = getCookie("username");
    let logedin_password = getCookie("password");
    let link = env;
    var delete_user = new WebSocket("ws://156.255.1.217:3000")
    delete_user.onopen = function(){
        delete_user.send("<-delete" + logedin_username + "/*/|" + logedin_password + "/*/|" + link);
    };
}



function server_add_user(){
    let logedin_username = getCookie("username");
    let logedin_password = getCookie("password");
    var add_user = new WebSocket("ws://156.255.1.217:3000")
    name_user = document.getElementById("name").value;
    traffic = document.getElementById("traffic").value;
    time = document.getElementById("time").value;
    add_user.onopen = function () {
        add_user.send("<-login" + logedin_username + "/*/|" + logedin_password + "/*/|" + name_user + "/*/|" + traffic + "/*/|" + time);
    };
}



var qrcode = new QRCode("qrcode");
function makeCode(text) {      
qrcode.makeCode(text);
document.getElementById("qrcode").setAttribute("style", "display:block;")
}

function hide(){
    document.getElementById("qrcode").setAttribute("style", "display:none;")
}



function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
        alert("copied");
        return window.clipboardData.setData("Text", text);

    }
    else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            alert("copied");
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        }
        catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            alert("copied");
            return prompt("Copy to clipboard: Ctrl+C, Enter", text);
        }
        finally {
            document.body.removeChild(textarea);
        }
    }
}



