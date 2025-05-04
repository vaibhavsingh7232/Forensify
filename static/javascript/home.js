document.addEventListener('DOMContentLoaded', function() {
    const optionCards = document.querySelectorAll('.option-card');
    
    optionCards.forEach(card => {
        card.addEventListener('click', function() {
            const platform = this.getAttribute('data-platform');
            // In a real app, this would redirect to the appropriate analysis page
            alert(`Redirecting to ${platform.charAt(0).toUpperCase() + platform.slice(1)} analysis tools...`);
            
            // Example of actual redirection:
            // window.location.href = `/${platform}-analyzer.html`;
        });
    });
    
    // Add animation to cards when page loads
    setTimeout(() => {
        optionCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.animation = `fadeInUp 0.5s ease forwards ${index * 0.1}s`;
        });
    }, 100);
});

// Add keyframe animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);