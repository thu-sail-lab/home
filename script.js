// Research Organization Website JavaScript

// Navigation functionality
class Navigation {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        this.mobileNav = document.querySelector('.mobile-nav');
        this.navLinks = document.querySelectorAll('.nav-links a, .mobile-nav-links a');
        this.pages = document.querySelectorAll('.page');

        this.init();
    }

    init() {
        this.setupScrollEffect();
        this.setupMobileMenu();
        this.setupPageNavigation();
        this.setupAnimations();
    }

    setupScrollEffect() {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                this.navbar.classList.add('scrolled');
            } else {
                this.navbar.classList.remove('scrolled');
            }
        });
    }

    setupMobileMenu() {
        if (this.mobileMenuBtn) {
            this.mobileMenuBtn.addEventListener('click', () => {
                this.mobileNav.classList.toggle('active');
                document.body.classList.toggle('mobile-nav-open');
                const icon = this.mobileMenuBtn.querySelector('i');
                if (this.mobileNav.classList.contains('active')) {
                    icon.className = 'fas fa-times';
                } else {
                    icon.className = 'fas fa-bars';
                }
            });
        }
    }

    setupPageNavigation() {
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetPage = link.getAttribute('data-page');
                if (targetPage) {
                    this.showPage(targetPage);
                    this.updateActiveLink(link);

                    // Close mobile menu if open
                    if (this.mobileNav.classList.contains('active')) {
                        this.mobileNav.classList.remove('active');
                        document.body.classList.remove('mobile-nav-open');
                        const icon = this.mobileMenuBtn.querySelector('i');
                        icon.className = 'fas fa-bars';
                    }
                }
            });
        });

        // Add event listeners for quick-nav-link elements and other data-page links
        document.addEventListener('click', (e) => {
            const link = e.target.closest('[data-page]');
            if (link && !link.classList.contains('nav-links') && !link.closest('.mobile-nav-links')) {
                e.preventDefault();
                const targetPage = link.getAttribute('data-page');
                if (targetPage) {
                    this.showPage(targetPage);
                    this.updateActiveLink(document.querySelector(`.nav-links a[data-page="${targetPage}"]`) || link);
                }
            }
        });

        // Show default page
        this.showPage('home');
    }

    showPage(pageName) {
        // Hide all pages
        this.pages.forEach(page => {
            page.classList.remove('active');
        });

        // Show target page
        const targetPage = document.getElementById(pageName);
        if (targetPage) {
            targetPage.classList.add('active');
            this.addPageAnimations(targetPage);
        }

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    updateActiveLink(activeLink) {
        // Remove active class from all links
        this.navLinks.forEach(link => {
            link.classList.remove('active');
        });

        // Add active class to clicked link
        activeLink.classList.add('active');

        // Also update corresponding desktop/mobile link
        const targetPage = activeLink.getAttribute('data-page');
        this.navLinks.forEach(link => {
            if (link.getAttribute('data-page') === targetPage) {
                link.classList.add('active');
            }
        });
    }

    setupAnimations() {
        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);

        // Observe all animatable elements
        document.querySelectorAll('.card, .member-card, .partner-card, .contact-card').forEach(el => {
            observer.observe(el);
        });
    }

    addPageAnimations(page) {
        // Remove any existing animation classes first
        this.resetPageAnimations(page);

        // Get page type for specific animations
        const pageId = page.id;

        // Hero section animation
        const heroContainer = page.querySelector('.hero-container');
        if (heroContainer) {
            heroContainer.classList.add('animate-on-enter');
            setTimeout(() => {
                heroContainer.classList.add('visible');
            }, 100);
        }

        // Section headers animation
        const sectionHeaders = page.querySelectorAll('.section-header');
        sectionHeaders.forEach((header, index) => {
            header.classList.add('animate-on-enter');
            setTimeout(() => {
                header.classList.add('visible');
            }, 200 + (index * 150));
        });

        // Page-specific animations
        switch(pageId) {
            case 'publications':
                this.animatePublicationsPage(page);
                break;
            case 'team':
                this.animateTeamPage(page);
                break;
            case 'research':
                this.animateResearchPage(page);
                break;
            case 'partners':
                this.animatePartnersPage(page);
                break;
            case 'contact':
                this.animateContactPage(page);
                break;
            case 'home':
                this.animateHomePage(page);
                break;
        }

        // Special sections that can appear on multiple pages
        this.animateSpecialSections(page);
    }

    resetPageAnimations(page) {
        // Remove animation classes from all elements
        const animatedElements = page.querySelectorAll('.animate-on-enter, .visible');
        animatedElements.forEach(el => {
            el.classList.remove('animate-on-enter', 'visible', 'fade-in', 'scale-in', 'fade-in-left', 'fade-in-right');
        });
    }

    animatePublicationsPage(page) {
        // Publication filter buttons
        const filterButtons = page.querySelectorAll('.publication-filter');
        filterButtons.forEach((button, index) => {
            button.classList.add('animate-on-enter');
            setTimeout(() => {
                button.classList.add('visible');
            }, 300 + (index * 50));
        });

        // Publication items with staggered animation
        const publicationItems = page.querySelectorAll('.publication-item');
        publicationItems.forEach((item, index) => {
            item.classList.add('animate-on-enter');
            setTimeout(() => {
                item.classList.add('visible');
            }, 400 + (index * 100));
        });

        // Year headers
        const yearHeaders = page.querySelectorAll('h3[style*="position: relative"]');
        yearHeaders.forEach((header, index) => {
            header.classList.add('publication-year-header', 'animate-on-enter');
            setTimeout(() => {
                header.classList.add('visible');
            }, 350 + (index * 200));
        });

        // Stats section
        const statsSection = page.querySelector('.stats-section');
        if (statsSection) {
            statsSection.classList.add('animate-on-enter');
            setTimeout(() => {
                statsSection.classList.add('visible');
            }, 600);
        }
    }

    animateTeamPage(page) {
        // Principal investigator (special animation)
        const principalSection = page.querySelector('.principal-section');
        if (principalSection) {
            principalSection.classList.add('animate-on-enter');
            setTimeout(() => {
                principalSection.classList.add('visible');
            }, 300);
        }

        // Team member cards
        const memberCards = page.querySelectorAll('.member-card');
        memberCards.forEach((card, index) => {
            card.classList.add('animate-on-enter');
            setTimeout(() => {
                card.classList.add('visible');
            }, 500 + (index * 150));
        });

        // CTA sections
        const ctaSections = page.querySelectorAll('[style*="background: linear-gradient(135deg, #2563eb"]');
        ctaSections.forEach((section, index) => {
            section.classList.add('animate-on-enter');
            setTimeout(() => {
                section.classList.add('visible');
            }, 800 + (index * 200));
        });
    }

    animateResearchPage(page) {
        // Research cards
        const researchCards = page.querySelectorAll('.card');
        researchCards.forEach((card, index) => {
            card.classList.add('animate-on-enter');
            setTimeout(() => {
                card.classList.add('visible');
            }, 300 + (index * 120));
        });
    }

    animatePartnersPage(page) {
        // Partner cards
        const partnerCards = page.querySelectorAll('.partner-card');
        partnerCards.forEach((card, index) => {
            card.classList.add('animate-on-enter');
            setTimeout(() => {
                card.classList.add('visible');
            }, 300 + (index * 100));
        });

        // Partner slider
        const partnerSlider = page.querySelector('.partners-slider-container');
        if (partnerSlider) {
            partnerSlider.classList.add('animate-on-enter');
            setTimeout(() => {
                partnerSlider.classList.add('visible');
            }, 600);
        }
    }

    animateContactPage(page) {
        // Contact cards
        const contactCards = page.querySelectorAll('.contact-card');
        contactCards.forEach((card, index) => {
            card.classList.add('animate-on-enter');
            setTimeout(() => {
                card.classList.add('visible');
            }, 300 + (index * 150));
        });
    }

    animateHomePage(page) {
        // Home page cards
        const homeCards = page.querySelectorAll('.card');
        homeCards.forEach((card, index) => {
            card.classList.add('animate-on-enter');
            setTimeout(() => {
                card.classList.add('visible');
            }, 300 + (index * 120));
        });

        // Stats section
        const statsSection = page.querySelector('.stats-section');
        if (statsSection) {
            statsSection.classList.add('animate-on-enter');
            setTimeout(() => {
                statsSection.classList.add('visible');
            }, 500);
        }

        // Recent publications on home
        const recentPublications = page.querySelectorAll('.publication-item');
        recentPublications.forEach((item, index) => {
            item.classList.add('animate-on-enter');
            setTimeout(() => {
                item.classList.add('visible');
            }, 400 + (index * 80));
        });
    }

    animateSpecialSections(page) {
        // Research impact section
        const researchImpactSection = page.querySelector('.research-impact-section');
        if (researchImpactSection) {
            researchImpactSection.classList.add('animate-on-enter');
            setTimeout(() => {
                researchImpactSection.classList.add('visible');
            }, 500);
        }

        // Key venues section
        const keyVenuesSection = page.querySelector('.key-venues-section');
        if (keyVenuesSection) {
            keyVenuesSection.classList.add('animate-on-enter');
            setTimeout(() => {
                keyVenuesSection.classList.add('visible');
            }, 600);
        }

        // Venue cards
        const venueCards = page.querySelectorAll('.venue-card');
        venueCards.forEach((card, index) => {
            card.classList.add('animate-on-enter');
            setTimeout(() => {
                card.classList.add('visible');
            }, 700 + (index * 100));
        });

        // Floating contact button
        const floatingContact = document.querySelector('.floating-contact');
        if (floatingContact) {
            floatingContact.classList.add('animate-on-enter');
            setTimeout(() => {
                floatingContact.classList.add('visible');
            }, 1000);
        }
    }
}

// Statistics Counter Animation
class StatsCounter {
    constructor() {
        this.counters = document.querySelectorAll('.stat-number');
        this.init();
    }

    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    this.animateCounter(entry.target);
                    entry.target.classList.add('counted');
                }
            });
        }, { threshold: 0.5 });

        this.counters.forEach(counter => {
            observer.observe(counter);
        });
    }

    animateCounter(element) {
        const target = parseInt(element.textContent);
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        };

        updateCounter();
    }
}

// Research Publications Filter
class PublicationsFilter {
    constructor() {
        this.filterButtons = document.querySelectorAll('.publication-filter');
        this.publications = document.querySelectorAll('.publication-item');
        this.countElement = document.getElementById('publication-count');
        this.init();
    }

    init() {
        if (this.filterButtons.length > 0) {
            this.setupFilters();
            this.updateCount('all');
        }
    }

    setupFilters() {
        this.filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                const filter = button.getAttribute('data-category');
                this.filterPublications(filter);
                this.updateActiveFilter(button);
                this.updateCount(filter);
            });
        });
    }

    filterPublications(filter) {
        let visibleCount = 0;
        this.publications.forEach(publication => {
            const categories = publication.getAttribute('data-category');
            
            // Check if publication matches filter
            let matches = false;
            
            if (filter === 'all') {
                matches = true;
            } else if (categories === filter) {
                // Traditional category matching (ieee, journals, conferences)
                matches = true;
            } else if (publication.hasAttribute(`data-${filter}`)) {
                // Topic-based filtering using data-{topic}="true" attributes
                matches = publication.getAttribute(`data-${filter}`) === 'true';
            }

            if (matches) {
                publication.style.display = 'block';
                publication.classList.add('fade-in');
                visibleCount++;
            } else {
                publication.style.display = 'none';
                publication.classList.remove('fade-in');
            }
        });
    }

    updateActiveFilter(activeButton) {
        this.filterButtons.forEach(button => {
            button.classList.remove('active');
            button.classList.remove('btn-primary');
            button.classList.add('btn-secondary');
        });
        activeButton.classList.add('active');
        activeButton.classList.remove('btn-secondary');
        activeButton.classList.add('btn-primary');
    }

    updateCount(filter) {
        if (this.countElement) {
            const visiblePubs = Array.from(this.publications).filter(pub => 
                pub.style.display !== 'none'
            );
            this.countElement.textContent = visiblePubs.length;
        }
    }
}

// Contact Form Handler
class ContactForm {
    constructor() {
        this.form = document.getElementById('contact-form');
        this.init();
    }

    init() {
        if (this.form) {
            this.setupFormSubmission();
        }
    }

    setupFormSubmission() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });
    }

    handleFormSubmit() {
        // Get form data
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData);

        // Simple validation
        if (!data.name || !data.email || !data.message) {
            this.showMessage('Please fill in all required fields.', 'error');
            return;
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            this.showMessage('Please enter a valid email address.', 'error');
            return;
        }

        // Simulate form submission
        this.showMessage('Thank you for your message! We\'ll get back to you soon.', 'success');
        this.form.reset();
    }

    showMessage(message, type) {
        // Remove existing message
        const existingMessage = document.querySelector('.form-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        // Create new message
        const messageEl = document.createElement('div');
        messageEl.className = `form-message ${type}`;
        messageEl.textContent = message;

        // Insert message
        this.form.insertBefore(messageEl, this.form.firstChild);

        // Remove message after 5 seconds
        setTimeout(() => {
            messageEl.remove();
        }, 5000);
    }
}

// Search Functionality
class SearchHandler {
    constructor() {
        this.searchInput = document.getElementById('search-input');
        this.searchResults = document.getElementById('search-results');
        this.searchableContent = [];
        this.init();
    }

    init() {
        if (this.searchInput) {
            this.buildSearchIndex();
            this.setupSearch();
        }
    }

    buildSearchIndex() {
        // Build searchable content from all pages
        const pages = document.querySelectorAll('.page');
        pages.forEach(page => {
            const pageId = page.id;
            const headings = page.querySelectorAll('h1, h2, h3, h4');
            const paragraphs = page.querySelectorAll('p');

            headings.forEach(heading => {
                this.searchableContent.push({
                    type: 'heading',
                    page: pageId,
                    title: heading.textContent,
                    content: heading.textContent,
                    element: heading
                });
            });

            paragraphs.forEach(paragraph => {
                if (paragraph.textContent.length > 50) {
                    this.searchableContent.push({
                        type: 'content',
                        page: pageId,
                        title: this.getHeadingContext(paragraph),
                        content: paragraph.textContent,
                        element: paragraph
                    });
                }
            });
        });
    }

    getHeadingContext(element) {
        let current = element.previousElementSibling;
        while (current) {
            if (current.matches('h1, h2, h3, h4, h5, h6')) {
                return current.textContent;
            }
            current = current.previousElementSibling;
        }
        return 'Content';
    }

    setupSearch() {
        this.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (query.length > 2) {
                this.performSearch(query);
            } else {
                this.hideSearchResults();
            }
        });

        // Hide search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.searchResults.contains(e.target)) {
                this.hideSearchResults();
            }
        });
    }

    performSearch(query) {
        const results = this.searchableContent.filter(item =>
            item.content.toLowerCase().includes(query.toLowerCase())
        );

        this.displaySearchResults(results, query);
    }

    displaySearchResults(results, query) {
        if (results.length === 0) {
            this.searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
        } else {
            const resultsHTML = results.slice(0, 8).map(result => `
                <div class="search-result-item" onclick="navigation.showPage('${result.page}')">
                    <div class="search-result-title">${result.title}</div>
                    <div class="search-result-content">${this.highlightQuery(result.content, query)}</div>
                    <div class="search-result-page">${this.formatPageName(result.page)}</div>
                </div>
            `).join('');

            this.searchResults.innerHTML = resultsHTML;
        }

        this.searchResults.style.display = 'block';
    }

    highlightQuery(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        const highlighted = text.replace(regex, '<mark>$1</mark>');

        // Truncate if too long
        if (highlighted.length > 150) {
            const queryIndex = highlighted.toLowerCase().indexOf(query.toLowerCase());
            const start = Math.max(0, queryIndex - 50);
            const end = Math.min(highlighted.length, queryIndex + query.length + 50);
            return '...' + highlighted.substring(start, end) + '...';
        }

        return highlighted;
    }

    formatPageName(pageId) {
        const pageNames = {
            'home': 'Home',
            'research': 'Research',
            'team': 'Team',
            'partners': 'Partners',
            'contact': 'Contact'
        };
        return pageNames[pageId] || pageId;
    }

    hideSearchResults() {
        this.searchResults.style.display = 'none';
    }
}

// Theme Toggle (optional feature)
class ThemeToggle {
    constructor() {
        this.toggleBtn = document.getElementById('theme-toggle');
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        if (this.toggleBtn) {
            this.applyTheme();
            this.setupToggle();
        }
    }

    setupToggle() {
        this.toggleBtn.addEventListener('click', () => {
            this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
            this.applyTheme();
            localStorage.setItem('theme', this.currentTheme);
        });
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        const icon = this.toggleBtn.querySelector('i');
        if (icon) {
            icon.className = this.currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all components
    window.navigation = new Navigation();
    new StatsCounter();
    new PublicationsFilter();
    new ContactForm();
    new SearchHandler();
    new ThemeToggle();

    // Add smooth scrolling to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states for images
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('load', () => {
            img.classList.add('loaded');
        });

        img.addEventListener('error', () => {
            img.classList.add('error');
            // Fallback for broken images
            img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0zNSA2NUw1MCA0NUw2NSA2NSIgc3Ryb2tlPSIjOTM5N0E0IiBzdHJva2Utd2lkdGg9IjIiIGZpbGw9Im5vbmUiLz4KPGNpcmNsZSBjeD0iNDAiIGN5PSIzNSIgcj0iNSIgZmlsbD0iIzkzOTdBNCIvPgo8L3N2Zz4K';
        });
    });

    // Performance optimization: Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});

// Old PublicationFilter class removed - using PublicationsFilter above instead

// Global utility functions
window.utils = {
    // Debounce function for performance optimization
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Format numbers with commas
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    // Copy text to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('Copied to clipboard');
        });
    },

    // Generate random ID
    generateId: function() {
        return Math.random().toString(36).substr(2, 9);
    }
};

// Publication Layout Enhancement
function enhancePublicationLayout() {
    // Add compact class to featured publications container
    const featuredContainer = document.getElementById('featured-publications');
    if (featuredContainer) {
        featuredContainer.classList.add('compact');
    }

    // Add compact class to all publications container
    const allPublicationsContainer = document.getElementById('all-publications');
    if (allPublicationsContainer) {
        allPublicationsContainer.classList.add('compact');
    }

    // Add compact class to all publication items
    const publicationItems = document.querySelectorAll('.publication-item');
    publicationItems.forEach(item => {
        item.classList.add('compact');
    });

    console.log(`Enhanced ${publicationItems.length} publication items with compact layout`);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize navigation
    initNavigation();

    // Initialize publication filters
    initPublicationFilters();

    // Initialize partners slider
    initPartnersSlider();

    // Enhance publication layout
    enhancePublicationLayout();
});
