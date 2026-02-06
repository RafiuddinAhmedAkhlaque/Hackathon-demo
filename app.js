/**
 * My Notes App
 * A simple note-taking application with localStorage persistence
 */

// DOM Elements
const noteTitleInput = document.getElementById('note-title');
const noteBodyInput = document.getElementById('note-body');
const saveBtn = document.getElementById('save-btn');
const notesContainer = document.getElementById('notes-container');
const emptyMessage = document.getElementById('empty-message');

// Constants
const STORAGE_KEY = 'my-notes-app-data';

// State
let editingNoteId = null;

/**
 * Initialize the application
 */
function init() {
    loadNotes();
    setupEventListeners();
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    saveBtn.addEventListener('click', handleSaveNote);
    
    // Allow saving with Ctrl/Cmd + Enter
    noteBodyInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            handleSaveNote();
        }
    });

    noteTitleInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            handleSaveNote();
        }
        
        // Allow canceling edit mode with Escape
        if (e.key === 'Escape' && editingNoteId) {
            cancelEdit();
        }
    });

    noteBodyInput.addEventListener('keydown', (e) => {
        // Allow canceling edit mode with Escape
        if (e.key === 'Escape' && editingNoteId) {
            cancelEdit();
        }
    });
}

/**
 * Handle saving a new note or updating an existing note
 */
function handleSaveNote() {
    const title = noteTitleInput.value.trim();
    const body = noteBodyInput.value.trim();

    // Validate input
    if (!title && !body) {
        shakeElement(noteTitleInput);
        shakeElement(noteBodyInput);
        return;
    }

    const notes = getNotes();

    if (editingNoteId) {
        // Update existing note
        const noteIndex = notes.findIndex(note => note.id === editingNoteId);
        if (noteIndex !== -1) {
            notes[noteIndex] = {
                ...notes[noteIndex],
                title: title || 'Untitled Note',
                body: body,
                updatedAt: new Date().toISOString()
            };
        }
        exitEditMode();
    } else {
        // Create new note
        const note = {
            id: generateId(),
            title: title || 'Untitled Note',
            body: body,
            createdAt: new Date().toISOString()
        };
        
        notes.unshift(note); // Add to beginning
    }

    // Save to localStorage
    saveNotes(notes);

    // Clear inputs
    noteTitleInput.value = '';
    noteBodyInput.value = '';

    // Re-render notes
    renderNotes();

    // Focus back on title input
    noteTitleInput.focus();
}

/**
 * Handle editing a note
 * @param {string} noteId - The ID of the note to edit
 */
function handleEditNote(noteId) {
    const notes = getNotes();
    const note = notes.find(n => n.id === noteId);
    
    if (!note) return;

    // Enter edit mode
    editingNoteId = noteId;
    
    // Populate form fields
    noteTitleInput.value = note.title === 'Untitled Note' ? '' : note.title;
    noteBodyInput.value = note.body;
    
    // Update UI to show edit mode
    updateSaveButtonForEdit();
    
    // Focus on title input and scroll to form
    noteTitleInput.focus();
    document.querySelector('.note-form').scrollIntoView({ 
        behavior: 'smooth',
        block: 'center'
    });

    // Highlight the note being edited
    highlightEditingNote(noteId);
}

/**
 * Exit edit mode and return to create mode
 */
function exitEditMode() {
    editingNoteId = null;
    updateSaveButtonForCreate();
    removeEditHighlight();
}

/**
 * Cancel edit mode without saving
 */
function cancelEdit() {
    exitEditMode();
    noteTitleInput.value = '';
    noteBodyInput.value = '';
    noteTitleInput.focus();
}

/**
 * Update save button appearance for edit mode
 */
function updateSaveButtonForEdit() {
    const btnIcon = saveBtn.querySelector('.btn-icon');
    const btnText = saveBtn.childNodes[saveBtn.childNodes.length - 1];
    
    btnIcon.textContent = '✓';
    btnText.textContent = 'Update Note';
    saveBtn.classList.add('btn-edit');
}

/**
 * Update save button appearance for create mode
 */
function updateSaveButtonForCreate() {
    const btnIcon = saveBtn.querySelector('.btn-icon');
    const btnText = saveBtn.childNodes[saveBtn.childNodes.length - 1];
    
    btnIcon.textContent = '+';
    btnText.textContent = 'Save Note';
    saveBtn.classList.remove('btn-edit');
}

/**
 * Highlight the note currently being edited
 * @param {string} noteId - The ID of the note being edited
 */
function highlightEditingNote(noteId) {
    // Remove any existing highlights
    removeEditHighlight();
    
    // Add highlight to the note being edited
    const noteCard = document.querySelector(`[data-note-id="${noteId}"]`);
    if (noteCard) {
        noteCard.classList.add('editing');
    }
}

/**
 * Remove edit highlight from all notes
 */
function removeEditHighlight() {
    const editingCards = document.querySelectorAll('.note-card.editing');
    editingCards.forEach(card => card.classList.remove('editing'));
}

/**
 * Handle deleting a note
 * @param {string} noteId - The ID of the note to delete
 */
function handleDeleteNote(noteId) {
    const noteCard = document.querySelector(`[data-note-id="${noteId}"]`);
    
    if (noteCard) {
        // If we're editing this note, cancel the edit
        if (editingNoteId === noteId) {
            cancelEdit();
        }
        
        // Add removing animation
        noteCard.classList.add('removing');
        
        // Wait for animation to complete before removing
        setTimeout(() => {
            const notes = getNotes().filter(note => note.id !== noteId);
            saveNotes(notes);
            renderNotes();
        }, 300);
    }
}

/**
 * Load notes from localStorage and render them
 */
function loadNotes() {
    renderNotes();
}

/**
 * Get notes from localStorage
 * @returns {Array} Array of note objects
 */
function getNotes() {
    try {
        const notes = localStorage.getItem(STORAGE_KEY);
        return notes ? JSON.parse(notes) : [];
    } catch (error) {
        console.error('Error loading notes:', error);
        return [];
    }
}

/**
 * Save notes to localStorage
 * @param {Array} notes - Array of note objects to save
 */
function saveNotes(notes) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
    } catch (error) {
        console.error('Error saving notes:', error);
    }
}

/**
 * Render all notes to the DOM
 */
function renderNotes() {
    const notes = getNotes();
    
    // Clear container
    notesContainer.innerHTML = '';
    
    // Toggle empty message
    if (notes.length === 0) {
        emptyMessage.classList.remove('hidden');
    } else {
        emptyMessage.classList.add('hidden');
        
        // Render each note
        notes.forEach(note => {
            const noteElement = createNoteElement(note);
            notesContainer.appendChild(noteElement);
        });
    }

    // Restore edit highlight if we're in edit mode
    if (editingNoteId) {
        highlightEditingNote(editingNoteId);
    }
}

/**
 * Create a note card element
 * @param {Object} note - The note object
 * @returns {HTMLElement} The note card element
 */
function createNoteElement(note) {
    const article = document.createElement('article');
    article.className = 'note-card';
    article.setAttribute('data-note-id', note.id);

    const header = document.createElement('div');
    header.className = 'note-card-header';

    const title = document.createElement('h3');
    title.className = 'note-title';
    title.textContent = note.title;

    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'note-actions';

    const editBtn = document.createElement('button');
    editBtn.className = 'btn-edit-note';
    editBtn.innerHTML = '✏️';
    editBtn.setAttribute('aria-label', 'Edit note');
    editBtn.setAttribute('title', 'Edit note');
    editBtn.addEventListener('click', () => handleEditNote(note.id));

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn-delete';
    deleteBtn.innerHTML = '&times;';
    deleteBtn.setAttribute('aria-label', 'Delete note');
    deleteBtn.setAttribute('title', 'Delete note');
    deleteBtn.addEventListener('click', () => handleDeleteNote(note.id));

    buttonContainer.appendChild(editBtn);
    buttonContainer.appendChild(deleteBtn);

    header.appendChild(title);
    header.appendChild(buttonContainer);

    const content = document.createElement('p');
    content.className = 'note-content';
    content.textContent = note.body || 'No content';

    const date = document.createElement('time');
    date.className = 'note-date';
    date.setAttribute('datetime', note.updatedAt || note.createdAt);
    const dateText = formatDate(note.updatedAt || note.createdAt);
    const prefix = note.updatedAt ? 'Updated ' : 'Created ';
    date.textContent = prefix + dateText;

    article.appendChild(header);
    article.appendChild(content);
    article.appendChild(date);

    return article;
}

/**
 * Format a date string for display
 * @param {string} isoString - ISO date string
 * @returns {string} Formatted date string
 */
function formatDate(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    // Just now (less than 1 minute)
    if (diffMins < 1) {
        return 'just now';
    }
    
    // Minutes ago
    if (diffMins < 60) {
        return `${diffMins} minute${diffMins === 1 ? '' : 's'} ago`;
    }
    
    // Hours ago
    if (diffHours < 24) {
        return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`;
    }
    
    // Yesterday
    if (diffDays === 1) {
        return 'yesterday';
    }
    
    // Within a week
    if (diffDays < 7) {
        return `${diffDays} days ago`;
    }

    // Default: formatted date
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Generate a unique ID for a note
 * @returns {string} Unique ID
 */
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * Add a shake animation to an element
 * @param {HTMLElement} element - The element to shake
 */
function shakeElement(element) {
    element.style.animation = 'none';
    element.offsetHeight; // Trigger reflow
    element.style.animation = 'shake 0.5s ease-in-out';
    
    setTimeout(() => {
        element.style.animation = '';
    }, 500);
}

// Add shake animation keyframes dynamically
const shakeKeyframes = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
}
`;
const styleSheet = document.createElement('style');
styleSheet.textContent = shakeKeyframes;
document.head.appendChild(styleSheet);

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', init);