/**
 * UI Interactions Script
 * Handles scroll effects, animations, and other UI enhancements.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.querySelector('.header');

    const handleScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Check initial state

    // Intersection Observer for Fade-in Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    // Select elements to animate
    const animatedElements = document.querySelectorAll('.content-text, .project-card, .onesite-card, .experience-card, .education-card, .publication-card, .interest-card, .photo-item');

    animatedElements.forEach(el => {
        // Add a base class for animation if not already present
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });
});
