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
    document.body.appendChild(canvas);

    let width, height;
    let particles = [];

    // Mouse state
    const mouse = { x: -1000, y: -1000, lastX: -1000, lastY: -1000 };

    // Color configuration based on page - Matching styles.css variables
    function getPageColor() {
        const path = window.location.pathname;

        if (path.includes('about')) return { hue: 160, sat: '84%', light: '39%' }; // Emerald (Green)
        if (path.includes('research')) return { hue: 260, sat: '60%', light: '60%' }; // Purple
        if (path.includes('projects')) return { hue: 24, sat: '95%', light: '53%' }; // Orange
        if (path.includes('photography')) return { hue: 330, sat: '70%', light: '60%' }; // Pink
        if (path.includes('books')) return { hue: 45, sat: '90%', light: '50%' }; // Amber/Yellow
        if (path.includes('blog')) return { hue: 220, sat: '80%', light: '60%' }; // Blue
        if (path.includes('one_page_websites')) return { hue: 0, sat: '0%', light: '80%' }; // White/Grey

        // Default (Home) - Cyan/Blue
        return { hue: 190, sat: '90%', light: '50%' }; 
    }

    const baseColor = getPageColor();

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }
    window.addEventListener('resize', resize);
    resize();

    // Track mouse movement
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;

        // Spawn particles based on movement distance
        const dx = mouse.x - mouse.lastX;
        const dy = mouse.y - mouse.lastY;
        const dist = Math.hypot(dx, dy);

        if (dist > 2) {
            const count = Math.min(3, Math.floor(dist / 5)); // Reduced count for cleaner look
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
            const speed = Math.random() * 1.0 + 0.2; // Slower, more fluid
            this.vx = Math.cos(angle) * speed;
            this.vy = Math.sin(angle) * speed;
            this.life = 1.0;
            this.decay = Math.random() * 0.015 + 0.005; // Slower decay
            this.size = Math.random() * 2.5 + 0.5; // Slightly smaller particles

            // Vary hue slightly for richness
            const hueVar = Math.random() * 30 - 15;
            this.color = `hsla(${baseColor.hue + hueVar}, ${baseColor.sat}, ${baseColor.light},`;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.vx *= 0.96; // Friction for fluid feel
            this.vy *= 0.96;
            this.life -= this.decay;
        }

        draw(ctx) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color + this.life + ')';
            ctx.fill();
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.update();
            p.draw(ctx);
            if (p.life <= 0) {
                particles.splice(i, 1);
            }
        }

        // Connect particles with lines if they are close (field effect)
        // Use the base color for lines but very transparent
        ctx.strokeStyle = `hsla(${baseColor.hue}, ${baseColor.sat}, ${baseColor.light}, 0.1)`;
        ctx.lineWidth = 0.5;
        
        // Optimization: Limit connections checks if too many particles
        const limit = particles.length > 100 ? 50 : 80; // Connection distance

        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.hypot(dx, dy);

                if (dist < limit) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    animate();
})();
