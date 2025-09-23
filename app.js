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
let selectedPrograms = []; // Store selected programs for bulk email

// Email integration
let emailAccounts = {
    gmail: { connected: false, email: '', accessToken: '' },
    outlook: { connected: false, email: '', accessToken: '' }
};
let emailSettings = {
    defaultProvider: 'gmail',
    signature: ''
};

// Subscription management
let userSubscription = {
    plan: 'free',
    emailsUsed: 0,
    emailsLimit: 0,
    searchesUsed: 0,
    searchesLimit: 'unlimited'
};

// Pagination variables
let currentPage = 1;
let resultsPerPage = 10;
let allSearchResults = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadUserData();
    setupEventListeners();
    loadInitialData();
    
    // Add event listener for profile form submission
    const profileForm = document.getElementById('userProfileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', saveUserProfile);
    }
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
        
        // Bulk email form
        const bulkEmailForm = document.getElementById('bulkEmailForm');
        if (bulkEmailForm) {
            bulkEmailForm.addEventListener('submit', handleBulkEmailSubmit);
            console.log('Bulk email form event listener attached');
        } else {
            console.error('Bulk email form not found');
        }
        
        // Email form
        const emailForm = document.getElementById('emailForm');
        if (emailForm) {
            emailForm.addEventListener('submit', handleEmailSubmit);
            console.log('Email form event listener attached');
        } else {
            console.error('Email form not found');
        }
        
        // Email type change listener for automatic AI generation
        const bulkEmailType = document.getElementById('bulkEmailType');
        if (bulkEmailType) {
            bulkEmailType.addEventListener('change', function() {
                // Add a small delay to ensure the value is updated
                setTimeout(() => {
                    generateEmailTypeBasedAI();
                }, 100);
            });
            console.log('Email type change listener attached');
        } else {
            console.error('Bulk email type dropdown not found');
        }
        
        // Email type change listener for coordinator email modal
        const emailType = document.getElementById('emailType');
        if (emailType) {
            emailType.addEventListener('change', function() {
                // Add a small delay to ensure the value is updated
                setTimeout(() => {
                    generateCoordinatorEmailTypeBasedAI();
                }, 100);
            });
            console.log('Coordinator email type change listener attached');
        } else {
            console.error('Coordinator email type dropdown not found');
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
        credentials: 'include', // Include cookies for session authentication
        ...options
    };
    
    // Remove JWT token authentication since we're using session auth
    // const token = localStorage.getItem('token');
    // if (token) {
    //     config.headers.Authorization = `Bearer ${token}`;
    // }
    
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
    card.className = 'bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow relative';
    
    // Check if program is in favorites
    const isFavorite = favoritePrograms.find(fav => fav.id === program.id);
    const heartIcon = isFavorite ? 'fas fa-heart text-red-500' : 'far fa-heart text-gray-400';
    const heartTitle = isFavorite ? 'Remove from favorites' : 'Add to favorites';
    
    card.innerHTML = `
        <div class="absolute top-4 right-4 flex items-center space-x-2">
            <button onclick="toggleFavorite(${program.id})" 
                    class="heart-button p-1 hover:bg-gray-100 rounded-full transition-colors" 
                    title="${heartTitle}">
                <i class="${heartIcon} text-lg"></i>
            </button>
            <input type="checkbox" 
                   id="program-${program.id}" 
                   class="program-checkbox w-4 h-4 text-indigo-600 bg-gray-100 border-gray-300 rounded focus:ring-indigo-500 focus:ring-2"
                   onchange="toggleProgramSelection(${program.id})">
        </div>
        <div class="mb-4 pr-16">
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
            credentials: 'include', // Include cookies for session authentication
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
            credentials: 'include', // Include cookies for session authentication
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

// Show login modal
function showLoginModal() {
    showModal('loginModal');
}

// Show register modal
function showRegisterModal() {
    showModal('registerModal');
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
        
        // Set global AI variables for the first coordinator
        if (coordinators.length > 0) {
            currentProgramForAI = programId;
            currentCoordinatorForAI = coordinators[0].id;
            console.log('AI variables set in loadEmailSuggestions:', { currentProgramForAI, currentCoordinatorForAI });
        }
        
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
function showEmailModal(programId = null) {
    console.log('Showing email modal for program:', programId);
    
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
    
    // If programId is provided, populate coordinator details
    if (programId) {
        populateCoordinatorDetails(programId);
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

// Populate coordinator details in the email modal
async function populateCoordinatorDetails(programId) {
    try {
        console.log('Populating coordinator details for program:', programId);
        
        // Find the program
        const program = allPrograms.find(p => p.id === programId) || searchResults.find(p => p.id === programId);
        if (!program) {
            console.error('Program not found for ID:', programId);
            return;
        }
        
        // Fetch coordinators for this program
        const data = await apiRequest(`/coordinators/?program_id=${program.program_id}`);
        const coordinators = data.results || data;
        
        if (coordinators.length > 0) {
            const coordinator = coordinators[0];
            const coordinatorDetails = document.getElementById('coordinatorDetails');
            
            if (coordinatorDetails) {
                coordinatorDetails.innerHTML = `
                    <p><strong>Name:</strong> ${coordinator.name || 'Unknown'}</p>
                    <p><strong>Email:</strong> ${coordinator.email || 'No email available'}</p>
                    <p><strong>Program:</strong> ${program.name}</p>
                    <p><strong>University:</strong> ${program.university ? program.university.name : 'Unknown'}</p>
                `;
                console.log('Coordinator details populated:', coordinator);
            }
        } else {
            console.log('No coordinators found for program:', programId);
            const coordinatorDetails = document.getElementById('coordinatorDetails');
            if (coordinatorDetails) {
                coordinatorDetails.innerHTML = `
                    <p><strong>Program:</strong> ${program.name}</p>
                    <p><strong>University:</strong> ${program.university ? program.university.name : 'Unknown'}</p>
                    <p><strong>Email:</strong> No coordinator email available</p>
                `;
            }
        }
        
        // Store the current program ID for email sending
        currentProgramId = programId;
        
    } catch (error) {
        console.error('Error populating coordinator details:', error);
        const coordinatorDetails = document.getElementById('coordinatorDetails');
        if (coordinatorDetails) {
            coordinatorDetails.innerHTML = '<p>Error loading coordinator information</p>';
        }
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

// Get coordinators for a program
async function getCoordinatorsForProgram(programId) {
    try {
        const response = await fetch(`/api/coordinators/?program_id=${programId}`);
        const data = await response.json();
        return data.coordinators || [];
    } catch (error) {
        console.error('Error fetching coordinators:', error);
        return [];
    }
}

// Send email from composition modal
async function sendEmailFromComposition(programId) {
    console.log('Sending email from composition modal for program:', programId);
    
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
    
    // Get form data
    const subject = document.getElementById('emailSubject')?.value;
    const body = document.getElementById('emailBody')?.value;
    
    if (!subject || !body) {
        showNotification('Please fill in both subject and message', 'error');
        return;
    }
    
    try {
        // Show loading state
        const sendButton = document.querySelector('button[onclick*="sendEmailFromComposition"]');
        if (sendButton) {
            sendButton.disabled = true;
            sendButton.textContent = 'Sending...';
        }
        
        // Get coordinator email from the program
        const coordinators = await getCoordinatorsForProgram(programId);
        if (!coordinators || coordinators.length === 0) {
            showNotification('No coordinators found for this program', 'error');
            return;
        }
        
        const coordinatorEmail = coordinators[0].email;
        if (!coordinatorEmail) {
            showNotification('No coordinator email available', 'error');
            return;
        }
        
        // Send email via OAuth2
        console.log('Sending email via OAuth2:', { subject, body, coordinatorEmail });
        
        // Use the OAuth2 email sending function
        const success = sendEmailViaOAuth2(coordinatorEmail, subject, body);
        
        if (success) {
            // Update email usage
            if (userSubscription) {
                userSubscription.emailsUsed = (userSubscription.emailsUsed || 0) + 1;
                saveSubscriptionData();
            }
            
            // Close the modal
            closeEmailCompositionModal();
            
            console.log('Email sent successfully via OAuth2');
        }
        
    } catch (error) {
        console.error('Error sending email:', error);
        showNotification('Failed to send email. Please try again.', 'error');
        
        // Re-enable button
        const sendButton = document.querySelector('button[onclick*="sendEmailFromComposition"]');
        if (sendButton) {
            sendButton.disabled = false;
            sendButton.textContent = 'Send Email';
        }
    }
}

// Send email to specific coordinator (old function - kept for compatibility)
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
async function showEmailCompositionModal(programId) {
    const program = allPrograms.find(p => p.id === programId) || searchResults.find(p => p.id === programId);
    if (!program) {
        showNotification('Program not found', 'error');
        return;
    }
    
    // Set global AI variables
    currentProgramForAI = programId;
    
    // Fetch coordinators to set the coordinator ID
    try {
        const data = await apiRequest(`/coordinators/?program_id=${program.program_id}`);
        const coordinators = data.results || data;
        
        if (coordinators.length > 0) {
            currentCoordinatorForAI = coordinators[0].id;
            console.log('AI variables set in showEmailCompositionModal:', { currentProgramForAI, currentCoordinatorForAI });
        } else {
            console.log('No coordinators found for program:', programId);
        }
    } catch (error) {
        console.error('Error fetching coordinators for AI:', error);
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
                    
                    <!-- AI Email Assistant -->
                    <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                        <label class="block text-sm font-medium text-gray-700 mb-2">🤖 AI Email Assistant</label>
                        
                        <!-- Language Selection -->
                        <div class="mb-4 bg-white p-3 rounded border">
                            <label class="block text-sm font-medium text-gray-600 mb-2">🌍 Language / Lingua / Langue / Idioma</label>
                            <select id="emailLanguage" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                                <option value="en">🇺🇸 English</option>
                                <option value="it">🇮🇹 Italiano</option>
                                <option value="fr">🇫🇷 Français</option>
                                <option value="es">🇪🇸 Español</option>
                                <option value="de">🇩🇪 Deutsch</option>
                                <option value="pt">🇵🇹 Português</option>
                                <option value="nl">🇳🇱 Nederlands</option>
                                <option value="ru">🇷🇺 Русский</option>
                                <option value="zh">🇨🇳 中文</option>
                                <option value="ja">🇯🇵 日本語</option>
                                <option value="ko">🇰🇷 한국어</option>
                                <option value="ar">🇸🇦 العربية</option>
                            </select>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                            <button type="button" onclick="generateAISuggestions()" 
                                    class="px-3 py-2 bg-blue-100 text-blue-800 rounded-md hover:bg-blue-200 text-sm">
                                <i class="fas fa-robot mr-1"></i>Generate Email
                            </button>
                            <button type="button" onclick="generateAISubjectOptions()" 
                                    class="px-3 py-2 bg-green-100 text-green-800 rounded-md hover:bg-green-200 text-sm">
                                <i class="fas fa-edit mr-1"></i>Subject Options
                            </button>
                            <button type="button" onclick="enhanceEmailContent()" 
                                    class="px-3 py-2 bg-purple-100 text-purple-800 rounded-md hover:bg-purple-200 text-sm">
                                <i class="fas fa-magic mr-1"></i>Enhance Content
                            </button>
                        </div>
                        
                        <!-- AI Suggestions Container -->
                        <div id="aiSuggestionsContainer" class="hidden mb-6">
                            <!-- AI suggestions will be populated here -->
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
                        <input type="text" id="emailSubject" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500" 
                               value="Inquiry about ${program.name} - ${program.university ? program.university.name : 'University'}">
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Message</label>
                        <textarea id="emailBody" rows="8" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500">Dear Coordinator,

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
                            <button onclick="sendEmailFromComposition(${programId})" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">Send Email</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Debug: Check if the language dropdown is present
    setTimeout(() => {
        const languageDropdown = document.getElementById('emailLanguage');
        if (languageDropdown) {
            console.log('✅ Language dropdown found:', languageDropdown);
            console.log('✅ Language dropdown options:', languageDropdown.options.length);
        } else {
            console.error('❌ Language dropdown NOT found!');
        }
    }, 100);
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
    
    // Load email settings and accounts
    loadEmailSettings();
    loadEmailAccounts();
    
    // Show development mode indicator if in development
    const devIndicator = document.getElementById('developmentModeIndicator');
    if (devIndicator && isDevelopmentMode()) {
        devIndicator.classList.remove('hidden');
    }
    
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
            credentials: 'include', // Include cookies for session authentication
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

// Toggle favorite status for a program
function toggleFavorite(programId) {
    console.log('=== TOGGLING FAVORITE ===', programId);
    
    if (!currentUser) {
        showNotification('Please login to manage favorites', 'error');
        return;
    }
    
    const program = allPrograms.find(p => p.id === programId) || searchResults.find(p => p.id === programId);
    if (!program) {
        console.error('Program not found with ID:', programId);
        showNotification('Program not found', 'error');
        return;
    }
    
    // Check if already in favorites
    const existingFavorite = favoritePrograms.find(fav => fav.id === programId);
    
    if (existingFavorite) {
        // Remove from favorites
        favoritePrograms = favoritePrograms.filter(fav => fav.id !== programId);
        saveFavorites();
        showNotification('Removed from favorites', 'info');
        console.log('=== PROGRAM REMOVED FROM FAVORITES ===');
    } else {
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
    
    // Update the heart icon in the program card
    updateHeartIcon(programId);
}

// Update heart icon for a specific program
function updateHeartIcon(programId) {
    const heartButton = document.querySelector(`button[onclick="toggleFavorite(${programId})"]`);
    if (heartButton) {
        const heartIcon = heartButton.querySelector('i');
        const isFavorite = favoritePrograms.find(fav => fav.id === programId);
        
        if (isFavorite) {
            heartIcon.className = 'fas fa-heart text-red-500 text-lg';
            heartButton.title = 'Remove from favorites';
        } else {
            heartIcon.className = 'far fa-heart text-gray-400 text-lg';
            heartButton.title = 'Add to favorites';
        }
    }
}

// Add program to favorites (legacy function for modal)
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
    
    // Update the heart icon
    updateHeartIcon(currentProgramId);
}

// Remove program from favorites
function removeFromFavorites(programId) {
    console.log('=== REMOVING FROM FAVORITES ===', programId);
    
    favoritePrograms = favoritePrograms.filter(fav => fav.id !== programId);
    saveFavorites();
    showNotification('Removed from favorites', 'success');
    
    // Update the heart icon
    updateHeartIcon(programId);
    
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
    const degreeLevel = document.getElementById('degreeFilter');
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
        allSearchResults = results; // Store all results for pagination
        currentPage = 1; // Reset to first page
        displaySearchResults(results.slice(0, resultsPerPage)); // Show only first 10 results
        
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
    const bulkEmailSection = document.getElementById('bulkEmailSection');
    
    if (!resultsSection || !container) return;
    
    resultsSection.classList.remove('hidden');
    
    // Clear existing results only if this is the first page
    if (currentPage === 1) {
        container.innerHTML = '';
    }
    
    if (results && results.length > 0) {
        // Show bulk email section for subscribed users
        if (currentUser && userSubscription && userSubscription.plan !== 'free') {
            if (bulkEmailSection) {
                bulkEmailSection.classList.remove('hidden');
            }
        }
        
        results.forEach(program => {
            const card = createProgramCard(program);
            container.appendChild(card);
        });
        
        // Update heart icons for all displayed programs
        results.forEach(program => {
            updateHeartIcon(program.id);
        });
        
        // Add or update "Show More" button
        updateShowMoreButton();
    } else {
        if (currentPage === 1) {
            container.innerHTML = '<p class="text-center text-gray-500 py-8">No programs found matching your criteria.</p>';
            // Hide bulk email section if no results
            if (bulkEmailSection) {
                bulkEmailSection.classList.add('hidden');
            }
        }
        // Remove "Show More" button if no more results
        removeShowMoreButton();
    }
}

// Pagination helper functions
function updateShowMoreButton() {
    const resultsSection = document.getElementById('searchResults');
    const container = document.getElementById('resultsContainer');
    
    if (!resultsSection || !container) return;
    
    // Remove existing button if it exists
    removeShowMoreButton();
    
    const totalResults = allSearchResults.length;
    const displayedResults = currentPage * resultsPerPage;
    const remainingResults = totalResults - displayedResults;
    
    if (remainingResults > 0) {
        const showMoreBtn = document.createElement('div');
        showMoreBtn.className = 'col-span-full flex justify-center mt-6';
        showMoreBtn.innerHTML = `
            <button id="showMoreBtn" onclick="showMoreResults()" 
                    class="bg-indigo-600 text-white px-8 py-3 rounded-md hover:bg-indigo-700 transition-colors font-semibold">
                <i class="fas fa-plus mr-2"></i>Show More (${remainingResults} remaining)
            </button>
        `;
        
        // Insert after the results container
        resultsSection.appendChild(showMoreBtn);
    }
}

function removeShowMoreButton() {
    const showMoreBtn = document.getElementById('showMoreBtn');
    if (showMoreBtn) {
        showMoreBtn.parentElement.remove();
    }
}

function showMoreResults() {
    currentPage++;
    const startIndex = (currentPage - 1) * resultsPerPage;
    const endIndex = startIndex + resultsPerPage;
    const nextResults = allSearchResults.slice(startIndex, endIndex);
    
    displaySearchResults(nextResults);
}

// Bulk Email Functions
function toggleProgramSelection(programId) {
    const checkbox = document.getElementById(`program-${programId}`);
    const program = searchResults.find(p => p.id === programId);
    
    if (!program) return;
    
    if (checkbox.checked) {
        if (!selectedPrograms.find(p => p.id === programId)) {
            selectedPrograms.push(program);
        }
    } else {
        selectedPrograms = selectedPrograms.filter(p => p.id !== programId);
    }
    
    updateSelectedCount();
    updateBulkEmailButtons();
    
    // Update the bulk email modal if it's open
    const modal = document.getElementById('bulkEmailModal');
    if (modal && !modal.classList.contains('hidden')) {
        updateSelectedProgramsList();
    }
}

function selectAllPrograms() {
    selectedPrograms = [...searchResults];
    
    // Check all checkboxes
    searchResults.forEach(program => {
        const checkbox = document.getElementById(`program-${program.id}`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    
    updateSelectedCount();
    updateBulkEmailButtons();
    
    // Update the bulk email modal if it's open
    const modal = document.getElementById('bulkEmailModal');
    if (modal && !modal.classList.contains('hidden')) {
        updateSelectedProgramsList();
    }
}

function clearAllPrograms() {
    selectedPrograms = [];
    
    // Uncheck all checkboxes
    searchResults.forEach(program => {
        const checkbox = document.getElementById(`program-${program.id}`);
        if (checkbox) {
            checkbox.checked = false;
        }
    });
    
    updateSelectedCount();
    updateBulkEmailButtons();
    
    // Update the bulk email modal if it's open
    const modal = document.getElementById('bulkEmailModal');
    if (modal && !modal.classList.contains('hidden')) {
        updateSelectedProgramsList();
    }
}

function updateSelectedCount() {
    const countElement = document.getElementById('selectedCount');
    if (countElement) {
        countElement.textContent = `${selectedPrograms.length} programs selected`;
    }
}

function updateBulkEmailButtons() {
    const sendBulkEmailBtn = document.getElementById('sendBulkEmailBtn');
    if (sendBulkEmailBtn) {
        if (selectedPrograms.length > 0) {
            sendBulkEmailBtn.disabled = false;
            sendBulkEmailBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            sendBulkEmailBtn.disabled = true;
            sendBulkEmailBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    }
}

function showBulkEmailModal() {
    if (!currentUser) {
        showNotification('Please login to send bulk emails', 'error');
        showLoginModal();
        return;
    }
    
    const subscription = userSubscription || { plan: 'free' };
    if (subscription.plan === 'free') {
        showNotification('Bulk email is a premium feature. Please upgrade to Premium or Pro plan.', 'error');
        showSubscriptionDashboard();
        return;
    }
    
    if (selectedPrograms.length === 0) {
        showNotification('Please select at least one program', 'error');
        return;
    }
    
    const modal = document.getElementById('bulkEmailModal');
    if (modal) {
        updateSelectedProgramsList();
        updateBulkEmailUsageInfo();
        modal.classList.remove('hidden');
    }
}

function closeBulkEmailModal() {
    const modal = document.getElementById('bulkEmailModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function updateSelectedProgramsList() {
    const listElement = document.getElementById('selectedProgramsList');
    if (!listElement) return;
    
    if (selectedPrograms.length === 0) {
        listElement.innerHTML = '<p class="text-gray-500">No programs selected</p>';
        return;
    }
    
    listElement.innerHTML = selectedPrograms.map(program => `
        <div class="flex items-center justify-between bg-white p-3 rounded border">
            <div>
                <h5 class="font-medium text-gray-900">${program.name}</h5>
                <p class="text-sm text-gray-600">${program.university ? program.university.name : 'Unknown University'}</p>
            </div>
            <button onclick="removeSelectedProgram(${program.id})" class="text-red-600 hover:text-red-700">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
}

function removeSelectedProgram(programId) {
    selectedPrograms = selectedPrograms.filter(p => p.id !== programId);
    
    // Uncheck the checkbox
    const checkbox = document.getElementById(`program-${programId}`);
    if (checkbox) {
        checkbox.checked = false;
    }
    
    updateSelectedCount();
    updateBulkEmailButtons();
    updateSelectedProgramsList();
    
    // Update the bulk email modal if it's open
    const modal = document.getElementById('bulkEmailModal');
    if (modal && !modal.classList.contains('hidden')) {
        updateSelectedProgramsList();
    }
}

function updateBulkEmailUsageInfo() {
    const usageElement = document.getElementById('bulkEmailUsageInfo');
    if (!usageElement) return;
    
    const subscription = userSubscription || { plan: 'free', emailsUsed: 0 };
    const emailsUsed = subscription.emailsUsed || 0;
    const emailLimit = subscription.plan === 'premium' ? 50 : 200;
    const remainingEmails = Math.max(0, emailLimit - emailsUsed);
    
    usageElement.textContent = `You have ${remainingEmails} emails remaining this month (${subscription.plan.charAt(0).toUpperCase() + subscription.plan.slice(1)} Plan)`;
}

function loadBulkEmailTemplate(templateType) {
    const emailBody = document.getElementById('bulkEmailBody');
    if (!emailBody) return;
    
    let template = '';
    
    switch (templateType) {
        case 'inquiry':
            template = `Dear Coordinators,

I hope this email finds you well. I am writing to inquire about the master's programs at your respective universities.

I am very interested in pursuing my master's degree and would like to learn more about:
- Available programs in my field of study
- Application requirements and deadlines
- Admission process and criteria
- Scholarship opportunities
- Career prospects after graduation

I would greatly appreciate any information you could provide about the programs and the application process.

Thank you for your time and consideration.

Best regards,
[Your Name]`;
            break;
            
        case 'admission':
            template = `Dear Admissions Committees,

I am writing to inquire about the admission requirements for the master's programs at your universities.

I am particularly interested in understanding:
- Academic requirements and prerequisites
- Application deadlines
- Required documents
- English language proficiency requirements
- Tuition fees and payment options

I have completed my bachelor's degree and am eager to continue my studies at your prestigious institutions.

Could you please provide me with detailed information about the admission process?

Thank you for your assistance.

Sincerely,
[Your Name]`;
            break;
            
        case 'scholarship':
            template = `Dear Scholarship Committees,

I hope this message finds you well. I am writing to inquire about scholarship opportunities for international students in the master's programs at your universities.

I am very interested in pursuing my master's degree at your institutions, but I would like to explore available financial aid options, including:
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
    }
    
    emailBody.value = template;
    showNotification('Bulk email template loaded', 'success');
}

// Handle bulk email form submission
async function handleBulkEmailSubmit(e) {
    e.preventDefault();
    console.log('=== BULK EMAIL SUBMISSION STARTED ===');
    
    if (selectedPrograms.length === 0) {
        showNotification('Please select at least one program', 'error');
        return;
    }
    
    const formData = new FormData(e.target);
    const subject = formData.get('subject');
    const body = formData.get('body');
    
    if (!subject || !body) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    // Check subscription and email limits
    const subscription = userSubscription || { plan: 'free', emailsUsed: 0 };
    const emailsUsed = subscription.emailsUsed || 0;
    const emailLimit = subscription.plan === 'premium' ? 50 : 200;
    
    if (emailsUsed >= emailLimit) {
        showNotification(`You have reached your monthly email limit (${emailLimit} emails). Please upgrade your plan or wait for next month.`, 'error');
        return;
    }
    
    // Get all coordinators from selected programs
    const allCoordinators = [];
    for (const program of selectedPrograms) {
        try {
            const data = await apiRequest(`/coordinators/?program_id=${program.program_id}`);
            const coordinators = data.results || data;
            coordinators.forEach(coordinator => {
                if (coordinator.email) {
                    allCoordinators.push({
                        ...coordinator,
                        program_name: program.name,
                        university_name: program.university ? program.university.name : 'Unknown University'
                    });
                }
            });
        } catch (error) {
            console.error(`Error fetching coordinators for program ${program.id}:`, error);
        }
    }
    
    if (allCoordinators.length === 0) {
        showNotification('No coordinators found for selected programs', 'error');
        return;
    }
    
    // Check if we have enough emails remaining
    if (emailsUsed + allCoordinators.length > emailLimit) {
        showNotification(`You can only send ${emailLimit - emailsUsed} more emails this month. Please select fewer programs or upgrade your plan.`, 'error');
        return;
    }
    
    // Send bulk email
    try {
        const response = await fetch(`${API_BASE_URL}/send-bulk-email/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies for session authentication
            body: JSON.stringify({
                coordinators: allCoordinators,
                subject: subject,
                body: body
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Bulk email sent successfully:', result);
            
            // Update email usage
            userSubscription.emailsUsed = (userSubscription.emailsUsed || 0) + allCoordinators.length;
            saveSubscriptionData();
            
            // Clear selected programs
            clearAllPrograms();
            
            // Close modal
            closeBulkEmailModal();
            
            // Show success notification
            showNotification(`Bulk email sent successfully to ${allCoordinators.length} coordinators!`, 'success');
            
            // Add to email history
            addBulkEmailToHistory(allCoordinators, subject, body);
            
        } else {
            const error = await response.json();
            console.error('Bulk email failed:', error);
            showNotification(`Failed to send bulk email: ${error.message || 'Unknown error'}`, 'error');
        }
        
    } catch (error) {
        console.error('Error sending bulk email:', error);
        showNotification('Error sending bulk email. Please try again.', 'error');
    }
}

// Add bulk email to history
function addBulkEmailToHistory(coordinators, subject, body) {
    const emailHistory = JSON.parse(localStorage.getItem('emailHistory') || '[]');
    
    emailHistory.push({
        type: 'bulk',
        coordinators: coordinators.map(c => ({
            name: c.name,
            email: c.email,
            program: c.program_name,
            university: c.university_name
        })),
        subject: subject,
        body: body,
        timestamp: new Date().toISOString(),
        count: coordinators.length
    });
    
    localStorage.setItem('emailHistory', JSON.stringify(emailHistory));
}

// OAuth2 Email Integration Functions
function connectGmail() {
    console.log('=== CONNECTING GMAIL ===');
    
    // Check if user is logged in
    if (!currentUser) {
        console.log('User not logged in, cannot connect Gmail');
        showNotification('Please login to connect Gmail', 'error');
        showLoginModal();
        return;
    }
    
    // Check if we're in development mode
    if (isDevelopmentMode()) {
        console.log('Development mode: Simulating Gmail connection');
        simulateGmailConnection();
        return;
    }
    
    // Gmail OAuth2 configuration
    const clientId = OAUTH2_CONFIG.gmail.clientId;
    const redirectUri = OAUTH2_CONFIG.gmail.redirectUri;
    const scope = OAUTH2_CONFIG.gmail.scope;
    
    // Create OAuth2 URL with user ID in state
    const state = `gmail-oauth-${currentUser.id}-${Date.now()}`;
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?` +
        `client_id=${clientId}&` +
        `redirect_uri=${encodeURIComponent(redirectUri)}&` +
        `scope=${encodeURIComponent(scope)}&` +
        `response_type=code&` +
        `access_type=offline&` +
        `prompt=consent&` +
        `state=${state}`;
    
    // Open OAuth2 popup
    const popup = window.open(authUrl, 'gmail-oauth', 'width=500,height=600,scrollbars=yes,resizable=yes');
    
    if (!popup) {
        showNotification('Popup blocked! Please allow popups for this site.', 'error');
        return;
    }
    
    // Listen for OAuth2 callback
    const checkClosed = setInterval(() => {
        if (popup.closed) {
            clearInterval(checkClosed);
            // Wait a moment for the callback to complete, then check status
            setTimeout(() => {
                console.log('Popup closed, checking OAuth2 status...');
                checkOAuth2Status('gmail');
            }, 3000);
        }
    }, 1000);
}

function connectOutlook() {
    console.log('=== CONNECTING OUTLOOK ===');
    
    // Check if user is logged in
    if (!currentUser) {
        console.log('User not logged in, cannot connect Outlook');
        showNotification('Please login to connect Outlook', 'error');
        showLoginModal();
        return;
    }
    
    // Check if we're in development mode
    if (isDevelopmentMode()) {
        console.log('Development mode: Simulating Outlook connection');
        simulateOutlookConnection();
        return;
    }
    
    // Outlook OAuth2 configuration
    const clientId = OAUTH2_CONFIG.outlook.clientId;
    const redirectUri = OAUTH2_CONFIG.outlook.redirectUri;
    const scope = OAUTH2_CONFIG.outlook.scope;
    
    // Create OAuth2 URL
    // Create OAuth2 URL with user ID in state
    const state = `outlook-oauth-${currentUser.id}-${Date.now()}`;
    const authUrl = `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?` +
        `client_id=${clientId}&` +
        `response_type=code&` +
        `redirect_uri=${encodeURIComponent(redirectUri)}&` +
        `scope=${encodeURIComponent(scope)}&` +
        `response_mode=query&` +
        `state=${state}`;
    
    // Open OAuth2 popup
    const popup = window.open(authUrl, 'outlook-oauth', 'width=500,height=600,scrollbars=yes,resizable=yes');
    
    if (!popup) {
        showNotification('Popup blocked! Please allow popups for this site.', 'error');
        return;
    }
    
    // Listen for OAuth2 callback
    const checkClosed = setInterval(() => {
        if (popup.closed) {
            clearInterval(checkClosed);
            // Wait a moment for the callback to complete, then check status
            setTimeout(() => {
                console.log('Popup closed, checking OAuth2 status...');
                checkOAuth2Status('outlook');
            }, 3000);
        }
    }, 1000);
}

// OAuth2 Configuration is loaded from oauth2_config.js

// Development Mode Functions
function isDevelopmentMode() {
    // Check if we're in development mode from OAuth2 config
    console.log('OAUTH2_CONFIG developmentMode:', OAUTH2_CONFIG.developmentMode);
    return OAUTH2_CONFIG.developmentMode === true;
}

// OAuth2 Message Handler
window.addEventListener('message', function(event) {
    console.log('=== MESSAGE RECEIVED ===');
    console.log('Event origin:', event.origin);
    console.log('Event data:', event.data);
    
    if (event.data && event.data.type === 'oauth_success') {
        const { provider, success } = event.data;
        console.log(`OAuth2 success for ${provider}:`, { success });
        
        if (provider === 'gmail') {
            console.log('Handling Gmail OAuth2 success...');
            handleGmailOAuthSuccess(null, null);
        } else if (provider === 'outlook') {
            console.log('Handling Outlook OAuth2 success...');
            handleOutlookOAuthSuccess(null, null);
        }
    } else {
        console.log('Message not OAuth2 success:', event.data);
    }
});

function handleGmailOAuthSuccess(code, state) {
    console.log('=== HANDLING GMAIL OAUTH SUCCESS ===');
    
    // Store connection status in localStorage
    localStorage.setItem('gmailConnected', 'true');
    
    // Check OAuth2 status to get the real connection status
    checkOAuth2Status('gmail');
    
    console.log('Gmail OAuth2 connection completed');
}

// Manual trigger for testing (remove in production)
function testGmailOAuthSuccess() {
    console.log('=== TESTING GMAIL OAUTH SUCCESS ===');
    handleGmailOAuthSuccess('test-code-12345', 'test-state-67890');
}

function handleOutlookOAuthSuccess(code, state) {
    console.log('=== HANDLING OUTLOOK OAUTH SUCCESS ===');
    
    // Store connection status in localStorage
    localStorage.setItem('outlookConnected', 'true');
    
    // Check OAuth2 status to get the real connection status
    checkOAuth2Status('outlook');
    
    console.log('Outlook OAuth2 connection completed');
}

function simulateGmailConnection() {
    // Simulate successful Gmail connection for demo
    emailAccounts.gmail.connected = true;
    emailAccounts.gmail.email = 'test@gmail.com';
    emailAccounts.gmail.accessToken = 'dev-gmail-token-12345';
    
    // Store in localStorage for email sending
    localStorage.setItem('gmailConnected', 'true');
    localStorage.setItem('gmailEmail', 'test@gmail.com');
    
    updateEmailAccountDisplay('gmail');
    showNotification('Gmail connected successfully! (Development Mode)', 'success');
    saveEmailAccounts();
}

function simulateOutlookConnection() {
    // Simulate successful Outlook connection for demo
    emailAccounts.outlook.connected = true;
    emailAccounts.outlook.email = 'test@outlook.com';
    emailAccounts.outlook.accessToken = 'dev-outlook-token-67890';
    
    // Store in localStorage for email sending
    localStorage.setItem('outlookConnected', 'true');
    localStorage.setItem('outlookEmail', 'test@outlook.com');
    
    updateEmailAccountDisplay('outlook');
    showNotification('Outlook connected successfully! (Development Mode)', 'success');
    saveEmailAccounts();
}

function checkOAuth2Status(provider) {
    // Check if OAuth2 connection was successful
    console.log(`Checking OAuth2 status for ${provider}`);
    
    // Check if user is logged in
    if (!currentUser) {
        console.log('User not logged in, cannot check OAuth2 status');
        showNotification('Please login to connect email accounts', 'error');
        return;
    }
    
    // Check if we're in development mode
    if (isDevelopmentMode()) {
        console.log('Development mode: Simulating OAuth2 connection');
        if (provider === 'gmail') {
            simulateGmailConnection();
        } else if (provider === 'outlook') {
            simulateOutlookConnection();
        }
        return;
    }
    
    // Real OAuth2 implementation - check with backend
    fetch('/api/oauth/tokens/', {
        method: 'GET',
        credentials: 'include', // Include cookies for session authentication
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log('OAuth2 status response:', data);
            if (data.success) {
                if (provider === 'gmail' && data.gmail.has_access_token) {
                    // Update UI to show Gmail is connected
                    emailAccounts.gmail.connected = true;
                    emailAccounts.gmail.email = 'Connected via OAuth2';
                    updateEmailAccountDisplay('gmail');
                    saveEmailAccounts(); // Save to localStorage
                    showNotification('Gmail connected successfully via OAuth2!', 'success');
                } else if (provider === 'outlook' && data.outlook.has_access_token) {
                    // Update UI to show Outlook is connected
                    emailAccounts.outlook.connected = true;
                    emailAccounts.outlook.email = 'Connected via OAuth2';
                    updateEmailAccountDisplay('outlook');
                    saveEmailAccounts(); // Save to localStorage
                    showNotification('Outlook connected successfully via OAuth2!', 'success');
                } else {
                    showNotification(`${provider} OAuth2 connection failed`, 'error');
                }
            } else {
                showNotification(`Failed to check ${provider} OAuth2 status: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error checking OAuth2 status:', error);
            showNotification(`Error checking ${provider} OAuth2 status`, 'error');
        });
}

function disconnectGmail() {
    console.log('=== DISCONNECTING GMAIL ===');
    
    emailAccounts.gmail.connected = false;
    emailAccounts.gmail.email = '';
    emailAccounts.gmail.accessToken = '';
    
    // Clear localStorage
    localStorage.removeItem('gmailConnected');
    localStorage.removeItem('gmailEmail');
    
    updateEmailAccountDisplay('gmail');
    showNotification('Gmail disconnected successfully!', 'info');
    saveEmailAccounts();
}

function disconnectOutlook() {
    console.log('=== DISCONNECTING OUTLOOK ===');
    
    emailAccounts.outlook.connected = false;
    emailAccounts.outlook.email = '';
    emailAccounts.outlook.accessToken = '';
    
    // Clear localStorage
    localStorage.removeItem('outlookConnected');
    localStorage.removeItem('outlookEmail');
    
    updateEmailAccountDisplay('outlook');
    showNotification('Outlook disconnected successfully!', 'info');
    saveEmailAccounts();
}

function updateEmailAccountDisplay(provider) {
    const statusElement = document.getElementById(`${provider}Status`);
    const accountInfoElement = document.getElementById(`${provider}AccountInfo`);
    const emailElement = document.getElementById(`${provider}Email`);
    const connectBtn = document.getElementById(`${provider}ConnectBtn`);
    const disconnectBtn = document.getElementById(`${provider}DisconnectBtn`);
    
    if (emailAccounts[provider].connected) {
        // Update status
        if (statusElement) {
            statusElement.innerHTML = '<span class="bg-green-100 text-green-800 px-2 py-1 rounded-full">Connected</span>';
        }
        
        // Show account info
        if (accountInfoElement) {
            accountInfoElement.classList.remove('hidden');
        }
        
        // Update email
        if (emailElement) {
            emailElement.textContent = emailAccounts[provider].email;
        }
        
        // Show disconnect button
        if (connectBtn) {
            connectBtn.classList.add('hidden');
        }
        if (disconnectBtn) {
            disconnectBtn.classList.remove('hidden');
        }
    } else {
        // Update status
        if (statusElement) {
            statusElement.innerHTML = '<span class="bg-gray-100 text-gray-800 px-2 py-1 rounded-full">Not Connected</span>';
        }
        
        // Hide account info
        if (accountInfoElement) {
            accountInfoElement.classList.add('hidden');
        }
        
        // Show connect button
        if (connectBtn) {
            connectBtn.classList.remove('hidden');
        }
        if (disconnectBtn) {
            disconnectBtn.classList.add('hidden');
        }
    }
}

function saveEmailSettings() {
    console.log('=== SAVING EMAIL SETTINGS ===');
    
    const defaultProvider = document.getElementById('defaultEmailProvider');
    const signature = document.getElementById('emailSignature');
    
    if (defaultProvider) {
        emailSettings.defaultProvider = defaultProvider.value;
    }
    
    if (signature) {
        emailSettings.signature = signature.value;
    }
    
    // Save to localStorage
    localStorage.setItem('emailSettings', JSON.stringify(emailSettings));
    
    showNotification('Email settings saved successfully!', 'success');
}

function loadEmailSettings() {
    console.log('=== LOADING EMAIL SETTINGS ===');
    
    // Load from localStorage
    const savedSettings = localStorage.getItem('emailSettings');
    if (savedSettings) {
        emailSettings = { ...emailSettings, ...JSON.parse(savedSettings) };
    }
    
    // Update UI
    const defaultProvider = document.getElementById('defaultEmailProvider');
    const signature = document.getElementById('emailSignature');
    
    if (defaultProvider) {
        defaultProvider.value = emailSettings.defaultProvider;
    }
    
    if (signature) {
        signature.value = emailSettings.signature;
    }
}

function loadEmailAccounts() {
    console.log('=== LOADING EMAIL ACCOUNTS ===');
    
    // Load from localStorage
    const savedAccounts = localStorage.getItem('emailAccounts');
    if (savedAccounts) {
        emailAccounts = { ...emailAccounts, ...JSON.parse(savedAccounts) };
    }
    
    // Check OAuth2 status with backend if user is logged in
    if (currentUser && !isDevelopmentMode()) {
        console.log('Checking OAuth2 status with backend...');
        checkOAuth2Status('gmail');
        checkOAuth2Status('outlook');
    }
    
    // Update UI
    updateEmailAccountDisplay('gmail');
    updateEmailAccountDisplay('outlook');
}

function saveEmailAccounts() {
    localStorage.setItem('emailAccounts', JSON.stringify(emailAccounts));
}

function getConnectedEmailProvider() {
    if (emailAccounts.gmail.connected) return 'gmail';
    if (emailAccounts.outlook.connected) return 'outlook';
    return null;
}

function sendEmailViaOAuth2(recipient, subject, body) {
    const provider = getConnectedEmailProvider();
    
    if (!provider) {
        showNotification('No email account connected. Please connect Gmail or Outlook first.', 'error');
        return false;
    }
    
    console.log(`=== SENDING EMAIL VIA ${provider.toUpperCase()} ===`);
    
    // Send email via backend API
    const emailData = {
        coordinator_email: recipient,
        subject: subject,
        body: body,
        email_provider: provider
    };
    
    fetch('/api/send-email/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(emailData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Email sent successfully:', data);
            showNotification(`Email sent successfully via ${provider.charAt(0).toUpperCase() + provider.slice(1)}!`, 'success');
        } else {
            console.error('Email sending failed:', data);
            showNotification(`Failed to send email: ${data.error}`, 'error');
        }
    })
    .catch(error => {
        console.error('Error sending email:', error);
        showNotification('Error sending email. Please try again.', 'error');
    });
    
    return true;
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

// User Profile Functions
async function showUserProfile() {
    closeAllModals();
    document.getElementById('userProfileModal').classList.remove('hidden');
    
    try {
        // Load user profile data
        await loadUserProfile();
    } catch (error) {
        console.error('Error loading user profile:', error);
        showNotification('Failed to load profile data', 'error');
    }
}

async function loadUserProfile() {
    try {
        const response = await apiRequest('/auth/profile/');
        const userData = response;
        
        // Populate form fields
        document.getElementById('profileFirstName').value = userData.first_name || '';
        document.getElementById('profileLastName').value = userData.last_name || '';
        document.getElementById('profileEmail').value = userData.email || '';
        document.getElementById('profilePhone').value = userData.phone_number || '';
        document.getElementById('profileNationality').value = userData.nationality || '';
        document.getElementById('profileAge').value = userData.age || '';
        
        // Academic information
        document.getElementById('profileDegree').value = userData.degree || '';
        document.getElementById('profileMajor').value = userData.major || '';
        document.getElementById('profileUniversity').value = userData.university || '';
        document.getElementById('profileGraduationYear').value = userData.graduation_year || '';
        document.getElementById('profileGPA').value = userData.gpa || '';
        
        // Professional information
        document.getElementById('profilePosition').value = userData.current_position || '';
        document.getElementById('profileCompany').value = userData.company || '';
        document.getElementById('profileExperience').value = userData.work_experience_years || '';
        
        // Additional information
        document.getElementById('profileExperience').value = userData.relevant_experience || '';
        document.getElementById('profileInterests').value = userData.interests || '';
        document.getElementById('profileLanguages').value = userData.languages_spoken || '';
        document.getElementById('profileLinkedIn').value = userData.linkedin_profile || '';
        document.getElementById('profilePortfolio').value = userData.portfolio_website || '';
        
        // Preferences
        document.getElementById('profileCountries').value = userData.preferred_countries || '';
        document.getElementById('profileBudget').value = userData.budget_range || '';
        
        // Update profile completeness
        updateProfileCompleteness(userData.profile_completeness || 0);
        
    } catch (error) {
        console.error('Error loading user profile:', error);
        throw error;
    }
}

function updateProfileCompleteness(completeness) {
    const completenessElement = document.getElementById('profileCompleteness');
    const progressBar = document.getElementById('profileProgressBar');
    
    if (completenessElement && progressBar) {
        completenessElement.textContent = `${completeness}%`;
        progressBar.style.width = `${completeness}%`;
        
        // Change color based on completeness
        if (completeness >= 70) {
            progressBar.className = 'bg-green-600 h-2 rounded-full transition-all duration-300';
        } else if (completeness >= 40) {
            progressBar.className = 'bg-yellow-600 h-2 rounded-full transition-all duration-300';
        } else {
            progressBar.className = 'bg-red-600 h-2 rounded-full transition-all duration-300';
        }
    }
}

async function saveUserProfile(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const profileData = {};
    
    // Convert FormData to object
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
            profileData[key] = value.trim();
        }
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies for session authentication
            body: JSON.stringify(profileData)
        });
        
        if (response.ok) {
            const updatedData = await response.json();
            showNotification('Profile updated successfully!', 'success');
            
            // Update profile completeness
            updateProfileCompleteness(updatedData.profile_completeness || 0);
            
            // Update current user data
            if (currentUser) {
                Object.assign(currentUser, updatedData);
                localStorage.setItem('currentUser', JSON.stringify(currentUser));
            }
            
        } else {
            const errorData = await response.json();
            showNotification(errorData.error || 'Failed to update profile', 'error');
        }
        
    } catch (error) {
        console.error('Error updating profile:', error);
        showNotification('Failed to update profile', 'error');
    }
}

// AI Email Assistant Functions
let currentProgramForAI = null;
let currentCoordinatorForAI = null;

// Generate AI-powered email suggestions
async function generateAISuggestions(programId = null, coordinatorId = null, emailType = null) {
    // Use global variables if parameters not provided
    if (!programId) programId = currentProgramForAI;
    if (!coordinatorId) coordinatorId = currentCoordinatorForAI;
    
    // Get selected language and email type from the UI
    const language = document.getElementById('emailLanguage')?.value || 'en';
    if (!emailType) {
        emailType = document.getElementById('emailType')?.value || 'inquiry';
    }
    
    console.log('AI function called with:', { programId, coordinatorId, emailType, language });
    console.log('Global variables:', { currentProgramForAI, currentCoordinatorForAI });
    
    if (!programId || !coordinatorId) {
        showNotification('Please select a program and coordinator first', 'error');
        console.error('Missing program or coordinator ID:', { programId, coordinatorId });
        return;
    }
    
    // Show loading state
    showAILoadingState('Generating AI email suggestions...');
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/ai/generate-suggestions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies for session authentication
            body: JSON.stringify({
                program_id: programId,
                coordinator_id: coordinatorId,
                email_type: emailType,
                language: language
            })
        });
        
        console.log('API Request sent with language:', language);
        console.log('Request body:', JSON.stringify({
            program_id: programId,
            coordinator_id: coordinatorId,
            email_type: emailType,
            language: language
        }));
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayAISuggestions(data.suggestions);
        } else {
            showNotification(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error generating AI suggestions:', error);
        showNotification('Failed to generate AI suggestions', 'error');
    }
}

// Generate AI subject for bulk email
async function generateBulkAISubject() {
    const token = localStorage.getItem('token');
    if (!token) {
        showNotification('Please log in to use AI features', 'error');
        return;
    }
    
    if (selectedPrograms.length === 0) {
        showNotification('Please select at least one program first', 'error');
        return;
    }
    
    try {
        // Use the first selected program for AI generation
        const firstProgram = selectedPrograms[0];
        
        // Get coordinators for the first program
        const data = await apiRequest(`/coordinators/?program_id=${firstProgram.program_id}`);
        const coordinators = data.results || data;
        
        if (coordinators.length === 0) {
            showNotification('No coordinators found for selected programs', 'error');
            return;
        }
        
        const coordinator = coordinators[0];
        const language = document.getElementById('bulkEmailLanguage')?.value || 'en';
        const emailType = document.getElementById('bulkEmailType')?.value || 'inquiry';
        
        // Generate AI subject
        const response = await fetch(`${API_BASE_URL}/ai/generate-subjects/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies for session authentication
            body: JSON.stringify({
                program_id: firstProgram.id,
                coordinator_id: coordinator.id,
                email_type: emailType,
                language: language,
                count: 1
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.subject_options && data.subject_options.length > 0) {
                document.getElementById('bulkEmailSubject').value = data.subject_options[0];
                showNotification('AI subject generated successfully!', 'success');
            } else {
                showNotification('Failed to generate AI subject', 'error');
            }
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
    } catch (error) {
        console.error('Error generating bulk AI subject:', error);
        showNotification('Failed to generate AI subject', 'error');
    }
}

// Generate AI content for bulk email
async function generateBulkAIContent() {
    const token = localStorage.getItem('token');
    if (!token) {
        showNotification('Please log in to use AI features', 'error');
        return;
    }
    
    if (selectedPrograms.length === 0) {
        showNotification('Please select at least one program first', 'error');
        return;
    }
    
    try {
        // Use the first selected program for AI generation
        const firstProgram = selectedPrograms[0];
        
        // Get coordinators for the first program
        const data = await apiRequest(`/coordinators/?program_id=${firstProgram.program_id}`);
        const coordinators = data.results || data;
        
        if (coordinators.length === 0) {
            showNotification('No coordinators found for selected programs', 'error');
            return;
        }
        
        const coordinator = coordinators[0];
        const language = document.getElementById('bulkEmailLanguage')?.value || 'en';
        const emailType = document.getElementById('bulkEmailType')?.value || 'inquiry';
        
        // Generate AI content
        const response = await fetch(`${API_BASE_URL}/ai/generate-suggestions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies for session authentication
            body: JSON.stringify({
                program_id: firstProgram.id,
                coordinator_id: coordinator.id,
                email_type: emailType,
                language: language
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.suggestions && data.suggestions.content) {
                document.getElementById('bulkEmailBody').value = data.suggestions.content;
                showNotification('AI content generated successfully!', 'success');
            } else {
                showNotification('Failed to generate AI content', 'error');
            }
        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
    } catch (error) {
        console.error('Error generating bulk AI content:', error);
        showNotification('Failed to generate AI content', 'error');
    }
}

// Generate both subject and content when email type changes
async function generateEmailTypeBasedAI() {
    const token = localStorage.getItem('token');
    if (!token) {
        return; // Don't show error for automatic generation
    }
    
    if (selectedPrograms.length === 0) {
        return; // Don't generate if no programs selected
    }
    
    try {
        // Use the first selected program for AI generation
        const firstProgram = selectedPrograms[0];
        
        // Get coordinators for the first program
        const data = await apiRequest(`/coordinators/?program_id=${firstProgram.program_id}`);
        const coordinators = data.results || data;
        
        if (coordinators.length === 0) {
            return; // Don't show error for automatic generation
        }
        
        const coordinator = coordinators[0];
        const language = document.getElementById('bulkEmailLanguage')?.value || 'en';
        const emailType = document.getElementById('bulkEmailType')?.value || 'inquiry';
        
        // Show loading state
        const subjectField = document.getElementById('bulkEmailSubject');
        const contentField = document.getElementById('bulkEmailBody');
        
        if (subjectField) subjectField.value = 'Generating AI subject...';
        if (contentField) contentField.value = 'Generating AI content...';
        
        // Generate AI suggestions (both subject and content)
        const response = await fetch(`${API_BASE_URL}/ai/generate-suggestions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                program_id: firstProgram.id,
                coordinator_id: coordinator.id,
                email_type: emailType,
                language: language
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.suggestions) {
                // Update subject
                if (data.suggestions.subject && subjectField) {
                    subjectField.value = data.suggestions.subject;
                }
                
                // Update content
                if (data.suggestions.content && contentField) {
                    contentField.value = data.suggestions.content;
                }
                
                // Show success notification
                showNotification(`AI generated ${emailType} email successfully!`, 'success');
            }
        }
        
    } catch (error) {
        console.error('Error generating email type based AI:', error);
        // Reset fields on error
        const subjectField = document.getElementById('bulkEmailSubject');
        const contentField = document.getElementById('bulkEmailBody');
        if (subjectField) subjectField.value = '';
        if (contentField) contentField.value = '';
    }
}

// Generate both subject and content when email type changes in coordinator modal
async function generateCoordinatorEmailTypeBasedAI() {
    const token = localStorage.getItem('token');
    if (!token) {
        return; // Don't show error for automatic generation
    }
    
    // Check if we have the required global variables for AI generation
    if (!currentProgramForAI || !currentCoordinatorForAI) {
        return; // Don't generate if no program/coordinator selected
    }
    
    try {
        const language = document.getElementById('emailLanguage')?.value || 'en';
        const emailType = document.getElementById('emailType')?.value || 'inquiry';
        
        // Show loading state
        const subjectField = document.getElementById('emailSubject');
        const contentField = document.getElementById('emailBody');
        
        if (subjectField) subjectField.value = 'Generating AI subject...';
        if (contentField) contentField.value = 'Generating AI content...';
        
        // Generate AI suggestions (both subject and content)
        const response = await fetch(`${API_BASE_URL}/ai/generate-suggestions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                program_id: currentProgramForAI,
                coordinator_id: currentCoordinatorForAI,
                email_type: emailType,
                language: language
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.suggestions) {
                // Update subject
                if (data.suggestions.subject && subjectField) {
                    subjectField.value = data.suggestions.subject;
                }
                
                // Update content
                if (data.suggestions.content && contentField) {
                    contentField.value = data.suggestions.content;
                }
                
                // Show success notification
                showNotification(`AI generated ${emailType} email successfully!`, 'success');
            }
        }
        
    } catch (error) {
        console.error('Error generating coordinator email type based AI:', error);
        // Reset fields on error
        const subjectField = document.getElementById('emailSubject');
        const contentField = document.getElementById('emailBody');
        if (subjectField) subjectField.value = '';
        if (contentField) contentField.value = '';
    }
}

// Generate multiple subject options
async function generateAISubjectOptions(programId = null, coordinatorId = null, emailType = null, count = 3) {
    // Use global variables if parameters not provided
    if (!programId) programId = currentProgramForAI;
    if (!coordinatorId) coordinatorId = currentCoordinatorForAI;
    
    // Get selected language and email type from the UI
    const language = document.getElementById('emailLanguage')?.value || 'en';
    if (!emailType) {
        emailType = document.getElementById('emailType')?.value || 'inquiry';
    }
    
    console.log('AI subject function called with:', { programId, coordinatorId, emailType, count, language });
    console.log('Global variables:', { currentProgramForAI, currentCoordinatorForAI });
    
    if (!programId || !coordinatorId) {
        showNotification('Please select a program and coordinator first', 'error');
        console.error('Missing program or coordinator ID:', { programId, coordinatorId });
        return;
    }
    
    // Show loading state
    showAILoadingState('Generating AI subject options...');
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/ai/generate-subjects/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies for session authentication
            body: JSON.stringify({
                program_id: programId,
                coordinator_id: coordinatorId,
                email_type: emailType,
                count: count,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayAISubjectOptions(data.subject_options);
        } else {
            showNotification(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error generating AI subject options:', error);
        showNotification('Failed to generate AI subject options', 'error');
    }
}

// Enhance existing email content
async function enhanceEmailContent(programId = null, coordinatorId = null, enhancementType = 'improve') {
    if (!programId) programId = currentProgramForAI;
    if (!coordinatorId) coordinatorId = currentCoordinatorForAI;
    
    // Get selected language and email type from the UI
    const language = document.getElementById('emailLanguage')?.value || 'en';
    const emailType = document.getElementById('emailType')?.value || 'inquiry';
    
    if (!programId || !coordinatorId) {
        showNotification('Please select a program and coordinator first', 'error');
        return;
    }
    
    const currentContent = document.getElementById('emailBody').value;
    if (!currentContent.trim()) {
        showNotification('Please write some content first', 'error');
        return;
    }
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/ai/enhance-content/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include cookies for session authentication
            body: JSON.stringify({
                program_id: programId,
                coordinator_id: coordinatorId,
                current_content: currentContent,
                email_type: emailType,
                enhancement_type: enhancementType,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayEnhancedContent(data.enhanced_content, data.original_content);
        } else {
            showNotification(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error enhancing email content:', error);
        showNotification('Failed to enhance email content', 'error');
    }
}

// Display AI suggestions
function displayAISuggestions(suggestions) {
    const container = document.getElementById('aiSuggestionsContainer');
    if (!container) return;
    
    container.innerHTML = `
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 class="font-semibold text-blue-800 mb-3">🤖 AI Email Assistant</h4>
            <div class="space-y-3">
                <div>
                    <label class="block text-sm font-medium text-blue-700 mb-1">Suggested Subject:</label>
                    <div class="flex items-center space-x-2">
                        <input type="text" id="aiSubject" value="${suggestions.subject}" 
                               class="flex-1 px-3 py-2 border border-blue-300 rounded-md text-sm">
                        <button onclick="useAISuggestion()" 
                                class="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm">
                            Use
                        </button>
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-blue-700 mb-1">Suggested Content:</label>
                    <div class="space-y-2">
                        <textarea id="aiContent" rows="6" 
                                  class="w-full px-3 py-2 border border-blue-300 rounded-md text-sm">${suggestions.content}</textarea>
                        <div class="flex space-x-2">
                            <button type="button" onclick="useAISuggestion(event)" 
                                    class="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm">
                                Use This Content
                            </button>
                            <button type="button" onclick="generateAISubjectOptions()" 
                                    class="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm">
                                More Subjects
                            </button>
                            <button type="button" onclick="generateAISuggestions()" 
                                    class="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm">
                                Generate Full Email
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.classList.remove('hidden');
}

// Display AI subject options
function displayAISubjectOptions(subjectOptions) {
    const container = document.getElementById('aiSuggestionsContainer');
    if (!container) return;
    
    const subjectsHtml = subjectOptions.map((subject, index) => `
        <div class="flex items-center space-x-2 p-2 bg-white border border-gray-200 rounded">
            <input type="text" value="${subject}" readonly 
                   class="flex-1 px-2 py-1 border-none bg-transparent text-sm">
            <button onclick="useAISubjectOption(${index})" 
                    class="px-2 py-1 bg-blue-600 text-white rounded text-xs hover:bg-blue-700">
                Use
            </button>
        </div>
    `).join('');
    
    container.innerHTML = `
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 class="font-semibold text-green-800 mb-3">📝 AI Subject Options</h4>
            <div class="space-y-2 mb-3">
                ${subjectsHtml}
            </div>
            <div class="flex space-x-2">
                <button onclick="generateAISubjectOptions()" 
                        class="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm">
                    Generate More
                </button>
                <button onclick="generateAISuggestions()" 
                        class="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm">
                    Generate Full Email
                </button>
            </div>
        </div>
    `;
    container.classList.remove('hidden');
}

// Display enhanced content
function displayEnhancedContent(enhancedContent, originalContent) {
    const container = document.getElementById('aiSuggestionsContainer');
    if (!container) return;
    
    container.innerHTML = `
        <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h4 class="font-semibold text-purple-800 mb-3">✨ Enhanced Content</h4>
            <div class="space-y-3">
                <div>
                    <label class="block text-sm font-medium text-purple-700 mb-1">Enhanced Version:</label>
                    <textarea id="enhancedContent" rows="6" 
                              class="w-full px-3 py-2 border border-purple-300 rounded-md text-sm">${enhancedContent}</textarea>
                </div>
                <div class="flex space-x-2">
                    <button type="button" onclick="useEnhancedContent(event)" 
                            class="px-3 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 text-sm">
                        Use Enhanced Version
                    </button>
                    <button type="button" onclick="showOriginalContent()" 
                            class="px-3 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 text-sm">
                        Show Original
                    </button>
                </div>
            </div>
        </div>
    `;
    container.classList.remove('hidden');
}

// Use AI suggestion
function useAISuggestion(event) {
    // Prevent any form submission or event propagation
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    const subject = document.getElementById('aiSubject')?.value;
    const content = document.getElementById('aiContent')?.value;
    
    console.log('useAISuggestion called - applying content:', { subject, content });
    
    if (subject) document.getElementById('emailSubject').value = subject;
    if (content) document.getElementById('emailBody').value = content;
    
    hideAISuggestions();
    showNotification('AI suggestion applied! You can now review and send the email.', 'success');
    
    // Scroll to the email form to make it visible
    const emailForm = document.getElementById('emailSubject');
    if (emailForm) {
        emailForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    console.log('useAISuggestion completed - email should NOT be sent');
}

// Use AI subject option
function useAISubjectOption(index) {
    const container = document.getElementById('aiSuggestionsContainer');
    const subjectInput = container.querySelectorAll('input[type="text"]')[index];
    if (subjectInput) {
        document.getElementById('emailSubject').value = subjectInput.value;
        hideAISuggestions();
        showNotification('Subject applied!', 'success');
    }
}

// Use enhanced content
function useEnhancedContent(event) {
    // Prevent any form submission or event propagation
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    const enhancedContent = document.getElementById('enhancedContent')?.value;
    if (enhancedContent) {
        console.log('useEnhancedContent called - applying enhanced content');
        document.getElementById('emailBody').value = enhancedContent;
        hideAISuggestions();
        showNotification('Enhanced content applied! You can now review and send the email.', 'success');
        
        // Scroll to the email form to make it visible
        const emailForm = document.getElementById('emailSubject');
        if (emailForm) {
            emailForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        console.log('useEnhancedContent completed - email should NOT be sent');
    }
}

// Show original content
function showOriginalContent() {
    const container = document.getElementById('aiSuggestionsContainer');
    if (container) {
        container.classList.add('hidden');
    }
}

// Hide AI suggestions
function hideAISuggestions() {
    const container = document.getElementById('aiSuggestionsContainer');
    if (container) {
        container.classList.add('hidden');
    }
}

// Show AI loading state
function showAILoadingState(message = 'Generating AI suggestions...') {
    const container = document.getElementById('aiSuggestionsContainer');
    if (!container) return;
    
    container.innerHTML = `
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex items-center space-x-3">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                <span class="text-gray-600">${message}</span>
            </div>
        </div>
    `;
    container.classList.remove('hidden');
}

// Missing functions that are called from HTML
function showSubscriptionDashboard() {
    const modal = document.getElementById('subscriptionDashboardModal');
    if (modal) {
        modal.classList.remove('hidden');
        updateSubscriptionDashboard();
    }
}

function closeSubscriptionDashboard() {
    const modal = document.getElementById('subscriptionDashboardModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function visitOfficialPage() {
    const program = currentProgramDetails;
    if (program && program.university && program.university.website) {
        window.open(program.university.website, '_blank');
    } else {
        showNotification('Official website not available', 'error');
    }
}

function scrollToSubscription() {
    const section = document.getElementById('subscription');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function updateSubscriptionDashboard() {
    // Update current plan display
    const currentPlanBadge = document.getElementById('currentPlanBadge');
    if (currentPlanBadge) {
        currentPlanBadge.textContent = userSubscription.plan.charAt(0).toUpperCase() + userSubscription.plan.slice(1);
    }
    
    // Update usage statistics
    const emailsUsed = document.getElementById('emailsUsed');
    const emailsProgress = document.getElementById('emailsProgress');
    const emailsLimit = document.getElementById('emailsLimit');
    
    if (emailsUsed) emailsUsed.textContent = userSubscription.emailsUsed;
    if (emailsLimit) emailsLimit.textContent = `${userSubscription.emailsUsed} / ${userSubscription.emailsLimit}`;
    if (emailsProgress) {
        const percentage = userSubscription.emailsLimit > 0 ? (userSubscription.emailsUsed / userSubscription.emailsLimit) * 100 : 0;
        emailsProgress.style.width = `${Math.min(percentage, 100)}%`;
    }
    
    const searchesUsed = document.getElementById('searchesUsed');
    const searchesProgress = document.getElementById('searchesProgress');
    const searchesLimit = document.getElementById('searchesLimit');
    
    if (searchesUsed) searchesUsed.textContent = userSubscription.searchesUsed;
    if (searchesLimit) searchesLimit.textContent = `${userSubscription.searchesUsed} / ${userSubscription.searchesLimit}`;
    if (searchesProgress) {
        const percentage = userSubscription.searchesLimit === 'unlimited' ? 0 : (userSubscription.searchesUsed / userSubscription.searchesLimit) * 100;
        searchesProgress.style.width = `${Math.min(percentage, 100)}%`;
    }
}

// Handle email form submission
async function handleEmailSubmit(e) {
    e.preventDefault();
    console.log('=== EMAIL FORM SUBMISSION STARTED ===');
    
    if (!currentUser) {
        showNotification('Please login to send emails', 'error');
        return;
    }
    
    // Get form data
    const subject = document.getElementById('emailSubject').value;
    const body = document.getElementById('emailBody').value;
    
    if (!subject || !body) {
        showNotification('Please fill in both subject and message', 'error');
        return;
    }
    
    // Get coordinator information from the modal
    const coordinatorInfo = document.getElementById('coordinatorDetails');
    if (!coordinatorInfo) {
        showNotification('Coordinator information not found', 'error');
        return;
    }
    
    console.log('Coordinator info element:', coordinatorInfo);
    console.log('Coordinator info HTML:', coordinatorInfo.innerHTML);
    console.log('Coordinator info text:', coordinatorInfo.textContent);
    
    // Extract coordinator email from the coordinator info
    let coordinatorEmail = null;
    
    // Try to find the email in the HTML structure
    const paragraphs = coordinatorInfo.querySelectorAll('p');
    for (let p of paragraphs) {
        const text = p.textContent;
        if (text.includes('Email:')) {
            const emailMatch = text.match(/Email:\s*([^\s\n]+)/);
            if (emailMatch) {
                coordinatorEmail = emailMatch[1];
                break;
            }
        }
    }
    
    // Fallback: try to extract from the entire text content
    if (!coordinatorEmail) {
        const coordinatorText = coordinatorInfo.textContent;
        const emailMatch = coordinatorText.match(/Email:\s*([^\s\n]+)/);
        if (emailMatch) {
            coordinatorEmail = emailMatch[1];
        }
    }
    
    // Check if email is valid (not "No email available")
    if (!coordinatorEmail || coordinatorEmail === 'No email available') {
        showNotification('Coordinator email not found or not available', 'error');
        return;
    }
    
    console.log('Extracted coordinator email:', coordinatorEmail);
    
    // Get the current program ID (you might need to store this when opening the modal)
    const programId = currentProgramId || 1; // Default fallback
    
    // Get the preferred email provider from user settings
    const emailProvider = getConnectedEmailProvider();
    if (!emailProvider) {
        showNotification('No email provider connected. Please connect Gmail or Outlook first.', 'error');
        return;
    }
    
    // Disable the send button
    const sendBtn = document.getElementById('sendEmailBtn');
    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Sending...';
    }
    
    try {
        console.log('Sending email with data:', {
            coordinator_email: coordinatorEmail,
            subject: subject,
            body: body,
            program_id: programId,
            email_provider: emailProvider
        });
        
        // Get CSRF token from cookies
        const csrfToken = getCookie('csrftoken');
        
        const response = await fetch(`${API_BASE_URL}/send-email/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'X-CSRFToken': csrfToken
            },
            credentials: 'include', // Include cookies for CSRF
            body: JSON.stringify({
                coordinator_email: coordinatorEmail,
                subject: subject,
                body: body,
                program_id: programId,
                email_provider: emailProvider
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification(`Email sent successfully via ${emailProvider}!`, 'success');
            closeEmailModal();
            
            // Update email usage
            if (userSubscription.emailsUsed < userSubscription.emailsLimit) {
                userSubscription.emailsUsed++;
                saveSubscriptionData();
                updateUserSubscriptionDisplay();
            }
        } else {
            showNotification(data.error || 'Failed to send email', 'error');
        }
        
    } catch (error) {
        console.error('Email sending error:', error);
        showNotification('Failed to send email. Please try again.', 'error');
    } finally {
        // Re-enable the send button
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="fas fa-paper-plane mr-2"></i>Send Email';
        }
    }
}

// Get the connected email provider
function getConnectedEmailProvider() {
    // Check localStorage for connected providers
    const gmailConnected = localStorage.getItem('gmailConnected') === 'true';
    const outlookConnected = localStorage.getItem('outlookConnected') === 'true';
    
    if (gmailConnected) return 'gmail';
    if (outlookConnected) return 'outlook';
    
    // Check from user settings
    const defaultProvider = document.getElementById('defaultEmailProvider');
    if (defaultProvider) {
        return defaultProvider.value;
    }
    
    return null;
}

// Get cookie value by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Global variables that might be missing
let currentProgramDetails = null;

console.log('UniWorld app.js loaded successfully!');