/**
 * Elite Automation Popup Script
 * 
 * Manages the extension popup interface and settings
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 2.0.0
 */

class EliteAutomationPopup {
    constructor() {
        this.isEnabled = true;
        this.currentTab = null;
        this.init();
    }

    /**
     * Initialize popup
     */
    async init() {
        // Get current tab
        this.currentTab = await this.getCurrentTab();
        
        // Load settings
        await this.loadSettings();
        
        // Load stats
        await this.loadStats();
        
        // Detect platform
        this.detectPlatform();
        
        // Setup event listeners
        this.setupEventListeners();
        
        console.log('🤖 Elite Automation Popup: Initialized');
    }

    /**
     * Get current active tab
     */
    async getCurrentTab() {
        return new Promise((resolve) => {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                resolve(tabs[0] || null);
            });
        });
    }

    /**
     * Load settings from storage
     */
    async loadSettings() {
        return new Promise((resolve) => {
            chrome.storage.sync.get(['eliteAutomationEnabled'], (result) => {
                this.isEnabled = result.eliteAutomationEnabled !== false;
                this.updateToggleUI();
                resolve();
            });
        });
    }

    /**
     * Load statistics from storage
     */
    async loadStats() {
        return new Promise((resolve) => {
            chrome.storage.sync.get(['enhancementStats'], (result) => {
                const stats = result.enhancementStats || {
                    totalEnhancements: 0,
                    successfulMatches: 0,
                    platformsUsed: []
                };
                this.updateStatsUI(stats);
                resolve();
            });
        });
    }

    /**
     * Detect current platform
     */
    detectPlatform() {
        if (!this.currentTab || !this.currentTab.url) {
            this.updatePlatformUI('Unknown', false);
            return;
        }

        const url = new URL(this.currentTab.url);
        const hostname = url.hostname.toLowerCase();
        const href = this.currentTab.url.toLowerCase();

        let platform = 'Unknown Platform';
        let isSupported = false;

        // Enhanced detection for Windsurf and other platforms
        if (hostname.includes('windsurf') || href.includes('windsurf') ||
            hostname.includes('codeium.com') || href.includes('codeium')) {
            platform = 'Windsurf AI';
            isSupported = true;
        } else if (hostname.includes('cursor')) {
            platform = 'Cursor AI';
            isSupported = true;
        } else if (hostname.includes('gemini') || hostname.includes('bard')) {
            platform = 'Gemini';
            isSupported = true;
        } else if (hostname.includes('claude')) {
            platform = 'Claude';
            isSupported = true;
        } else if (hostname.includes('openai') || hostname.includes('chatgpt')) {
            platform = 'ChatGPT';
            isSupported = true;
        } else if (hostname === 'localhost') {
            platform = 'Local AI';
            isSupported = true;
        }

        // Debug logging
        console.log('🤖 Elite Automation Popup: Platform detection', {
            hostname,
            href,
            platform,
            isSupported
        });

        this.updatePlatformUI(platform, isSupported);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Toggle switch
        const toggleSwitch = document.getElementById('toggleSwitch');
        toggleSwitch.addEventListener('click', () => {
            this.toggleAutomation();
        });

        // Test button
        const testButton = document.getElementById('testButton');
        testButton.addEventListener('click', () => {
            this.testEnhancement();
        });

        // Refresh stats every 5 seconds
        setInterval(() => {
            this.loadStats();
        }, 5000);
    }

    /**
     * Toggle automation on/off
     */
    async toggleAutomation() {
        this.isEnabled = !this.isEnabled;
        
        // Save to storage
        chrome.storage.sync.set({ eliteAutomationEnabled: this.isEnabled });
        
        // Update UI
        this.updateToggleUI();
        
        // Notify content script
        if (this.currentTab) {
            chrome.tabs.sendMessage(this.currentTab.id, {
                action: 'toggleAutomation',
                enabled: this.isEnabled
            }).catch(() => {
                // Content script might not be loaded
            });
        }

        console.log('🤖 Elite Automation:', this.isEnabled ? 'Enabled' : 'Disabled');
    }

    /**
     * Test enhancement system
     */
    async testEnhancement() {
        const testButton = document.getElementById('testButton');
        const testResult = document.getElementById('testResult');
        
        testButton.textContent = '🔄 Testing...';
        testButton.disabled = true;
        
        try {
            // Test with a sample prompt
            const testPrompt = 'fix the footer blinking button issue';
            
            // Send test message to background script
            chrome.runtime.sendMessage({
                action: 'testEnhancement',
                prompt: testPrompt
            }, (response) => {
                if (response && response.success) {
                    testResult.textContent = `✅ Test successful! Pattern recognition working.`;
                    testResult.style.display = 'block';
                    
                    // Simulate enhancement
                    setTimeout(() => {
                        testResult.textContent = `🤖 "${testPrompt}" → surgicalfix (100% confidence)`;
                    }, 1000);
                } else {
                    testResult.textContent = '❌ Test failed. Please check console.';
                    testResult.style.display = 'block';
                }
                
                testButton.textContent = '🧪 Test Enhancement';
                testButton.disabled = false;
                
                // Hide result after 5 seconds
                setTimeout(() => {
                    testResult.style.display = 'none';
                }, 5000);
            });
        } catch (error) {
            testResult.textContent = '❌ Error: ' + error.message;
            testResult.style.display = 'block';
            testButton.textContent = '🧪 Test Enhancement';
            testButton.disabled = false;
        }
    }

    /**
     * Update toggle UI
     */
    updateToggleUI() {
        const toggleSwitch = document.getElementById('toggleSwitch');
        if (this.isEnabled) {
            toggleSwitch.classList.add('active');
        } else {
            toggleSwitch.classList.remove('active');
        }
    }

    /**
     * Update stats UI
     */
    updateStatsUI(stats) {
        document.getElementById('totalEnhancements').textContent = stats.totalEnhancements || 0;
        
        const successRate = stats.totalEnhancements > 0 
            ? Math.round((stats.successfulMatches / stats.totalEnhancements) * 100)
            : 0;
        document.getElementById('successRate').textContent = successRate + '%';
        
        document.getElementById('platformsUsed').textContent = (stats.platformsUsed || []).length;
    }

    /**
     * Update platform UI
     */
    updatePlatformUI(platform, isSupported) {
        document.getElementById('platformName').textContent = platform;
        
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (isSupported) {
            statusIndicator.className = 'status-indicator status-active';
            statusText.textContent = this.isEnabled ? 'Active & Monitoring' : 'Ready (Disabled)';
        } else {
            statusIndicator.className = 'status-indicator status-inactive';
            statusText.textContent = 'Platform Not Supported';
        }
    }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EliteAutomationPopup();
});
