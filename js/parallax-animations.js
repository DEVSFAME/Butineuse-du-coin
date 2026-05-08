// Parallax et animations pour Les Butineuses du Coin
document.addEventListener('DOMContentLoaded', function() {
    // Variables pour l'effet parallaxe
    const parallaxBg = document.querySelector('.parallax-bg');
    const parallaxContent = document.querySelector('.parallax-content');
    
    // Intersection Observer pour les animations au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observer pour les éléments de révélation
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    });

    // Ajouter les classes d'animation aux sections
    const sections = document.querySelectorAll('.section_persona, .section_product6, .section_layout218, .section_layout472, .section_testimonial10, .section_blog34, .section_cta3');
    sections.forEach(section => {
        section.classList.add('scroll-animate');
        observer.observe(section);
    });

    // Observer les éléments produits
    const productItems = document.querySelectorAll('.product6_item');
    productItems.forEach(item => {
        item.classList.add('reveal-on-scroll');
        revealObserver.observe(item);
    });

    // Observer les articles de blog
    const blogItems = document.querySelectorAll('.blog34_item');
    blogItems.forEach(item => {
        item.classList.add('reveal-on-scroll');
        revealObserver.observe(item);
    });

    // Effet parallaxe au scroll avec effets élaborés pour le titre
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.7; // Vitesse de parallaxe background
        const rateContent = scrolled * -0.2; // Vitesse différente pour le contenu
        const titleElement = document.querySelector('.hero_heading');
        const heroSection = document.querySelector('.section_hero');
        
        if (parallaxBg) {
            parallaxBg.style.transform = `translate3d(0, ${rate}px, 0)`;
        }
        
        if (parallaxContent) {
            parallaxContent.style.transform = `translate3d(0, ${rateContent}px, 0)`;
        }
        
        // Effet parallaxe élaboré pour le titre
        if (titleElement && heroSection) {
            const heroHeight = heroSection.offsetHeight;
            const scrollPercent = scrolled / heroHeight;
            const titleRate = scrolled * -0.4;
            const scaleValue = Math.max(0.8, 1 - scrollPercent * 0.3);
            const opacityValue = Math.max(0, 1 - scrollPercent * 1.5);
            const rotateValue = scrollPercent * 5;
            
            titleElement.style.transform = `translate3d(0, ${titleRate}px, 0) scale(${scaleValue}) rotateX(${rotateValue}deg)`;
            titleElement.style.opacity = opacityValue;
            
            // Effet de perspective 3D sur le titre
            if (scrollPercent < 0.8) {
                titleElement.style.filter = `blur(${scrollPercent * 2}px) brightness(${1 + scrollPercent * 0.3})`;
            }
        }
        
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }

    // Écouter le scroll pour l'effet parallaxe
    window.addEventListener('scroll', requestTick);

    // Animation des cartes produits au hover
    const productCards = document.querySelectorAll('.product6_item-link');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Animation du titre avec effet de machine à écrire
    function typewriterEffect() {
        const title = document.querySelector('.animate-title');
        if (title) {
            const text = title.textContent;
            title.textContent = '';
            title.style.opacity = '1';
            
            let i = 0;
            const timer = setInterval(() => {
                if (i < text.length) {
                    title.textContent += text.charAt(i);
                    i++;
                } else {
                    clearInterval(timer);
                }
            }, 80);
        }
    }

    // Démarrer l'effet machine à écrire après un délai
    setTimeout(typewriterEffect, 1000);

    // Smooth scroll pour les liens d'ancrage
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Effet de parallaxe pour les particules
    const particles = document.querySelectorAll('.particle');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        particles.forEach((particle, index) => {
            const speed = 0.5 + (index * 0.1);
            const yPos = -(scrolled * speed);
            particle.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });
    });

    // Animation des statistiques avec compteur
    function animateCounters() {
        const counters = document.querySelectorAll('.heading-style-h2');
        counters.forEach(counter => {
            const target = parseInt(counter.textContent);
            if (target && !isNaN(target)) {
                let count = 0;
                const increment = target / 50;
                
                const timer = setInterval(() => {
                    count += increment;
                    if (count >= target) {
                        counter.textContent = target;
                        clearInterval(timer);
                    } else {
                        counter.textContent = Math.floor(count);
                    }
                }, 50);
            }
        });
    }

    // Observer pour les compteurs
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const statsSection = document.querySelector('.section_layout218');
    if (statsSection) {
        counterObserver.observe(statsSection);
    }

    // Amélioration de la performance avec will-change
    function optimizeForAnimation() {
        const animatedElements = document.querySelectorAll('.parallax-bg, .parallax-content, .particle');
        animatedElements.forEach(el => {
            el.style.willChange = 'transform';
        });
    }

    optimizeForAnimation();

    // Gérer le changement de logo au scroll
    const logoImage = document.querySelector('.navbar2_logo-image');
    const logoClairSrc = 'images/logo-clair.png';
    const logoFonceSrc = 'logo.jpg';

    function handleLogoScroll() {
        if (window.scrollY > 50) {
            if (logoImage && !logoImage.src.includes(logoFonceSrc)) {
                logoImage.src = logoFonceSrc;
            }
        } else {
            if (logoImage && !logoImage.src.includes(logoClairSrc)) {
                logoImage.src = logoClairSrc;
            }
        }
    }

    window.addEventListener('scroll', handleLogoScroll);
});

// Fonction pour gérer le redimensionnement de la fenêtre
window.addEventListener('resize', function() {
    // Recalculer les positions si nécessaire
    const particles = document.querySelectorAll('.particle');
    particles.forEach(particle => {
        particle.style.transform = 'translate3d(0, 0, 0)';
    });
});
