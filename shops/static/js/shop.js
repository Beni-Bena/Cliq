document.addEventListener('DOMContentLoaded', function() {
    // Éléments du DOM
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const resetSearchBtn = document.getElementById('reset-search');
    const productsGrid = document.getElementById('products-grid');
    const productCards = document.querySelectorAll('.product-card');
    const productCount = document.getElementById('product-count');
    const noProductsMessage = document.getElementById('no-products-message');
    
    // Fonction de recherche
    function searchProducts() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;
        
        // Parcourir tous les produits
        productCards.forEach(card => {
            const productName = card.getAttribute('data-name') || '';
            const productDescription = card.getAttribute('data-description') || '';
            
            // Vérifier si le produit correspond à la recherche
            const matches = productName.includes(searchTerm) || 
                           productDescription.includes(searchTerm);
            
            if (searchTerm === '' || matches) {
                card.classList.remove('hidden');
                visibleCount++;
            } else {
                card.classList.add('hidden');
            }
        });
        
        // Mettre à jour le compteur de produits
        updateProductCount(visibleCount);
        
        // Afficher ou masquer le message "aucun produit"
        if (searchTerm !== '' && visibleCount === 0) {
            noProductsMessage.style.display = 'block';
            productsGrid.style.display = 'none';
        } else {
            noProductsMessage.style.display = 'none';
            productsGrid.style.display = 'grid';
        }
    }
    
    // Mettre à jour le compteur de produits
    function updateProductCount(count) {
        if (productCount) {
            productCount.textContent = `${count} produit${count !== 1 ? 's' : ''}`;
        }
    }
    
    // Effacer la recherche
    function clearSearch() {
        searchInput.value = '';
        searchInput.focus();
        searchProducts();
    }
    
    // Réinitialiser la recherche
    function resetSearch() {
        clearSearch();
    }
    
    // Écouteurs d'événements
    if (searchInput) {
        searchInput.addEventListener('input', searchProducts);
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Escape') {
                clearSearch();
            }
        });
    }
    
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', clearSearch);
    }
    
    if (resetSearchBtn) {
        resetSearchBtn.addEventListener('click', resetSearch);
    }
    
    // Animation des cartes au chargement
    function animateProducts() {
        productCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
    
    // Initialiser les animations
    animateProducts();
    
    // Focus sur la barre de recherche avec la touche "/"
    document.addEventListener('keydown', function(e) {
        if (e.key === '/' && e.target !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    });
    
    // Initialiser le compteur de produits
    updateProductCount(productCards.length);
});

// Ajoutez ceci à votre fichier shop.js après le chargement du DOM

// Animation des cartes produits
function animateProducts() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.setProperty('--i', index);
        
        // Faire apparaître les cartes une par une
        setTimeout(() => {
            card.style.opacity = '1';
        }, index * 100);
    });
}

// Appeler la fonction au chargement
document.addEventListener('DOMContentLoaded', function() {
    animateProducts();
    
    // Le reste de votre code JavaScript existant...
});