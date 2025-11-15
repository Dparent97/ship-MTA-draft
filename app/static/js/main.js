// Ship Maintenance Tracker - Main JavaScript

console.log('Ship Maintenance Tracker loaded');

/**
 * Initialize Bootstrap tooltips for status badges and other elements
 */
function initializeTooltips() {
    // Get all elements with tooltip attribute
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');

    // Initialize Bootstrap tooltips
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl =>
        new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover focus',
            animation: true,
            delay: { show: 300, hide: 100 }
        })
    );

    return tooltipList;
}

/**
 * Apply status change animation to a badge element
 */
function animateStatusChange(badgeElement) {
    if (!badgeElement) return;

    badgeElement.classList.add('status-changed');

    // Remove the animation class after it completes
    setTimeout(() => {
        badgeElement.classList.remove('status-changed');
    }, 500);
}

// Initialize tooltips when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeTooltips();

    // Reinitialize tooltips when content is dynamically updated
    // This is useful for AJAX-loaded content or dynamic status updates
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                initializeTooltips();
            }
        });
    });

    // Observe the document body for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Export functions for use in other scripts
window.MTATracker = {
    initializeTooltips,
    animateStatusChange
};

