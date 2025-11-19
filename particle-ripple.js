(function () {
    // Create and configure canvas
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '9999';
    // Modern blending for glowing effect
    canvas.style.mixBlendMode = 'screen';
    document.body.appendChild(canvas);

    let width, height;
    let particles = [];
    let glassElements = [];

    // Mouse state
    const mouse = { x: -1000, y: -1000, lastX: -1000, lastY: -1000 };

    // Color configuration based on page - Modern Neon Palette
    function getPageColor() {
        const path = window.location.pathname;

        if (path.includes('about')) return { hue: 210, sat: '100%', light: '60%' }; // Electric Blue
        if (path.includes('research')) return { hue: 280, sat: '90%', light: '65%' }; // Neon Purple
        if (path.includes('projects')) return { hue: 30, sat: '100%', light: '60%' }; // Neon Orange
        if (path.includes('photography')) return { hue: 320, sat: '90%', light: '60%' }; // Hot Pink
        if (path.includes('books')) return { hue: 50, sat: '100%', light: '55%' }; // Bright Amber
        if (path.includes('blog')) return { hue: 190, sat: '95%', light: '60%' }; // Cyan

        // Default (Home) - Dynamic Blue/Cyan
        return { hue: 200, sat: '100%', light: '60%' };
    }

    const baseColor = getPageColor();

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        // Cache glass elements for interaction
        glassElements = Array.from(document.querySelectorAll('.project-card, .experience-card, .education-card, .skills-category, .publication-card, .interest-card, .hero-image, .info-column'));
    }
    window.addEventListener('resize', resize);
    // Delay initial resize to ensure DOM is ready
    setTimeout(resize, 100);

    // Track mouse movement
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;

        // Spawn particles based on movement distance
        const dx = mouse.x - mouse.lastX;
        const dy = mouse.y - mouse.lastY;
        const dist = Math.hypot(dx, dy);

        if (dist > 2) {
            const count = Math.min(4, Math.floor(dist / 4));
            for (let i = 0; i < count; i++) {
                particles.push(new Particle(mouse.x, mouse.y));
            }
        }

        mouse.lastX = mouse.x;
        mouse.lastY = mouse.y;
    });

    class Particle {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 1.5 + 0.5;
            this.vx = Math.cos(angle) * speed;
            this.vy = Math.sin(angle) * speed;
            this.life = 1.0;
            this.decay = Math.random() * 0.02 + 0.01;
            this.size = Math.random() * 3 + 1;

            // Glass interaction state
            this.nearGlass = false;

            // Vary hue slightly for richness
            const hueVar = Math.random() * 40 - 20;
            this.color = `hsla(${baseColor.hue + hueVar}, ${baseColor.sat}, ${baseColor.light},`;
            this.glowColor = `hsla(${baseColor.hue + hueVar}, 100%, 80%,`;
        }

        update() {
            // Check proximity to glass elements
            this.nearGlass = false;
            for (const el of glassElements) {
                const rect = el.getBoundingClientRect();
                // Simple AABB check + margin
                if (this.x > rect.left - 50 && this.x < rect.right + 50 &&
                    this.y > rect.top - 50 && this.y < rect.bottom + 50) {
                    this.nearGlass = true;

                    // Slight attraction to glass center
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const dx = centerX - this.x;
                    const dy = centerY - this.y;
                    this.vx += dx * 0.001;
                    this.vy += dy * 0.001;
                    break;
                }
            }

            this.x += this.vx;
            this.y += this.vy;
            this.vx *= 0.95;
            this.vy *= 0.95;
            this.life -= this.decay;
        }

        draw(ctx) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * (this.nearGlass ? 1.5 : 1), 0, Math.PI * 2);

            if (this.nearGlass) {
                // Glowing effect near glass
                ctx.shadowBlur = 10;
                ctx.shadowColor = this.glowColor + '0.8)';
                ctx.fillStyle = this.glowColor + this.life + ')';
            } else {
                ctx.shadowBlur = 0;
                ctx.fillStyle = this.color + this.life + ')';
            }

            ctx.fill();
            ctx.shadowBlur = 0; // Reset
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        // Enable additive blending for "glowing" look
        ctx.globalCompositeOperation = 'lighter';

        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.update();
            p.draw(ctx);
            if (p.life <= 0) {
                particles.splice(i, 1);
            }
        }

        // Connect particles with lines
        ctx.lineWidth = 0.5;

        const limit = 80;

        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.hypot(dx, dy);

                if (dist < limit) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);

                    // Lines glow near glass too
                    if (particles[i].nearGlass || particles[j].nearGlass) {
                        ctx.strokeStyle = `hsla(${baseColor.hue}, 100%, 80%, ${0.2 * particles[i].life})`;
                    } else {
                        ctx.strokeStyle = `hsla(${baseColor.hue}, ${baseColor.sat}, ${baseColor.light}, ${0.1 * particles[i].life})`;
                    }

                    ctx.stroke();
                }
            }
        }

        ctx.globalCompositeOperation = 'source-over'; // Reset
        requestAnimationFrame(animate);
    }

    animate();
})();
