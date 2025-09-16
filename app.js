// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// Data storage
let allUniversities = [];
let allPrograms = [];
let displayedUniversities = 0;
let displayedPrograms = 0;
let searchResults = []; // Store search results for favorites
let displayedSearchResults = 0;
let currentProgramId = null; // Store current program ID for favorites

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
    loadUserData();
    setupEventListeners();
    loadInitialData();
});

// Load user data from localStorage
// Removed duplicate loadUserData function

// Load initial data
async function loadInitialData() {
    console.log('=== LOADING INITIAL DATA ===');
    try {
        await Promise.all([
            loadUniversities(),
            loadPrograms(),
            loadCountries(),
            loadFieldsOfStudy(),
            loadUniversitiesForFilter()
        ]);
        console.log('=== ALL INITIAL DATA LOADED SUCCESSFULLY ===');
    } catch (error) {
        console.error('Error loading initial data:', error);
        showNotification('Error loading data. Please refresh the page.', 'error');
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
    // Wait for DOM to be fully loaded
    setTimeout(() => {
        // Login form
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', handleLogin);
            console.log('Login form event listener attached');
        } else {
            console.error('Login form not found');
        }
        
        // Register form
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', handleRegister);
            console.log('Register form event listener attached');
        } else {
            console.error('Register form not found');
        }
        
        // Login/Register buttons
        const loginBtn = document.getElementById('loginBtn');
        if (loginBtn) {
            loginBtn.addEventListener('click', () => showModal('loginModal'));
            console.log('Login button event listener attached');
        } else {
            console.error('Login button not found');
        }
        
        const registerBtn = document.getElementById('registerBtn');
        if (registerBtn) {
            registerBtn.addEventListener('click', () => showModal('registerModal'));
            console.log('Register button event listener attached');
        } else {
            console.error('Register button not found');
        }
        
        // User menu
        const userBtn = document.getElementById('userBtn');
        if (userBtn) {
            userBtn.addEventListener('click', toggleUserMenu);
            console.log('User button event listener attached');
        }
        
        // Search button
        const searchBtn = document.getElementById('searchBtn');
        if (searchBtn) {
            searchBtn.addEventListener('click', searchPrograms);
            console.log('Search button event listener attached');
        } else {
            console.error('Search button not found');
        }
        
        // Navigation buttons
        const startSearchBtn = document.querySelector('button[onclick*="scrollToSection"]');
        if (startSearchBtn) {
            startSearchBtn.addEventListener('click', function(e) {
                e.preventDefault();
                scrollToSection('search');
            });
            console.log('Start search button event listener attached');
        }
        
        const browseUniBtn = document.querySelector('button[onclick*="scrollToSection"]');
        if (browseUniBtn) {
            browseUniBtn.addEventListener('click', function(e) {
                e.preventDefault();
                scrollToSection('universities');
            });
            console.log('Browse universities button event listener attached');
        }
        
        // Password change form
        const passwordChangeForm = document.getElementById('passwordChangeForm');
        if (passwordChangeForm) {
            passwordChangeForm.addEventListener('submit', handlePasswordChange);
            console.log('Password change form event listener attached');
        } else {
            console.error('Password change form not found');
        }
        
    }, 100);
}

// Load universities for filter dropdown
async function loadUniversitiesForFilter() {
    console.log('Loading universities for filter...');
    try {
        const response = await fetch(`${API_BASE_URL}/universities/`);
        console.log('Universities API response status:', response.status);
        
        const data = await response.json();
        console.log('Universities API response data:', data);
        
        const universities = data.results || data;
        console.log('Universities array:', universities);
        
        const universityFilter = document.getElementById('universityFilter');
        console.log('University filter element:', universityFilter);
        
        if (universityFilter) {
            universityFilter.innerHTML = '<option value="">All Universities</option>';
            universities.forEach(university => {
                const option = document.createElement('option');
                option.value = university.name;
                option.textContent = university.name;
                universityFilter.appendChild(option);
            });
            console.log('University filter loaded with', universities.length, 'universities');
        } else {
            console.error('University filter element not found');
        }
    } catch (error) {
        console.error('Error loading universities for filter:', error);
    }
}

// Load user data on page load
function loadUserData() {
    console.log('=== LOADING USER DATA ===');
    
    // Load current user
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        console.log('User loaded from localStorage:', currentUser);
    }
    
    // Load subscription data
    loadSubscriptionData();
    
    // Update UI
    updateUserInterface();
    updateUserSubscriptionDisplay();
    
    console.log('User data loaded and UI updated');
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
    console.log('=== LOADING UNIVERSITIES ===');
    try {
        const universities = await apiRequest('/universities/');
        console.log('Universities API response:', universities);
        allUniversities = universities.results || universities;
        console.log('Universities array:', allUniversities);
        displayedUniversities = Math.min(10, allUniversities.length);
        displayUniversities(allUniversities.slice(0, displayedUniversities));
        
        // Show "Show More" button if there are more universities
        if (allUniversities.length > 10) {
            const showMoreBtn = document.getElementById('showMoreUniversities');
            if (showMoreBtn) {
                showMoreBtn.classList.remove('hidden');
            }
        }
        console.log('Universities loaded successfully');
    } catch (error) {
        console.error('Error loading universities:', error);
    }
}

// Load programs
async function loadPrograms() {
    console.log('=== LOADING PROGRAMS ===');
    try {
        const programs = await apiRequest('/programs/');
        console.log('Programs API response:', programs);
        allPrograms = programs.results || programs;
        console.log('Programs array:', allPrograms);
        displayedPrograms = Math.min(10, allPrograms.length);
        displayPrograms(allPrograms.slice(0, displayedPrograms));
        
        // Show "Show More" button if there are more programs
        if (allPrograms.length > 10) {
            const showMoreBtn = document.getElementById('showMorePrograms');
            if (showMoreBtn) {
                showMoreBtn.classList.remove('hidden');
            }
        }
        console.log('Programs loaded successfully');
    } catch (error) {
        console.error('Error loading programs:', error);
    }
}

// Load countries
async function loadCountries() {
    console.log('=== LOADING COUNTRIES ===');
    try {
        const data = await apiRequest('/countries/');
        console.log('Countries API response:', data);
        const countries = data.results || data;
        console.log('Countries array:', countries);
        populateSelect('countryFilter', countries);
        console.log('Countries loaded successfully');
    } catch (error) {
        console.error('Error loading countries:', error);
    }
}

// Load fields of study
async function loadFieldsOfStudy() {
    console.log('=== LOADING FIELDS OF STUDY ===');
    try {
        const data = await apiRequest('/fields-of-study/');
        console.log('Fields API response:', data);
        const fields = data.results || data;
        console.log('Fields array:', fields);
        populateSelect('fieldFilter', fields);
        console.log('Fields loaded successfully');
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
    const container = document.getElementById('universitiesContainer');
    if (!container) return;
    container.innerHTML = '';
    
    universities.forEach(university => {
        const card = createUniversityCard(university);
        container.appendChild(card);
    });
}

// Display programs
function displayPrograms(programs) {
    const container = document.getElementById('programsContainer');
    if (!container) return;
    container.innerHTML = '';
    
    programs.forEach(program => {
        const card = createProgramCard(program);
        container.appendChild(card);
    });
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
    console.log('=== LOGIN ATTEMPT STARTED ===');
    
    const email = document.getElementById('loginEmail');
    const password = document.getElementById('loginPassword');
    
    if (!email || !password) {
        console.error('Login form elements not found');
        showNotification('Login form not found', 'error');
        return;
    }
    
    const emailValue = email.value;
    const passwordValue = password.value;
    
    if (!emailValue || !passwordValue) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    console.log('Login credentials:', { email: emailValue, passwordLength: passwordValue.length });
    console.log('API Base URL:', API_BASE_URL);
    
    try {
        const loginData = { 
            username: emailValue,
            email: emailValue,
            password: passwordValue
        };
        
        console.log('Sending login request:', loginData);
        
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });
        
        console.log('Login response status:', response.status);
        console.log('Login response headers:', response.headers);
        
        const data = await response.json();
        console.log('Login response data:', data);
        
        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('currentUser', JSON.stringify(data.user));
            localStorage.setItem('token', data.token || 'demo_token');
            closeModal('loginModal');
            
            console.log('Login successful, updating UI...');
            updateUserInterface();
            loadSubscriptionData();
            updateUserSubscriptionDisplay();
            showNotification('Login successful!', 'success');
            console.log('=== LOGIN SUCCESSFUL ===');
        } else {
            console.error('Login failed:', data);
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
    console.log('=== REGISTER ATTEMPT STARTED ===');
    
    const username = document.getElementById('registerUsername');
    const email = document.getElementById('registerEmail');
    const password = document.getElementById('registerPassword');
    
    if (!username || !email || !password) {
        console.error('Register form elements not found');
        showNotification('Register form not found', 'error');
        return;
    }
    
    const usernameValue = username.value;
    const emailValue = email.value;
    const passwordValue = password.value;
    
    if (!usernameValue || !emailValue || !passwordValue) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    console.log('Register data:', { username: usernameValue, email: emailValue, passwordLength: passwordValue.length });
    
    try {
        const registerData = {
            username: usernameValue,
            email: emailValue,
            password: passwordValue
        };
        
        console.log('Sending register request:', registerData);
        
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registerData)
        });
        
        console.log('Register response status:', response.status);
        const data = await response.json();
        console.log('Register response data:', data);
        
        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('currentUser', JSON.stringify(data.user));
            localStorage.setItem('token', data.token || 'demo_token');
            closeModal('registerModal');
            updateUserInterface();
            loadSubscriptionData();
            updateUserSubscriptionDisplay();
            showNotification('Registration successful!', 'success');
            console.log('=== REGISTRATION SUCCESSFUL ===');
        } else {
            console.error('Registration failed:', data);
            showNotification(data.error || 'Registration failed', 'error');
        }
        
    } catch (error) {
        console.error('Registration error:', error);
        showNotification('Registration failed. Please try again.', 'error');
    }
}

// Logout function
function logout() {
    console.log('=== LOGOUT STARTED ===');
    
    // Clear all user data
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('token');
    localStorage.removeItem('userSubscription');
    localStorage.removeItem('favoritePrograms');
    localStorage.removeItem('userSettings');
    
    // Reset global variables
    authToken = null;
    currentUser = null;
    userSubscription = {
        plan: 'free',
        emailsUsed: 0,
        emailsLimit: 0,
        searchesUsed: 0,
        searchesLimit: 'unlimited'
    };
    
    // Update UI
    updateUserInterface();
    updateUserSubscriptionDisplay();
    closeAllModals();
    
    // Show success message
    showNotification('Logged out successfully', 'success');
    console.log('=== LOGOUT COMPLETED ===');
}

// Close all modals
function closeAllModals() {
    const modals = ['loginModal', 'registerModal', 'userMenu', 'dashboardModal', 'passwordChangeModal'];
    modals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
        }
    });
}

// Update user interface
function updateUserInterface() {
    console.log('=== UPDATING USER INTERFACE ===');
    console.log('Current user:', currentUser);
    
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const userBtn = document.getElementById('userBtn');
    const userMenu = document.getElementById('userMenu'); // This is the container div
    const userName = document.getElementById('userName');
    
    console.log('Elements found:', {
        loginBtn: !!loginBtn,
        registerBtn: !!registerBtn,
        userBtn: !!userBtn,
        userMenu: !!userMenu,
        userName: !!userName
    });
    
    if (currentUser) {
        console.log('User is logged in, showing user menu');
        if (loginBtn) loginBtn.style.display = 'none';
        if (registerBtn) registerBtn.style.display = 'none';
        if (userMenu) userMenu.style.display = 'block'; // Show the container
        if (userName) userName.textContent = currentUser.username || 'User';
        console.log('User interface updated for logged in user');
    } else {
        console.log('No user logged in, showing login/register buttons');
        if (loginBtn) loginBtn.style.display = 'block';
        if (registerBtn) registerBtn.style.display = 'block';
        if (userMenu) userMenu.style.display = 'none'; // Hide the container
        console.log('User interface updated for guest user');
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
    console.log('=== TOGGLING USER MENU ===');
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        userDropdown.classList.toggle('hidden');
        console.log('User dropdown toggled');
    } else {
        console.error('User dropdown element not found');
    }
}

// Show notification
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notificationContainer');
    if (!container) return;

    const notification = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-green-500' : 
                   type === 'error' ? 'bg-red-500' : 
                   type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500';
    
    notification.className = `${bgColor} text-white px-6 py-4 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full`;
    notification.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 
                              type === 'error' ? 'fa-exclamation-circle' : 
                              type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle'} mr-3"></i>
                <span>${message}</span>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    container.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);

    // Auto remove
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, duration);
}

// View program details
function viewProgramDetails(programId) {
    console.log('=== VIEW PROGRAM DETAILS CALLED ===');
    console.log('Program ID:', programId);
    console.log('All programs:', allPrograms);
    console.log('Search results:', searchResults);
    
    // Store current program ID for favorites
    currentProgramId = programId;
    
    // Find program in allPrograms or searchResults
    let program = allPrograms.find(p => p.id === programId);
    console.log('Found in allPrograms:', program);
    
    if (!program) {
        program = searchResults.find(p => p.id === programId);
        console.log('Found in searchResults:', program);
    }
    
    if (!program) {
        console.error('Program not found with ID:', programId);
        showNotification('Program not found', 'error');
        return;
    }

    console.log('Found program:', program);

    // Check if modal elements exist
    const titleElement = document.getElementById('programDetailsTitle');
    const universityElement = document.getElementById('programDetailsUniversity');
    const locationElement = document.getElementById('programDetailsLocation');
    const contentElement = document.getElementById('programDetailsContent');
    const modalElement = document.getElementById('programDetailsModal');
    
    console.log('Modal elements:', {
        titleElement: !!titleElement,
        universityElement: !!universityElement,
        locationElement: !!locationElement,
        contentElement: !!contentElement,
        modalElement: !!modalElement
    });

    if (!titleElement || !universityElement || !locationElement || !contentElement || !modalElement) {
        console.error('Modal elements not found!');
        showNotification('Modal elements not found', 'error');
        return;
    }

    // Update modal title and header
    titleElement.textContent = program.name;
    universityElement.textContent = program.university?.name || 'Unknown University';
    locationElement.textContent = `${program.university?.city || 'Unknown City'}, ${program.university?.country || 'Unknown Country'}`;

    console.log('Updated modal header');

    // Create detailed content
    contentElement.innerHTML = `
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="space-y-4">
                <div class="bg-gray-50 rounded-lg p-4">
                    <h4 class="font-semibold text-gray-900 mb-2">
                        <i class="fas fa-graduation-cap text-indigo-600 mr-2"></i>Program Information
                    </h4>
                    <p class="text-gray-700"><strong>Field:</strong> ${program.field_of_study || 'Not specified'}</p>
                    <p class="text-gray-700"><strong>Degree Level:</strong> ${program.degree_level || 'Not specified'}</p>
                    <p class="text-gray-700"><strong>Language:</strong> ${program.language || 'Not specified'}</p>
                    <p class="text-gray-700"><strong>Duration:</strong> ${program.duration_months ? program.duration_months + ' months' : 'Not specified'}</p>
                </div>
                
                <div class="bg-gray-50 rounded-lg p-4">
                    <h4 class="font-semibold text-gray-900 mb-2">
                        <i class="fas fa-university text-indigo-600 mr-2"></i>University Information
                    </h4>
                    <p class="text-gray-700"><strong>Name:</strong> ${program.university?.name || 'Not specified'}</p>
                    <p class="text-gray-700"><strong>Location:</strong> ${program.university?.city || 'Unknown'}, ${program.university?.country || 'Unknown'}</p>
                    <p class="text-gray-700"><strong>Website:</strong> 
                        <a href="${program.university?.website || '#'}" target="_blank" class="text-indigo-600 hover:text-indigo-800">
                            ${program.university?.website || 'Not available'}
                        </a>
                    </p>
                </div>
            </div>
            
            <div class="space-y-4">
                <div class="bg-gray-50 rounded-lg p-4">
                    <h4 class="font-semibold text-gray-900 mb-2">
                        <i class="fas fa-info-circle text-indigo-600 mr-2"></i>Description
                    </h4>
                    <p class="text-gray-700">${program.description || 'No description available.'}</p>
                </div>
                
                <div class="bg-gray-50 rounded-lg p-4">
                    <h4 class="font-semibold text-gray-900 mb-2">
                        <i class="fas fa-calendar text-indigo-600 mr-2"></i>Application Details
                    </h4>
                    <p class="text-gray-700"><strong>Application Deadline:</strong> ${program.application_deadline || 'Not specified'}</p>
                    <p class="text-gray-700"><strong>Start Date:</strong> ${program.start_date || 'Not specified'}</p>
                    <p class="text-gray-700"><strong>Tuition Fee:</strong> ${program.tuition_fee_euro ? '€' + program.tuition_fee_euro : 'Not specified'}</p>
                </div>
            </div>
        </div>
    `;

    console.log('Updated modal content');

    // Load email suggestions
    loadEmailSuggestions(programId);

    // Show modal
    modalElement.classList.remove('hidden');
    console.log('Modal should be visible now');
}

// Load email suggestions for a program
async function loadEmailSuggestions(programId) {
    console.log('Loading email suggestions for program:', programId);
    
    // Check if user has subscription to access email features
    if (!currentUser) {
        const suggestionsContainer = document.getElementById('emailSuggestions');
        if (suggestionsContainer) {
            suggestionsContainer.innerHTML = `
                <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
                    <i class="fas fa-lock text-yellow-600 text-2xl mb-3"></i>
                    <h3 class="text-lg font-semibold text-yellow-800 mb-2">Login Required</h3>
                    <p class="text-yellow-700 mb-4">Please login to view coordinator contact information.</p>
                    <button onclick="showLoginModal()" class="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                        <i class="fas fa-sign-in-alt mr-2"></i>Login
                    </button>
                </div>
            `;
        }
        return;
    }
    
    // Check subscription plan
    const subscription = userSubscription || { plan: 'free' };
    if (subscription.plan === 'free') {
        const suggestionsContainer = document.getElementById('emailSuggestions');
        if (suggestionsContainer) {
            suggestionsContainer.innerHTML = `
                <div class="bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-lg p-6 text-center">
                    <i class="fas fa-crown text-purple-600 text-3xl mb-4"></i>
                    <h3 class="text-xl font-semibold text-purple-800 mb-2">Premium Feature</h3>
                    <p class="text-purple-700 mb-4">Email coordinators directly is a premium feature. Upgrade to Premium or Pro to access coordinator contact information and send emails.</p>
                    <div class="space-y-3">
                        <div class="flex justify-center space-x-4">
                            <button onclick="subscribeToPlan('premium')" class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                                <i class="fas fa-star mr-2"></i>Upgrade to Premium
                            </button>
                            <button onclick="subscribeToPlan('pro')" class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
                                <i class="fas fa-crown mr-2"></i>Upgrade to Pro
                            </button>
                        </div>
                        <p class="text-sm text-purple-600">
                            <i class="fas fa-envelope mr-1"></i>Premium: 50 emails/month | Pro: 200 emails/month
                        </p>
                    </div>
                </div>
            `;
        }
        return;
    }
    
    try {
        // First, let's get the program to find its program_id
        let program = allPrograms.find(p => p.id === programId);
        if (!program) {
            program = searchResults.find(p => p.id === programId);
        }
        
        if (!program) {
            console.error('Program not found for coordinator loading');
            return;
        }
        
        console.log('Found program for coordinators:', program);
        console.log('Program ID:', program.program_id);
        
        // Use the program_id to filter coordinators
        const data = await apiRequest(`/coordinators/?program_id=${program.program_id}`);
        console.log('Coordinators API response:', data);
        
        const coordinators = data.results || data;
        console.log('Filtered coordinators:', coordinators);
        
        const suggestionsContainer = document.getElementById('emailSuggestions');
        if (!suggestionsContainer) {
            console.log('Email suggestions container not found');
            return;
        }
        
        if (coordinators.length === 0) {
            suggestionsContainer.innerHTML = `
                <div class="text-gray-500 text-center py-4">
                    <i class="fas fa-info-circle mr-2"></i>
                    No coordinators available for this program.
                </div>
            `;
            return;
        }
        
        // Show coordinator info with email access for subscribed users
        suggestionsContainer.innerHTML = `
            <div class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                <div class="flex items-center">
                    <i class="fas fa-check-circle text-green-600 mr-2"></i>
                    <span class="text-green-800 font-medium">${subscription.plan.charAt(0).toUpperCase() + subscription.plan.slice(1)} Plan Active</span>
                    <span class="ml-2 text-sm text-green-600">
                        ${subscription.plan === 'premium' ? '50 emails/month' : '200 emails/month'}
                    </span>
                </div>
            </div>
            ${coordinators.map(coordinator => `
                <div class="bg-white rounded-lg p-4 border border-gray-200">
                    <div class="flex items-center justify-between">
                        <div>
                            <h5 class="font-semibold text-gray-900">${coordinator.name || 'Unknown Name'}</h5>
                            <p class="text-sm text-gray-600">${coordinator.role || 'Coordinator'}</p>
                            <p class="text-sm text-indigo-600">${coordinator.email || 'No email available'}</p>
                        </div>
                        <button onclick="sendEmailToCoordinator('${coordinator.email || ''}', '${coordinator.name || 'Unknown'}')" 
                                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                                ${!coordinator.email ? 'disabled' : ''}>
                            <i class="fas fa-envelope mr-2"></i>Email
                        </button>
                    </div>
                </div>
            `).join('')}
        `;
        
        console.log('Email suggestions loaded successfully for program:', programId);
        
    } catch (error) {
        console.error('Error loading email suggestions:', error);
        const suggestionsContainer = document.getElementById('emailSuggestions');
        if (suggestionsContainer) {
            suggestionsContainer.innerHTML = `
                <div class="text-red-500 text-center py-4">
                    <i class="fas fa-exclamation-triangle mr-2"></i>
                    Error loading coordinators.
                </div>
            `;
        }
    }
}

// Show email modal
function showEmailModal() {
    console.log('Showing email modal');
    
    // Check if user is logged in
    if (!currentUser) {
        showNotification('Please login to send emails', 'error');
        showLoginModal();
        return;
    }
    
    // Check subscription plan
    const subscription = userSubscription || { plan: 'free' };
    if (subscription.plan === 'free') {
        showNotification('Email sending is a premium feature. Please upgrade to Premium or Pro plan.', 'error');
        showSubscriptionDashboard();
        return;
    }
    
    const modal = document.getElementById('emailModal');
    if (modal) {
        modal.classList.remove('hidden');
        console.log('Email modal is now visible');
        
        // Update email usage info when modal is shown
        updateEmailUsageInfo();
    } else {
        console.error('Email modal not found');
        showNotification('Email modal not found', 'error');
    }
}

// Close email modal
function closeEmailModal() {
    console.log('Closing email modal');
    const modal = document.getElementById('emailModal');
    if (modal) {
        modal.classList.add('hidden');
        console.log('Email modal is now hidden');
    } else {
        console.error('Email modal not found');
    }
}

// Update email usage info
function updateEmailUsageInfo() {
    console.log('Updating email usage info');
    const emailUsageElement = document.getElementById('emailUsageInfo');
    if (!emailUsageElement) {
        console.log('Email usage element not found');
        return;
    }
    
    // Get user subscription info
    const subscription = userSubscription || { plan: 'free', emailsUsed: 0, emailsLimit: 0 };
    
    let message = '';
    let remainingEmails = 0;
    
    switch (subscription.plan) {
        case 'free':
            message = 'Free users cannot send emails. Upgrade to Premium or Pro to send emails.';
            break;
        case 'premium':
            remainingEmails = Math.max(0, 50 - (subscription.emailsUsed || 0));
            message = `You have ${remainingEmails} emails remaining this month (Premium Plan: 50 emails/month)`;
            break;
        case 'pro':
            remainingEmails = Math.max(0, 200 - (subscription.emailsUsed || 0));
            message = `You have ${remainingEmails} emails remaining this month (Pro Plan: 200 emails/month)`;
            break;
        default:
            message = 'Please select a subscription plan to send emails.';
    }
    
    emailUsageElement.textContent = message;
    console.log('Email usage info updated:', message);
}

// Load email template
function loadEmailTemplate(templateType) {
    console.log('Loading email template:', templateType);
    
    const emailBody = document.getElementById('emailBody');
    if (!emailBody) {
        console.error('Email body field not found');
        showNotification('Email body field not found', 'error');
        return;
    }
    
    let template = '';
    
    switch (templateType) {
        case 'inquiry':
            template = `Dear Professor,

I hope this email finds you well. I am writing to inquire about the [Program Name] program at [University Name].

I am very interested in pursuing my master's degree in this field and would like to learn more about:
- Program requirements and application process
- Course curriculum and structure
- Research opportunities
- Career prospects after graduation

I would greatly appreciate any information you could provide about the program and the application process.

Thank you for your time and consideration.

Best regards,
[Your Name]`;
            break;
            
        case 'admission':
            template = `Dear Admissions Committee,

I am writing to inquire about the admission requirements for the [Program Name] program at [University Name].

I am particularly interested in understanding:
- Academic requirements and prerequisites
- Application deadlines
- Required documents
- English language proficiency requirements
- Tuition fees and payment options

I have completed my bachelor's degree in [Your Field] and am eager to continue my studies at your prestigious institution.

Could you please provide me with detailed information about the admission process?

Thank you for your assistance.

Sincerely,
[Your Name]`;
            break;
            
        case 'scholarship':
            template = `Dear Scholarship Committee,

I hope this message finds you well. I am writing to inquire about scholarship opportunities for international students in the [Program Name] program at [University Name].

I am very interested in pursuing my master's degree at your institution, but I would like to explore available financial aid options, including:
- Merit-based scholarships
- Need-based financial aid
- Research assistantships
- Teaching assistantships
- External funding opportunities

I am committed to academic excellence and would be grateful for any information about scholarship programs that might be available to me.

Thank you for considering my inquiry.

Best regards,
[Your Name]`;
            break;
            
        default:
            template = 'Please select a template type.';
    }
    
    emailBody.value = template;
    console.log('Email template loaded successfully');
    showNotification('Email template loaded', 'success');
}

// Send email to specific coordinator
function sendEmailToCoordinator(email, name) {
    console.log('Sending email to coordinator:', email, name);
    
    // Check if user is logged in
    if (!currentUser) {
        showNotification('Please login to send emails', 'error');
        showLoginModal();
        return;
    }
    
    // Check subscription plan
    const subscription = userSubscription || { plan: 'free' };
    if (subscription.plan === 'free') {
        showNotification('Email sending is a premium feature. Please upgrade to Premium or Pro plan.', 'error');
        showSubscriptionDashboard();
        return;
    }
    
    // Check email limits for subscribed users
    const emailsUsed = subscription.emailsUsed || 0;
    const emailLimit = subscription.plan === 'premium' ? 50 : 200;
    
    if (emailsUsed >= emailLimit) {
        showNotification(`You have reached your monthly email limit (${emailLimit} emails). Please upgrade your plan or wait for next month.`, 'error');
        showSubscriptionDashboard();
        return;
    }
    
    // Update coordinator details in the modal
    const coordinatorDetails = document.getElementById('coordinatorDetails');
    if (coordinatorDetails) {
        coordinatorDetails.innerHTML = `
            <p><strong>Name:</strong> ${name}</p>
            <p><strong>Email:</strong> ${email || 'No email available'}</p>
        `;
    }
    
    // Set the coordinator email in the email form
    const emailForm = document.getElementById('emailForm');
    if (emailForm) {
        const recipientField = emailForm.querySelector('input[name="recipient"]');
        if (recipientField) {
            recipientField.value = email || '';
        }
        const subjectField = emailForm.querySelector('input[name="subject"]');
        if (subjectField) {
            subjectField.value = `Inquiry about Master's Program - ${name}`;
        }
    }
    
    // Show email modal
    showEmailModal();
}

// Close program details modal
function closeProgramDetails() {
    const modal = document.getElementById('programDetailsModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Email coordinator function
function emailCoordinator(programId) {
    console.log('Email coordinator for program:', programId);
    
    // Check if user has subscription
    if (!currentUser) {
        showNotification('Please login to email coordinators', 'error');
        return;
    }
    
    if (userSubscription.plan === 'free') {
        showNotification('Email functionality requires Premium or Pro subscription', 'error');
        showSubscriptionPlans();
        return;
    }
    
    // Check email limits
    if (userSubscription.emailsUsed >= userSubscription.emailLimit) {
        showNotification('Email limit reached for this month', 'error');
        return;
    }
    
    // Show email composition modal
    showEmailCompositionModal(programId);
}

// Show subscription plans
function showSubscriptionPlans() {
    const subscriptionSection = document.getElementById('subscription');
    if (subscriptionSection) {
        subscriptionSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Subscribe to plan
async function subscribeToPlan(planType) {
    console.log('=== SUBSCRIPTION ATTEMPT STARTED ===');
    console.log('Plan type:', planType);
    
    if (!currentUser) {
        showNotification('Please login to subscribe', 'error');
        return;
    }
    
    if (planType === 'free') {
        // Free plan - just update locally
        userSubscription = {
            plan: 'free',
            status: 'active',
            emailsUsed: 0,
            emailLimit: 0,
            startDate: new Date().toISOString(),
            endDate: null
        };
        saveSubscriptionData();
        updateUserSubscriptionDisplay();
        showNotification('Switched to Free plan', 'success');
        console.log('=== FREE PLAN ACTIVATED ===');
        return;
    }
    
    // For paid plans, simulate subscription (in real app, integrate with Stripe)
    try {
        console.log('Processing subscription for plan:', planType);
        
        // For demo purposes, simulate successful subscription without API call
        console.log('Simulating subscription success for demo...');
        
        // Simulate successful subscription
        if (planType === 'premium') {
            userSubscription = {
                plan: 'premium',
                status: 'active',
                emailsUsed: 0,
                emailLimit: 50,
                startDate: new Date().toISOString(),
                endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString() // 30 days
            };
        } else if (planType === 'pro') {
            userSubscription = {
                plan: 'pro',
                status: 'active',
                emailsUsed: 0,
                emailLimit: 200,
                startDate: new Date().toISOString(),
                endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString() // 30 days
            };
        }
        
        saveSubscriptionData();
        updateUserSubscriptionDisplay();
        showNotification(`${planType.charAt(0).toUpperCase() + planType.slice(1)} subscription activated!`, 'success');
        console.log('=== SUBSCRIPTION SUCCESSFUL ===');
        
    } catch (error) {
        console.error('Subscription error:', error);
        showNotification('Subscription failed. Please try again.', 'error');
    }
}

// Show email composition modal
function showEmailCompositionModal(programId) {
    const program = allPrograms.find(p => p.id === programId) || searchResults.find(p => p.id === programId);
    if (!program) {
        showNotification('Program not found', 'error');
        return;
    }
    
    const modalHTML = `
        <div id="emailCompositionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                <div class="flex justify-between items-start mb-6">
                    <h2 class="text-2xl font-bold text-gray-900">Email Coordinator</h2>
                    <button onclick="closeEmailCompositionModal()" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
                </div>
                
                <div class="space-y-4">
                    <div>
                        <h3 class="text-lg font-semibold text-indigo-600 mb-2">Program Information</h3>
                        <p class="text-gray-700"><strong>Program:</strong> ${program.name}</p>
                        <p class="text-gray-700"><strong>University:</strong> ${program.university ? program.university.name : 'Unknown'}</p>
                        <p class="text-gray-700"><strong>Field:</strong> ${program.field_of_study}</p>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
                        <input type="text" id="emailSubject" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500" 
                               value="Inquiry about ${program.name} - ${program.university ? program.university.name : 'University'}">
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Message</label>
                        <textarea id="emailMessage" rows="8" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500">Dear Coordinator,

I am writing to inquire about the ${program.name} program at ${program.university ? program.university.name : 'your university'}.

I am very interested in this program and would like to know more about:
- Application requirements and deadlines
- Program structure and curriculum
- Admission process
- Any specific prerequisites

I would appreciate any information you can provide about this program.

Thank you for your time and consideration.

Best regards,
[Your Name]</textarea>
                    </div>
                    
                    <div class="flex justify-between items-center pt-4 border-t">
                        <div class="text-sm text-gray-500">
                            <span>Emails used this month: ${userSubscription.emailsUsed}/${userSubscription.emailLimit}</span>
                        </div>
                        <div class="space-x-2">
                            <button onclick="closeEmailCompositionModal()" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">Cancel</button>
                            <button onclick="sendEmailToCoordinator(${programId})" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">Send Email</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Close email composition modal
function closeEmailCompositionModal() {
    const modal = document.getElementById('emailCompositionModal');
    if (modal) {
        modal.remove();
    }
}

// Dashboard Functions
function showDashboard() {
    console.log('=== SHOWING DASHBOARD ===');
    
    if (!currentUser) {
        showNotification('Please login to access dashboard', 'error');
        return;
    }
    
    // Populate dashboard data
    document.getElementById('dashboardUsername').textContent = currentUser.username || 'N/A';
    document.getElementById('dashboardEmail').textContent = currentUser.email || 'N/A';
    document.getElementById('dashboardMemberSince').textContent = currentUser.date_joined ? new Date(currentUser.date_joined).toLocaleDateString() : 'N/A';
    
    // Update subscription info
    document.getElementById('dashboardPlan').textContent = userSubscription.plan.charAt(0).toUpperCase() + userSubscription.plan.slice(1);
    document.getElementById('dashboardEmailsUsed').textContent = `${userSubscription.emailsUsed} / ${userSubscription.emailLimit}`;
    document.getElementById('dashboardStatus').textContent = userSubscription.status.charAt(0).toUpperCase() + userSubscription.status.slice(1);
    
    // Show modal
    const modal = document.getElementById('dashboardModal');
    modal.classList.remove('hidden');
    
    // Close user dropdown
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        userDropdown.classList.add('hidden');
    }
}

function closeDashboard() {
    const modal = document.getElementById('dashboardModal');
    modal.classList.add('hidden');
}

// Password Change Functions
function showPasswordChange() {
    console.log('=== SHOWING PASSWORD CHANGE ===');
    
    if (!currentUser) {
        showNotification('Please login to change password', 'error');
        return;
    }
    
    // Clear form
    document.getElementById('currentPassword').value = '';
    document.getElementById('newPassword').value = '';
    document.getElementById('confirmNewPassword').value = '';
    
    // Show modal
    const modal = document.getElementById('passwordChangeModal');
    modal.classList.remove('hidden');
    
    // Close other modals
    closeDashboard();
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        userDropdown.classList.add('hidden');
    }
}

function closePasswordChange() {
    const modal = document.getElementById('passwordChangeModal');
    modal.classList.add('hidden');
}

// Handle password change form submission
async function handlePasswordChange(e) {
    e.preventDefault();
    console.log('=== PASSWORD CHANGE ATTEMPT ===');
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmNewPassword = document.getElementById('confirmNewPassword').value;
    
    if (!currentPassword || !newPassword || !confirmNewPassword) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    if (newPassword !== confirmNewPassword) {
        showNotification('New passwords do not match', 'error');
        return;
    }
    
    if (newPassword.length < 6) {
        showNotification('New password must be at least 6 characters', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/change-password/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword,
                username: currentUser.username
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Password changed successfully!', 'success');
            closePasswordChange();
            console.log('=== PASSWORD CHANGE SUCCESSFUL ===');
        } else {
            console.error('Password change failed:', data);
            showNotification(data.error || 'Password change failed', 'error');
        }
        
    } catch (error) {
        console.error('Password change error:', error);
        showNotification('Password change failed. Please try again.', 'error');
    }
}

// Favorites Functions
let favoritePrograms = [];

// Load favorites from localStorage
function loadFavorites() {
    const savedFavorites = localStorage.getItem('favoritePrograms');
    if (savedFavorites) {
        favoritePrograms = JSON.parse(savedFavorites);
    }
}

// Save favorites to localStorage
function saveFavorites() {
    localStorage.setItem('favoritePrograms', JSON.stringify(favoritePrograms));
}

// Add program to favorites
function addToFavorites() {
    console.log('=== ADDING TO FAVORITES ===', currentProgramId);
    
    if (!currentUser) {
        showNotification('Please login to add favorites', 'error');
        return;
    }
    
    if (!currentProgramId) {
        console.error('No program ID available');
        showNotification('No program selected', 'error');
        return;
    }
    
    const program = allPrograms.find(p => p.id === currentProgramId) || searchResults.find(p => p.id === currentProgramId);
    if (!program) {
        console.error('Program not found with ID:', currentProgramId);
        showNotification('Program not found', 'error');
        return;
    }
    
    // Check if already in favorites
    if (favoritePrograms.find(fav => fav.id === currentProgramId)) {
        showNotification('Program already in favorites', 'info');
        return;
    }
    
    // Add to favorites
    favoritePrograms.push({
        id: program.id,
        name: program.name,
        university: program.university ? program.university.name : 'Unknown',
        field_of_study: program.field_of_study,
        degree_level: program.degree_level,
        added_date: new Date().toISOString()
    });
    
    saveFavorites();
    showNotification('Added to favorites!', 'success');
    console.log('=== PROGRAM ADDED TO FAVORITES ===');
}

// Remove program from favorites
function removeFromFavorites(programId) {
    console.log('=== REMOVING FROM FAVORITES ===', programId);
    
    favoritePrograms = favoritePrograms.filter(fav => fav.id !== programId);
    saveFavorites();
    showNotification('Removed from favorites', 'success');
    
    // Refresh favorites display if modal is open
    if (!document.getElementById('favoritesModal').classList.contains('hidden')) {
        showFavorites();
    }
}

// Show favorites modal
function showFavorites() {
    console.log('=== SHOWING FAVORITES ===');
    
    if (!currentUser) {
        showNotification('Please login to view favorites', 'error');
        return;
    }
    
    loadFavorites();
    
    const favoritesList = document.getElementById('favoritesList');
    favoritesList.innerHTML = '';
    
    if (favoritePrograms.length === 0) {
        favoritesList.innerHTML = `
            <div class="col-span-full text-center py-8">
                <i class="fas fa-heart text-gray-400 text-4xl mb-4"></i>
                <p class="text-gray-500 text-lg">No favorite programs yet</p>
                <p class="text-gray-400 text-sm">Start exploring programs and add them to your favorites!</p>
            </div>
        `;
    } else {
        favoritePrograms.forEach(fav => {
            const favoriteCard = document.createElement('div');
            favoriteCard.className = 'bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow';
            favoriteCard.innerHTML = `
                <div class="mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">${fav.name}</h3>
                    <p class="text-indigo-600 font-medium">${fav.university}</p>
                    <p class="text-gray-600 text-sm">${fav.field_of_study}</p>
                </div>
                <div class="mb-4">
                    <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">${fav.degree_level}</span>
                </div>
                <div class="flex justify-between items-center">
                    <div class="text-sm text-gray-500">
                        <span>Added ${new Date(fav.added_date).toLocaleDateString()}</span>
                    </div>
                    <div class="space-x-2">
                        <button onclick="viewProgramDetails(${fav.id})" class="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
                            View Details
                        </button>
                        <button onclick="removeFromFavorites(${fav.id})" class="text-red-600 hover:text-red-700 text-sm font-medium">
                            Remove
                        </button>
                    </div>
                </div>
            `;
            favoritesList.appendChild(favoriteCard);
        });
    }
    
    // Show modal
    const modal = document.getElementById('favoritesModal');
    modal.classList.remove('hidden');
    
    // Close other modals
    closeDashboard();
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        userDropdown.classList.add('hidden');
    }
}

function closeFavorites() {
    const modal = document.getElementById('favoritesModal');
    modal.classList.add('hidden');
}

// Simple navigation functions
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Simple search function
async function searchPrograms() {
    console.log('Search function called');
    
    const country = document.getElementById('countryFilter');
    const field = document.getElementById('fieldFilter');
    const university = document.getElementById('universityFilter');
    const degreeLevel = document.getElementById('degreeLevelFilter');
    const language = document.getElementById('languageFilter');
    
    if (!country || !field || !university) {
        console.error('Filter elements not found');
        showNotification('Search filters not found', 'error');
        return;
    }
    
    const countryValue = country.value;
    const fieldValue = field.value;
    const universityValue = university.value;
    const degreeLevelValue = degreeLevel ? degreeLevel.value : '';
    const languageValue = language ? language.value : '';
    
    console.log('Search filters:', { 
        country: countryValue, 
        field: fieldValue, 
        university: universityValue,
        degreeLevel: degreeLevelValue,
        language: languageValue
    });
    
    try {
        const params = new URLSearchParams();
        if (countryValue && countryValue !== 'all') params.append('country', countryValue);
        if (fieldValue && fieldValue !== 'all') params.append('field_of_study', fieldValue);
        if (universityValue && universityValue !== 'all') params.append('university', universityValue);
        if (degreeLevelValue && degreeLevelValue !== 'all') params.append('degree_level', degreeLevelValue);
        if (languageValue && languageValue !== 'all') params.append('language', languageValue);
        
        const url = `${API_BASE_URL}/search/?${params.toString()}`;
        console.log('Search URL:', url);
        
        const response = await fetch(url);
        console.log('Search response status:', response.status);
        console.log('Search response ok:', response.ok);
        
        if (!response.ok) {
            console.error('Search API error:', response.status, response.statusText);
            showNotification(`Search API error: ${response.status}`, 'error');
            return;
        }
        
        const data = await response.json();
        console.log('Search response data:', data);
        console.log('Search results count:', data.count || data.length || (data.results ? data.results.length : 0));
        
        // Handle different response formats
        let results = [];
        if (data.programs) {
            results = data.programs;
        } else if (data.results) {
            results = data.results;
        } else if (Array.isArray(data)) {
            results = data;
        }
        
        console.log('Final results array:', results);
        searchResults = results; // Store results globally for favorites
        displaySearchResults(results);
        
        // Scroll to search results section
        scrollToSection('search-results');
        
    } catch (error) {
        console.error('Error searching programs:', error);
        showNotification('Error searching programs. Please try again.', 'error');
    }
}

function displaySearchResults(results) {
    const resultsSection = document.getElementById('searchResults');
    const container = document.getElementById('resultsContainer');
    
    if (!resultsSection || !container) return;
    
    resultsSection.classList.remove('hidden');
    container.innerHTML = '';
    
    if (results && results.length > 0) {
        results.forEach(program => {
            const card = createProgramCard(program);
            container.appendChild(card);
        });
    } else {
        container.innerHTML = '<p class="text-center text-gray-500 py-8">No programs found matching your criteria.</p>';
    }
}

// Show more functions
function showMoreUniversities() {
    displayedUniversities = Math.min(displayedUniversities + 10, allUniversities.length);
    displayUniversities(allUniversities.slice(0, displayedUniversities));
    
    if (displayedUniversities >= allUniversities.length) {
        const showMoreBtn = document.getElementById('showMoreUniversities');
        if (showMoreBtn) {
            showMoreBtn.classList.add('hidden');
        }
    }
}

function showMorePrograms() {
    displayedPrograms = Math.min(displayedPrograms + 10, allPrograms.length);
    displayPrograms(allPrograms.slice(0, displayedPrograms));
    
    if (displayedPrograms >= allPrograms.length) {
        const showMoreBtn = document.getElementById('showMorePrograms');
        if (showMoreBtn) {
            showMoreBtn.classList.add('hidden');
        }
    }
}

console.log('UniWorld app.js loaded successfully!');