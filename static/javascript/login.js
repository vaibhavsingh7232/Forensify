document.addEventListener('DOMContentLoaded', function() {
    // Get the selected platform from localStorage
    const platform = localStorage.getItem('selectedPlatform') || 'default';
    const platformIcon = document.getElementById('platform-icon');
    const platformName = document.getElementById('platform-name');
    
    // Set platform-specific styling and text
    switch(platform) {
        case 'instagram':
            platformIcon.className = 'fab fa-instagram';
            platformName.textContent = 'Login with Instagram';
            document.querySelector('.login-btn').style.backgroundColor = '#E1306C';
            break;
        case 'reddit':
            platformIcon.className = 'fab fa-reddit';
            platformName.textContent = 'Login with Reddit';
            document.querySelector('.login-btn').style.backgroundColor = '#FF5700';
            break;
        case 'twitter':
            platformIcon.className = 'fab fa-twitter';
            platformName.textContent = 'Login with X (Twitter)';
            document.querySelector('.login-btn').style.backgroundColor = '#1DA1F2';
            break;
        default:
            platformIcon.className = 'fab fa-user';
            platformName.textContent = 'Login';
    }
    
    // Form submission
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const messageElement = document.getElementById('message');
        
        // Simple validation
        if (username && password) {
            messageElement.textContent = `Connecting to ${platformName.textContent}...`;
            messageElement.className = 'message success';
            
            // Simulate API call
            setTimeout(() => {
                messageElement.textContent = `Successfully connected to ${platformName.textContent}!`;
                // In a real app, you would redirect to the dashboard
            }, 1500);
        } else {
            messageElement.textContent = 'Please enter both username and password';
            messageElement.className = 'message error';
        }
    });
});