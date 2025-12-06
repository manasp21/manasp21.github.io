document.addEventListener('DOMContentLoaded', () => {
    // 1. Intersection Observer for Entrance Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-fade-up, .animate-scale-in, .intro-card');
    animatedElements.forEach(el => {
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });

    // 2. Magnetic Buttons Effect
    const magneticButtons = document.querySelectorAll('.magnetic-btn, .nav-links a, .cta-button');

    magneticButtons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            // Strength of the magnetic pull
            const strength = 0.3;

            btn.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0, 0)';
        });
    });

    // 3. Scroll-Linked Parallax & Blur
    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;

        // Hero Section Parallax
        const heroSection = document.querySelector('.hero-section');
        const heroText = document.querySelector('.hero-text');
        const heroImage = document.querySelector('.hero-image');

        if (heroSection && scrolled < window.innerHeight) {
            // Parallax for text (moves slower)
            if (heroText) {
                heroText.style.transform = `translateY(${scrolled * 0.3}px)`;
                heroText.style.opacity = 1 - (scrolled / 600);
                heroText.style.filter = `blur(${scrolled / 100}px)`;
            }

            // Parallax for image (moves faster)
            if (heroImage) {
                heroImage.style.transform = `translateY(${scrolled * 0.5}px)`;
                heroImage.style.opacity = 1 - (scrolled / 500);
            }
        }

        // Glass Panels Blur-out on exit
        const glassPanels = document.querySelectorAll('.glass-panel, .intro-card');
        glassPanels.forEach(panel => {
            const rect = panel.getBoundingClientRect();
            const viewportHeight = window.innerHeight;

            // If element is nearing the top of the viewport
            if (rect.top < 100 && rect.bottom > 0) {
                const blurAmount = (100 - rect.top) / 10;
                const opacityAmount = 1 - ((100 - rect.top) / 300);
                // panel.style.filter = `blur(${blurAmount}px)`; // Optional: can be performance heavy
                // panel.style.opacity = opacityAmount;
            } else {
                // panel.style.filter = 'none';
                // panel.style.opacity = 1;
            }
        });
    });
});
