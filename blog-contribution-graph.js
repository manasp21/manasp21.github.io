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
        this.generateGraph();
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

    generateGraph() {
        const container = document.getElementById('contribution-graph');
        if (!container) return;

        // Calculate date range (365 days ending today)
        const today = new Date();
        const startDate = new Date(today);
        startDate.setDate(today.getDate() - 364); // 365 days including today

        // Adjust to start on a Sunday (GitHub style)
        const startDay = startDate.getDay();
        if (startDay !== 0) {
            startDate.setDate(startDate.getDate() - startDay);
        }

        // Clear container
        container.innerHTML = '';

        // Create graph structure
        const graphContainer = document.createElement('div');
        graphContainer.className = 'graph-container';

        // Create grid only (no labels)
        const grid = this.createGrid(startDate, today);
        graphContainer.appendChild(grid);
        container.appendChild(graphContainer);
    }


    createGrid(startDate, today) {
        const grid = document.createElement('div');
        grid.className = 'graph-grid';

        // Generate 53 weeks of days
        for (let week = 0; week < 53; week++) {
            for (let day = 0; day < 7; day++) {
                const currentDate = new Date(startDate);
                currentDate.setDate(startDate.getDate() + (week * 7) + day);
                
                // Skip if date is in the future
                if (currentDate > today) {
                    // Add empty cell to maintain grid structure
                    const emptyDay = document.createElement('div');
                    emptyDay.className = 'contribution-day level-0';
                    emptyDay.style.visibility = 'hidden';
                    grid.appendChild(emptyDay);
                    continue;
                }

                const dayElement = this.createDayElement(currentDate);
                grid.appendChild(dayElement);
            }
        }

        return grid;
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
        tooltip.textContent = postCount > 0 ? `Posted on ${dateStr}` : `No posts on ${dateStr}`;
        
        return tooltip;
    }

    getContributionLevel(postCount) {
        return postCount > 0 ? 1 : 0;
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
        return postCount > 0 ? `Posted on ${dateStr}` : `No posts on ${dateStr}`;
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
        const container = document.getElementById('contribution-graph');
        if (container) container.innerHTML = '';
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