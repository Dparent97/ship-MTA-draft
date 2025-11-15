/**
 * Enhanced Photo Upload System
 * Features: Drag-and-drop, instant previews, delete buttons, loading states
 */

class PhotoUploadManager {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.photos = [];
        this.photoCount = 0;

        // Configuration
        this.maxPhotos = options.maxPhotos || 10;
        this.minPhotos = options.minPhotos || 0;
        this.acceptedTypes = options.acceptedTypes || ['image/jpeg', 'image/jpg', 'image/png', 'image/heic', 'image/heif'];
        this.maxFileSize = options.maxFileSize || 10 * 1024 * 1024; // 10MB default

        // Elements
        this.dropZone = null;
        this.previewContainer = null;
        this.addButton = null;
        this.fileInput = null;

        this.init();
    }

    init() {
        this.createDropZone();
        this.createPreviewContainer();
        this.setupEventListeners();
    }

    createDropZone() {
        const dropZoneHTML = `
            <div class="photo-drop-zone" id="photoDropZone">
                <div class="drop-zone-content">
                    <svg width="64" height="64" fill="currentColor" class="mb-3" viewBox="0 0 16 16">
                        <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                        <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
                    </svg>
                    <h5 class="mb-2">Drag & Drop Photos Here</h5>
                    <p class="text-muted mb-3">or</p>
                    <button type="button" class="btn btn-primary" id="photoSelectBtn">
                        📷 Choose Photos
                    </button>
                    <input type="file" id="photoFileInput" multiple accept="${this.acceptedTypes.join(',')}" style="display: none;">
                    <p class="text-muted small mt-3 mb-0">
                        Maximum ${this.maxPhotos} photos • JPG, PNG, HEIC • Max 10MB each
                    </p>
                </div>
                <div class="drop-zone-overlay">
                    <div class="drop-zone-overlay-content">
                        <svg width="80" height="80" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                            <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
                        </svg>
                        <h4 class="mt-3">Drop photos to upload</h4>
                    </div>
                </div>
            </div>
        `;

        this.container.insertAdjacentHTML('beforeend', dropZoneHTML);
        this.dropZone = document.getElementById('photoDropZone');
        this.addButton = document.getElementById('photoSelectBtn');
        this.fileInput = document.getElementById('photoFileInput');
    }

    createPreviewContainer() {
        const previewHTML = `
            <div class="photo-preview-container" id="photoPreviewContainer">
                <!-- Photo previews will be added here -->
            </div>
        `;

        this.container.insertAdjacentHTML('beforeend', previewHTML);
        this.previewContainer = document.getElementById('photoPreviewContainer');
    }

    setupEventListeners() {
        // Button click to open file picker
        this.addButton.addEventListener('click', () => {
            this.fileInput.click();
        });

        // File input change
        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
            e.target.value = ''; // Reset input
        });

        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, () => {
                this.dropZone.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, () => {
                this.dropZone.classList.remove('drag-over');
            });
        });

        this.dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleFiles(files) {
        const fileArray = Array.from(files);

        // Check if adding these files would exceed max
        if (this.photos.length + fileArray.length > this.maxPhotos) {
            this.showError(`Maximum ${this.maxPhotos} photos allowed. You can add ${this.maxPhotos - this.photos.length} more.`);
            return;
        }

        // Process each file
        fileArray.forEach(file => {
            if (this.validateFile(file)) {
                this.addPhoto(file);
            }
        });

        this.updateDropZoneVisibility();
    }

    validateFile(file) {
        // Check file type
        if (!this.acceptedTypes.includes(file.type)) {
            this.showError(`${file.name}: Invalid file type. Please use JPG, PNG, or HEIC images.`);
            return false;
        }

        // Check file size
        if (file.size > this.maxFileSize) {
            this.showError(`${file.name}: File too large. Maximum size is 10MB.`);
            return false;
        }

        return true;
    }

    addPhoto(file) {
        this.photoCount++;
        const photoId = `photo-${Date.now()}-${this.photoCount}`;

        const photoData = {
            id: photoId,
            file: file,
            caption: ''
        };

        this.photos.push(photoData);

        // Create preview with loading state
        this.createPhotoPreview(photoData);

        // Load image preview
        this.loadImagePreview(photoData);
    }

    createPhotoPreview(photoData) {
        const previewHTML = `
            <div class="photo-preview-card" id="${photoData.id}" data-photo-id="${photoData.id}">
                <div class="photo-preview-loading">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="small text-muted mt-2 mb-0">Loading preview...</p>
                    <div class="photo-upload-progress" style="width: 100%; max-width: 200px; margin-top: 1rem;">
                        <div class="progress" style="height: 6px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated"
                                 role="progressbar"
                                 style="width: 0%"
                                 aria-valuenow="0"
                                 aria-valuemin="0"
                                 aria-valuemax="100"></div>
                        </div>
                        <small class="text-muted d-block mt-1">Preparing...</small>
                    </div>
                </div>
                <div class="photo-preview-content" style="display: none;">
                    <div class="photo-preview-image">
                        <img src="" alt="Photo preview" class="img-fluid">
                        <button type="button" class="photo-delete-btn" data-photo-id="${photoData.id}" title="Remove photo">
                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
                        </button>
                    </div>
                    <div class="photo-preview-info">
                        <input type="text"
                               class="form-control form-control-sm photo-caption-input"
                               placeholder="Add a caption (optional)"
                               data-photo-id="${photoData.id}">
                        <small class="text-muted photo-filename">${this.truncateFileName(photoData.file.name)}</small>
                        <small class="text-muted photo-filesize">${this.formatFileSize(photoData.file.size)}</small>
                    </div>
                </div>
            </div>
        `;

        this.previewContainer.insertAdjacentHTML('beforeend', previewHTML);

        // Add event listener for delete button
        const deleteBtn = document.querySelector(`[data-photo-id="${photoData.id}"].photo-delete-btn`);
        deleteBtn.addEventListener('click', () => this.removePhoto(photoData.id));

        // Add event listener for caption input
        const captionInput = document.querySelector(`input.photo-caption-input[data-photo-id="${photoData.id}"]`);
        captionInput.addEventListener('input', (e) => {
            const photo = this.photos.find(p => p.id === photoData.id);
            if (photo) {
                photo.caption = e.target.value;
            }
        });
    }

    loadImagePreview(photoData) {
        const reader = new FileReader();
        const card = document.getElementById(photoData.id);
        const progressBar = card.querySelector('.progress-bar');
        const progressText = card.querySelector('.photo-upload-progress small');

        // Simulate progressive loading with progress bar
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 90) progress = 90;

            if (progressBar) {
                progressBar.style.width = `${progress}%`;
                progressBar.setAttribute('aria-valuenow', progress);
            }
            if (progressText) {
                progressText.textContent = `Loading... ${Math.round(progress)}%`;
            }
        }, 100);

        reader.onprogress = (e) => {
            if (e.lengthComputable) {
                const percentLoaded = Math.round((e.loaded / e.total) * 100);
                if (progressBar) {
                    progressBar.style.width = `${percentLoaded}%`;
                    progressBar.setAttribute('aria-valuenow', percentLoaded);
                }
                if (progressText) {
                    progressText.textContent = `Loading... ${percentLoaded}%`;
                }
            }
        };

        reader.onload = (e) => {
            clearInterval(progressInterval);

            const loadingDiv = card.querySelector('.photo-preview-loading');
            const contentDiv = card.querySelector('.photo-preview-content');
            const img = card.querySelector('.photo-preview-image img');

            img.src = e.target.result;

            // Complete progress bar
            if (progressBar) {
                progressBar.style.width = '100%';
                progressBar.setAttribute('aria-valuenow', 100);
            }
            if (progressText) {
                progressText.textContent = 'Complete!';
            }

            // Hide loading, show content
            setTimeout(() => {
                loadingDiv.style.display = 'none';
                contentDiv.style.display = 'block';
                card.classList.add('loaded');
            }, 300); // Small delay for smooth transition
        };

        reader.onerror = () => {
            clearInterval(progressInterval);
            this.showError(`Failed to load preview for ${photoData.file.name}`);
            this.removePhoto(photoData.id);
        };

        reader.readAsDataURL(photoData.file);
    }

    removePhoto(photoId) {
        // Remove from array
        this.photos = this.photos.filter(p => p.id !== photoId);

        // Remove from DOM
        const card = document.getElementById(photoId);
        if (card) {
            card.classList.add('removing');
            setTimeout(() => {
                card.remove();
                this.updateDropZoneVisibility();
            }, 300);
        }
    }

    updateDropZoneVisibility() {
        if (this.photos.length >= this.maxPhotos) {
            this.dropZone.classList.add('hidden');
        } else {
            this.dropZone.classList.remove('hidden');
        }

        // Update button text
        const remaining = this.maxPhotos - this.photos.length;
        if (remaining === 0) {
            this.addButton.disabled = true;
            this.addButton.textContent = `Maximum ${this.maxPhotos} photos reached`;
        } else {
            this.addButton.disabled = false;
            this.addButton.textContent = `📷 Choose Photos (${remaining} remaining)`;
        }
    }

    showError(message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'photo-upload-toast error';
        toast.innerHTML = `
            <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
            </svg>
            <span>${message}</span>
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    truncateFileName(name, maxLength = 30) {
        if (name.length <= maxLength) return name;
        const ext = name.split('.').pop();
        const nameWithoutExt = name.substring(0, name.lastIndexOf('.'));
        const truncated = nameWithoutExt.substring(0, maxLength - ext.length - 4);
        return `${truncated}...${ext}`;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    // Get photos for form submission
    getPhotos() {
        return this.photos;
    }

    // Method to prepare form data for submission
    appendToFormData(formData) {
        this.photos.forEach((photo, index) => {
            formData.append('photos', photo.file);
            formData.append('photo_captions', photo.caption || '');
        });
        return formData;
    }
}

// Auto-initialize if container exists
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('photoUploadContainer');
    if (container) {
        // Get max photos from data attribute or use default
        const maxPhotos = parseInt(container.dataset.maxPhotos) || 10;
        const minPhotos = parseInt(container.dataset.minPhotos) || 0;

        window.photoUploadManager = new PhotoUploadManager('photoUploadContainer', {
            maxPhotos: maxPhotos,
            minPhotos: minPhotos
        });
    }
});
