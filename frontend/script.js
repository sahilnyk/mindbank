const API_BASE_URL = window.location.origin;

let messages = [];
let selectedPersonality = 'calm_mentor';

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
}

function addMessage() {
    const input = document.getElementById('message-input');
    const content = input.value.trim();

    if (!content) {
        alert('Please enter a message');
        return;
    }

    const message = {
        index: messages.length,
        role: 'user',
        content: content
    };

    messages.push(message);
    renderMessages();
    input.value = '';
}

async function load30Messages() {
    try {
        const response = await fetch('/30_messages.json');

        if (!response.ok) {
            throw new Error('Failed to load sample messages');
        }

        const data = await response.json();

        messages = data.map((msg, index) => ({
            index: index,
            role: msg.role || 'user',
            content: msg.content
        }));

        renderMessages();

        const successMsg = document.createElement('div');
        successMsg.textContent = `Loaded ${messages.length} sample messages successfully!`;
        successMsg.style.cssText = 'background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 10px; border-radius: 6px; margin: 10px 0; font-size: 0.85rem; border: 1px solid rgba(16, 185, 129, 0.3);';
        document.getElementById('messages-list').prepend(successMsg);

        setTimeout(() => successMsg.remove(), 3000);

    } catch (error) {
        alert(`Error loading sample messages: ${error.message}`);
    }
}

function clearMessages() {
    if (messages.length === 0) {
        alert('No messages to clear');
        return;
    }

    if (confirm(`Clear all ${messages.length} messages?`)) {
        messages = [];
        renderMessages();
    }
}

function renderMessages() {
    const listContainer = document.getElementById('messages-list');

    if (messages.length === 0) {
        listContainer.innerHTML = '<p style="color: #666666; font-size: 0.85rem;">No messages added yet. Add some messages or load sample data!</p>';
        return;
    }

    const countInfo = `<div class="message-count-info">
        Total Messages: ${messages.length}
    </div>`;

    const messagesList = messages.map((msg, idx) => `
        <div class="message-item">
            <span class="message-index">#${idx}</span>
            <span class="message-text">${msg.content}</span>
            <button class="btn btn-danger" onclick="removeMessage(${idx})">Remove</button>
        </div>
    `).join('');

    listContainer.innerHTML = countInfo + messagesList;
}

function removeMessage(index) {
    messages.splice(index, 1);
    messages.forEach((msg, idx) => {
        msg.index = idx;
    });
    renderMessages();
}

async function extractMemories() {
    if (messages.length === 0) {
        alert('Please add at least one message');
        return;
    }

    const useLLM = document.getElementById('extract-use-llm').checked;
    const resultContainer = document.getElementById('extract-result');
    const extractBtn = document.querySelector('.btn-success.btn-large');

    extractBtn.disabled = true;
    extractBtn.textContent = 'Extracting...';

    resultContainer.innerHTML = '<div style="text-align: center; padding: 40px;"><div class="loading"></div><p style="margin-top: 20px; font-size: 0.85rem; color: #777777;">Analyzing messages...</p></div>';
    resultContainer.classList.add('show');

    try {
        const response = await fetch(`${API_BASE_URL}/extract`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: messages,
                use_llm: useLLM
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Extraction failed');
        }

        const data = await response.json();
        displayExtractionResult(data);

    } catch (error) {
        resultContainer.innerHTML = `
            <div style="color: #ef4444; text-align: center; padding: 40px;">
                <h3 style="font-size: 1rem; margin-bottom: 10px;">Error</h3>
                <p style="font-size: 0.85rem;">${error.message}</p>
                <button class="btn btn-primary" style="margin-top: 20px;" onclick="document.getElementById('extract-result').classList.remove('show')">Close</button>
            </div>
        `;
    } finally {
        extractBtn.disabled = false;
        extractBtn.textContent = 'Extract Memories';
    }
}

function displayExtractionResult(data) {
    const resultContainer = document.getElementById('extract-result');
    const memory = data.memory;

    const html = `
        <div class="result-header">
            <h3>Extraction Complete</h3>
            <span class="method-badge method-${data.method}">${data.method.toUpperCase()}</span>
        </div>
        
        <div class="memory-section">
            <h4>Preferences (${memory.preferences.length})</h4>
            <div class="memory-items">
                ${memory.preferences.map(pref => `
                    <div class="memory-item">
                        <strong>${pref.category}:</strong> ${pref.value}
                        <span class="confidence">${(pref.confidence * 100).toFixed(0)}% confidence</span>
                        <br><small>From messages: ${pref.source_messages.join(', ')}</small>
                    </div>
                `).join('') || '<p style="color: #666666; font-size: 0.8rem;">No preferences found</p>'}
            </div>
        </div>
        
        <div class="memory-section">
            <h4>Emotional Patterns (${memory.emotional_patterns.length})</h4>
            <div class="memory-items">
                ${memory.emotional_patterns.map(pattern => `
                    <div class="memory-item">
                        <strong>${pattern.pattern}</strong>
                        <span class="confidence">${(pattern.confidence * 100).toFixed(0)}% confidence</span>
                        <br><small>From messages: ${pattern.source_messages.join(', ')}</small>
                    </div>
                `).join('') || '<p style="color: #666666; font-size: 0.8rem;">No emotional patterns found</p>'}
            </div>
        </div>
        
        <div class="memory-section">
            <h4>Facts (${memory.facts.length})</h4>
            <div class="memory-items">
                ${memory.facts.map(fact => `
                    <div class="memory-item">
                        <strong>${fact.fact_type}:</strong> ${fact.value}
                        <span class="confidence">${(fact.confidence * 100).toFixed(0)}% confidence</span>
                        <br><small>From messages: ${fact.source_messages.join(', ')}</small>
                    </div>
                `).join('') || '<p style="color: #666666; font-size: 0.8rem;">No facts found</p>'}
            </div>
        </div>
        
        <div class="memory-section">
            <h4>Raw Extractions (${memory.raw_extractions.length})</h4>
            <div class="memory-items">
                ${memory.raw_extractions.map(raw => `
                    <div class="memory-item">
                        <strong>${raw.text}</strong> <small>(${raw.entity_type})</small>
                        <br><small>From message: ${raw.message_index}</small>
                    </div>
                `).join('') || '<p style="color: #666666; font-size: 0.8rem;">No raw extractions</p>'}
            </div>
        </div>
        
        <div style="margin-top: 24px; text-align: center;">
            <button class="btn btn-primary" onclick="document.getElementById('extract-result').classList.remove('show')">Close</button>
        </div>
    `;

    resultContainer.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', () => {
    const personalityButtons = document.querySelectorAll('.personality-btn');

    personalityButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            personalityButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedPersonality = btn.dataset.personality;
        });
    });

    renderMessages();
});

async function rewriteText() {
    const input = document.getElementById('rewrite-input');
    const text = input.value.trim();

    if (!text) {
        alert('Please enter some text to rewrite');
        return;
    }

    const useLLM = document.getElementById('rewrite-use-llm').checked;
    const resultContainer = document.getElementById('rewrite-result');
    const rewriteBtn = document.querySelector('#rewrite-tab .btn-success.btn-large');

    rewriteBtn.disabled = true;
    rewriteBtn.textContent = 'Rewriting...';

    resultContainer.innerHTML = '<div style="text-align: center; padding: 40px;"><div class="loading"></div><p style="margin-top: 20px; font-size: 0.85rem; color: #777777;">Transforming text...</p></div>';
    resultContainer.classList.add('show');

    try {
        const response = await fetch(`${API_BASE_URL}/rewrite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                personality: selectedPersonality,
                use_llm: useLLM
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Rewrite failed');
        }

        const data = await response.json();
        displayRewriteResult(data);

    } catch (error) {
        resultContainer.innerHTML = `
            <div style="color: #ef4444; text-align: center; padding: 40px;">
                <h3 style="font-size: 1rem; margin-bottom: 10px;">Error</h3>
                <p style="font-size: 0.85rem;">${error.message}</p>
                <button class="btn btn-primary" style="margin-top: 20px;" onclick="document.getElementById('rewrite-result').classList.remove('show')">Close</button>
            </div>
        `;
    } finally {
        rewriteBtn.disabled = false;
        rewriteBtn.textContent = 'Transform Text';
    }
}

function displayRewriteResult(data) {
    const resultContainer = document.getElementById('rewrite-result');

    const html = `
        <div class="result-header">
            <h3>Rewrite Complete</h3>
            <span class="method-badge method-${data.method}">${data.method.toUpperCase()}</span>
        </div>
        
        <div class="rewrite-comparison">
            <div class="text-box">
                <h4>Original Text</h4>
                <p>${data.original}</p>
            </div>
            
            <div class="text-box" style="border-left-color: #10b981;">
                <h4>${data.personality.replace('_', ' ').toUpperCase()}</h4>
                <p>${data.rewritten}</p>
            </div>
        </div>
        
        <div style="margin-top: 24px; text-align: center;">
            <button class="btn btn-primary" onclick="document.getElementById('rewrite-result').classList.remove('show')">Close</button>
        </div>
    `;

    resultContainer.innerHTML = html;
}