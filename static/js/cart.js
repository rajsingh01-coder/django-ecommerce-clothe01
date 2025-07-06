// Cart JavaScript for Fashion Store

$(document).ready(function() {
    // Add to cart functionality
    $('.add-to-cart-btn').on('click', function(e) {
        e.preventDefault();
        
        var button = $(this);
        var productId = button.data('product-id');
        var form = button.closest('form');
        
        if (form.length) {
            // Use form data
            var formData = form.serialize();
            addToCart(form.attr('action'), formData, button);
        } else {
            // Use default quantity
            var quantity = 1;
            var size = '';
            var color = '';
            
            // Get size and color if available
            var sizeSelect = form.find('select[name="size"]');
            var colorSelect = form.find('select[name="color"]');
            
            if (sizeSelect.length && sizeSelect.val()) {
                size = sizeSelect.val();
            }
            if (colorSelect.length && colorSelect.val()) {
                color = colorSelect.val();
            }
            
            var data = {
                'quantity': quantity,
                'size': size,
                'color': color,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            };
            
            addToCart('/add-to-cart/' + productId + '/', data, button);
        }
    });

    // Add to cart AJAX function
    function addToCart(url, data, button) {
        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            beforeSend: function() {
                button.prop('disabled', true);
                button.html('<span class="loading"></span>');
            },
            success: function(response) {
                if (response.success) {
                    // Update cart count
                    updateCartCount(response.cart_total);
                    
                    // Show success animation
                    FashionStore.addToCartAnimation(button);
                    
                    // Show success message
                    showMessage('Product added to cart successfully!', 'success');
                } else {
                    showMessage('Error: ' + response.message, 'error');
                    button.prop('disabled', false);
                    button.html('<i class="fas fa-cart-plus"></i>');
                }
            },
            error: function(xhr, status, error) {
                showMessage('Error adding product to cart', 'error');
                button.prop('disabled', false);
                button.html('<i class="fas fa-cart-plus"></i>');
            }
        });
    }

    // Update cart count
    function updateCartCount(count) {
        $('#cartCount').text(count);
        
        // Add animation
        $('#cartCount').addClass('pulse');
        setTimeout(function() {
            $('#cartCount').removeClass('pulse');
        }, 1000);
    }

    // Show message function
    function showMessage(message, type) {
        var alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        var icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
        
        var alert = $('<div class="alert ' + alertClass + ' alert-dismissible fade show" role="alert">' +
            '<i class="' + icon + ' me-2"></i>' + message +
            '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
            '</div>');
        
        // Insert at top of container
        $('.container').first().prepend(alert);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            alert.fadeOut();
        }, 5000);
    }

    // Cart item quantity update
    $('.cart-quantity-input').on('change', function() {
        var input = $(this);
        var itemId = input.data('item-id');
        var quantity = input.val();
        
        updateCartItem(itemId, quantity);
    });

    // Update cart item
    function updateCartItem(itemId, quantity) {
        $.ajax({
            url: '/cart/',
            method: 'POST',
            data: {
                'item_id': itemId,
                'action': 'update',
                'quantity': quantity,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.success) {
                    // Reload page to update totals
                    location.reload();
                } else {
                    showMessage('Error updating cart', 'error');
                }
            },
            error: function() {
                showMessage('Error updating cart', 'error');
            }
        });
    }

    // Remove cart item
    $('.remove-cart-item').on('click', function(e) {
        e.preventDefault();
        
        if (confirm('Are you sure you want to remove this item from your cart?')) {
            var button = $(this);
            var itemId = button.data('item-id');
            
                    $.ajax({
            url: '/cart/',
            method: 'POST',
            data: {
                'item_id': itemId,
                'action': 'remove',
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
                success: function(response) {
                    if (response.success) {
                        // Remove item from DOM
                        button.closest('.cart-item').fadeOut();
                        
                        // Update cart count
                        updateCartCount(response.cart_total);
                        
                        // Show success message
                        showMessage('Item removed from cart', 'success');
                        
                        // Reload page if cart is empty
                        if (response.cart_total === 0) {
                            setTimeout(function() {
                                location.reload();
                            }, 1000);
                        }
                    } else {
                        showMessage('Error removing item', 'error');
                    }
                },
                error: function() {
                    showMessage('Error removing item', 'error');
                }
            });
        }
    });

    // Cart total calculation
    function calculateCartTotal() {
        var total = 0;
        $('.cart-item-total').each(function() {
            total += parseFloat($(this).data('price')) * parseInt($(this).data('quantity'));
        });
        return total;
    }

    // Update cart totals
    function updateCartTotals() {
        var subtotal = calculateCartTotal();
        var shipping = 0; // Free shipping
        var tax = 0; // No tax for demo
        var total = subtotal + shipping + tax;
        
        $('#cart-subtotal').text('$' + subtotal.toFixed(2));
        $('#cart-shipping').text('$' + shipping.toFixed(2));
        $('#cart-tax').text('$' + tax.toFixed(2));
        $('#cart-total').text('$' + total.toFixed(2));
    }

    // Initialize cart functionality
    function initCart() {
        // Update totals on page load
        updateCartTotals();
        
        // Add quantity change listeners
        $('.cart-quantity-input').on('change', function() {
            updateCartTotals();
        });
    }

    // Initialize if on cart page
    if ($('.cart-page').length) {
        initCart();
    }

    // Mini cart dropdown
    $('.cart-dropdown-toggle').on('click', function(e) {
        e.preventDefault();
        
        // Load cart contents via AJAX
        $.ajax({
            url: '/cart/mini/',
            method: 'GET',
            success: function(response) {
                $('.cart-dropdown-menu').html(response);
            },
            error: function() {
                $('.cart-dropdown-menu').html('<div class="p-3 text-center">Error loading cart</div>');
            }
        });
    });

    // Checkout form validation
    $('.checkout-form').on('submit', function(e) {
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
            e.preventDefault();
            showMessage('Please fill in all required fields', 'error');
            return false;
        }
    });

    // Promo code functionality
    $('.promo-code-form').on('submit', function(e) {
        e.preventDefault();
        
        var code = $(this).find('input[name="promo_code"]').val();
        
        if (code) {
            // Simulate promo code validation
            setTimeout(function() {
                showMessage('Promo code applied successfully!', 'success');
            }, 1000);
        }
    });

    console.log('Cart functionality initialized!');
}); 