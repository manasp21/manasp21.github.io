/**
 * Book Theme Switcher - Simple & Reliable
 * Elegant theme switching between dark and book-like light themes
 */

(function() {
    'use strict';
    
    // Theme management
    let currentTheme = localStorage.getItem('preferred-theme') || 'dark';
    let isTransitioning = false;
    
    // Apply theme immediately to prevent flash
    function applyTheme(theme) {
        currentTheme = theme;
        
        if (theme === 'book') {
            document.documentElement.setAttribute('data-theme', 'book');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
        
        localStorage.setItem('preferred-theme', theme);
        updateButtonState();
        
        // Dispatch event for other components
        if (window.CustomEvent) {
            window.dispatchEvent(new CustomEvent('themeChanged', {
                detail: { theme: theme }
            }));
        }
    }
    
    // Update button appearance
    function updateButtonState() {
        const button = document.getElementById('theme-toggle');
        if (!button) return;
        
        const isBookTheme = currentTheme === 'book';
        button.setAttribute('title', 
            isBookTheme ? 'Switch to dark theme' : 'Switch to book theme'
        );
        button.setAttribute('aria-label', 
            isBookTheme ? 'Switch to dark theme' : 'Switch to book theme'
        );
    }
    
    // Toggle between themes
    function toggleTheme() {
        if (isTransitioning) return;
        
        const newTheme = currentTheme === 'dark' ? 'book' : 'dark';
        applyTheme(newTheme);
        animateButton();
    }
    
    // Button animation
    function animateButton() {
        isTransitioning = true;
        const button = document.getElementById('theme-toggle');
        
        if (button) {
            button.style.transform = 'scale(1.2) rotate(180deg)';
            setTimeout(() => {
                button.style.transform = '';
                isTransitioning = false;
            }, 300);
        } else {
            isTransitioning = false;
        }
    }
    
    // Create the toggle button
    function createToggleButton() {
        // Check if button already exists
        if (document.getElementById('theme-toggle')) {
            console.log('Theme toggle button already exists');
            return;
        }
        
        console.log('Creating theme toggle button...');
        
        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.className = 'theme-toggle-btn';
        button.setAttribute('aria-label', 'Toggle between dark and book themes');
        button.setAttribute('title', 'Switch theme');
        
        // Simple icons using Unicode symbols
        button.innerHTML = `
            <svg class="theme-icon sun-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/>
                <path d="m12 2 0 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="m12 20 0 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="m4.93 4.93 1.41 1.41" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="m17.66 17.66 1.41 1.41" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="m2 12 2 0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="m20 12 2 0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="m6.34 17.66-1.41 1.41" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="m19.07 4.93-1.41 1.41" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <svg class="theme-icon moon-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        
        // Add click handler
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Theme toggle clicked');
            toggleTheme();
        });
        
        // Add keyboard support
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTheme();
            }
        });
        
        // Add to page
        if (document.body) {
            document.body.appendChild(button);
            console.log('Theme toggle button added to page');
            updateButtonState();
        } else {
            console.error('document.body not available');
        }
    }
    
    // Initialize everything
    function init() {
        console.log('Initializing theme switcher...');
        
        // Apply saved theme immediately
        applyTheme(currentTheme);
        
        // Create button
        createToggleButton();
        
        // Initialize dynamic glass effects
        initDynamicGlassEffects();
        
        console.log('Theme switcher initialized with theme:', currentTheme);
    }
    
    // Wait for DOM or run immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // Try immediate execution
        if (document.body) {
            init();
        } else {
            // If body not ready, wait a bit
            setTimeout(init, 100);
        }
    }
    
    // Fallback: try again after a delay if button still doesn't exist
    setTimeout(function() {
        if (!document.getElementById('theme-toggle')) {
            console.log('Button not found, retrying...');
            createToggleButton();
        }
    }, 1000);
    
    // Dynamic Glass Effects System
    function initDynamicGlassEffects() {
        console.log('Initializing dynamic glass effects...');
        
        const glassDynamicElements = document.querySelectorAll(
            '.header, .content-section, .onesite-card, .project-card, .experience-card, .education-card, .publication-card, .interest-card'
        );
        
        let scrollTimeout = null;
        let isScrolling = false;
        
        function updateGlassIntensity() {
            const scrolled = window.scrollY;
            const windowHeight = window.innerHeight;
            const scrollPercent = Math.min(scrolled / windowHeight, 1);
            
            // Enhanced glass effects based on scroll position
            glassDynamicElements.forEach(element => {
                if (!element) return;
                
                // Add scroll-based class for CSS targeting
                if (scrolled > 100) {
                    element.classList.add('glass-scroll-enhanced');
                } else {
                    element.classList.remove('glass-scroll-enhanced');
                }
                
                // Dynamic backdrop blur intensity
                const baseBlur = 12; // Default medium blur
                const maxBlur = 25;  // Maximum blur
                const dynamicBlur = baseBlur + (maxBlur - baseBlur) * scrollPercent;
                
                // Apply dynamic blur with CSS custom property
                element.style.setProperty('--dynamic-blur', `blur(${dynamicBlur}px)`);
                
                // Dynamic glass opacity
                const baseOpacity = 0.1;
                const maxOpacity = 0.2;
                const dynamicOpacity = baseOpacity + (maxOpacity - baseOpacity) * scrollPercent;
                
                element.style.setProperty('--dynamic-glass-opacity', dynamicOpacity);
            });
            
            // Special header enhancement
            const header = document.querySelector('.header');
            if (header) {
                if (scrolled > 50) {
                    header.classList.add('header-scrolled');
                } else {
                    header.classList.remove('header-scrolled');
                }
            }
        }
        
        function handleScroll() {
            if (!isScrolling) {
                isScrolling = true;
                requestAnimationFrame(() => {
                    updateGlassIntensity();
                    isScrolling = false;
                });
            }
            
            // Clear timeout and set new one
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                updateGlassIntensity();
            }, 100);
        }
        
        // Intersection Observer for performance optimization
        const observerOptions = {
            root: null,
            rootMargin: '100px',
            threshold: [0, 0.1, 0.5, 1]
        };
        
        const glassObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const element = entry.target;
                if (entry.isIntersecting) {
                    element.classList.add('glass-in-view');
                } else {
                    element.classList.remove('glass-in-view');
                }
            });
        }, observerOptions);
        
        // Observe all glass elements
        glassDynamicElements.forEach(element => {
            if (element) {
                glassObserver.observe(element);
            }
        });
        
        // Add scroll listener with throttling
        window.addEventListener('scroll', handleScroll, { passive: true });
        
        // Initial update
        updateGlassIntensity();
        
        console.log('Dynamic glass effects initialized for', glassDynamicElements.length, 'elements');
    }
    
    // Export for debugging
    window.toggleTheme = toggleTheme;
    window.getCurrentTheme = function() { return currentTheme; };
    window.initDynamicGlassEffects = initDynamicGlassEffects;
    
    console.log('Theme switcher script loaded');
})();