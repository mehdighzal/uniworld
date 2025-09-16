# UniWorld Testing Guide

## 🧪 Complete Testing Checklist

### 1. **Backend API Testing**

#### Test Universities API:
```bash
curl -s http://127.0.0.1:8000/api/universities/
```
**Expected**: JSON response with universities array

#### Test Programs API:
```bash
curl -s http://127.0.0.1:8000/api/programs/
```
**Expected**: JSON response with programs array

#### Test Search API:
```bash
curl -s "http://127.0.0.1:8000/api/search/?country=Italy"
```
**Expected**: JSON response with filtered programs

#### Test Countries API:
```bash
curl -s http://127.0.0.1:8000/api/countries/
```
**Expected**: JSON response with countries array

#### Test Fields of Study API:
```bash
curl -s http://127.0.0.1:8000/api/fields-of-study/
```
**Expected**: JSON response with fields array

### 2. **Frontend Testing**

#### Test User Registration:
1. Open browser console (F12)
2. Click "Register" button
3. Fill in: username, email, password
4. Submit form
5. **Expected Console Output**:
   ```
   === REGISTER ATTEMPT STARTED ===
   Register data: {username: "testuser", email: "test@test.com", passwordLength: 7}
   Sending register request: {username: "testuser", email: "test@test.com", password: "test123"}
   Register response status: 201
   === REGISTRATION SUCCESSFUL ===
   ```

#### Test User Login:
1. Click "Login" button
2. Use registered credentials
3. Submit form
4. **Expected Console Output**:
   ```
   === LOGIN ATTEMPT STARTED ===
   Login credentials: {email: "test@test.com", passwordLength: 7}
   Sending login request: {username: "test@test.com", email: "test@test.com", password: "test123"}
   Login response status: 200
   === LOGIN SUCCESSFUL ===
   ```

#### Test Program Search:
1. Select filters (country, field of study, university)
2. Click "Search Programs"
3. **Expected Console Output**:
   ```
   Search function called
   Search filters: {country: "Italy", field: "...", university: ""}
   Search URL: http://127.0.0.1:8000/api/search/?country=Italy&field_of_study=...
   Search response status: 200
   Search results count: X
   Final results array: [array of programs]
   ```

#### Test View Program Details:
1. Click "View Details" on any program card
2. **Expected**: Beautiful modal with complete program information
3. **Expected Console Output**:
   ```
   View program details called for ID: 45
   Found program: {id: 45, name: "Advanced Molecular Sciences", ...}
   ```

#### Test Subscription System:
1. Click "Plans" in navigation
2. Click "Upgrade to Premium" or "Upgrade to Pro"
3. **Expected Console Output**:
   ```
   === SUBSCRIPTION ATTEMPT STARTED ===
   Plan type: premium
   Processing subscription for plan: premium
   Payment session created: {session_id: "..."}
   === SUBSCRIPTION SUCCESSFUL ===
   ```

#### Test Email Functionality:
1. View program details
2. Click "Email Coordinator"
3. Fill in subject and message
4. Click "Send Email"
5. **Expected Console Output**:
   ```
   === SENDING EMAIL TO COORDINATOR ===
   Email sent successfully!
   === EMAIL SENT SUCCESSFULLY ===
   ```

### 3. **Feature Testing Checklist**

#### ✅ User Authentication:
- [ ] User registration works
- [ ] User login works
- [ ] User logout works
- [ ] User data persists on page refresh
- [ ] Error handling for invalid credentials

#### ✅ Program Search & Filtering:
- [ ] Universities dropdown populates
- [ ] Countries dropdown populates
- [ ] Fields of study dropdown populates
- [ ] Search returns results
- [ ] Filters work correctly
- [ ] Search results display properly

#### ✅ Program Details:
- [ ] View Details button works
- [ ] Modal displays complete information
- [ ] Modal closes properly
- [ ] Visit University link works
- [ ] Email Coordinator button works

#### ✅ Subscription System:
- [ ] Free plan works (no email access)
- [ ] Premium plan activation works
- [ ] Pro plan activation works
- [ ] Subscription data persists
- [ ] User interface updates correctly
- [ ] Email limits enforced

#### ✅ Email Functionality:
- [ ] Email composition modal works
- [ ] Email templates pre-filled
- [ ] Email sending works
- [ ] Usage tracking works
- [ ] Email limits enforced
- [ ] Error handling for limits

### 4. **Browser Console Testing**

#### Expected Console Messages:
```
Loading universities for filter...
Universities API response status: 200
University filter loaded with 5 universities

Event listener attached: Login form event listener attached
Event listener attached: Register form event listener attached
Event listener attached: Search button event listener attached

=== LOGIN ATTEMPT STARTED ===
=== REGISTER ATTEMPT STARTED ===
=== SUBSCRIPTION ATTEMPT STARTED ===
=== SENDING EMAIL TO COORDINATOR ===
```

### 5. **Error Testing**

#### Test Error Scenarios:
1. **Invalid Login**: Use wrong credentials
2. **Empty Forms**: Submit empty registration/login forms
3. **Email Limits**: Try to send emails when limit reached
4. **No Subscription**: Try to email without subscription
5. **Network Issues**: Test with server offline

### 6. **Performance Testing**

#### Test Performance:
1. **Page Load**: Should load quickly
2. **Search Speed**: Search should return results quickly
3. **Modal Performance**: Modals should open/close smoothly
4. **Data Persistence**: Data should persist across page refreshes

## 🚀 Deployment Checklist

### Before Going Live:
- [ ] All APIs working correctly
- [ ] All frontend features working
- [ ] Error handling implemented
- [ ] User data persistence working
- [ ] Subscription system functional
- [ ] Email functionality working
- [ ] Console logs cleaned up (optional)
- [ ] Database populated with real data
- [ ] Stripe integration configured (for production)

## 🎯 Success Criteria

The UniWorld platform is ready when:
1. ✅ Users can register and login
2. ✅ Users can search and filter programs
3. ✅ Users can view detailed program information
4. ✅ Users can subscribe to plans
5. ✅ Users can email coordinators (with subscription)
6. ✅ All data persists across page refreshes
7. ✅ Error handling works properly
8. ✅ Console shows detailed debugging information

## 🔧 Troubleshooting

### Common Issues:
1. **APIs not responding**: Check Django server is running
2. **Login not working**: Check user exists in database
3. **Search not working**: Check API endpoints
4. **Subscription not persisting**: Check localStorage
5. **Email not working**: Check subscription status

### Debug Steps:
1. Open browser console (F12)
2. Check for error messages
3. Look for detailed debug logs
4. Test API endpoints directly
5. Check network tab for failed requests

---

**🎉 The UniWorld platform is now complete and ready for testing!**
