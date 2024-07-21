def get_html():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Chat App</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        html, body {
            height: 100%;
            margin: 0; /* Remove any default margin */
        }

        #chat-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
            background: white;
        }

        #chatbox {
            flex-grow: 1; /* Makes the chatbox take up available space */
            border: 1px solid #ccc;
            padding: 10px;
            overflow-y: scroll;
        }

        #message-container {
            display: flex;
            padding: 10px;
            border-top: 1px solid #ccc;
        }

        #message {
            flex: 1;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-right: 10px;
        }

        button {
            padding: 5px 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="chatbox"></div>
        <div id="message-container">
            <input type="text" id="message" class="form-control" placeholder="Type your message">
            <button class="btn btn-primary" onclick="sendMessage()">Send</button>
        </div>
    </div>

<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        var ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            var data = JSON.parse(event.data);
            
            var messageElement = document.createElement('p');
            // Checks if it's a user message or a response
            if (data.username) {
                messageElement.innerHTML = marked.parse(data.username + ': ' + data.message); 
            } else {
                // If no username, assumes it's the user's question
                messageElement.innerHTML = marked.parse('You: ' + data.message); 
            }
            document.getElementById('chatbox').appendChild(messageElement);
        };

        function sendMessage() {
            var message = document.getElementById('message').value;
            // Adds the question to the chatbox before sending
            var messageElement = document.createElement('p');
            messageElement.innerHTML = marked.parse('You: ' + message); 
            document.getElementById('chatbox').appendChild(messageElement);

            var data = {
                "message": message
            };
            ws.send(JSON.stringify(data));
            document.getElementById('message').value = '';
        }
    </script>
</body>
</html>
    """