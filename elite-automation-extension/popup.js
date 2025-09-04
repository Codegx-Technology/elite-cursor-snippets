/**
 * Elite Automation Popup Interface
 * 
 * @author Paps (Kenya-First Engineering)
 * @version 2.0.0
 */

document.addEventListener('DOMContentLoaded', function() {
    const toggleSwitch = document.getElementById('toggleSwitch');
    const enhancedCount = document.getElementById('enhancedCount');
    const successRate = document.getElementById('successRate');
    const currentPlatform = document.getElementById('currentPlatform');
    const testBtn = document.getElementById('testBtn');
    const settingsBtn = document.getElementById('settingsBtn');

    // Load saved settings
    chrome.storage.sync.get(['eliteEnabled', 'enhancedCount', 'successRate'], function(result) {
        const isEnabled = result.eliteEnabled !== false; // Default to true
        toggleSwitch.classList.toggle('active', isEnabled);
        
        enhancedCount.textContent = result.enhancedCount || 0;
        successRate.textContent = (result.successRate || 100) + '%';
    });

    // Get current tab info
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const tab = tabs[0];
        const hostname = new URL(tab.url).hostname.toLowerCase();
        
        let platform = 'Unknown';
        if (hostname.includes('cursor')) platform = 'Cursor AI';
        else if (hostname.includes('windsurf')) platform = 'Windsurf AI';
        else if (hostname.includes('gemini')) platform = 'Gemini';
        else if (hostname.includes('claude')) platform = 'Claude';
        else if (hostname.includes('openai') || hostname.includes('chatgpt')) platform = 'ChatGPT';
        
        currentPlatform.textContent = platform;
    });

    // Toggle functionality
    toggleSwitch.addEventListener('click', function() {
        const isActive = toggleSwitch.classList.contains('active');
        const newState = !isActive;
        
        toggleSwitch.classList.toggle('active', newState);
        
        // Save setting
        chrome.storage.sync.set({eliteEnabled: newState});
        
        // Notify content script
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'toggleEliteAutomation',
                enabled: newState
            });
        });
    });

    // Test functionality
    testBtn.addEventListener('click', function() {
        const testPrompts = [
            'fix the footer blinking button issue',
            'optimize React component performance',
            'convert USD to Kenya Shilling format',
            'write tests for authentication function',
            'debug CSS styling problem'
        ];
        
        const randomPrompt = testPrompts[Math.floor(Math.random() * testPrompts.length)];
        
        // Send test message to content script
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'testEliteAutomation',
                prompt: randomPrompt
            }, function(response) {
                if (response && response.enhanced) {
                    showTestResult(randomPrompt, response.enhanced);
                } else {
                    showTestResult(randomPrompt, 'No enhancement available');
                }
            });
        });
    });

    // Settings functionality
    settingsBtn.addEventListener('click', function() {
        chrome.tabs.create({
            url: chrome.runtime.getURL('settings.html')
        });
    });

    // Show test result
    function showTestResult(original, enhanced) {
        const popup = document.createElement('div');
        popup.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 20px;
            border-radius: 8px;
            max-width: 300px;
            z-index: 10000;
            font-size: 12px;
            line-height: 1.4;
        `;
        
        popup.innerHTML = `
            <div style="margin-bottom: 10px; font-weight: bold;">🧪 Test Result</div>
            <div style="margin-bottom: 8px;"><strong>Original:</strong> ${original}</div>
            <div style="margin-bottom: 15px;"><strong>Enhanced:</strong> ${enhanced}</div>
            <button onclick="this.parentElement.remove()" style="
                background: #667eea;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 11px;
            ">Close</button>
        `;
        
        document.body.appendChild(popup);
        
        setTimeout(() => {
            if (popup.parentElement) {
                popup.remove();
            }
        }, 5000);
    }

    // Listen for updates from content script
    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
        if (request.action === 'updateStats') {
            enhancedCount.textContent = request.enhancedCount;
            successRate.textContent = request.successRate + '%';
            
            // Save updated stats
            chrome.storage.sync.set({
                enhancedCount: request.enhancedCount,
                successRate: request.successRate
            });
        }
    });
});
