// -----------------------------
// Gestion des formulaires
// -----------------------------

// Sélection des éléments
const signupChoice = document.getElementById('signupChoice');
const loginChoice = document.getElementById('loginChoice');
const signupForm = document.getElementById('signupForm');
const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const mobileLoginBtn = document.getElementById('mobileLoginBtn');
const menuToggle = document.getElementById('menuToggle');
const mobileNav = document.getElementById('mobileNav');

// -----------------------------
// Changer entre inscription et connexion
// -----------------------------
function showSignupForm() {
    if (signupChoice && loginChoice && signupForm && loginForm) {
        signupChoice.classList.add('active');
        loginChoice.classList.remove('active');
        signupForm.style.display = 'block';
        loginForm.style.display = 'none';
    }
}

function showLoginForm() {
    if (loginChoice && signupChoice && loginForm && signupForm) {
        loginChoice.classList.add('active');
        signupChoice.classList.remove('active');
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
    }
}

if (signupChoice && loginChoice) {
    signupChoice.addEventListener('click', showSignupForm);
    loginChoice.addEventListener('click', showLoginForm);
}

if (loginBtn) {
    loginBtn.addEventListener('click', showLoginForm);
}

if (mobileLoginBtn) {
    mobileLoginBtn.addEventListener('click', function(e) {
        e.preventDefault();
        showLoginForm();
        if (mobileNav) mobileNav.classList.remove('active');
    });
}

// -----------------------------
// Validation basique côté client
// -----------------------------
function validateSignupForm() {
    const password = document.getElementById("password")?.value;
    const confirmPassword = document.getElementById("confirmPassword")?.value;
    const terms = document.getElementById("terms")?.checked;

    if (password !== confirmPassword) {
        alert("Les mots de passe ne correspondent pas.");
        return false;
    }

    if (!terms) {
        alert("Veuillez accepter les conditions d'utilisation.");
        return false;
    }

    return true;
}

// -----------------------------
// Gestion du menu mobile
// -----------------------------
if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', function() {
        mobileNav.classList.toggle('active');
    });

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileNav.classList.remove('active');
        });
    });
}

// -----------------------------
// Gestion des modals (optionnel)
// -----------------------------
const modalClose = document.getElementById('modalClose');
const modalButton = document.getElementById('modalButton');

if (modalClose) {
    modalClose.addEventListener('click', function() {
        document.getElementById('confirmationModal').style.display = 'none';
    });
}

if (modalButton) {
    modalButton.addEventListener('click', function() {
        document.getElementById('confirmationModal').style.display = 'none';
    });
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('confirmationModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
