document.addEventListener('DOMContentLoaded', function () {
    // Initialize Intersection Observer for Scroll Reveal
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Stop observing once revealed
                // observer.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: "0px 0px -50px 0px" // Offset to trigger slightly before bottom
    });

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });

    // Add 'reveal' class to common elements if they don't have it
    // This automates the effect for major sections without manual HTML editing everywhere
    const autoRevealSelectors = [
        '.hero-text',
        '.hero-image',
        '.section-title',
        '.project-card',
        '.onesite-card',
        '.photo-item',
        '.blog-post',
        '.publication-card',
        '.book-card'
    ];

    autoRevealSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach((el, index) => {
            el.classList.add('reveal');
            // Add staggered delay for grids
            if (el.parentElement.classList.contains('grid') ||
                el.parentElement.classList.contains('projects-grid') ||
                el.parentElement.classList.contains('onesite-grid') ||
                el.parentElement.classList.contains('photo-grid')) {
                el.style.transitionDelay = `${index * 100}ms`;
            }
        });
        // Re-observe newly added classes
        document.querySelectorAll(selector).forEach(el => revealObserver.observe(el));
    });

    // Header Scroll Effect
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('floating-nav');
            } else {
                header.classList.remove('floating-nav');
            }
        });
    }
});
