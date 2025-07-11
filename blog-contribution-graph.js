/**
 * Blog Contribution Graph - GitHub-style visualization
 * Generates a 365-day contribution graph showing blog post activity
 */

class BlogContributionGraph {
    constructor() {
        this.posts = [];
        this.postCounts = {};
        this.monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        this.init();
    }

    init() {
        this.loadPostData();
        this.calculatePostCounts();
        this.generateGrid();
        this.generateMonthLabels();
    }

    loadPostData() {
        try {
            const dataScript = document.getElementById('blog-post-data');
            if (dataScript) {
                const data = JSON.parse(dataScript.textContent);
                this.posts = data.posts || [];
            }
        } catch (error) {
            console.error('Error loading blog post data:', error);
            this.posts = [];
        }
    }

    calculatePostCounts() {
        this.postCounts = {};
        this.posts.forEach(post => {
            const date = post.date;
            if (this.postCounts[date]) {
                this.postCounts[date]++;
            } else {
                this.postCounts[date] = 1;
            }
        });
    }

    generateGrid() {
        const grid = document.getElementById('contribution-grid');
        if (!grid) return;

        const today = new Date();
        const startDate = new Date(today);
        startDate.setDate(today.getDate() - 364); // 365 days including today

        // Adjust to start on a Sunday (GitHub style)
        const startDay = startDate.getDay();
        if (startDay !== 0) {
            startDate.setDate(startDate.getDate() - startDay);
        }

        // Generate 53 weeks of days
        for (let week = 0; week < 53; week++) {
            for (let day = 0; day < 7; day++) {
                const currentDate = new Date(startDate);
                currentDate.setDate(startDate.getDate() + (week * 7) + day);
                
                // Skip if date is in the future
                if (currentDate > today) continue;

                const dayElement = this.createDayElement(currentDate);
                grid.appendChild(dayElement);
            }
        }
    }

    createDayElement(date) {
        const dayElement = document.createElement('div');
        dayElement.className = 'contribution-day';
        
        const dateString = this.formatDate(date);
        const postCount = this.postCounts[dateString] || 0;
        const level = this.getContributionLevel(postCount);
        
        dayElement.classList.add(`level-${level}`);
        dayElement.setAttribute('data-date', dateString);
        dayElement.setAttribute('data-count', postCount);
        dayElement.setAttribute('aria-label', this.getAriaLabel(date, postCount));
        
        // Add tooltip
        const tooltip = this.createTooltip(date, postCount);
        dayElement.appendChild(tooltip);
        
        // Add click handler for posts
        if (postCount > 0) {
            dayElement.style.cursor = 'pointer';
            dayElement.addEventListener('click', () => this.handleDayClick(date, postCount));
        }
        
        return dayElement;
    }

    createTooltip(date, postCount) {
        const tooltip = document.createElement('div');
        tooltip.className = 'contribution-tooltip';
        
        const dateStr = this.formatDateForTooltip(date);
        if (postCount === 0) {
            tooltip.textContent = `No posts on ${dateStr}`;
        } else if (postCount === 1) {
            tooltip.textContent = `1 post on ${dateStr}`;
        } else {
            tooltip.textContent = `${postCount} posts on ${dateStr}`;
        }
        
        return tooltip;
    }

    getContributionLevel(postCount) {
        if (postCount === 0) return 0;
        if (postCount === 1) return 1;
        if (postCount === 2) return 2;
        if (postCount === 3) return 3;
        return 4; // 4 or more posts
    }

    formatDate(date) {
        return date.toISOString().split('T')[0];
    }

    formatDateForTooltip(date) {
        const options = { 
            weekday: 'short', 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        };
        return date.toLocaleDateString('en-US', options);
    }

    getAriaLabel(date, postCount) {
        const dateStr = this.formatDateForTooltip(date);
        if (postCount === 0) {
            return `No posts on ${dateStr}`;
        } else if (postCount === 1) {
            return `1 post on ${dateStr}`;
        } else {
            return `${postCount} posts on ${dateStr}`;
        }
    }

    generateMonthLabels() {
        const monthsContainer = document.querySelector('.graph-months');
        if (!monthsContainer) return;

        const today = new Date();
        const labels = [];
        
        // Generate labels for the last 12 months
        for (let i = 11; i >= 0; i--) {
            const date = new Date(today);
            date.setMonth(today.getMonth() - i);
            labels.push({
                month: this.monthNames[date.getMonth()],
                width: this.calculateMonthWidth(date)
            });
        }

        // Clear existing labels
        monthsContainer.innerHTML = '';

        // Add month labels
        labels.forEach(label => {
            const monthElement = document.createElement('div');
            monthElement.className = 'month-label';
            monthElement.textContent = label.month;
            monthElement.style.width = label.width + 'px';
            monthsContainer.appendChild(monthElement);
        });
    }

    calculateMonthWidth(date) {
        // Calculate approximate width based on weeks in view
        // This is a simplified calculation - could be more precise
        const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
        const weeksInMonth = Math.ceil(daysInMonth / 7);
        return weeksInMonth * 14; // 12px day + 2px gap approximation
    }

    handleDayClick(date, postCount) {
        // Find posts for this date
        const dateString = this.formatDate(date);
        const postsForDate = this.posts.filter(post => post.date === dateString);
        
        if (postsForDate.length === 1) {
            // Single post - navigate directly
            window.location.href = postsForDate[0].url;
        } else if (postsForDate.length > 1) {
            // Multiple posts - show a simple alert or could implement a popup
            let message = `${postsForDate.length} posts on ${this.formatDateForTooltip(date)}:\n\n`;
            postsForDate.forEach((post, index) => {
                message += `${index + 1}. ${post.title}\n`;
            });
            
            if (confirm(message + '\nClick OK to view the first post, Cancel to stay here.')) {
                window.location.href = postsForDate[0].url;
            }
        }
    }

    // Public method to refresh the graph (useful for dynamic updates)
    refresh() {
        const grid = document.getElementById('contribution-grid');
        const monthsContainer = document.querySelector('.graph-months');
        
        if (grid) grid.innerHTML = '';
        if (monthsContainer) monthsContainer.innerHTML = '';
        
        this.init();
    }
}

// Initialize the contribution graph when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BlogContributionGraph();
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BlogContributionGraph;
}