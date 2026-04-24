(function () {
    // Skip on touch devices — no mouse cursor, no need for particles
    if (window.matchMedia('(hover: none)').matches) return;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;mix-blend-mode:screen';
    document.body.appendChild(canvas);

    let width, height;
    const MAX_PARTICLES = 40;
    let particles = [];

    function getPageColor() {
        const path = window.location.pathname;
        if (path.includes('projects'))   return { hue: 350, sat: '100%', light: '50%' };
        if (path.includes('research'))   return { hue: 0,   sat: '100%', light: '40%' };
        if (path.includes('about'))      return { hue: 0,   sat: '0%',   light: '90%' };
        if (path.includes('photography'))return { hue: 0,   sat: '0%',   light: '100%' };
        if (path.includes('books'))      return { hue: 0,   sat: '0%',   light: '80%' };
        if (path.includes('blog'))       return { hue: 0,   sat: '0%',   light: '70%' };
        return { hue: 355, sat: '100%', light: '50%' };
    }
    const baseColor = getPageColor();

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize, { passive: true });
    resize();

    const mouse = { x: -1000, y: -1000, lastX: -1000, lastY: -1000 };

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;

        const dist = Math.hypot(mouse.x - mouse.lastX, mouse.y - mouse.lastY);
        if (dist > 3 && particles.length < MAX_PARTICLES) {
            const count = Math.min(2, Math.floor(dist / 6));
            for (let i = 0; i < count; i++) {
                particles.push(new Particle(mouse.x, mouse.y));
            }
        }
        mouse.lastX = mouse.x;
        mouse.lastY = mouse.y;
    }, { passive: true });

    class Particle {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 1.2 + 0.3;
            this.vx = Math.cos(angle) * speed;
            this.vy = Math.sin(angle) * speed;
            this.life = 1.0;
            this.decay = Math.random() * 0.025 + 0.015;
            this.size = Math.random() * 2.5 + 0.5;
            const hueVar = Math.random() * 30 - 15;
            this.color = `hsla(${baseColor.hue + hueVar},${baseColor.sat},${baseColor.light},`;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.vx *= 0.94;
            this.vy *= 0.94;
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
        ctx.globalCompositeOperation = 'lighter';

        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update();
            particles[i].draw(ctx);
            if (particles[i].life <= 0) particles.splice(i, 1);
        }

        ctx.globalCompositeOperation = 'source-over';
        requestAnimationFrame(animate);
    }

    animate();
})();
