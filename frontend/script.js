const API_BASE_URL = '';

let messages = [];
let extractedMemory = null;
let currentRewritePersonality = 'calm_mentor';
let currentResponsePersonality = 'calm_mentor';

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

async function load30Messages() {
    try {
        const response = await fetch('/30_messages.json');
        const data = await response.json();

        messages = data.map((msg, index) => ({
            index: index,
            role: msg.role || 'user',
            content: msg.content
        }));

        renderMessages();
    } catch (error) {
        alert('Failed to load messages: ' + error.message);
    }
}

function clearMessages() {
    messages = [];
    renderMessages();
}

function addMessage() {
    const input = document.getElementById('message-input');
    const content = input.value.trim();

    if (!content) return;

    messages.push({
        index: messages.length,
        role: 'user',
        content: content
    });

    input.value = '';
    renderMessages();
}

function renderMessages() {
    const container = document.getElementById('messages-list');

    if (messages.length === 0) {
        container.innerHTML = '';
        return;
    }

    const countInfo = `<div class="message-count-info">${messages.length} message${messages.length !== 1 ? 's' : ''} loaded</div>`;

    const messageItems = messages.map(msg => `
        <div class="message-item">
            <span class="message-index">${msg.index + 1}</span>
            <span class="message-text">${msg.content}</span>
            <button class="btn btn-danger" onclick="removeMessage(${msg.index})" style="padding: 5px 10px; font-size: 0.7rem;">Remove</button>
        </div>
    `).join('');

    container.innerHTML = countInfo + messageItems;
}

function removeMessage(index) {
    messages = messages.filter(msg => msg.index !== index);
    messages.forEach((msg, i) => msg.index = i);
    renderMessages();
}

async function extractMemories() {
    if (messages.length === 0) {
        alert('Please add some messages first');
        return;
    }

    const useLLM = document.getElementById('extract-use-llm').checked;

    try {
        const response = await fetch(`${API_BASE_URL}/extract`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                messages: messages,
                use_llm: useLLM
            })
        });

        if (!response.ok) throw new Error('Extraction failed');

        const data = await response.json();

        // Store the extracted memory globally
        extractedMemory = data.memory;

        console.log('Extracted Memory:', extractedMemory); // Debug log

        displayExtractionResult(data.memory, data.method);
    } catch (error) {
        console.error('Extraction error:', error);
        alert('Extraction failed: ' + error.message);
    }
}

function displayExtractionResult(memory, method) {
    const container = document.getElementById('extract-result');

    const methodBadge = method === 'llm'
        ? '<span class="method-badge method-llm">LLM</span>'
        : '<span class="method-badge method-deterministic">Deterministic</span>';

    let html = `
        <div class="result-header">
            <h3>Extracted Memory</h3>
            ${methodBadge}
        </div>
    `;

    if (memory.preferences && memory.preferences.length > 0) {
        html += `
            <div class="memory-section">
                <h4>Preferences (${memory.preferences.length})</h4>
                <div class="memory-items">
                    ${memory.preferences.map(pref => {
            if (typeof pref === 'object' && pref.value) {
                const categoryTag = pref.category ? `<span class="category-tag">${pref.category.replace('_', ' ')}</span>` : '';
                const confidencePercent = pref.confidence ? Math.round(pref.confidence * 100) : 0;
                const confidenceClass = confidencePercent >= 90 ? 'high' : confidencePercent >= 85 ? 'medium' : '';
                const confidence = pref.confidence ? `<span class="confidence ${confidenceClass}">${confidencePercent}%</span>` : '';
                return `
                            <div class="memory-item">
                                <div class="item-content">
                                    ${categoryTag}
                                    <span class="item-value">${pref.value}</span>
                                </div>
                                ${confidence}
                            </div>`;
            }
            return `<div class="memory-item"><span class="item-value">${pref}</span></div>`;
        }).join('')}
                </div>
            </div>
        `;
    }

    if (memory.emotional_patterns && memory.emotional_patterns.length > 0) {
        html += `
            <div class="memory-section">
                <h4>Emotional Patterns (${memory.emotional_patterns.length})</h4>
                <div class="memory-items">
                    ${memory.emotional_patterns.map(pattern => {
            if (typeof pattern === 'object' && pattern.pattern) {
                const confidencePercent = pattern.confidence ? Math.round(pattern.confidence * 100) : 0;
                const confidenceClass = confidencePercent >= 90 ? 'high' : confidencePercent >= 85 ? 'medium' : '';
                const confidence = pattern.confidence ? `<span class="confidence ${confidenceClass}">${confidencePercent}%</span>` : '';
                return `
                            <div class="memory-item">
                                <div class="item-content">
                                    <span class="item-value">${pattern.pattern}</span>
                                </div>
                                ${confidence}
                            </div>`;
            }
            return `<div class="memory-item"><span class="item-value">${pattern}</span></div>`;
        }).join('')}
                </div>
            </div>
        `;
    }

    if (memory.facts && memory.facts.length > 0) {
        html += `
            <div class="memory-section">
                <h4>Facts (${memory.facts.length})</h4>
                <div class="memory-items">
                    ${memory.facts.map(fact => {
            if (typeof fact === 'object' && fact.value) {
                const factTag = fact.fact_type ? `<span class="category-tag">${fact.fact_type}</span>` : '';
                const confidencePercent = fact.confidence ? Math.round(fact.confidence * 100) : 0;
                const confidenceClass = confidencePercent >= 90 ? 'high' : confidencePercent >= 85 ? 'medium' : '';
                const confidence = fact.confidence ? `<span class="confidence ${confidenceClass}">${confidencePercent}%</span>` : '';
                return `
                            <div class="memory-item">
                                <div class="item-content">
                                    ${factTag}
                                    <span class="item-value">${fact.value}</span>
                                </div>
                                ${confidence}
                            </div>`;
            }
            return `<div class="memory-item"><span class="item-value">${fact}</span></div>`;
        }).join('')}
                </div>
            </div>
        `;
    }

    container.innerHTML = html;
    container.classList.add('show');
}

function useSuggestion(text) {
    document.getElementById('rewrite-input').value = text;
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.personality-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const parentSelector = this.closest('.personality-selector');
            parentSelector.querySelectorAll('.personality-btn').forEach(b => {
                b.classList.remove('active');
            });
            this.classList.add('active');

            const personality = this.getAttribute('data-personality');

            if (this.closest('#rewrite-tab')) {
                currentRewritePersonality = personality;
            } else if (this.closest('#response-tab')) {
                currentResponsePersonality = personality;
            }
        });
    });
});

async function rewriteText() {
    const text = document.getElementById('rewrite-input').value.trim();

    if (!text) {
        alert('Please enter some text to rewrite');
        return;
    }

    const useLLM = document.getElementById('rewrite-use-llm').checked;

    try {
        const response = await fetch(`${API_BASE_URL}/rewrite`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                personality: currentRewritePersonality,
                use_llm: useLLM
            })
        });

        if (!response.ok) throw new Error('Rewrite failed');

        const data = await response.json();
        displayRewriteResult(data.original, data.rewritten, data.personality, data.method);
    } catch (error) {
        alert('Rewrite failed: ' + error.message);
    }
}

function displayRewriteResult(original, rewritten, personality, method) {
    const container = document.getElementById('rewrite-result');

    const methodBadge = method === 'llm'
        ? '<span class="method-badge method-llm">LLM</span>'
        : '<span class="method-badge method-deterministic">Deterministic</span>';

    container.innerHTML = `
        <div class="result-header">
            <h3>Personality: ${personality.replace('_', ' ')}</h3>
            ${methodBadge}
        </div>
        <div class="rewrite-comparison">
            <div class="text-box">
                <h4>Original</h4>
                <p>${original}</p>
            </div>
            <div class="text-box">
                <h4>Transformed</h4>
                <p>${rewritten}</p>
            </div>
        </div>
    `;

    container.classList.add('show');
}

async function generateResponse() {
    console.log('Generate Response called');
    console.log('extractedMemory:', extractedMemory);

    if (!extractedMemory) {
        alert('Please extract memories first from the Memory Extraction tab');
        return;
    }

    const userMessage = document.getElementById('user-message-input').value.trim();

    if (!userMessage) {
        alert('Please enter a user message');
        return;
    }

    const useLLM = document.getElementById('response-use-llm').checked;

    try {
        const response = await fetch(`${API_BASE_URL}/generate-response`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                memory: extractedMemory,
                user_message: userMessage,
                personality: currentResponsePersonality,
                use_llm: useLLM
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Response generation failed');
        }

        const data = await response.json();
        displayResponseResult(data.base_response, data.personalized_response, data.personality, data.method);
    } catch (error) {
        console.error('Response generation error:', error);
        alert('Response generation failed: ' + error.message);
    }
}

function displayResponseResult(baseResponse, personalizedResponse, personality, method) {
    const container = document.getElementById('response-result');

    const methodBadge = method === 'llm'
        ? '<span class="method-badge method-llm">LLM</span>'
        : '<span class="method-badge method-deterministic">Deterministic</span>';

    container.innerHTML = `
        <div class="result-header">
            <h3>Personality: ${personality.replace('_', ' ')}</h3>
            ${methodBadge}
        </div>
        <div class="response-comparison">
            <div class="text-box">
                <h4>Before (Generic)</h4>
                <p>${baseResponse}</p>
            </div>
            <div class="text-box">
                <h4>After (Personalized)</h4>
                <p>${personalizedResponse}</p>
            </div>
        </div>
    `;

    container.classList.add('show');
}