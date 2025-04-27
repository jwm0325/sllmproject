function sendMessage() {
    const messageInput = document.getElementById('user-message');
    const chatBox = document.getElementById('chat-box');

    const data = {
        message: messageInput.value
    };

    if (data.message.trim() === '') return;

    chatBox.innerHTML += "<p><strong>You:</strong> " + data.message + "</p>";

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/chat/",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        data: JSON.stringify(data),
    }).done(function(response) {
        chatBox.innerHTML += "<p><strong>Bot:</strong> " + response.response + "</p>";
        messageInput.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
        console.log(response);
    }).fail(function(response) {
        alert("fail: " + JSON.stringify(response));
    });
}