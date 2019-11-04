document.addEventListener('DOMContentLoaded', () => {

    //set channel name to sessionStorage
    

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    
    socket.on('connect', () => {
        socket.emit("channel get");

        const button = document.querySelector('#send_btn');
        const message = document.querySelector('#message');
        
        message.addEventListener("keypress", (event) => {
            if (event.keyCode === 13) {
                event.preventDefault();
                button.click();
            }
        })
        
        button.onclick = () => {
        const new_msg = message.value;
        const fromChannel = sessionStorage.getItem("channel_name");
        let get_time = new Date();
        const time = get_time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                    
        socket.emit('send message', {'new_msg': new_msg, 'time': time, 'channel_name': fromChannel});
        message.value = "";
        }


        
    
        });

        socket.on("send channel", data => {
            sessionStorage.setItem("channel_name", data.channel_name);
            sessionStorage.setItem("user_name", data.username);
    
        });

    



    socket.on('show message', data => {
        const channel_name = data["channel_name"];

        if (channel_name == sessionStorage.getItem("channel_name")) {

            const liMsg = document.createElement('li');
            const div1 = document.createElement('div');
            div1.setAttribute("id", "msg");

            const img = document.createElement('img');
            img.setAttribute("src", `../static/imgs/${data['image']}`);
            div1.appendChild(img);

            const div2 = document.createElement('div');
            div2.innerHTML = `<div class="the-message"><h5>${data["username"]}</h5><h5 id="msg">${data["message"]}</h5><h6 id="time">${data["date"]}</h6></div>`
            div1.append(div2);

            liMsg.append(div1);

            document.querySelector('#msgss').append(liMsg);


        }


    });

        
});








