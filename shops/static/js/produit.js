// Éléments DOM
const modal = document.getElementById('product-modal');
const modalTitle = document.getElementById('modal-title');
const addProductBtn = document.getElementById('add-product-btn');
const closeModalBtn = document.getElementById('close-modal');
const cancelBtn = document.getElementById('cancel-btn');
const imageUpload = document.getElementById('image-upload');
const imageInput = document.getElementById('product-image');
const imagePreview = document.getElementById('image-preview');
const deleteModal = document.getElementById('delete-modal');
let productIdToDelete = null;

// Configuration des événements
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    addProductBtn.addEventListener('click', () => openModal());
    closeModalBtn.addEventListener('click', () => closeModal());
    cancelBtn.addEventListener('click', () => closeModal());
    
    imageUpload.addEventListener('click', () => imageInput.click());
    imageInput.addEventListener('change', handleImagePreview);
    
    // Fermer modal avec ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
            closeDeleteModal();
        }
    });
    
    // Fermer modal en cliquant en dehors
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });
    
    deleteModal.addEventListener('click', (e) => {
        if (e.target === deleteModal) closeDeleteModal();
    });
}

// Ouvrir modal pour ajout/modification
function openModal(product = null) {
    const form = document.getElementById('product-form');
    
    if (product) {
        modalTitle.textContent = 'Modifier le produit';
        document.getElementById('product-id').value = product.id;
        document.getElementById('product-name').value = product.name;
        document.getElementById('product-description').value = product.description || '';
        document.getElementById('product-price').value = product.price;
        
        if (product.image_url) {
            imagePreview.src = product.image_url;
            imagePreview.style.display = 'block';
        }
    } else {
        modalTitle.textContent = 'Ajouter un produit';
        form.reset();
        imagePreview.style.display = 'none';
    }
    
    modal.style.display = 'flex';
    document.getElementById('product-name').focus();
}

// Fermer modal
function closeModal() {
    modal.style.display = 'none';
    document.getElementById('product-form').reset();
    imagePreview.style.display = 'none';
}

// Prévisualisation d'image
function handleImagePreview(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    // Vérifier la taille du fichier (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        alert('L\'image est trop volumineuse (max 5MB)');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Éditer un produit (sera appelé depuis le template)
window.editProduct = function(productId) {
    // Récupérer les données du produit depuis les attributs data
    const productCard = document.querySelector(`.product-card[data-id="${productId}"]`);
    
    if (productCard) {
        const product = {
            id: productId,
            name: productCard.querySelector('.product-name').textContent,
            description: productCard.querySelector('.product-description').textContent,
            price: parseFloat(productCard.querySelector('.product-price').textContent),
            image_url: productCard.querySelector('img').src
        };
        
        openModal(product);
    }
};

// Supprimer un produit (ouvrir modal de confirmation)
window.deleteProduct = function(productId) {
    productIdToDelete = productId;
    document.getElementById('delete-product-id').value = productId;
    deleteModal.style.display = 'flex';
};

// Fermer la modal de suppression
function closeDeleteModal() {
    deleteModal.style.display = 'none';
    productIdToDelete = null;
}

// Suppression via AJAX (optionnel)
window.deleteProductAjax = function(productId) {
    if (confirm('Voulez-vous vraiment supprimer ce produit ?')) {
        fetch(`/delete-product/${productId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Supprimer l'élément du DOM
                const productCard = document.querySelector(`.product-card[data-id="${productId}"]`);
                if (productCard) {
                    productCard.remove();
                    updateProductCount();
                }
                showNotification('Produit supprimé avec succès', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Erreur lors de la suppression', 'error');
        });
    }
};

// Mettre à jour le compteur de produits
function updateProductCount() {
    const count = document.querySelectorAll('.product-card').length;
    document.getElementById('product-count').textContent = `${count} produit${count > 1 ? 's' : ''}`;
}

// Fonction utilitaire pour récupérer le cookie CSRF
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

// Afficher une notification (pour les messages AJAX)
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    
    document.querySelector('.messages').appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Auto-suppression des messages Django après 5 secondes
setTimeout(() => {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(msg => {
        msg.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => msg.remove(), 300);
    });
}, 5000);