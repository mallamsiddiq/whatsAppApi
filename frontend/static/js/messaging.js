document.addEventListener("DOMContentLoaded", function () {
    const user_username = JSON.parse(document.getElementById('user_username').textContent);
    const roomID = JSON.parse(document.getElementById('room-id').textContent);

    // const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomID}/?token=${'1234567890vgty'}`)
    const socket = new WebSocket(`wss://${window.location.host}/ws/chat/${roomID}/`);
    // const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomID}/`, [
    //     'authorization', 'Bearer', '1234567890vgty',
    // ]);

    socket.addEventListener("open", (event) => {
        console.log("WebSocket connection opened:");
    });

    socket.addEventListener("message", (event) => {
        const data = JSON.parse(event.data);
        console.log("WebSocket message received: ");
        appendMessage(data.sender, data.content, data.sender === user_username, data.attachment);
    });

    socket.addEventListener("close", (event) => {
        console.log("WebSocket connection closed:");
    });

    document.getElementById("send-button").addEventListener("click", () => {
        const messageInput = document.getElementById("message-input");
        const message = messageInput.value.trim();
        const fileInput = document.getElementById("file-input");
        const file = fileInput.files[0];

        if (message !== "" || file) {
            const data = {
                message: message,
                attachment: null,
                isOwnMessage: true,
            };

            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    data.attachment = e.target.result.split(",")[1]; // Base64-encoded file data
                    sendMessage(data);
                };
                reader.readAsDataURL(file);
            } else {
                sendMessage(data);
            }

            messageInput.value = "";
            fileInput.value = "";
        }
    });

    function sendMessage(data) {
        socket.send(JSON.stringify(data));
    }

    function appendMessage(sender, message, isOwnMessage, attachment = null) {
        const chatArea = document.getElementById("chat-area");
        const template = document.getElementById("message-template");
        
        const clone = document.importNode(template.content, true);

        // Modify the content of the cloned template
        clone.querySelector(".tmplt-sender-name").textContent = sender;
        clone.querySelector(".tmplt-message-body").textContent = message;

        if (isOwnMessage) {
            clone.querySelector(".tmplt-sender-name").textContent = "You";
            clone.querySelector(".message").classList.add("own-message");
            clone.querySelector(".message-body").classList.add("text-end");
        }

        if (attachment) {
            clone.querySelector("#tmplt-img").src = `${attachment}`;
        } else {
            clone.querySelector("#tmplt-img").classList.add("d-none");
        }        

        chatArea.appendChild(clone);
    }
});
