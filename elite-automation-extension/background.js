/**
 * Elite Automation Background Script
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 2.0.0
 */

// Installation handler
chrome.runtime.onInstalled.addListener(function(details) {
    if (details.reason === 'install') {
        // Set default settings
        chrome.storage.sync.set({
            eliteEnabled: true,
            enhancedCount: 0,
            successRate: 100,
            debugMode: false
        });
        
        // Open welcome page
        chrome.tabs.create({
            url: chrome.runtime.getURL('welcome.html')
        });
        
        console.log('🤖 Elite Automation: Installed successfully');
    }
});

// Message handling
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    switch (request.action) {
        case 'getSettings':
            chrome.storage.sync.get(null, function(settings) {
                sendResponse(settings);
            });
            return true; // Keep message channel open
            
        case 'updateSettings':
            chrome.storage.sync.set(request.settings, function() {
                sendResponse({success: true});
            });
            return true;
            
        case 'logEnhancement':
            // Log enhancement for analytics
            chrome.storage.sync.get(['enhancedCount'], function(result) {
                const newCount = (result.enhancedCount || 0) + 1;
                chrome.storage.sync.set({enhancedCount: newCount});
            });
            break;
            
        default:
            console.log('Unknown action:', request.action);
    }
});

// Context menu (optional)
chrome.contextMenus.create({
    id: 'eliteAutomation',
    title: 'Enhance with Elite Automation',
    contexts: ['selection']
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
    if (info.menuItemId === 'eliteAutomation') {
        chrome.tabs.sendMessage(tab.id, {
            action: 'enhanceSelection',
            text: info.selectionText
        });
    }
});
