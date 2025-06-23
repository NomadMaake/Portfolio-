document.addEventListener('DOMContentLoaded', () => {
    // Hamburger menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Contact form submission
    const contactForm = document.getElementById('contact-form');
    const formMessage = document.getElementById('form-message');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            formMessage.textContent = 'Thank you for your message! We will get back to you soon.';
            contactForm.reset();
        });
    }

    // Slideshow for New Arrivals with seamless fade transition
    let slideIndex = 0;
    const slides = document.querySelectorAll('.slideshow-container .slide');
    if (slides.length > 0) {
        slides.forEach((slide, i) => {
            slide.style.opacity = i === 0 ? '1' : '0';
            slide.style.display = 'block';
            slide.style.transition = 'opacity 1s';
        });

        setInterval(() => {
            slides[slideIndex].style.opacity = '0';
            slideIndex = (slideIndex + 1) % slides.length;
            slides[slideIndex].style.opacity = '1';
        }, 3500);
    }

    // Checkout Modal and Yoco Integration
    const checkoutButtons = document.querySelectorAll('.checkout-button');
    const yoco = new YocoSDK({
        // IMPORTANT: Replace with your actual Yoco public key
        publicKey: 'pk_test_a6fDE84F392F42597d74',
    });

    checkoutButtons.forEach(button => {
        button.addEventListener('click', () => {
            const card = button.closest('.option-card');
            const priceText = card.querySelector('.price').textContent;
            
            // Extract the number from the price string (e.g., "R4,500" -> 4500)
            const amountInCents = parseInt(priceText.replace(/[^0-9]/g, '')) * 100;

            if (isNaN(amountInCents)) {
                alert("This item requires custom pricing. Please contact us to complete your order.");
                return;
            }

            yoco.showPopup({
                amountInCents: amountInCents,
                currency: 'ZAR',
                name: 'Elite Tiles & Construction',
                description: `Purchase of ${card.querySelector('h3').textContent}`,
                callback: function (result) {
                    // This function is called when the payment process is complete
                    // result.error is null if payment is successful
                    if (result.error) {
                        const errorMessage = result.error.message;
                        alert("Payment failed: " + errorMessage);
                    } else {
                        alert("Payment successful! Your transaction ID is " + result.id);
                        // Here you would typically send `result.id` to your backend 
                        // to verify the transaction and update your order system.
                    }
                }
            });
        });
    });
});