// Gestion du modal d'ajout de produit
const openProductModalBtn = document.getElementById('openProductModalBtn');
const addProductModal = document.getElementById('addProductModal');
const modalClose = document.getElementById('modalClose');
const productForm = document.getElementById('productForm');

// Ouvrir le modal
if (openProductModalBtn && addProductModal) {
    openProductModalBtn.addEventListener('click', function() {
        addProductModal.style.display = 'flex';
    });
}

// Fermer le modal
function closeProductModal() {
    if (addProductModal) {
        addProductModal.style.display = 'none';
    }
}

if (modalClose) {
    modalClose.addEventListener('click', closeProductModal);
}

// Fermer en cliquant en dehors du modal
window.addEventListener('click', function(event) {
    if (event.target === addProductModal) {
        closeProductModal();
    }
});

// Gestion de la soumission du formulaire
if (productForm) {
    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendProductRequest();
    });
}

// Fonction pour envoyer la demande d'ajout de produit
function sendProductRequest() {
    const productName = document.getElementById('productName').value;
    const productDescription = document.getElementById('productDescription').value;
    const productPrice = document.getElementById('productPrice').value;
    const productCategory = document.getElementById('productCategory').value;
    const productImage = document.getElementById('productImage').value;

    // Validation simple
    if (!productName || !productDescription || !productPrice || !productCategory) {
        alert('Veuillez remplir tous les champs obligatoires.');
        return;
    }

    // Numéro du développeur
    const devNumber = "243890076669";

    // Message à envoyer
    const message = `
🛍️ *NOUVEAU PRODUIT À AJOUTER*

*Informations du produit :*
📦 Nom : ${productName}
📝 Description : ${productDescription}
💰 Prix : ${productPrice} $
🏷️ Catégorie : ${productCategory}
🖼️ Image : ${productImage || 'À ajouter'}

Merci d'ajouter ce produit à ma vitrine Cliq !`;
    
    // Ouvrir WhatsApp
    const url = `https://wa.me/${devNumber}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
    
    // Fermer le modal et réinitialiser le formulaire
    closeProductModal();
    productForm.reset();
    
    // Afficher un message de confirmation
    alert('Demande envoyée avec succès ! Vous allez être redirigé vers WhatsApp.');
}