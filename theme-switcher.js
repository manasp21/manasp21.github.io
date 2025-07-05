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
    
    // Device Performance Detection (Apple Liquid Glass Optimization)
    function detectDevicePerformance() {
        // Basic performance detection
        const deviceMemory = navigator.deviceMemory || 4; // Default to 4GB if unknown
        const hardwareConcurrency = navigator.hardwareConcurrency || 4; // Default to 4 cores
        const connection = navigator.connection || { effectiveType: '4g' };
        
        // Performance scoring
        let performanceScore = 0;
        if (deviceMemory >= 8) performanceScore += 3;
        else if (deviceMemory >= 4) performanceScore += 2;
        else performanceScore += 1;
        
        if (hardwareConcurrency >= 8) performanceScore += 3;
        else if (hardwareConcurrency >= 4) performanceScore += 2;
        else performanceScore += 1;
        
        if (connection.effectiveType === '4g') performanceScore += 2;
        else if (connection.effectiveType === '3g') performanceScore += 1;
        
        // Determine glass performance level
        const isHighPerformance = performanceScore >= 6;
        const isMediumPerformance = performanceScore >= 4;
        
        console.log(`Device performance detected: ${performanceScore}/8 (${isHighPerformance ? 'High' : isMediumPerformance ? 'Medium' : 'Low'})`);
        
        return { isHighPerformance, isMediumPerformance, score: performanceScore };
    }
    
    // Dynamic Glass Effects System
    function initDynamicGlassEffects() {
        console.log('Initializing enhanced liquid glass effects...');
        
        // Detect device performance capabilities
        const devicePerformance = detectDevicePerformance();
        
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
                
                // Add scroll-based class for CSS targeting (matches plan.md specification)
                if (scrolled > 100) {
                    element.classList.add('glass-scroll-dynamic');
                    element.classList.add('scrolled'); // For .glass-scroll-dynamic.scrolled CSS rule
                } else {
                    element.classList.remove('glass-scroll-dynamic');
                    element.classList.remove('scrolled');
                }
                
                // Performance-optimized dynamic blur (Apple Liquid Glass standard)
                let baseBlur, maxBlur, saturation;
                if (devicePerformance.isHighPerformance) {
                    baseBlur = 12; // Default medium blur
                    maxBlur = 40;  // Ultra blur for high-performance devices
                    saturation = 220; // Maximum saturation enhancement
                } else if (devicePerformance.isMediumPerformance) {
                    baseBlur = 12; // Default medium blur
                    maxBlur = 30;  // Strong blur for medium-performance devices
                    saturation = 180; // Standard saturation enhancement
                } else {
                    baseBlur = 8;  // Light blur for low-performance devices
                    maxBlur = 20;  // Strong blur for low-performance devices
                    saturation = 150; // Reduced saturation for performance
                }
                
                const dynamicBlur = baseBlur + (maxBlur - baseBlur) * scrollPercent;
                
                // Apply performance-optimized blur with saturation enhancement
                element.style.setProperty('--dynamic-blur', `blur(${dynamicBlur}px) saturate(${saturation}%)`);
                
                // Enhanced dynamic glass opacity with liquid glass values
                const baseOpacity = 0.15; // Matches --liquid-glass-bg-primary
                const maxOpacity = devicePerformance.isHighPerformance ? 0.25 : 0.22; // Enhanced for high-performance
                const dynamicOpacity = baseOpacity + (maxOpacity - baseOpacity) * scrollPercent;
                
                element.style.setProperty('--dynamic-glass-opacity', dynamicOpacity);
                
                // Page-specific accent color integration
                const computedStyle = getComputedStyle(document.body);
                const accentRGB = computedStyle.getPropertyValue('--page-accent-rgb').trim();
                if (accentRGB) {
                    const accentIntensity = 0.08 + (0.12 * scrollPercent); // Dynamic accent opacity
                    element.style.setProperty('--dynamic-accent-bg', `rgba(${accentRGB}, ${accentIntensity})`);
                }
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
        
        console.log(`Enhanced liquid glass effects initialized for ${glassDynamicElements.length} elements`);
        console.log(`Performance profile: ${devicePerformance.isHighPerformance ? 'High' : devicePerformance.isMediumPerformance ? 'Medium' : 'Low'} (${devicePerformance.score}/8)`);
        console.log('Features: Saturation enhancement, dynamic blur, page-specific accents, performance optimization');
    }
    
    // Export for debugging
    window.toggleTheme = toggleTheme;
    window.getCurrentTheme = function() { return currentTheme; };
    window.initDynamicGlassEffects = initDynamicGlassEffects;
    
    console.log('Theme switcher script loaded');
})();