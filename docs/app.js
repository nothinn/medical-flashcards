/**
 * Flash Card Application
 * Manages the interactive flash card UI for veterinary medications
 */

class FlashCardApp {
    constructor() {
        this.medications = [];
        this.currentIndex = 0;
        this.isFlipped = false;
        this.viewedCards = new Set();

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
        this.progressFill = document.getElementById('progress-fill');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.flipBtn = document.getElementById('flip-btn');
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
        this.medications = await response.json();
        this.totalCardsSpan.textContent = this.medications.length;
    }

    setupEventListeners() {
        // Button clicks
        this.flipBtn.addEventListener('click', () => this.flipCard());
        this.nextBtn.addEventListener('click', () => this.nextCard());
        this.prevBtn.addEventListener('click', () => this.previousCard());

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

        // Update progress bar
        const progressPercent = ((this.currentIndex + 1) / this.medications.length) * 100;
        this.progressFill.style.width = `${progressPercent}%`;
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
