document.addEventListener('DOMContentLoaded', () => {

    //set channel name to sessionStorage
    

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    
    socket.on('connect', () => {
        socket.emit("channel get");

        const button = document.querySelector('#send_btn');
        const message = document.querySelector('#message');

        button.onclick = () => {
            const new_msg = message.value;
            const fromChannel = sessionStorage.getItem("channel_name");
                    
            socket.emit('send message', {'new_msg': new_msg, 'channel_name': fromChannel});
            message.value = "";
            }

        const channel_button = document.querySelector('#button_channel');
        const channel_create = document.querySelector('#new_channel');

        channel_button.onclick = () => {
            const new_channel = channel_create.value;
            const onUser = sessionStorage.getItem("user_name");

            socket.emit('new channel', {'new_channel': new_channel, 'username': onUser});
            channel_create.value = "";
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

    socket.on('show channel', data => {
        const user_name = data["username"];

        if (user_name == sessionStorage.getItem("user_name")) {

            const a = document.createElement('a');
            const divList = document.querySelector('#list');

            a.setAttribute("href", "{{ url_for('channel', channel_name=channel) }}")

            a.innerHTML = `<h5 id="channel_name">#_${data["channel_name"]}</h5>`

            divList.append(a);



        }


    });

        
});








