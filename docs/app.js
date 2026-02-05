/**
 * Flash Card Application
 * Manages the interactive flash card UI for veterinary medications
 */

class FlashCardApp {
    constructor() {
        this.allMedications = []; // Original full list
        this.medications = [];    // Current active list (filtered)
        this.currentIndex = 0;
        this.isFlipped = false;
        this.viewedCards = new Set();
        this.knownCards = new Set(); // Track cards marked as known

        // DOM elements
        this.flashcard = document.getElementById('flashcard');
        this.cardQuestion = document.getElementById('card-question');
        this.cardVarenr = document.getElementById('card-varenr');
        this.matchNotice = document.getElementById('match-notice');
        this.unavailableNotice = document.getElementById('unavailable-notice');
        this.aktivtStofList = document.getElementById('aktivt-stof-list');
        this.indikationerList = document.getElementById('indikationer-list');
        this.sourceLink = document.getElementById('source-link');
        this.currentCardSpan = document.getElementById('current-card');
        this.totalCardsSpan = document.getElementById('total-cards');
        this.knownCardsSpan = document.getElementById('known-cards');
        this.progressFill = document.getElementById('progress-fill');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.flipBtn = document.getElementById('flip-btn');
        this.shuffleBtn = document.getElementById('shuffle-btn');
        this.removeUnknownBtn = document.getElementById('remove-unknown-btn');
        this.markKnownBtn = document.getElementById('mark-known-btn');
    }

    async init() {
        try {
            await this.loadData();
            this.setupEventListeners();
            this.showCard(0);
        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.showError('Kunne ikke indlæse medicin data. Prøv at genindlæse siden.');
        }
    }

    async loadData() {
        const response = await fetch('data/medications.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.allMedications = await response.json();
        this.medications = [...this.allMedications]; // Copy for active list
        this.updateTotalCards();
    }

    setupEventListeners() {
        // Button clicks
        this.flipBtn.addEventListener('click', () => this.flipCard());
        this.nextBtn.addEventListener('click', () => this.nextCard());
        this.prevBtn.addEventListener('click', () => this.previousCard());
        this.shuffleBtn.addEventListener('click', () => this.shuffleCards());
        this.removeUnknownBtn.addEventListener('click', () => this.removeUnknownMeds());
        this.markKnownBtn.addEventListener('click', () => this.markAsKnown());

        // Card click to flip
        this.flashcard.addEventListener('click', () => this.flipCard());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                this.previousCard();
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                this.nextCard();
            } else if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.flipCard();
            }
        });
    }

    showCard(index) {
        const med = this.medications[index];

        // Reset card state
        this.clearCard();

        // Always show the medication name
        this.cardQuestion.textContent = med.input_name;

        if (!med.found) {
            // Medication data not available
            this.unavailableNotice.textContent = 'Data ikke tilgængelig på vetisearch.dk';
            this.unavailableNotice.style.display = 'block';

            // Show varenr if available
            if (med.varenr) {
                this.cardVarenr.textContent = `Varenr: ${med.varenr}`;
                this.cardVarenr.style.display = 'block';
            }

            // Hide back content
            this.hideBackContent();
        } else {
            // Medication data available
            // Show varenr
            this.cardVarenr.textContent = `Varenr: ${med.varenr || 'N/A'}`;
            this.cardVarenr.style.display = 'block';

            // Show match notice if not exact match
            if (!med.exact_match) {
                this.matchNotice.textContent = `⚠️ Viser: ${med.variant_name}`;
                this.matchNotice.style.display = 'block';
            }

            // Populate back of card
            this.renderAktivtStof(med.aktivt_stof);
            this.renderIndikationer(med.indikationer);
            this.sourceLink.href = med.spc_url;
            this.sourceLink.style.display = 'inline-block';
        }

        this.updateProgress();
    }

    clearCard() {
        // Clear all content
        this.cardVarenr.style.display = 'none';
        this.matchNotice.style.display = 'none';
        this.unavailableNotice.style.display = 'none';
        this.aktivtStofList.innerHTML = '';
        this.indikationerList.innerHTML = '';
        this.sourceLink.style.display = 'none';
    }

    hideBackContent() {
        // For medications without data, hide back content
        this.aktivtStofList.innerHTML = '<li>Data ikke tilgængelig</li>';
        this.indikationerList.innerHTML = '<p>Data ikke tilgængelig</p>';
        this.sourceLink.style.display = 'none';
    }

    renderAktivtStof(aktivtStof) {
        if (!aktivtStof || aktivtStof.length === 0) {
            this.aktivtStofList.innerHTML = '<li>Ingen data</li>';
            return;
        }

        this.aktivtStofList.innerHTML = '';
        aktivtStof.forEach(stof => {
            const li = document.createElement('li');
            li.textContent = stof;
            this.aktivtStofList.appendChild(li);
        });
    }

    renderIndikationer(indikationer) {
        if (!indikationer || indikationer.length === 0) {
            this.indikationerList.innerHTML = '<p>Ingen indikationer fundet</p>';
            return;
        }

        this.indikationerList.innerHTML = '';
        indikationer.forEach(indikation => {
            const p = document.createElement('p');
            p.textContent = indikation;
            this.indikationerList.appendChild(p);
        });
    }

    flipCard() {
        this.isFlipped = !this.isFlipped;
        this.flashcard.classList.toggle('flipped');
        this.markAsViewed(this.currentIndex);
    }

    nextCard() {
        this.currentIndex = (this.currentIndex + 1) % this.medications.length;
        this.resetCard();
    }

    previousCard() {
        this.currentIndex = (this.currentIndex - 1 + this.medications.length) % this.medications.length;
        this.resetCard();
    }

    resetCard() {
        this.isFlipped = false;
        this.flashcard.classList.remove('flipped');
        this.showCard(this.currentIndex);
    }

    markAsViewed(index) {
        this.viewedCards.add(index);
    }

    updateProgress() {
        // Update card counter
        this.currentCardSpan.textContent = this.currentIndex + 1;

        // Update known cards counter
        this.knownCardsSpan.textContent = this.knownCards.size;

        // Update progress bar based on position in current deck
        const progressPercent = ((this.currentIndex + 1) / this.medications.length) * 100;
        this.progressFill.style.width = `${progressPercent}%`;
    }

    updateTotalCards() {
        this.totalCardsSpan.textContent = this.medications.length;
        this.knownCardsSpan.textContent = this.knownCards.size;
    }

    shuffleCards() {
        // Fisher-Yates shuffle algorithm
        const shuffled = [...this.medications];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        this.medications = shuffled;
        this.currentIndex = 0;
        this.resetCard();
        this.showMessage('Kortene er blandet!', 'success');
    }

    removeUnknownMeds() {
        const beforeCount = this.medications.length;
        this.medications = this.medications.filter(med => med.found);
        const removedCount = beforeCount - this.medications.length;

        if (removedCount > 0) {
            // Adjust current index if needed
            if (this.currentIndex >= this.medications.length) {
                this.currentIndex = Math.max(0, this.medications.length - 1);
            }
            this.updateTotalCards();
            this.resetCard();
            this.showMessage(`${removedCount} ukendte mediciner fjernet!`, 'success');
        } else {
            this.showMessage('Ingen ukendte mediciner at fjerne', 'info');
        }
    }

    markAsKnown() {
        const currentMed = this.medications[this.currentIndex];
        const medId = `${currentMed.input_name}-${currentMed.varenr}`;

        // Mark as known
        this.knownCards.add(medId);

        // Remove from active medications
        this.medications.splice(this.currentIndex, 1);

        if (this.medications.length === 0) {
            this.showMessage('Tillykke! Alle kort er markeret som kendt! 🎉', 'success');
            this.currentIndex = 0;
        } else {
            // Adjust index if at end of deck
            if (this.currentIndex >= this.medications.length) {
                this.currentIndex = 0;
            }
        }

        this.updateTotalCards();
        this.resetCard();
        this.showMessage('Markeret som kendt!', 'success');
    }

    showMessage(message, type = 'info') {
        // Create a temporary message element
        const messageEl = document.createElement('div');
        messageEl.className = `message message-${type}`;
        messageEl.textContent = message;
        document.body.appendChild(messageEl);

        // Remove after 2 seconds
        setTimeout(() => {
            messageEl.classList.add('fade-out');
            setTimeout(() => messageEl.remove(), 300);
        }, 2000);
    }

    showError(message) {
        this.cardQuestion.textContent = 'Fejl';
        this.unavailableNotice.textContent = message;
        this.unavailableNotice.style.display = 'block';
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const app = new FlashCardApp();
        app.init();
    });
} else {
    const app = new FlashCardApp();
    app.init();
}
