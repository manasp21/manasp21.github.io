/**
 * Mobile Navigation Controller
 * Handles hamburger menu functionality and mobile UX
 */

class MobileNavigation {
    constructor() {
        this.mobileMenuButton = null;
        this.mobileMenu = null;
        this.body = document.body;
        this.isMenuOpen = false;
        
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
        this.mobileMenuButton = document.querySelector('.mobile-menu-button');
        this.mobileMenu = document.querySelector('.mobile-nav-menu');
        
        if (!this.mobileMenuButton || !this.mobileMenu) {
            console.warn('Mobile navigation elements not found');
            return;
        }
        
        this.bindEvents();
    }
    
    bindEvents() {
        // Hamburger button click
        this.mobileMenuButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMenu();
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isMenuOpen && 
                !this.mobileMenu.contains(e.target) && 
                !this.mobileMenuButton.contains(e.target)) {
                this.closeMenu();
            }
        });
        
        // Close menu with ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isMenuOpen) {
                this.closeMenu();
            }
        });
        
        // Close menu when clicking on navigation links
        const navLinks = this.mobileMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                setTimeout(() => this.closeMenu(), 150);
            });
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && this.isMenuOpen) {
                this.closeMenu();
            }
        });
        
        // Prevent menu from staying open on orientation change
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                if (this.isMenuOpen) {
                    this.closeMenu();
                }
            }, 500);
        });
    }
    
    toggleMenu() {
        if (this.isMenuOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }
    
    openMenu() {
        this.isMenuOpen = true;
        this.mobileMenuButton.classList.add('active');
        this.mobileMenu.classList.add('active');
        this.body.classList.add('mobile-menu-open');
        
        // Update ARIA attributes
        this.mobileMenuButton.setAttribute('aria-expanded', 'true');
        this.mobileMenu.setAttribute('aria-hidden', 'false');
        
        // Focus management
        const firstLink = this.mobileMenu.querySelector('a');
        if (firstLink) {
            setTimeout(() => firstLink.focus(), 300);
        }
    }
    
    closeMenu() {
        this.isMenuOpen = false;
        this.mobileMenuButton.classList.remove('active');
        this.mobileMenu.classList.remove('active');
        this.body.classList.remove('mobile-menu-open');
        
        // Update ARIA attributes
        this.mobileMenuButton.setAttribute('aria-expanded', 'false');
        this.mobileMenu.setAttribute('aria-hidden', 'true');
    }
}

// Initialize mobile navigation when script loads
new MobileNavigation();

// Touch gesture improvements for iOS Safari
document.addEventListener('touchstart', function() {}, { passive: true });

// Prevent zoom on double tap for better UX
let lastTouchEnd = 0;
document.addEventListener('touchend', function (event) {
    const now = (new Date()).getTime();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, false);

// Smooth scroll behavior for anchor links on mobile
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});