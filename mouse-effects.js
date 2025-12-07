/**
 * Mouse Effects - Advanced Interactive Effects
 * Includes: Custom Cursor, 3D Tilt, Mouse Parallax, Spotlight
 */

document.addEventListener('DOMContentLoaded', () => {
    // ====== 1. CUSTOM ANIMATED CURSOR ======
    const cursorDot = document.createElement('div');
    cursorDot.className = 'cursor-dot';
    const cursorRing = document.createElement('div');
    cursorRing.className = 'cursor-ring';
    document.body.appendChild(cursorDot);
    document.body.appendChild(cursorRing);

    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;

        // Dot follows instantly
        cursorDot.style.left = `${mouseX}px`;
        cursorDot.style.top = `${mouseY}px`;
    });

    // Ring follows with delay using requestAnimationFrame
    function animateRing() {
        const ease = 0.15;
        ringX += (mouseX - ringX) * ease;
        ringY += (mouseY - ringY) * ease;

        cursorRing.style.left = `${ringX}px`;
        cursorRing.style.top = `${ringY}px`;

        requestAnimationFrame(animateRing);
    }
    animateRing();

    // Cursor hover states
    const interactiveElements = document.querySelectorAll('a, button, .intro-card, .project-card, .onesite-card');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursorDot.classList.add('cursor-hover');
            cursorRing.classList.add('cursor-hover');
        });
        el.addEventListener('mouseleave', () => {
            cursorDot.classList.remove('cursor-hover');
            cursorRing.classList.remove('cursor-hover');
        });
    });

    // Click feedback
    document.addEventListener('mousedown', () => {
        cursorDot.classList.add('cursor-click');
        cursorRing.classList.add('cursor-click');
    });
    document.addEventListener('mouseup', () => {
        cursorDot.classList.remove('cursor-click');
        cursorRing.classList.remove('cursor-click');
    });

    // ====== 2. 3D TILT EFFECT ON CARDS ======
    const tiltCards = document.querySelectorAll('.intro-card, .project-card, .onesite-card');

    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // X position within element
            const y = e.clientY - rect.top;  // Y position within element

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10; // Tilt intensity
            const rotateY = (centerX - x) / 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
        });
    });

    // ====== 3. MOUSE-BASED PARALLAX ======
    const heroSection = document.querySelector('.hero-section');
    const heroText = document.querySelector('.hero-text');
    const heroImage = document.querySelector('.hero-image');

    if (heroSection) {
        heroSection.addEventListener('mousemove', (e) => {
            const rect = heroSection.getBoundingClientRect();
            const x = (e.clientX - rect.left - rect.width / 2) / rect.width;
            const y = (e.clientY - rect.top - rect.height / 2) / rect.height;

            if (heroText) {
                heroText.style.transform = `translate(${x * 20}px, ${y * 20}px)`;
            }
            if (heroImage) {
                heroImage.style.transform = `translate(${x * -30}px, ${y * -30}px)`;
            }
        });

        heroSection.addEventListener('mouseleave', () => {
            if (heroText) heroText.style.transform = 'translate(0, 0)';
            if (heroImage) heroImage.style.transform = 'translate(0, 0)';
        });
    }

    // ====== 4. SPOTLIGHT REVEAL EFFECT ======
    const spotlight = document.createElement('div');
    spotlight.className = 'spotlight-overlay';
    document.body.appendChild(spotlight);

    document.addEventListener('mousemove', (e) => {
        spotlight.style.background = `radial-gradient(circle 150px at ${e.clientX}px ${e.clientY}px, rgba(255, 45, 85, 0.08), transparent 70%)`;
    });

    // ====== 5. ICON PARALLAX IN CARDS ======
    const cardIcons = document.querySelectorAll('.intro-card-icon');
    cardIcons.forEach(icon => {
        const card = icon.closest('.intro-card');
        if (card) {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left - rect.width / 2) / rect.width;
                const y = (e.clientY - rect.top - rect.height / 2) / rect.height;
                icon.style.transform = `translate(${x * 15}px, ${y * 15}px) scale(1.1)`;
            });
            card.addEventListener('mouseleave', () => {
                icon.style.transform = 'translate(0, 0) scale(1)';
            });
        }
    });
});
