document.addEventListener('DOMContentLoaded', () => {

    //set channel name to sessionStorage
    

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    
    socket.on('connect', () => {
        socket.emit("channel get");

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








