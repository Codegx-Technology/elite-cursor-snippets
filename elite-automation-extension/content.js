/**
 * Elite Automation Content Script
 *
 * Auto-intercepts AI chat inputs and enhances prompts in real-time
 * Universal compatibility across all AI platforms
 *
 * @author Paps (Kenya-First Engineering)
 * @version 2.0.0
 */

class EliteAutomationContent {
    constructor() {
        this.core = new EliteAutomationCore();
        this.isEnabled = true;
        this.platform = this.detectPlatform();
        this.lastEnhancement = null;

        this.init();
    }

    /**
     * Initialize the automation system
     */
    init() {
        console.log('🤖 Elite Automation: Initializing on', this.platform);
        
        // Record platform usage
        this.core.recordPlatformUsage(this.platform);
        
        // Check if enabled
        chrome.storage.sync.get(['eliteAutomationEnabled'], (result) => {
            this.isEnabled = result.eliteAutomationEnabled !== false; // Default to true
            
            if (this.isEnabled) {
                this.setupInterceptors();
                console.log('🤖 Elite Automation: Active and monitoring inputs');
            }
        });

        // Listen for enable/disable messages
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            if (request.action === 'toggleAutomation') {
                this.isEnabled = request.enabled;
                if (this.isEnabled) {
                    this.setupInterceptors();
                } else {
                    this.removeInterceptors();
                }
                sendResponse({ success: true });
            } else if (request.action === 'getStats') {
                sendResponse(this.core.getStats());
            }
        });
    }

    /**
     * Detect current AI platform
     */
    detectPlatform() {
        const hostname = window.location.hostname.toLowerCase();
        const href = window.location.href.toLowerCase();

        // Check both hostname and full URL for better detection
        if (hostname.includes('windsurf') || href.includes('windsurf') ||
            hostname.includes('codeium.com') || href.includes('codeium')) return 'Windsurf AI';
        if (hostname.includes('cursor')) return 'Cursor AI';
        if (hostname.includes('gemini') || hostname.includes('bard')) return 'Gemini';
        if (hostname.includes('claude')) return 'Claude';
        if (hostname.includes('openai') || hostname.includes('chatgpt')) return 'ChatGPT';
        if (hostname.includes('localhost')) return 'Local AI';

        // Debug logging
        console.log('🤖 Elite Automation: Platform detection', { hostname, href });

        return 'Unknown AI Platform';
    }

    /**
     * Get platform-specific selectors for input fields
     */
    getPlatformSelectors() {
        const platform = this.platform.toLowerCase();
        
        // Universal selectors that work across most platforms
        const universalSelectors = [
            'textarea[placeholder*="message"]',
            'textarea[placeholder*="prompt"]',
            'textarea[placeholder*="ask"]',
            'textarea[placeholder*="chat"]',
            'textarea[placeholder*="type"]',
            'div[contenteditable="true"]',
            'input[type="text"][placeholder*="message"]',
            'input[type="text"][placeholder*="prompt"]',
            '.chat-input textarea',
            '.prompt-input textarea',
            '.message-input textarea',
            '[data-testid*="input"]',
            '[data-testid*="textarea"]',
            '[role="textbox"]'
        ];

        // Platform-specific selectors
        const platformSelectors = {
            'cursor': [
                '.cursor-chat-input textarea',
                '.chat-input-container textarea',
                'textarea[placeholder*="Ask Cursor"]'
            ],
            'windsurf': [
                'textarea[placeholder*="Ask Windsurf"]',
                'textarea[placeholder*="Type a message"]',
                'textarea[placeholder*="Chat with"]',
                '.windsurf-chat-input textarea',
                '.chat-container textarea',
                '.chat-input-container textarea',
                '.codeium-chat textarea'
            ],
            'gemini': [
                'textarea[placeholder*="Enter a prompt"]',
                '.chat-input textarea'
            ],
            'claude': [
                'textarea[placeholder*="Talk to Claude"]',
                '.claude-input textarea'
            ],
            'chatgpt': [
                'textarea[placeholder*="Message ChatGPT"]',
                '#prompt-textarea'
            ]
        };

        // Combine universal and platform-specific selectors
        const specific = platformSelectors[platform] || [];
        return [...specific, ...universalSelectors];
    }

    /**
     * Setup input interceptors
     */
    setupInterceptors() {
        // Remove existing interceptors first
        this.removeInterceptors();

        // Setup new interceptors with debouncing
        this.setupInputMonitoring();
        this.setupSubmitInterception();
        
        // Monitor for dynamically added inputs
        this.setupMutationObserver();
    }

    /**
     * Monitor input fields for changes
     */
    setupInputMonitoring() {
        this.selectors.forEach(selector => {
            const inputs = document.querySelectorAll(selector);
            inputs.forEach(input => {
                if (!input.dataset.eliteAutomationAttached) {
                    input.dataset.eliteAutomationAttached = 'true';
                    
                    // Add input event listener with debouncing
                    let debounceTimer;
                    input.addEventListener('input', (e) => {
                        clearTimeout(debounceTimer);
                        debounceTimer = setTimeout(() => {
                            this.handleInputChange(e.target);
                        }, 300); // 300ms debounce
                    });

                    // Add keydown listener for Enter key
                    input.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            this.handleSubmit(e.target);
                        }
                    });
                }
            });
        });
    }

    /**
     * Setup submit button interception
     */
    setupSubmitInterception() {
        // Common submit button selectors
        const submitSelectors = [
            'button[type="submit"]',
            'button[aria-label*="Send"]',
            'button[title*="Send"]',
            '.send-button',
            '.submit-button',
            '[data-testid*="send"]',
            'button:has(svg[data-icon="send"])'
        ];

        submitSelectors.forEach(selector => {
            const buttons = document.querySelectorAll(selector);
            buttons.forEach(button => {
                if (!button.dataset.eliteAutomationAttached) {
                    button.dataset.eliteAutomationAttached = 'true';
                    button.addEventListener('click', (e) => {
                        const input = this.findNearestInput(button);
                        if (input) {
                            this.handleSubmit(input);
                        }
                    });
                }
            });
        });
    }

    /**
     * Setup mutation observer for dynamic content
     */
    setupMutationObserver() {
        if (this.mutationObserver) {
            this.mutationObserver.disconnect();
        }

        this.mutationObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        // Check if the added node or its children contain input fields
                        const inputs = node.querySelectorAll ? 
                            node.querySelectorAll(this.selectors.join(', ')) : [];
                        
                        if (inputs.length > 0) {
                            setTimeout(() => this.setupInputMonitoring(), 100);
                        }
                    }
                });
            });
        });

        this.mutationObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Handle input field changes
     */
    handleInputChange(input) {
        if (!this.isEnabled || !input.value.trim()) return;

        const prompt = input.value.trim();
        const enhancement = this.core.analyzePrompt(prompt);

        if (enhancement && enhancement.confidence > 0.7) {
            // Store enhancement for potential use
            this.lastEnhancement = {
                original: prompt,
                enhanced: this.core.enhancePrompt(prompt, enhancement),
                snippet: enhancement.snippet,
                confidence: enhancement.confidence
            };

            // Show subtle indicator (optional)
            this.showEnhancementIndicator(input, enhancement);
        }
    }

    /**
     * Handle form submission
     */
    handleSubmit(input) {
        if (!this.isEnabled || !this.lastEnhancement) return;

        const currentPrompt = input.value.trim();
        
        // Check if current prompt matches our last enhancement
        if (currentPrompt === this.lastEnhancement.original) {
            // Replace with enhanced prompt
            input.value = this.lastEnhancement.enhanced;
            
            // Trigger input event to notify the platform
            input.dispatchEvent(new Event('input', { bubbles: true }));
            
            console.log('🤖 Elite Automation: Enhanced prompt', {
                snippet: this.lastEnhancement.snippet,
                confidence: this.lastEnhancement.confidence,
                platform: this.platform
            });

            // Clear the enhancement
            this.lastEnhancement = null;
        }
    }

    /**
     * Show enhancement indicator
     */
    showEnhancementIndicator(input, enhancement) {
        // Remove existing indicator
        const existingIndicator = input.parentNode.querySelector('.elite-automation-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }

        // Create new indicator
        const indicator = document.createElement('div');
        indicator.className = 'elite-automation-indicator';
        indicator.innerHTML = `
            <div style="
                position: absolute;
                top: -25px;
                right: 0;
                background: #4F79A4;
                color: white;
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 10px;
                font-family: monospace;
                z-index: 10000;
                opacity: 0.8;
            ">
                🤖 ${enhancement.snippet} (${(enhancement.confidence * 100).toFixed(0)}%)
            </div>
        `;

        // Position relative to input
        input.parentNode.style.position = 'relative';
        input.parentNode.appendChild(indicator);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.remove();
            }
        }, 3000);
    }

    /**
     * Find nearest input field to a button
     */
    findNearestInput(button) {
        // Look for input in same container
        const container = button.closest('form, .chat-container, .input-container, .message-container');
        if (container) {
            const input = container.querySelector(this.selectors.join(', '));
            if (input) return input;
        }

        // Look for input in previous siblings
        let sibling = button.previousElementSibling;
        while (sibling) {
            if (this.selectors.some(sel => sibling.matches && sibling.matches(sel))) {
                return sibling;
            }
            const input = sibling.querySelector && sibling.querySelector(this.selectors.join(', '));
            if (input) return input;
            sibling = sibling.previousElementSibling;
        }

        return null;
    }

    /**
     * Remove all interceptors
     */
    removeInterceptors() {
        // Remove input listeners
        document.querySelectorAll('[data-elite-automation-attached]').forEach(element => {
            element.removeAttribute('data-elite-automation-attached');
        });

        // Disconnect mutation observer
        if (this.mutationObserver) {
            this.mutationObserver.disconnect();
        }

        // Remove indicators
        document.querySelectorAll('.elite-automation-indicator').forEach(indicator => {
            indicator.remove();
        });
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new EliteAutomationContent();
    });
} else {
    new EliteAutomationContent();
}
