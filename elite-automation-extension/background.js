/**
 * Elite Automation Background Script
 * 
 * Manages extension state and communication between components
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 2.0.0
 */

// Extension installation and startup
chrome.runtime.onInstalled.addListener((details) => {
    console.log('🤖 Elite Automation: Extension installed/updated');
    
    // Set default settings
    chrome.storage.sync.set({
        eliteAutomationEnabled: true,
        enhancementStats: {
            totalEnhancements: 0,
            successfulMatches: 0,
            platformsUsed: []
        }
    });

    // Show welcome notification
    if (details.reason === 'install') {
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE2IDRDOS4zNzI1OCA0IDQgOS4zNzI1OCA0IDE2QzQgMjIuNjI3NCA5LjM3MjU4IDI4IDE2IDI4QzIyLjYyNzQgMjggMjggMjIuNjI3NCAyOCAxNkMyOCA5LjM3MjU4IDIyLjYyNzQgNCAxNiA0WiIgZmlsbD0iIzRGNzlBNCIvPgo8cGF0aCBkPSJNMTIgMTJIMjBWMTZIMTJWMTJaIiBmaWxsPSJ3aGl0ZSIvPgo8cGF0aCBkPSJNMTIgMThIMjBWMjJIMTJWMThaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4=',
            title: 'Elite Automation Ready!',
            message: 'AI chat enhancement is now active. Just type naturally in any AI platform!'
        });
    }
});

// Handle messages from content scripts and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    switch (request.action) {
        case 'getSettings':
            chrome.storage.sync.get(['eliteAutomationEnabled'], (result) => {
                sendResponse({ enabled: result.eliteAutomationEnabled !== false });
            });
            return true; // Keep message channel open for async response

        case 'toggleAutomation':
            chrome.storage.sync.set({ eliteAutomationEnabled: request.enabled }, () => {
                // Notify all content scripts
                chrome.tabs.query({}, (tabs) => {
                    tabs.forEach(tab => {
                        chrome.tabs.sendMessage(tab.id, {
                            action: 'toggleAutomation',
                            enabled: request.enabled
                        }).catch(() => {
                            // Ignore errors for tabs without content script
                        });
                    });
                });
                sendResponse({ success: true });
            });
            return true;

        case 'updateStats':
            chrome.storage.sync.get(['enhancementStats'], (result) => {
                const stats = result.enhancementStats || {
                    totalEnhancements: 0,
                    successfulMatches: 0,
                    platformsUsed: []
                };
                
                // Update stats
                stats.totalEnhancements += request.stats.totalEnhancements || 0;
                stats.successfulMatches += request.stats.successfulMatches || 0;
                
                if (request.stats.platform && !stats.platformsUsed.includes(request.stats.platform)) {
                    stats.platformsUsed.push(request.stats.platform);
                }
                
                chrome.storage.sync.set({ enhancementStats: stats });
                sendResponse({ success: true });
            });
            return true;

        case 'getStats':
            chrome.storage.sync.get(['enhancementStats'], (result) => {
                sendResponse(result.enhancementStats || {
                    totalEnhancements: 0,
                    successfulMatches: 0,
                    platformsUsed: []
                });
            });
            return true;

        case 'testEnhancement':
            // Test the enhancement system
            const testPrompt = request.prompt || 'fix the footer blinking button issue';
            sendResponse({
                success: true,
                result: `🤖 Test successful! Prompt "${testPrompt}" would trigger enhancement.`
            });
            return true;

        default:
            sendResponse({ error: 'Unknown action' });
    }
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
    // Open popup (this is handled automatically by manifest)
    console.log('🤖 Elite Automation: Icon clicked');
});

// Monitor tab updates to inject content script if needed
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        const url = new URL(tab.url);
        const supportedDomains = [
            'cursor.sh',
            'windsurf.greptile.com',
            'gemini.google.com',
            'bard.google.com',
            'claude.ai',
            'chat.openai.com',
            'chatgpt.com',
            'codeium.com'
        ];

        if (supportedDomains.some(domain => url.hostname.includes(domain)) || 
            url.hostname === 'localhost') {
            
            // Ensure content script is injected
            chrome.scripting.executeScript({
                target: { tabId: tabId },
                files: ['elite-automation-core.js', 'content.js']
            }).catch(() => {
                // Content script might already be injected
            });
        }
    }
});

// Periodic cleanup and maintenance
setInterval(() => {
    // Clean up old data if needed
    chrome.storage.sync.get(['enhancementStats'], (result) => {
        const stats = result.enhancementStats;
        if (stats && stats.totalEnhancements > 10000) {
            // Reset stats if they get too large
            chrome.storage.sync.set({
                enhancementStats: {
                    totalEnhancements: 0,
                    successfulMatches: 0,
                    platformsUsed: stats.platformsUsed || []
                }
            });
        }
    });
}, 24 * 60 * 60 * 1000); // Daily cleanup

console.log('🤖 Elite Automation: Background script loaded');
