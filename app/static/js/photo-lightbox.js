/**
 * Photo Lightbox Gallery with Swipe Gestures
 * Features: Full-screen viewing, swipe navigation, captions, photo count
 */

class PhotoLightbox {
    constructor(options = {}) {
        this.photos = [];
        this.currentIndex = 0;
        this.lightboxElement = null;
        this.touchStartX = 0;
        this.touchEndX = 0;
        this.touchStartY = 0;
        this.touchEndY = 0;
        this.isDragging = false;
        this.dragThreshold = 50; // pixels to trigger swipe

        // Configuration
        this.enableSwipe = options.enableSwipe !== false;
        this.enableKeyboard = options.enableKeyboard !== false;
        this.enableZoom = options.enableZoom !== false;
        this.animationDuration = options.animationDuration || 300;

        this.init();
    }

    init() {
        this.createLightboxHTML();
        this.setupEventListeners();
    }

    createLightboxHTML() {
        const lightboxHTML = `
            <div class="photo-lightbox" id="photoLightbox">
                <div class="lightbox-overlay"></div>
                <div class="lightbox-content">
                    <!-- Close Button -->
                    <button class="lightbox-close" id="lightboxClose" title="Close (Esc)">
                        <svg width="32" height="32" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                        </svg>
                    </button>

                    <!-- Photo Counter -->
                    <div class="lightbox-counter" id="lightboxCounter">
                        <span class="counter-current">1</span> / <span class="counter-total">1</span>
                    </div>

                    <!-- Previous Button -->
                    <button class="lightbox-nav lightbox-prev" id="lightboxPrev" title="Previous (←)">
                        <svg width="48" height="48" fill="currentColor" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
                        </svg>
                    </button>

                    <!-- Next Button -->
                    <button class="lightbox-nav lightbox-next" id="lightboxNext" title="Next (→)">
                        <svg width="48" height="48" fill="currentColor" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
                        </svg>
                    </button>

                    <!-- Image Container -->
                    <div class="lightbox-image-container" id="lightboxImageContainer">
                        <div class="lightbox-loading">
                            <div class="spinner-border text-light" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        <img src="" alt="" class="lightbox-image" id="lightboxImage">
                    </div>

                    <!-- Caption -->
                    <div class="lightbox-caption" id="lightboxCaption">
                        <!-- Caption text will be inserted here -->
                    </div>

                    <!-- Swipe Hint (Mobile) -->
                    <div class="lightbox-swipe-hint" id="lightboxSwipeHint">
                        Swipe to navigate
                    </div>
                </div>
            </div>
        `;

        // Add to body
        document.body.insertAdjacentHTML('beforeend', lightboxHTML);
        this.lightboxElement = document.getElementById('photoLightbox');
    }

    setupEventListeners() {
        // Close button
        const closeBtn = document.getElementById('lightboxClose');
        closeBtn.addEventListener('click', () => this.close());

        // Navigation buttons
        const prevBtn = document.getElementById('lightboxPrev');
        const nextBtn = document.getElementById('lightboxNext');
        prevBtn.addEventListener('click', () => this.previous());
        nextBtn.addEventListener('click', () => this.next());

        // Click outside to close
        const overlay = this.lightboxElement.querySelector('.lightbox-overlay');
        overlay.addEventListener('click', () => this.close());

        // Keyboard navigation
        if (this.enableKeyboard) {
            document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        }

        // Touch/Swipe events
        if (this.enableSwipe) {
            const container = document.getElementById('lightboxImageContainer');
            container.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: true });
            container.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
            container.addEventListener('touchend', (e) => this.handleTouchEnd(e), { passive: true });

            // Mouse drag events for desktop
            container.addEventListener('mousedown', (e) => this.handleMouseDown(e));
            container.addEventListener('mousemove', (e) => this.handleMouseMove(e));
            container.addEventListener('mouseup', (e) => this.handleMouseUp(e));
            container.addEventListener('mouseleave', (e) => this.handleMouseUp(e));
        }

        // Prevent image drag
        const lightboxImage = document.getElementById('lightboxImage');
        lightboxImage.addEventListener('dragstart', (e) => e.preventDefault());

        // Image load event
        lightboxImage.addEventListener('load', () => this.onImageLoad());
        lightboxImage.addEventListener('error', () => this.onImageError());
    }

    handleKeyboard(e) {
        if (!this.lightboxElement.classList.contains('active')) return;

        switch(e.key) {
            case 'Escape':
                this.close();
                break;
            case 'ArrowLeft':
                this.previous();
                break;
            case 'ArrowRight':
                this.next();
                break;
        }
    }

    handleTouchStart(e) {
        this.touchStartX = e.changedTouches[0].screenX;
        this.touchStartY = e.changedTouches[0].screenY;
        this.isDragging = true;

        // Hide swipe hint after first touch
        const swipeHint = document.getElementById('lightboxSwipeHint');
        if (swipeHint) {
            swipeHint.style.display = 'none';
        }
    }

    handleTouchMove(e) {
        if (!this.isDragging) return;

        const currentX = e.changedTouches[0].screenX;
        const currentY = e.changedTouches[0].screenY;
        const diffX = Math.abs(currentX - this.touchStartX);
        const diffY = Math.abs(currentY - this.touchStartY);

        // Prevent default if horizontal swipe is detected
        if (diffX > diffY && diffX > 10) {
            e.preventDefault();
        }
    }

    handleTouchEnd(e) {
        if (!this.isDragging) return;

        this.touchEndX = e.changedTouches[0].screenX;
        this.touchEndY = e.changedTouches[0].screenY;
        this.isDragging = false;

        this.handleSwipeGesture();
    }

    handleMouseDown(e) {
        this.touchStartX = e.screenX;
        this.touchStartY = e.screenY;
        this.isDragging = true;
        e.preventDefault();
    }

    handleMouseMove(e) {
        if (!this.isDragging) return;

        const currentX = e.screenX;
        const diffX = Math.abs(currentX - this.touchStartX);

        // Visual feedback for drag
        const container = document.getElementById('lightboxImageContainer');
        const dragDistance = currentX - this.touchStartX;

        if (Math.abs(dragDistance) > 10) {
            container.style.transform = `translateX(${dragDistance * 0.5}px)`;
            container.style.opacity = `${1 - Math.abs(dragDistance) * 0.001}`;
        }
    }

    handleMouseUp(e) {
        if (!this.isDragging) return;

        this.touchEndX = e.screenX;
        this.touchEndY = e.screenY;

        // Reset transform
        const container = document.getElementById('lightboxImageContainer');
        container.style.transform = '';
        container.style.opacity = '';

        this.isDragging = false;
        this.handleSwipeGesture();
    }

    handleSwipeGesture() {
        const diffX = this.touchEndX - this.touchStartX;
        const diffY = this.touchEndY - this.touchStartY;

        // Check if it's a horizontal swipe
        if (Math.abs(diffX) > Math.abs(diffY)) {
            if (Math.abs(diffX) > this.dragThreshold) {
                if (diffX > 0) {
                    // Swipe right - previous photo
                    this.previous();
                } else {
                    // Swipe left - next photo
                    this.next();
                }
            }
        }
    }

    open(photos, startIndex = 0) {
        this.photos = photos;
        this.currentIndex = startIndex;

        // Show lightbox
        this.lightboxElement.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling

        // Load first image
        this.loadImage(this.currentIndex);

        // Update counter
        this.updateCounter();

        // Update navigation buttons
        this.updateNavigationButtons();

        // Show swipe hint on mobile (hide after 3 seconds)
        if (this.isMobile() && this.photos.length > 1) {
            const swipeHint = document.getElementById('lightboxSwipeHint');
            swipeHint.style.display = 'block';
            setTimeout(() => {
                swipeHint.style.opacity = '0';
                setTimeout(() => {
                    swipeHint.style.display = 'none';
                    swipeHint.style.opacity = '1';
                }, 300);
            }, 3000);
        }
    }

    close() {
        this.lightboxElement.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling

        // Clear image after animation
        setTimeout(() => {
            const lightboxImage = document.getElementById('lightboxImage');
            lightboxImage.src = '';
        }, this.animationDuration);
    }

    next() {
        if (this.currentIndex < this.photos.length - 1) {
            this.currentIndex++;
            this.loadImage(this.currentIndex, 'next');
            this.updateCounter();
            this.updateNavigationButtons();
        }
    }

    previous() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.loadImage(this.currentIndex, 'prev');
            this.updateCounter();
            this.updateNavigationButtons();
        }
    }

    loadImage(index, direction = 'none') {
        const photo = this.photos[index];
        const lightboxImage = document.getElementById('lightboxImage');
        const lightboxCaption = document.getElementById('lightboxCaption');
        const loading = this.lightboxElement.querySelector('.lightbox-loading');

        // Show loading
        loading.style.display = 'flex';
        lightboxImage.style.opacity = '0';

        // Add slide animation class
        if (direction !== 'none') {
            const container = document.getElementById('lightboxImageContainer');
            container.classList.add(`slide-${direction}`);
            setTimeout(() => {
                container.classList.remove(`slide-${direction}`);
            }, this.animationDuration);
        }

        // Load new image
        lightboxImage.src = photo.url;
        lightboxImage.alt = photo.caption || 'Photo';

        // Update caption
        if (photo.caption) {
            lightboxCaption.innerHTML = `<p>${this.escapeHtml(photo.caption)}</p>`;
            lightboxCaption.style.display = 'block';
        } else {
            lightboxCaption.innerHTML = '';
            lightboxCaption.style.display = 'none';
        }
    }

    onImageLoad() {
        const lightboxImage = document.getElementById('lightboxImage');
        const loading = this.lightboxElement.querySelector('.lightbox-loading');

        // Hide loading, show image
        setTimeout(() => {
            loading.style.display = 'none';
            lightboxImage.style.opacity = '1';
        }, 100);
    }

    onImageError() {
        const lightboxCaption = document.getElementById('lightboxCaption');
        const loading = this.lightboxElement.querySelector('.lightbox-loading');

        loading.style.display = 'none';
        lightboxCaption.innerHTML = '<p class="text-danger">Failed to load image</p>';
        lightboxCaption.style.display = 'block';
    }

    updateCounter() {
        const counterCurrent = this.lightboxElement.querySelector('.counter-current');
        const counterTotal = this.lightboxElement.querySelector('.counter-total');

        counterCurrent.textContent = this.currentIndex + 1;
        counterTotal.textContent = this.photos.length;

        // Hide counter if only one photo
        const counter = document.getElementById('lightboxCounter');
        counter.style.display = this.photos.length > 1 ? 'block' : 'none';
    }

    updateNavigationButtons() {
        const prevBtn = document.getElementById('lightboxPrev');
        const nextBtn = document.getElementById('lightboxNext');

        // Hide/show based on position
        prevBtn.style.display = this.currentIndex > 0 ? 'flex' : 'none';
        nextBtn.style.display = this.currentIndex < this.photos.length - 1 ? 'flex' : 'none';

        // Hide both if only one photo
        if (this.photos.length <= 1) {
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
        }
    }

    isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Static method to initialize lightbox on photo grids
    static initializePhotoGrids() {
        // Initialize lightbox instance
        const lightbox = new PhotoLightbox();

        // Find all photo grids and add click listeners
        document.querySelectorAll('.photo-gallery-grid').forEach(grid => {
            const photoElements = grid.querySelectorAll('.photo-gallery-item');

            photoElements.forEach((photoEl, index) => {
                photoEl.style.cursor = 'pointer';
                photoEl.addEventListener('click', (e) => {
                    e.preventDefault();

                    // Build photos array from grid
                    const photos = Array.from(photoElements).map(el => ({
                        url: el.dataset.fullUrl || el.querySelector('img').src,
                        caption: el.dataset.caption || el.querySelector('img').alt || ''
                    }));

                    // Open lightbox at clicked photo
                    lightbox.open(photos, index);
                });
            });
        });

        return lightbox;
    }
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize lightbox for all photo grids
    window.photoLightbox = PhotoLightbox.initializePhotoGrids();
});
