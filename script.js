/**
 * Quantum Portfolio - Interactive JavaScript
 * Atomic Physics + Music + Poetry Inspired Interactions
 */

class QuantumPortfolio {
    constructor() {
        this.init();
        this.bindEvents();
        this.createParticles();
        this.initScrollAnimations();
    }

    init() {
        // Initialize on DOM load
        this.mobileMenu = document.getElementById('mobile-menu');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.sections = document.querySelectorAll('section[id]');
        this.quantumCards = document.querySelectorAll('.quantum-card');
        
        // Configuration
        this.particleCount = window.innerWidth < 768 ? 15 : 30;
        this.isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        // Advanced simulation tracking
        this.quantumElements = {
            electronClouds: document.querySelectorAll('.electron-cloud'),
            waveFunctions: document.querySelectorAll('.wave-function'),
            harmonicSeries: document.querySelectorAll('.harmonic-series'),
            entanglementPairs: document.querySelectorAll('.entanglement-pair')
        };
    }

    bindEvents() {
        // Mobile menu toggle
        const mobileMenuBtn = document.querySelector('[onclick="toggleMobileMenu()"]');
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleMobileMenu();
            });
        }

        // Smooth scrolling for navigation links (only for anchor links on same page)
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    this.smoothScrollTo(target);
                }
                this.closeMobileMenu();
            });
        });

        // Handle navigation for multi-page links
        document.querySelectorAll('a[href$=".html"]').forEach(link => {
            link.addEventListener('click', () => {
                this.closeMobileMenu();
            });
        });

        // Scroll events
        window.addEventListener('scroll', this.throttle(() => {
            this.updateActiveNavigation();
            this.handleParallaxEffects();
        }, 16));

        // Resize events
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize();
        }, 250));

        // Quantum card interactions
        this.quantumCards.forEach(card => {
            card.addEventListener('mouseenter', () => this.handleCardHover(card, true));
            card.addEventListener('mouseleave', () => this.handleCardHover(card, false));
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.mobileMenu.classList.contains('hidden')) {
                this.closeMobileMenu();
            }
        });
    }

    toggleMobileMenu() {
        if (this.mobileMenu) {
            this.mobileMenu.classList.toggle('hidden');
            
            // Update ARIA attributes for accessibility
            const isHidden = this.mobileMenu.classList.contains('hidden');
            this.mobileMenu.setAttribute('aria-hidden', isHidden);
        }
    }

    closeMobileMenu() {
        if (this.mobileMenu && !this.mobileMenu.classList.contains('hidden')) {
            this.mobileMenu.classList.add('hidden');
            this.mobileMenu.setAttribute('aria-hidden', 'true');
        }
    }

    smoothScrollTo(target) {
        const targetPosition = target.offsetTop - 80; // Account for fixed nav
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 800;
        let start = null;

        const animation = (currentTime) => {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const run = this.easeInOutQuad(timeElapsed, startPosition, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        };

        requestAnimationFrame(animation);
    }

    easeInOutQuad(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    updateActiveNavigation() {
        let current = '';
        const scrollPosition = window.pageYOffset + 100;

        this.sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        this.navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    }

    createParticles() {
        if (this.isReducedMotion) return;

        const particlesContainer = document.querySelector('.quantum-particles');
        if (!particlesContainer) return;

        // Clear existing particles
        particlesContainer.innerHTML = '';

        for (let i = 0; i < this.particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Randomize particle properties
            const randomLeft = Math.random() * 100;
            const randomDelay = Math.random() * 8;
            const randomDuration = 6 + Math.random() * 4;
            
            particle.style.left = randomLeft + '%';
            particle.style.animationDelay = randomDelay + 's';
            particle.style.animationDuration = randomDuration + 's';
            
            particlesContainer.appendChild(particle);
        }
    }

    handleParallaxEffects() {
        if (this.isReducedMotion) return;

        const scrolled = window.pageYOffset;
        const particles = document.querySelectorAll('.particle');
        const rate = scrolled * -0.1;

        particles.forEach(particle => {
            particle.style.transform = `translateY(${rate}px)`;
        });
    }

    handleCardHover(card, isHovering) {
        if (this.isReducedMotion) return;

        if (isHovering) {
            // Add quantum glow effect with red colors
            card.style.boxShadow = `
                0 25px 50px rgba(220, 38, 38, 0.3),
                0 0 30px rgba(239, 68, 68, 0.4),
                inset 0 0 25px rgba(220, 38, 38, 0.15)
            `;
            card.classList.add('quantum-glow');
        } else {
            // Reset box shadow
            card.style.boxShadow = '';
            card.classList.remove('quantum-glow');
        }
    }

    initScrollAnimations() {
        if (this.isReducedMotion) return;

        // Intersection Observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, observerOptions);

        // Observe quantum cards and sections
        this.quantumCards.forEach(card => observer.observe(card));
        
        // Add fade-in animation class
        const style = document.createElement('style');
        style.textContent = `
            .animate-fade-in {
                animation: fadeInUp 0.8s ease-out forwards;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(style);
    }

    handleResize() {
        // Update particle count based on screen size
        const newParticleCount = window.innerWidth < 768 ? 15 : 30;
        if (newParticleCount !== this.particleCount) {
            this.particleCount = newParticleCount;
            this.createParticles();
        }

        // Close mobile menu if screen becomes large
        if (window.innerWidth >= 768) {
            this.closeMobileMenu();
        }
    }

    // Utility functions
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    debounce(func, wait, immediate) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }
}

// Enhanced Quantum Particle System with Red Theme
class QuantumParticleSystem {
    constructor(container) {
        this.container = container;
        this.particles = [];
        this.mouse = { x: 0, y: 0 };
        this.canvas = null;
        this.ctx = null;
        this.animationId = null;
        
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.init();
        }
    }

    init() {
        // Create canvas for more advanced particle effects
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.style.position = 'absolute';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '1';
        
        this.resize();
        this.createParticles();
        this.animate();
        
        this.container.appendChild(this.canvas);
        
        // Event listeners
        window.addEventListener('resize', () => this.resize());
        document.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const particleCount = Math.min(50, Math.floor(window.innerWidth / 20));
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2,
                hue: 0 + Math.random() * 20 // Red color range
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;
            
            // Mouse interaction
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 100) {
                const force = (100 - distance) / 100;
                particle.vx += (dx / distance) * force * 0.01;
                particle.vy += (dy / distance) * force * 0.01;
            }
            
            // Apply friction
            particle.vx *= 0.99;
            particle.vy *= 0.99;
            
            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = `hsla(${particle.hue}, 80%, 60%, ${particle.opacity})`;
            this.ctx.fill();
            
            // Add glow effect
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = `hsla(${particle.hue}, 80%, 60%, 0.9)`;
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        });
        
        // Connect nearby particles
        this.connectParticles();
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }

    connectParticles() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 80) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.strokeStyle = `rgba(220, 38, 38, ${0.3 * (1 - distance / 80)})`;
                    this.ctx.lineWidth = 1.5;
                    this.ctx.stroke();
                }
            }
        }
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.canvas && this.canvas.parentNode) {
            this.canvas.parentNode.removeChild(this.canvas);
        }
    }
}

// Music visualization for poetry section
class MusicVisualizer {
    constructor(container) {
        this.container = container;
        this.notes = ['♪', '♫', '♬', '♭', '♯'];
        this.activeNotes = [];
        
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.init();
        }
    }

    init() {
        this.createFloatingNotes();
        
        // Add interaction
        this.container.addEventListener('mouseenter', () => {
            this.createBurst();
        });
    }

    createFloatingNotes() {
        setInterval(() => {
            if (this.activeNotes.length < 5) {
                this.createNote();
            }
        }, 2000);
    }

    createNote() {
        const note = document.createElement('div');
        note.className = 'music-note';
        note.textContent = this.notes[Math.floor(Math.random() * this.notes.length)];
        
        // Random positioning
        note.style.left = Math.random() * 80 + 10 + '%';
        note.style.top = Math.random() * 60 + 20 + '%';
        note.style.fontSize = (Math.random() * 0.5 + 1) + 'rem';
        note.style.animationDelay = Math.random() * 2 + 's';
        note.style.animationDuration = (Math.random() * 4 + 6) + 's';
        
        this.container.appendChild(note);
        this.activeNotes.push(note);
        
        // Remove after animation
        setTimeout(() => {
            if (note.parentNode) {
                note.parentNode.removeChild(note);
                this.activeNotes = this.activeNotes.filter(n => n !== note);
            }
        }, 8000);
    }

    createBurst() {
        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                this.createNote();
            }, i * 200);
        }
    }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Main portfolio functionality
    new QuantumPortfolio();
    
    // Enhanced particle system for hero
    const heroSection = document.querySelector('section:first-of-type');
    if (heroSection) {
        new QuantumParticleSystem(heroSection);
    }
    
    // Initialize advanced simulations
    initAdvancedSimulations();
    
    // Music visualizer for poetry section  
    const poetrySection = document.getElementById('poetry');
    if (poetrySection) {
        new MusicVisualizer(poetrySection);
    }
    
    // Add loading animation
    document.body.classList.add('loaded');
    
    // Console easter egg for fellow developers
    console.log(`
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🌌 Quantum Portfolio 🌌                    ║
    ║                                                              ║
    ║  "In the quantum realm of code, where particles dance       ║
    ║   between possibility and reality, we find the poetry       ║
    ║   of computation."                                           ║
    ║                                                              ║
    ║  Built with atomic precision and musical harmony             ║
    ║  by Manas Pandey - Physics Student exploring AI             ║
    ║                                                              ║
    ║  Inspired by: Quantum Mechanics • Music • Poetry            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    `);
});

// Advanced Physics Simulations Controller
function initAdvancedSimulations() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    
    // Quantum field simulation
    initQuantumField();
    
    // Electron cloud interactions
    initElectronClouds();
    
    // Wave function interactions
    initWaveFunctions();
    
    // Harmonic series interactions
    initHarmonicSeries();
    
    // Entanglement visualization
    initQuantumEntanglement();
    
    // Poetry meter visualization
    initPoetryMeter();
}

// Quantum Field Background Animation
function initQuantumField() {
    const quantumField = document.querySelector('.quantum-field');
    if (!quantumField) return;
    
    let mouseX = 0, mouseY = 0;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth) * 100;
        mouseY = (e.clientY / window.innerHeight) * 100;
        
        quantumField.style.background = `
            radial-gradient(circle at ${mouseX}% ${mouseY}%, rgba(220, 38, 38, 0.05) 0%, transparent 50%),
            radial-gradient(circle at ${100-mouseX}% ${100-mouseY}%, rgba(220, 38, 38, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(220, 38, 38, 0.02) 0%, transparent 50%)
        `;
    });
}

// Interactive Electron Clouds
function initElectronClouds() {
    const electronClouds = document.querySelectorAll('.electron-cloud');
    
    electronClouds.forEach((cloud, index) => {
        cloud.addEventListener('mouseenter', () => {
            cloud.style.filter = 'blur(1px)';
            cloud.style.transform = 'scale(1.1)';
            cloud.style.animationDuration = '4s';
        });
        
        cloud.addEventListener('mouseleave', () => {
            cloud.style.filter = 'blur(2px)';
            cloud.style.transform = 'scale(1)';
            cloud.style.animationDuration = '8s';
        });
        
        // Add click interaction for wave function collapse
        cloud.addEventListener('click', () => {
            cloud.style.transform = 'scale(0.8)';
            cloud.style.opacity = '0.3';
            
            setTimeout(() => {
                cloud.style.transform = 'scale(1)';
                cloud.style.opacity = '1';
            }, 300);
        });
    });
}

// Wave Function Interactions
function initWaveFunctions() {
    const waveFunctions = document.querySelectorAll('.wave-function');
    
    waveFunctions.forEach(waveFunc => {
        waveFunc.addEventListener('mouseenter', () => {
            const waveBefore = waveFunc.querySelector('::before');
            waveFunc.style.setProperty('--wave-speed', '2s');
        });
        
        waveFunc.addEventListener('mouseleave', () => {
            waveFunc.style.setProperty('--wave-speed', '4s');
        });
    });
}

// Harmonic Series Audio Visualization
function initHarmonicSeries() {
    const harmonicSeries = document.querySelectorAll('.harmonic-series');
    
    harmonicSeries.forEach(series => {
        const harmonics = series.querySelectorAll('.harmonic');
        
        series.addEventListener('mouseenter', () => {
            harmonics.forEach((harmonic, index) => {
                harmonic.style.animationDelay = (index * 0.1) + 's';
                harmonic.style.animationDuration = '2s';
            });
        });
        
        series.addEventListener('mouseleave', () => {
            harmonics.forEach((harmonic, index) => {
                harmonic.style.animationDelay = (index * 0.5) + 's';
                harmonic.style.animationDuration = '4s';
            });
        });
        
        // Add click to play "note"
        harmonics.forEach((harmonic, index) => {
            harmonic.addEventListener('click', () => {
                // Visual feedback for "playing" the harmonic
                harmonic.style.transform = 'scaleY(2) scaleX(1.5)';
                harmonic.style.filter = 'brightness(1.5)';
                
                // Create ripple effect
                const ripple = document.createElement('div');
                ripple.style.cssText = `
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 20px;
                    height: 20px;
                    border: 2px solid var(--accent-red);
                    border-radius: 50%;
                    transform: translate(-50%, -50%);
                    animation: ripple 1s ease-out;
                    pointer-events: none;
                `;
                
                harmonic.style.position = 'relative';
                harmonic.appendChild(ripple);
                
                setTimeout(() => {
                    harmonic.style.transform = '';
                    harmonic.style.filter = '';
                    if (ripple.parentNode) {
                        ripple.parentNode.removeChild(ripple);
                    }
                }, 1000);
            });
        });
    });
    
    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            0% {
                width: 20px;
                height: 20px;
                opacity: 1;
            }
            100% {
                width: 100px;
                height: 100px;
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Quantum Entanglement Interaction
function initQuantumEntanglement() {
    const entanglementPairs = document.querySelectorAll('.entanglement-pair');
    
    entanglementPairs.forEach(pair => {
        const particles = pair.querySelectorAll('.entangled-particle');
        
        particles.forEach((particle, index) => {
            particle.addEventListener('click', () => {
                // Show entanglement effect
                particles.forEach(p => {
                    p.style.transform = 'scale(1.5)';
                    p.style.boxShadow = '0 0 30px var(--accent-red-glow)';
                });
                
                const connection = pair.querySelector('::before');
                pair.style.setProperty('--connection-intensity', '1');
                
                setTimeout(() => {
                    particles.forEach(p => {
                        p.style.transform = '';
                        p.style.boxShadow = '';
                    });
                    pair.style.setProperty('--connection-intensity', '0.4');
                }, 800);
            });
        });
    });
}

// Poetry Meter Interactive Visualization
function initPoetryMeter() {
    const verses = document.querySelectorAll('.verse');
    
    verses.forEach(verse => {
        verse.addEventListener('mouseenter', () => {
            // Create dynamic meter pattern
            const meterPattern = document.createElement('div');
            meterPattern.className = 'meter-pattern';
            
            // Create stressed/unstressed pattern (iambic pentameter example)
            const pattern = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]; // unstressed=0, stressed=1
            
            pattern.forEach(stress => {
                const beat = document.createElement('div');
                beat.className = stress ? 'stressed' : 'unstressed';
                meterPattern.appendChild(beat);
            });
            
            verse.appendChild(meterPattern);
        });
        
        verse.addEventListener('mouseleave', () => {
            const meterPattern = verse.querySelector('.meter-pattern');
            if (meterPattern) {
                meterPattern.remove();
            }
        });
    });
}

// Enhanced Music Visualizer with Physics
class AdvancedMusicVisualizer extends MusicVisualizer {
    constructor(container) {
        super(container);
        this.frequencies = [262, 294, 330, 349, 392, 440, 494, 523]; // C major scale
        this.isPlaying = false;
    }
    
    createNote() {
        super.createNote();
        
        // Add frequency-based size variation
        const notes = this.container.querySelectorAll('.music-note');
        const lastNote = notes[notes.length - 1];
        
        if (lastNote) {
            const frequency = this.frequencies[Math.floor(Math.random() * this.frequencies.length)];
            const size = (frequency / 523) * 1.5 + 0.5; // Scale based on frequency
            
            lastNote.style.fontSize = size + 'rem';
            lastNote.style.filter = `brightness(${0.8 + size * 0.2})`;
            
            // Add harmonic resonance effect
            lastNote.addEventListener('animationend', () => {
                this.createHarmonicResonance(lastNote, frequency);
            });
        }
    }
    
    createHarmonicResonance(note, baseFreq) {
        // Create visual harmonics
        for (let i = 2; i <= 4; i++) {
            const harmonic = document.createElement('div');
            harmonic.className = 'music-note';
            harmonic.textContent = '◦';
            harmonic.style.cssText = `
                position: absolute;
                left: ${note.style.left};
                top: ${note.style.top};
                font-size: ${parseFloat(note.style.fontSize) / i}rem;
                opacity: ${0.3 / i};
                animation: harmonic-fade 2s ease-out;
                pointer-events: none;
                color: var(--accent-red-glow);
            `;
            
            this.container.appendChild(harmonic);
            
            setTimeout(() => {
                if (harmonic.parentNode) {
                    harmonic.parentNode.removeChild(harmonic);
                }
            }, 2000);
        }
    }
}

// Legacy function for mobile menu (backward compatibility)
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}