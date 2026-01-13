// Gestion de l'affichage/masquage du mot de passe
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Changer l'icône
        const icon = this.querySelector('i');
        if (type === 'password') {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        } else {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        }
    });
}

// Validation basique du formulaire
const loginForm = document.querySelector('.login-form');
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        if (!email || !password) {
            e.preventDefault();
            alert('Veuillez remplir tous les champs.');
            return false;
        }
        
        // Validation basique de l'email/whatsapp
        if (!isValidEmailOrPhone(email)) {
            e.preventDefault();
            alert('Veuillez entrer une adresse email valide ou un numéro WhatsApp.');
            return false;
        }
        
        return true;
    });
}

function isValidEmailOrPhone(value) {
    // Validation email simple
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // Validation numéro (accepte les numéros internationaux)
    const phoneRegex = /^[\+]?[0-9]{10,15}$/;
    
    return emailRegex.test(value) || phoneRegex.test(value.replace(/\s+/g, ''));
}

// Gestion du chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier s'il y a des messages d'erreur
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        // Faire défiler jusqu'au premier message d'erreur
        alerts[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Focus sur le premier champ
    const emailField = document.getElementById('email');
    if (emailField) {
        emailField.focus();
    }
});