document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    // Event listener for send button click
    sendButton.addEventListener('click', sendMessage);

    // Event listener for Enter key press in input field
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });

    // Function to handle sending messages to backend
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        // Append user message to chat box
        appendMessage(message, 'user');
        userInput.value = '';

        // Send message to backend via POST request
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Append bot's response to chat box
            appendMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('Oops! Something went wrong.', 'bot');
        });
    }

    // Function to append messages to the chat box
    function appendMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const icon = document.createElement('i');
        icon.classList.add('fas', sender === 'user' ? 'fa-user' : 'fa-robot');
        
        messageDiv.appendChild(icon);

        const text = document.createTextNode(message);
        messageDiv.appendChild(text);

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});