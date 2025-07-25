// Main JavaScript for Fashion Store

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Add loading state to buttons
    $('form').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        if (submitBtn.length) {
            var originalText = submitBtn.html();
            submitBtn.html('<span class="loading"></span> Processing...');
            submitBtn.prop('disabled', true);
            
            // Re-enable button after 5 seconds (fallback)
            setTimeout(function() {
                submitBtn.html(originalText);
                submitBtn.prop('disabled', false);
            }, 5000);
        }
    });

    // Product image gallery
    $('.thumbnail-img').on('click', function() {
        var slideIndex = $(this).data('bs-slide-to');
        $('#productCarousel').carousel(slideIndex);
    });

    // Quantity input validation
    $('input[type="number"]').on('input', function() {
        var value = parseInt($(this).val());
        var min = parseInt($(this).attr('min')) || 1;
        var max = parseInt($(this).attr('max')) || 99;
        
        if (value < min) {
            $(this).val(min);
        } else if (value > max) {
            $(this).val(max);
        }
    });

    // Search suggestions (placeholder)
    var searchTimeout;
    $('input[name="query"]').on('input', function() {
        clearTimeout(searchTimeout);
        var query = $(this).val();
        
        if (query.length > 2) {
            searchTimeout = setTimeout(function() {
                // Here you could implement AJAX search suggestions
                console.log('Searching for:', query);
            }, 300);
        }
    });

    // Newsletter subscription
    $('.newsletter-form').on('submit', function(e) {
        e.preventDefault();
        var email = $(this).find('input[type="email"]').val();
        
        if (email) {
            // Show success message
            $(this).html('<div class="alert alert-success">Thank you for subscribing!</div>');
        }
    });

    // Mobile menu toggle
    $('.navbar-toggler').on('click', function() {
        $(this).toggleClass('active');
    });

    // Back to top button
    var backToTop = $('<button class="btn btn-primary position-fixed" style="bottom: 20px; right: 20px; z-index: 1000; display: none;"><i class="fas fa-arrow-up"></i></button>');
    $('body').append(backToTop);

    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 300) {
            backToTop.fadeIn();
        } else {
            backToTop.fadeOut();
        }
    });

    backToTop.on('click', function() {
        $('html, body').animate({scrollTop: 0}, 800);
    });

    // Product card hover effects
    $('.product-card').on('mouseenter', function() {
        $(this).addClass('hover');
    }).on('mouseleave', function() {
        $(this).removeClass('hover');
    });

    // Form validation
    $('form').on('submit', function() {
        var isValid = true;
        var requiredFields = $(this).find('[required]');
        
        requiredFields.each(function() {
            if (!$(this).val()) {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            return false;
        }
    });

    // Remove validation classes on input
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid');
    });

    // Price formatting
    function formatPrice(price) {
        return '$' + parseFloat(price).toFixed(2);
    }

    // Update cart count
    function updateCartCount(count) {
        $('#cartCount').text(count);
    }

    // Add to cart animation
    function addToCartAnimation(button) {
        var originalText = button.html();
        button.html('<i class="fas fa-check"></i> Added!');
        button.addClass('btn-success').removeClass('btn-primary');
        
        setTimeout(function() {
            button.html(originalText);
            button.addClass('btn-primary').removeClass('btn-success');
        }, 2000);
    }

    // Global functions
    window.FashionStore = {
        formatPrice: formatPrice,
        updateCartCount: updateCartCount,
        addToCartAnimation: addToCartAnimation
    };

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
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

    // Responsive table
    $('.table-responsive').each(function() {
        var table = $(this).find('table');
        if (table.width() > $(this).width()) {
            $(this).addClass('table-scroll');
        }
    });

    // Auto-hide alerts
    $('.alert').each(function() {
        var alert = $(this);
        setTimeout(function() {
            alert.fadeOut();
        }, 5000);
    });

    // Success popup functionality
    function showSuccessPopup(message, title = 'Success!') {
        // Create popup HTML
        var popupHTML = `
            <div class="modal fade" id="successPopup" tabindex="-1" aria-labelledby="successPopupLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header bg-success text-white">
                            <h5 class="modal-title" id="successPopupLabel">
                                <i class="fas fa-check-circle me-2"></i>${title}
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center py-4">
                            <div class="mb-3">
                                <i class="fas fa-check-circle text-success" style="font-size: 3rem;"></i>
                            </div>
                            <p class="lead mb-0">${message}</p>
                        </div>
                        <div class="modal-footer justify-content-center">
                            <button type="button" class="btn btn-success" data-bs-dismiss="modal">OK</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing popup if any
        $('#successPopup').remove();
        
        // Add popup to body
        $('body').append(popupHTML);
        
        // Show popup
        var popup = new bootstrap.Modal(document.getElementById('successPopup'));
        popup.show();
        
        // Auto-hide after 3 seconds
        setTimeout(function() {
            popup.hide();
        }, 3000);
    }

    // Check for success messages and show popup
    if ($('.alert-success').length > 0) {
        var successMessage = $('.alert-success').first().text().trim();
        showSuccessPopup(successMessage);
    }

    // Contact form success handling
    $('form').on('submit', function(e) {
        var form = $(this);
        var submitBtn = form.find('button[type="submit"]');
        
        // Check if this is contact form
        if (form.find('input[name="name"], input[name="email"], textarea[name="message"]').length > 0) {
            // This is likely a contact form
            var originalText = submitBtn.html();
            submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Sending...');
            submitBtn.prop('disabled', true);
            
            // Re-enable button after form submission
            setTimeout(function() {
                submitBtn.html(originalText);
                submitBtn.prop('disabled', false);
            }, 3000);
        }
    });

    // Global success popup function
    window.showSuccessPopup = showSuccessPopup;

    // Initialize any additional plugins or features
    console.log('Fashion Store initialized successfully!');
}); 