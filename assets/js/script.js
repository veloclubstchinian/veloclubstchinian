// 1. Données des circuits favoris
function getCircuitsData() {
    const fromWindow = window.circuitsData || [];
    if (Array.isArray(fromWindow)) {
        return fromWindow;
    }
    if (fromWindow && Array.isArray(fromWindow.data)) {
        return fromWindow.data;
    }
    return [];
}

function renderCircuits() {
    const container = document.getElementById("circuits-container");
    if (!container) return;

    const circuitsData = getCircuitsData();
    container.innerHTML = "";

    if (!circuitsData.length) {
        container.innerHTML = '<div class="pdf-card"><p>Aucun circuit favori pour le moment.</p></div>';
        return;
    }

    circuitsData.forEach(circuit => {
        const link = circuit.lienGps || circuit.link || "#";
        const label = link === "#" ? "Aucun tracé disponible" : "Voir le tracé OpenRunner";
        const card = document.createElement("a");
        card.className = "circuit-card circuit-card-link";
        card.href = link;
        card.target = link === "#" ? "_self" : "_blank";
        card.rel = "noopener";
        card.innerHTML = `
            <h4>${circuit.nom || 'Circuit'}</h4>
            <p><strong>Distance :</strong> ${circuit.distance || ''}</p>
            <p><strong>Dénivelé :</strong> ${circuit.denivele || ''}</p>
            <p><strong>Difficulté :</strong> ${circuit.difficulte || ''}</p>
            <p><strong>Description :</strong> ${circuit.description || ''}</p>
            <span class="btn-gps"><i class="fa-solid fa-map-location-dot"></i> ${label}</span>
        `;
        container.appendChild(card);
    });
}

// 2. Affichage automatique des circuits dans le HTML
document.addEventListener("DOMContentLoaded", () => {
    renderCircuits();
});

// 3. Gestion du carrousel d'images
const images = Array.from(document.querySelectorAll('.carousel-image'));
let currentImageIndex = 0;

function showNextImage() {
    images.forEach((img, index) => {
        img.classList.toggle('active', index === currentImageIndex);
    });
    currentImageIndex = (currentImageIndex + 1) % images.length;
}

if (images.length > 0) {
    showNextImage();
    setInterval(showNextImage, 5000);
}

// 4. Affichage des sorties depuis le fichier data/prochaines_sorties.js ou data/evenements.js
function renderSorties(events) {
    // Gestion avec tableau HTML (prochaines-sorties-tbody)
    const tbody = document.getElementById('prochaines-sorties-tbody');
    if (tbody) {
        if (!events || !events.length) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:15px;">Aucune sortie programmée.</td></tr>';
            return;
        }
        tbody.innerHTML = events.map(e => `
            <tr>
                <td><strong>${e.jourHeure || e.date || ''}</strong></td>
                <td>${e.type || e.nom || ''}</td>
                <td>${e.rendezVous || ''}</td>
            </tr>
        `).join('');
        return;
    }

    // Gestion avec div/grid (agenda-table)
    const table = document.getElementById('agenda-table');
    if (table) {
        const rows = table.querySelectorAll('.agenda-row:not(.header)');
        rows.forEach(row => row.remove());

        events.forEach((event) => {
            const div = document.createElement('div');
            div.className = 'agenda-row';
            div.innerHTML = `
                <div>${event.jourHeure || event.date || ''}</div>
                <div>${event.type || event.nom || ''}</div>
                <div>${event.rendezVous || ''}</div>
            `;
            table.appendChild(div);
        });
    }
}

function loadSorties() {
    const events = window.prochainesSortiesData || window.evenementsData || [];
    renderSorties(events);
}

document.addEventListener('DOMContentLoaded', loadSorties);

// 5. Gestion du menu mobile (Sécurisé pour éviter l'erreur si l'élément n'existe pas)
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenu = document.getElementById("mobile-menu");
    const navMenu = document.querySelector(".nav-menu");

    if (mobileMenu && navMenu) {
        mobileMenu.addEventListener("click", () => {
            const isOpen = navMenu.style.display === "flex";
            navMenu.style.display = isOpen ? "none" : "flex";
            if (!isOpen) {
                navMenu.style.flexDirection = "column";
                navMenu.style.position = "absolute";
                navMenu.style.top = "80px";
                navMenu.style.left = "0";
                navMenu.style.width = "100%";
                navMenu.style.background = "#2c3e50";
                navMenu.style.padding = "20px";
            }
        });
    }
});