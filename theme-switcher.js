/**
 * Book Theme Switcher
 * Elegant theme switching between dark and book-like light themes
 * Preserves user preferences and provides smooth transitions
 */

class BookThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('preferred-theme') || 'dark';
        this.isTransitioning = false;
        this.init();
    }
    
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }
    
    setup() {
        this.createToggleButton();
        this.applyTheme(this.currentTheme);
        this.bindEvents();
        
        // Apply theme immediately to prevent flash
        this.applyThemeImmediate();
        
        console.log('Book Theme Manager initialized');
    }
    
    createToggleButton() {
        // Check if button already exists
        if (document.getElementById('theme-toggle')) {
            return;
        }
        
        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.className = 'theme-toggle-btn';
        button.setAttribute('aria-label', 'Toggle between dark and book themes');
        button.setAttribute('title', 'Switch theme');
        
        // SVG icons for sun (book theme) and moon (dark theme)
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
        
        // Add to body
        document.body.appendChild(button);
        
        // Update button state immediately
        this.updateButtonState();
    }
    
    bindEvents() {
        const button = document.getElementById('theme-toggle');
        if (!button) return;
        
        // Click event
        button.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleTheme();
        });
        
        // Keyboard accessibility
        button.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggleTheme();
            }
        });
        
        // Listen for system theme changes
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                // Only apply system preference if user hasn't manually set a theme
                if (!localStorage.getItem('preferred-theme')) {
                    this.applyTheme(e.matches ? 'dark' : 'book');
                }
            });
        }
    }
    
    toggleTheme() {
        if (this.isTransitioning) return;
        
        const newTheme = this.currentTheme === 'dark' ? 'book' : 'dark';
        this.applyTheme(newTheme);
        this.animateThemeTransition();
    }
    
    applyTheme(theme) {
        this.currentTheme = theme;
        
        if (theme === 'book') {
            document.documentElement.setAttribute('data-theme', 'book');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
        
        // Save preference
        localStorage.setItem('preferred-theme', theme);
        
        // Update button state
        this.updateButtonState();
        
        // Dispatch custom event for other components to listen to
        window.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme: theme }
        }));
    }
    
    applyThemeImmediate() {
        // Apply theme without animation for initial load
        const savedTheme = localStorage.getItem('preferred-theme');
        if (savedTheme) {
            this.applyTheme(savedTheme);
        } else {
            // Respect system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
                this.applyTheme('book');
            } else {
                this.applyTheme('dark');
            }
        }
    }
    
    updateButtonState() {
        const button = document.getElementById('theme-toggle');
        if (!button) return;
        
        const isBookTheme = this.currentTheme === 'book';
        button.setAttribute('title', 
            isBookTheme ? 'Switch to dark theme' : 'Switch to book theme'
        );
        button.setAttribute('aria-label', 
            isBookTheme ? 'Switch to dark theme' : 'Switch to book theme'
        );
    }
    
    animateThemeTransition() {
        this.isTransitioning = true;
        const button = document.getElementById('theme-toggle');
        
        if (button) {
            // Add animation class
            button.style.transform = 'scale(1.2) rotate(180deg)';
            
            setTimeout(() => {
                button.style.transform = '';
                this.isTransitioning = false;
            }, 300);
        } else {
            this.isTransitioning = false;
        }
    }
    
    // Public method to get current theme
    getCurrentTheme() {
        return this.currentTheme;
    }
    
    // Public method to set theme programmatically
    setTheme(theme) {
        if (theme === 'book' || theme === 'dark') {
            this.applyTheme(theme);
        }
    }
}

// Initialize theme manager when script loads
let themeManager;

// Ensure script runs after DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        themeManager = new BookThemeManager();
    });
} else {
    themeManager = new BookThemeManager();
}

// Export for potential use by other scripts
window.BookThemeManager = BookThemeManager;
window.themeManager = themeManager;

// Performance optimization: prevent zoom on double tap for better UX
let lastTouchEnd = 0;
document.addEventListener('touchend', function (event) {
    const now = (new Date()).getTime();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, false);