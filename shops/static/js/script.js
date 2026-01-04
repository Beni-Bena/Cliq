function contactDeveloper() {
    const name = document.getElementById("name").value;
    const storeName = document.getElementById("storeName").value;
    const whatsapp = document.getElementById("whatsapp").value;
    const email = document.getElementById("email").value;

    // Validation simple
    if (!name || !storeName || !whatsapp || !email) {
        alert("Veuillez remplir tous les champs obligatoires.");
        return;
    }

    const devNumber = "243890076669"; // numéro du développeur (format international, sans +)

    const message = `
Bonjour 👋
Je souhaite créer ma vitrine sur Cliq.

Nom : ${name}
Nom du magasin : ${storeName}
WhatsApp : ${whatsapp}
Email : ${email}
`;

    const url = `https://wa.me/${devNumber}?text=${encodeURIComponent(message)}`;
    window.open(url, "_blank");
}