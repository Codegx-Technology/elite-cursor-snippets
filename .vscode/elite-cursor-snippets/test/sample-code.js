// Sample code with various issues for testing Elite Auto-Fix

// Issue 1: Console.log statements (noconlog)
console.log('Debug message');
console.warn('Warning message');

// Issue 2: Long function (srpcheck)
function processUserData(userData) {
    console.log('Processing user data');
    if (userData && userData.name) {
        const name = userData.name.trim();
        if (name.length > 0) {
            const formattedName = name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
            if (userData.email) {
                const email = userData.email.trim().toLowerCase();
                if (email.includes('@')) {
                    const domain = email.split('@')[1];
                    if (domain && domain.length > 0) {
                        const user = {
                            name: formattedName,
                            email: email,
                            domain: domain,
                            createdAt: new Date(),
                            isValid: true
                        };
                        return user;
                    }
                }
            }
        }
    }
    return null;
}

// Issue 3: USD currency format (kenyacheck)
const price = '$25.99';
const totalAmount = 'Total: $150.00 USD';

// Issue 4: US phone format (kenyacheck)
const phoneNumber = '+1234567890';

// Issue 5: Missing error handling (errorcheck)
async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    const data = await response.json();
    return data;
}

// Issue 6: Security vulnerability (securitycheck)
function displayMessage(message) {
    document.getElementById('output').innerHTML = message;
}

// Issue 7: Performance issue (perfcheck)
function expensiveOperation(items) {
    return items.map(item => item.id).map(id => id.toString()).map(str => str.padStart(5, '0'));
}

// Issue 8: Class component (hookcheck) - React
class UserComponent extends React.Component {
    componentDidMount() {
        this.fetchData();
    }
    
    render() {
        return <div>User Component</div>;
    }
}

// Issue 9: Missing accessibility (a11ycheck)
const ImageComponent = () => {
    return (
        <div>
            <img src="user-avatar.jpg" />
            <button onClick={handleClick}>Click me</button>
            <input type="text" />
        </div>
    );
};

// Issue 10: Fixed pixel units (mobilecheck)
const styles = {
    container: {
        width: '800px',
        height: '600px',
        fontSize: '16px'
    }
};

// Issue 11: Nested loops (perfcheck)
function findMatches(array1, array2) {
    const matches = [];
    for (let i = 0; i < array1.length; i++) {
        for (let j = 0; j < array2.length; j++) {
            if (array1[i] === array2[j]) {
                matches.push(array1[i]);
            }
        }
    }
    return matches;
}

// Issue 12: eval usage (securitycheck)
function executeCode(code) {
    return eval(code);
}

// Issue 13: Hardcoded credentials (securitycheck)
const config = {
    apiKey: 'sk-1234567890abcdef',
    password: 'mySecretPassword123'
};

// Issue 14: Missing key prop in React (hookcheck)
const ListComponent = ({ items }) => {
    return (
        <ul>
            {items.map(item => <li>{item.name}</li>)}
        </ul>
    );
};

// Issue 15: British vs American spelling (kenyacheck)
const userPreferences = {
    color: 'blue',
    center: 'nairobi',
    meter: 100
};

export { processUserData, fetchUserData, UserComponent, ImageComponent };
