// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// Data storage
let allUniversities = [];
let allPrograms = [];
let displayedUniversities = 0;
let displayedPrograms = 0;

// Subscription management
let userSubscription = {
    plan: 'free',
    emailsUsed: 0,
    emailsLimit: 0,
    searchesUsed: 0,
    searchesLimit: 'unlimited'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('UniUp app initializing...');
    loadUserData();
    setupEventListeners();
    loadInitialData();
});

// Load user data from localStorage
function loadUserData() {
    const savedUser = localStorage.getItem('currentUser');
    const savedToken = localStorage.getItem('token');
    
    if (savedUser && savedToken) {
        currentUser = JSON.parse(savedUser);
        updateUserInterface();
        loadSubscriptionData();
        updateUserSubscriptionDisplay();
    }
}

// Load subscription data from localStorage
function loadSubscriptionData() {
    const savedSubscription = localStorage.getItem('userSubscription');
    if (savedSubscription) {
        userSubscription = JSON.parse(savedSubscription);
    }
}

// Save subscription data to localStorage
function saveSubscriptionData() {
    localStorage.setItem('userSubscription', JSON.stringify(userSubscription));
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Login/Register buttons
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => showModal('loginModal'));
    }
    
    const registerBtn = document.getElementById('registerBtn');
    if (registerBtn) {
        registerBtn.addEventListener('click', () => showModal('registerModal'));
    }
    
    // User menu
    const userBtn = document.getElementById('userBtn');
    if (userBtn) {
        userBtn.addEventListener('click', toggleUserMenu);
    }
}

// Load initial data
async function loadInitialData() {
    try {
        console.log('Starting to load initial data...');
        await Promise.all([
            loadUniversities(),
            loadPrograms(),
            loadCountries(),
            loadFieldsOfStudy()
        ]);
        console.log('Initial data loading completed');
    } catch (error) {
        console.error('Error loading initial data:', error);
        showNotification('Error loading data. Please refresh the page.', 'error');
    }
}

// API Functions
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        ...options
    };
    
    if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
    }
    
    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Load universities
async function loadUniversities() {
    try {
        console.log('Loading universities...');
        const universities = await apiRequest('/universities/');
        console.log('Universities loaded:', universities);
        allUniversities = universities.results || universities;
        displayedUniversities = Math.min(10, allUniversities.length);
        console.log('Displaying universities:', allUniversities.slice(0, displayedUniversities));
        displayUniversities(allUniversities.slice(0, displayedUniversities));
        
        // Show "Show More" button if there are more universities
        if (allUniversities.length > 10) {
            const showMoreBtn = document.getElementById('showMoreUniversities');
            if (showMoreBtn) {
                showMoreBtn.classList.remove('hidden');
            }
        }
    } catch (error) {
        console.error('Error loading universities:', error);
    }
}

// Load programs
async function loadPrograms() {
    try {
        console.log('Loading programs...');
        const programs = await apiRequest('/programs/');
        console.log('Programs loaded:', programs);
        allPrograms = programs.results || programs;
        displayedPrograms = Math.min(10, allPrograms.length);
        console.log('Displaying programs:', allPrograms.slice(0, displayedPrograms));
        displayPrograms(allPrograms.slice(0, displayedPrograms));
        
        // Show "Show More" button if there are more programs
        if (allPrograms.length > 10) {
            const showMoreBtn = document.getElementById('showMorePrograms');
            if (showMoreBtn) {
                showMoreBtn.classList.remove('hidden');
            }
        }
    } catch (error) {
        console.error('Error loading programs:', error);
    }
}

// Load countries
async function loadCountries() {
    try {
        const data = await apiRequest('/countries/');
        const countries = data.results || data;
        populateSelect('countryFilter', countries);
    } catch (error) {
        console.error('Error loading countries:', error);
    }
}

// Load fields of study
async function loadFieldsOfStudy() {
    try {
        const data = await apiRequest('/fields-of-study/');
        const fields = data.results || data;
        populateSelect('fieldFilter', fields);
    } catch (error) {
        console.error('Error loading fields of study:', error);
    }
}

// Populate select dropdown
function populateSelect(selectId, options) {
    const select = document.getElementById(selectId);
    if (!select) return;
    
    // Clear existing options except the first one
    while (select.children.length > 1) {
        select.removeChild(select.lastChild);
    }
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
}

// Display universities
function displayUniversities(universities) {
    console.log('displayUniversities called with:', universities);
    const container = document.getElementById('universitiesContainer');
    console.log('Container found:', container);
    if (!container) {
        console.error('universitiesContainer not found!');
        return;
    }
    container.innerHTML = '';
    
    universities.forEach(university => {
        const card = createUniversityCard(university);
        container.appendChild(card);
    });
    console.log('Universities displayed successfully');
}

// Display programs
function displayPrograms(programs) {
    console.log('displayPrograms called with:', programs);
    const container = document.getElementById('programsContainer');
    console.log('Programs container found:', container);
    if (!container) {
        console.error('programsContainer not found!');
        return;
    }
    container.innerHTML = '';
    
    programs.forEach(program => {
        const card = createProgramCard(program);
        container.appendChild(card);
    });
    console.log('Programs displayed successfully');
}

// Create university card
function createUniversityCard(university) {
    const card = document.createElement('div');
    card.className = 'bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow';
    card.innerHTML = `
        <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mr-4">
                <i class="fas fa-university text-indigo-600"></i>
            </div>
            <div>
                <h3 class="text-lg font-semibold text-gray-900">${university.name}</h3>
                <p class="text-gray-600">${university.city}, ${university.country}</p>
            </div>
        </div>
        <p class="text-gray-700 mb-4">${university.description || 'No description available'}</p>
        <div class="flex justify-between items-center">
            <div class="text-sm text-gray-500">
                <span>Est. ${university.established_year || 'N/A'}</span>
                <span class="mx-2">•</span>
                <span>${university.student_count ? university.student_count.toLocaleString() : 'N/A'} students</span>
            </div>
            <a href="${university.website}" target="_blank" class="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
                Visit Website <i class="fas fa-external-link-alt ml-1"></i>
            </a>
        </div>
    `;
    return card;
}

// Create program card
function createProgramCard(program) {
    const card = document.createElement('div');
    card.className = 'bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow';
    card.innerHTML = `
        <div class="mb-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">${program.name}</h3>
            <p class="text-indigo-600 font-medium">${program.university ? program.university.name : 'Unknown University'}</p>
            <p class="text-gray-600 text-sm">${program.university ? program.university.city : 'Unknown City'}, ${program.university ? program.university.country : 'Unknown Country'}</p>
        </div>
        <div class="mb-4">
            <span class="inline-block bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full mr-2">${program.field_of_study}</span>
            <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">${program.degree_level}</span>
        </div>
        <p class="text-gray-700 mb-4">${program.description || 'No description available'}</p>
        <div class="flex justify-between items-center">
            <div class="text-sm text-gray-500">
                <span>${program.coordinators_count || 0} coordinators</span>
            </div>
            <button onclick="viewProgramDetails(${program.id})" class="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
                View Details <i class="fas fa-arrow-right ml-1"></i>
            </button>
        </div>
    `;
    return card;
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                username: email,
                email: email,
                password 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('currentUser', JSON.stringify(data.user));
            localStorage.setItem('token', data.token || 'demo_token');
            closeModal('loginModal');
            updateUserInterface();
            loadSubscriptionData();
            updateUserSubscriptionDisplay();
            showNotification('Login successful!', 'success');
        } else {
            showNotification(data.error || 'Login failed', 'error');
        }
        
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Login failed. Please try again.', 'error');
    }
}

// Handle register
async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('currentUser', JSON.stringify(data.user));
            localStorage.setItem('token', data.token || 'demo_token');
            closeModal('registerModal');
            updateUserInterface();
            loadSubscriptionData();
            updateUserSubscriptionDisplay();
            showNotification('Registration successful!', 'success');
        } else {
            showNotification(data.error || 'Registration failed', 'error');
        }
        
    } catch (error) {
        console.error('Registration error:', error);
        showNotification('Registration failed. Please try again.', 'error');
    }
}

// Logout function
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('token');
    localStorage.removeItem('userSubscription');
    authToken = null;
    currentUser = null;
    userSubscription = {
        plan: 'free',
        emailsUsed: 0,
        emailsLimit: 0,
        searchesUsed: 0,
        searchesLimit: 'unlimited'
    };
    updateUserInterface();
    updateUserSubscriptionDisplay();
    showNotification('Logged out successfully.', 'success');
}

// Update user interface
function updateUserInterface() {
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const userBtn = document.getElementById('userBtn');
    const userMenu = document.getElementById('userMenu');
    
    if (currentUser) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (registerBtn) registerBtn.style.display = 'none';
        if (userBtn) userBtn.style.display = 'block';
        if (userMenu) {
            const usernameSpan = userMenu.querySelector('#username');
            if (usernameSpan) usernameSpan.textContent = currentUser.username;
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'block';
        if (registerBtn) registerBtn.style.display = 'block';
        if (userBtn) userBtn.style.display = 'none';
    }
}

// Update user subscription display
function updateUserSubscriptionDisplay() {
    const userPlan = document.getElementById('userPlan');
    if (userPlan) {
        userPlan.textContent = userSubscription.plan.charAt(0).toUpperCase() + userSubscription.plan.slice(1);
    }
}

// Show modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
    }
}

// Close modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Toggle user menu
function toggleUserMenu() {
    const userMenu = document.getElementById('userMenu');
    if (userMenu) {
        userMenu.classList.toggle('hidden');
    }
}

// Show notification
function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// View program details
function viewProgramDetails(programId) {
    const program = allPrograms.find(p => p.id === programId);
    if (program) {
        alert(`Program: ${program.name}\nUniversity: ${program.university ? program.university.name : 'Unknown'}\nField: ${program.field_of_study}\nDegree: ${program.degree_level}`);
    } else {
        showNotification('Program not found', 'error');
    }
}

console.log('UniUp app.js loaded successfully!');
