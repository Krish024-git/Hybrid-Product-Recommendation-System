/* --- Dynamic Application Script: Animations, Search, Filters, & Canvas Background --- */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Floating Particles Background Canvas
    initParticlesBackground();
    
    // 2. Set Up Range Sliders dynamic value updates
    setupRangeSliders();
    
    // 3. Configure Search and Filters
    setupSearchAndFilters();
    
    // 4. Set Up Page Transitions & Animations
    setupPageAnimations();
});

/**
 * Renders a lightweight, high-performance canvas particle field in the background.
 */
function initParticlesBackground() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationFrameId;
    let mouse = { x: null, y: null, radius: 140 };
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    
    window.addEventListener('mouseleave', () => {
        mouse.x = null;
        mouse.y = null;
    });
    
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2.5 + 1; // Slightly larger particles
            this.speedX = (Math.random() - 0.5) * 0.4;
            this.speedY = (Math.random() - 0.5) * 0.4;
            this.color = Math.random() > 0.5 ? 'rgba(37, 99, 235, 0.15)' : 'rgba(139, 92, 246, 0.15)';
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            
            // Loop screen boundaries
            if (this.x < 0) this.x = canvas.width;
            if (this.x > canvas.width) this.x = 0;
            if (this.y < 0) this.y = canvas.height;
            if (this.y > canvas.height) this.y = 0;
        }
        
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function init() {
        const count = Math.min(Math.floor((canvas.width * canvas.height) / 12000), 80);
        particles = [];
        for (let i = 0; i < count; i++) {
            particles.push(new Particle());
        }
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw constellation lines
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            
            for (let j = i + 1; j < particles.length; j++) {
                const dist = Math.hypot(particles[i].x - particles[j].x, particles[i].y - particles[j].y);
                if (dist < 110) {
                    const alpha = (1 - dist / 110) * 0.08;
                    ctx.strokeStyle = `rgba(37, 99, 235, ${alpha})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
            
            // Connect to mouse cursor
            if (mouse.x !== null && mouse.y !== null) {
                const distToMouse = Math.hypot(particles[i].x - mouse.x, particles[i].y - mouse.y);
                if (distToMouse < mouse.radius) {
                    const alpha = (1 - distToMouse / mouse.radius) * 0.12;
                    ctx.strokeStyle = `rgba(37, 99, 235, ${alpha})`;
                    ctx.lineWidth = 0.6;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(mouse.x, mouse.y);
                    ctx.stroke();
                }
            }
        }
        
        animationFrameId = requestAnimationFrame(animate);
    }
    
    init();
    animate();
    
    // Re-initialize count on resize
    window.addEventListener('resize', () => {
        init();
    });
}

/**
 * Automatically updates text labels attached to sliders when adjusted.
 */
function setupRangeSliders() {
    const priceSlider = document.getElementById('price-range');
    const priceVal = document.getElementById('price-val');
    if (priceSlider && priceVal) {
        priceSlider.addEventListener('input', (e) => {
            priceVal.textContent = `₹${parseFloat(e.target.value).toLocaleString()}`;
        });
    }
    
    const ratingSlider = document.getElementById('rating-range');
    const ratingVal = document.getElementById('rating-val');
    if (ratingSlider && ratingVal) {
        ratingSlider.addEventListener('input', (e) => {
            ratingVal.textContent = `${parseFloat(e.target.value).toFixed(1)} ★`;
        });
    }

    const alphaSlider = document.getElementById('alpha-range');
    const alphaVal = document.getElementById('alpha-val');
    if (alphaSlider && alphaVal) {
        alphaSlider.addEventListener('input', (e) => {
            alphaVal.textContent = parseFloat(e.target.value).toFixed(1);
        });
        alphaSlider.addEventListener('change', (e) => {
            const val = e.target.value;
            const url = new URL(window.location.href);
            url.searchParams.set('alpha', val);
            window.location.href = url.toString();
        });
    }
}

/**
 * Implements real-time filtering on the products listing container (Local Search & Filters).
 */
function setupSearchAndFilters() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const brandFilter = document.getElementById('brand-filter');
    const priceSlider = document.getElementById('price-range');
    const ratingSlider = document.getElementById('rating-range');
    
    const productGrid = document.getElementById('product-grid');
    const productCards = document.querySelectorAll('.product-card-item');
    const heroSearchInput = document.getElementById('hero-search-input');
    
    // Exit if filters are not on the current page
    if (!productCards.length) return;
    
    // Sync Hero Search input and Sidebar Search input
    if (heroSearchInput && searchInput) {
        heroSearchInput.addEventListener('input', (e) => {
            searchInput.value = e.target.value;
            filterProducts();
        });
        searchInput.addEventListener('input', (e) => {
            heroSearchInput.value = e.target.value;
            filterProducts();
        });
    }
    
    function filterProducts() {
        const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const selectedCategory = categoryFilter ? categoryFilter.value : 'all';
        const selectedBrand = brandFilter ? brandFilter.value : 'all';
        const maxPrice = priceSlider ? parseFloat(priceSlider.value) : Infinity;
        const minRating = ratingSlider ? parseFloat(ratingSlider.value) : 0;
        
        let visibleCount = 0;
        
        productCards.forEach(card => {
            const name = card.dataset.name.toLowerCase();
            const brand = card.dataset.brand.toLowerCase();
            const category = card.dataset.category.toLowerCase();
            const price = parseFloat(card.dataset.price);
            const rating = parseFloat(card.dataset.rating);
            const desc = card.dataset.desc ? card.dataset.desc.toLowerCase() : '';
            
            // Checking filters match
            const queryMatch = query === '' || 
                               name.includes(query) || 
                               brand.includes(query) || 
                               desc.includes(query) ||
                               category.includes(query);
                               
            const categoryMatch = selectedCategory === 'all' || category === selectedCategory.toLowerCase();
            const brandMatch = selectedBrand === 'all' || brand === selectedBrand.toLowerCase();
            const priceMatch = price <= maxPrice;
            const ratingMatch = rating >= minRating;
            
            if (queryMatch && categoryMatch && brandMatch && priceMatch && ratingMatch) {
                card.style.display = 'block';
                // Add fade-in transition
                card.classList.add('fade-in');
                visibleCount++;
            } else {
                card.style.display = 'none';
                card.classList.remove('fade-in');
            }
        });
        
        if (noResults) {
            if (visibleCount === 0) {
                noResults.classList.remove('hidden');
            } else {
                noResults.classList.add('hidden');
            }
        }
    }
    
    // Bind listeners
    if (searchInput) searchInput.addEventListener('input', filterProducts);
    if (heroSearchInput) heroSearchInput.addEventListener('input', filterProducts);
    if (categoryFilter) categoryFilter.addEventListener('change', filterProducts);
    if (brandFilter) brandFilter.addEventListener('change', filterProducts);
    if (priceSlider) priceSlider.addEventListener('input', filterProducts);
    if (ratingSlider) ratingSlider.addEventListener('input', filterProducts);
}

/**
 * Handles smooth load actions and page load transitions.
 */
function setupPageAnimations() {
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
}

/**
 * Triggers recommendation feedback and displays asynchronous loading states.
 */
function requestRecommendationFeedback(productId, btn) {
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg> Logged!
    `;
    
    // Simulated AJAX request logging interaction for SQLite and training
    setTimeout(() => {
        btn.innerHTML = `<span class="text-emerald-600">✓ Logged</span>`;
        btn.classList.add('border-emerald-300', 'bg-emerald-50');
        
        // Dynamic notification toast
        showToast("Success", "Recommendation logged successfully to your database history.");
    }, 800);
}

/**
 * Simple client-side notification toast.
 */
function showToast(title, message) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-5 right-5 glass p-4 rounded-xl border border-blue-200 shadow-xl flex flex-col z-50 fade-in max-w-sm';
    toast.innerHTML = `
        <div class="flex justify-between items-center mb-1">
            <span class="font-bold text-sm text-blue-600 font-display">${title}</span>
            <button class="text-xs text-slate-400 hover:text-slate-700" onclick="this.parentElement.parentElement.remove()">✕</button>
        </div>
        <p class="text-xs text-slate-600">${message}</p>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.5s ease';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}
