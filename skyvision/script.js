// script.js
document.addEventListener("DOMContentLoaded", function () {
    // Simple contact form handler
    const form = document.getElementById('contact-form');
    const msg = document.getElementById('form-message');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            msg.textContent = "Thank you for contacting SkyVision! We'll get back to you soon.";
            form.reset();
        });
    }

    // Buy Now button handler
    document.querySelectorAll('.buy-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            alert('Thank you for your interest! Online orders coming soon.');
        });
    });
});