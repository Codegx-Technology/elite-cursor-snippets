/**
 * Elite Automation Content Script
 * 
 * Intercepts AI chat inputs and automatically enhances them
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 2.0.0
 */

(function() {
    'use strict';

    // Initialize Elite Automation Core
    let eliteCore = null;
    
    // Load the core engine
    function initializeEliteCore() {
        if (typeof EliteAutomationCore !== 'undefined') {
            eliteCore = new EliteAutomationCore();
            console.log('🤖 Elite Automation: Initialized');
        } else {
            // Inject the core script
            const script = document.createElement('script');
            script.src = chrome.runtime.getURL('elite-automation-core.js');
            script.onload = () => {
                eliteCore = new EliteAutomationCore();
                console.log('🤖 Elite Automation: Core loaded and initialized');
            };
            document.head.appendChild(script);
        }
    }

    // AI Platform Detection
    const AI_PLATFORMS = {
        cursor: {
            selectors: [
                'textarea[placeholder*="Ask"]',
                'textarea[placeholder*="chat"]',
                '.chat-input textarea',
                '[data-testid="chat-input"]'
            ],
            name: 'Cursor AI'
        },
        windsurf: {
            selectors: [
                'textarea[placeholder*="Ask"]',
                'textarea[placeholder*="Message"]',
                '.message-input textarea',
                '.chat-textarea'
            ],
            name: 'Windsurf AI'
        },
        gemini: {
            selectors: [
                'textarea[placeholder*="Enter a prompt"]',
                'textarea[aria-label*="Message"]',
                '.ql-editor',
                '[data-testid="input-area"] textarea'
            ],
            name: 'Gemini'
        },
        claude: {
            selectors: [
                'textarea[placeholder*="Talk to Claude"]',
                '.ProseMirror',
                '[data-testid="chat-input"]'
            ],
            name: 'Claude'
        },
        openai: {
            selectors: [
                'textarea[placeholder*="Message ChatGPT"]',
                '#prompt-textarea',
                '[data-testid="chat-input"]'
            ],
            name: 'ChatGPT'
        }
    };

    // Detect current AI platform
    function detectAIPlatform() {
        const hostname = window.location.hostname.toLowerCase();
        
        if (hostname.includes('cursor')) return 'cursor';
        if (hostname.includes('windsurf')) return 'windsurf';
        if (hostname.includes('gemini') || hostname.includes('bard')) return 'gemini';
        if (hostname.includes('claude')) return 'claude';
        if (hostname.includes('openai') || hostname.includes('chatgpt')) return 'openai';
        
        return null;
    }

    // Find chat input elements
    function findChatInputs() {
        const platform = detectAIPlatform();
        if (!platform) return [];

        const config = AI_PLATFORMS[platform];
        const inputs = [];

        for (const selector of config.selectors) {
            const elements = document.querySelectorAll(selector);
            inputs.push(...elements);
        }

        return inputs.filter(el => el && el.offsetParent !== null); // Only visible elements
    }

    // Enhanced input handler with real-time enhancement
    function createEnhancedInputHandler(originalInput) {
        let isEnhancing = false;
        let lastEnhancedValue = '';
        let enhancementTimeout = null;

        return function(event) {
            if (!eliteCore || isEnhancing) return;

            const currentValue = originalInput.value || originalInput.textContent || '';

            // Skip if already enhanced or too short
            if (currentValue === lastEnhancedValue || currentValue.length < 5) {
                return;
            }

            // Clear previous timeout
            if (enhancementTimeout) {
                clearTimeout(enhancementTimeout);
            }

            // Check for Enter key (immediate enhancement)
            if (event.type === 'keydown' && event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault(); // Prevent sending original
                isEnhancing = true;

                const enhancedPrompt = eliteCore.enhancePrompt(currentValue);

                if (enhancedPrompt !== currentValue) {
                    // Update the input with enhanced prompt
                    if (originalInput.value !== undefined) {
                        originalInput.value = enhancedPrompt;
                    } else {
                        originalInput.textContent = enhancedPrompt;
                    }

                    // Trigger input events
                    originalInput.dispatchEvent(new Event('input', { bubbles: true }));

                    lastEnhancedValue = enhancedPrompt;
                    showEnhancementNotification(currentValue, enhancedPrompt);
                }

                // Now send the enhanced prompt
                setTimeout(() => {
                    const enterEvent = new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        bubbles: true
                    });
                    originalInput.dispatchEvent(enterEvent);
                    isEnhancing = false;
                }, 200);

            } else {
                // Real-time enhancement preview (delayed)
                enhancementTimeout = setTimeout(() => {
                    const enhancedPrompt = eliteCore.enhancePrompt(currentValue);
                    if (enhancedPrompt !== currentValue) {
                        showEnhancementPreview(originalInput, enhancedPrompt);
                    }
                }, 1000);
            }
        };
    }

    // Show enhancement notification
    function showEnhancementNotification(original, enhanced) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'elite-automation-notification';
        notification.innerHTML = `
            <div class="elite-notification-content">
                <span class="elite-icon">🤖</span>
                <span class="elite-text">Elite Automation Enhanced Your Prompt</span>
                <button class="elite-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 3000);
    }

    // Setup input monitoring
    function setupInputMonitoring() {
        const inputs = findChatInputs();
        
        inputs.forEach(input => {
            if (input.dataset.eliteEnhanced) return; // Already enhanced
            
            const handler = createEnhancedInputHandler(input);
            
            // Add event listeners
            input.addEventListener('keydown', handler);
            input.addEventListener('paste', handler);
            
            // Mark as enhanced
            input.dataset.eliteEnhanced = 'true';
            
            console.log('🤖 Elite Automation: Enhanced input element');
        });
    }

    // Mutation observer to handle dynamic content
    function setupMutationObserver() {
        const observer = new MutationObserver((mutations) => {
            let shouldSetup = false;
            
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // Check if new chat inputs were added
                            const newInputs = findChatInputs();
                            if (newInputs.some(input => !input.dataset.eliteEnhanced)) {
                                shouldSetup = true;
                            }
                        }
                    });
                }
            });
            
            if (shouldSetup) {
                setTimeout(setupInputMonitoring, 500);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Initialize everything
    function initialize() {
        console.log('🤖 Elite Automation: Starting initialization...');
        
        // Initialize core
        initializeEliteCore();
        
        // Setup initial monitoring
        setTimeout(() => {
            setupInputMonitoring();
            setupMutationObserver();
        }, 1000);
        
        // Re-setup periodically for dynamic content
        setInterval(setupInputMonitoring, 5000);
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }

    // Add CSS for notifications
    const style = document.createElement('style');
    style.textContent = `
        .elite-automation-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            animation: slideIn 0.3s ease-out;
        }
        
        .elite-notification-content {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .elite-icon {
            font-size: 16px;
        }
        
        .elite-close {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 18px;
            margin-left: 8px;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);

})();
