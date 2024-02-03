let isMinimized = false;
        
        function toggleChatbot() {
            const chatbot = document.getElementById('chat-container');
            const minimizeButton = document.getElementById('minimize-button');
            if (isMinimized) {
                chatbot.style.height = '400px'; // Adjust the height as needed
                minimizeButton.innerHTML = '-';
            } else {
                chatbot.style.height = '50px'; // Adjust the height as needed
                minimizeButton.innerHTML = '+';
            }
            isMinimized = !isMinimized;
        }
        
        function scrollToBottom() {
            const chatContent = document.getElementById('chat-content');
            chatContent.scrollTop = chatContent.scrollHeight;
        }
        function sendMessage() {
            const userMessage = document.getElementById('user-input').value.toLowerCase(); // Convert user input to lowercase
            if (userMessage) {
                let response = 'I\'m sorry, I don\'t understand. Please ask a valid question.';
                for (const keyword in commandResponses) {
                    // Convert each keyword to lowercase for case-insensitive matching
                    if (userMessage.includes(keyword.toLowerCase())) {
                        response = commandResponses[keyword];
                        break; // Stop searching once a match is found
                    }
                }
                addMessage(response, 'chatbot');
                addMessage(userMessage, 'user');
                document.getElementById('user-input').value = '';
                scrollToBottom();
            }
        }
        
        const commandResponses = {
            
            
            'Hi' : 'Hello welcome to J-Tech my name is Jiji an AI who is willing to assist you, how can i help you?',
            'Hello' : 'Hi welcome to J-tech my name is Jiji an AI who is willing to assist you, how can i help you?',
            'Name' : 'Hi my name is Jiji, How can i help ?', 
            
        };
        
        function sendMessage() {
            const userMessage = document.getElementById('user-input').value;
            if (userMessage) {
                addMessage(userMessage, 'user');
        
                let response = 'I\'m sorry, I don\'t understand. Please ask a valid question.';
                for (const keyword in commandResponses) {
                    const regex = new RegExp(keyword, 'i'); 
                    if (regex.test(userMessage)) {
                        response = commandResponses[keyword];
                        break;
                    }
                }
        
                if (response) {
                    
                    addMessage(response, 'chatbot');
                } else {
                 
                    const defaultResponse = 'I can assist you with our offer services. How can I help you today?';
                    addMessage(defaultResponse, 'chatbot');
                }
        
                document.getElementById('user-input').value = '';
            }
        }
        
        function addMessage(message, sender) {
            const chatContent = document.getElementById('chat-content');
            const messageElement = document.createElement('div');
            messageElement.className = `message ${sender}`;
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = message;
            messageElement.appendChild(messageContent);
            chatContent.appendChild(messageElement);
        
        
            chatContent.scrollTop = chatContent.scrollHeight;
        }
        document.getElementById('user-input').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });
        