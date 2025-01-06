document.querySelectorAll('.btn-add-to-cart').forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();
        const productId = button.dataset.productId;

        fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        }).then(response => {
            if (response.ok) {
                alert('Item added to cart!');
            } else {
                alert('Error adding item to cart.');
            }
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
