/**
 * Yojana Mitra - AngularJS 1.8.3 Application Module & Controller
 */

(function () {
  'use strict';

  var app = angular.module('yojanaMitraApp', []);

  // -------------------------------------------------------------
  // API Service
  // -------------------------------------------------------------
  app.factory('Api', ['$http', function ($http) {
    // Determine base URL:
    // If served via Django on port 8000, use relative '/api'
    // If opened via file:// or http://localhost:3000 / other port, use 'http://localhost:8000/api'
    var isSameHost = (window.location.port === '8000');
    var BASE_URL = isSameHost ? '/api' : 'http://localhost:8000/api';

    function getAuthHeaders() {
      var token = localStorage.getItem('ym_token');
      var headers = {
        'Content-Type': 'application/json'
      };
      if (token) {
        headers['Authorization'] = 'Bearer ' + token;
      }
      return headers;
    }

    return {
      getBaseUrl: function () {
        return BASE_URL;
      },
      setBaseUrl: function (url) {
        BASE_URL = url;
      },
      getTaxonomy: function () {
        return $http.get(BASE_URL + '/taxonomy');
      },
      requestOtp: function (email) {
        return $http.post(BASE_URL + '/auth/request-otp', { email: email });
      },
      verifyOtp: function (email, code) {
        return $http.post(BASE_URL + '/auth/verify-otp', { email: email, code: code });
      },
      getMe: function () {
        return $http.get(BASE_URL + '/me', { headers: getAuthHeaders() });
      },
      updateProfile: function (profile) {
        return $http.put(BASE_URL + '/me/profile', { profile: profile }, { headers: getAuthHeaders() });
      },
      toggleSaved: function (slug) {
        return $http.post(BASE_URL + '/me/saved/' + encodeURIComponent(slug), {}, { headers: getAuthHeaders() });
      },
      getSchemes: function () {
        return $http.get(BASE_URL + '/schemes', { headers: getAuthHeaders() });
      },
      getScheme: function (slug) {
        return $http.get(BASE_URL + '/schemes/' + encodeURIComponent(slug), { headers: getAuthHeaders() });
      }
    };
  }]);

  // -------------------------------------------------------------
  // Main Controller
  // -------------------------------------------------------------
  app.controller('MainCtrl', ['$scope', '$timeout', 'Api', function ($scope, $timeout, Api) {
    // Current Active Screen: 'welcome' | 'form' | 'dashboard' | 'detail' | 'profile'
    $scope.currentScreen = 'welcome';
    $scope.theme = localStorage.getItem('ym_theme') || 'light';
    $scope.toasts = [];

    // State lists & dictionaries
    $scope.statesList = [
      "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
      "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
      "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
      "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
      "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
      "Uttar Pradesh", "Uttarakhand", "West Bengal",
      "Andaman and Nicobar Islands", "Chandigarh",
      "Dadra and Nagar Haveli and Daman and Diu", "Delhi (NCT)",
      "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ];

    // Taxonomy dictionary
    $scope.taxonomy = {};
    $scope.categoriesList = [];

    // Auth & User State
    $scope.currentUser = null;
    $scope.token = localStorage.getItem('ym_token') || null;

    // Login Form State
    $scope.authForm = {
      email: '',
      code: '',
      otpRequested: false,
      devOtp: null,
      loading: false,
      errorMsg: null,
      successMsg: null
    };

    // Wizard Form State
    $scope.formStep = 1;
    $scope.categorySearch = '';
    $scope.profileForm = {
      name: '',
      age: 28,
      gender: 'Male',
      state: 'Uttar Pradesh',
      area: 'Rural',
      income: 150000,
      land: 'Small/Marginal (< 5 Acres)',
      bpl: false,
      categories: ['Farmer', 'Rural Household'],
      subCategories: ['Small/Marginal Farmer', 'Land Owner'],
      occupation: 'Farmer / Self-Employed',
      interest: 'Agricultural Subsidies & Health'
    };

    // Dashboard State
    $scope.schemes = [];
    $scope.selectedScheme = null;
    $scope.selectedCategoryGroup = null;
    $scope.stats = {
      total: 0,
      eligible: 0,
      mismatch: 0,
      rate: 0,
      saved: 0
    };

    $scope.filters = {
      search: '',
      category: 'All',
      status: 'All',
      savedOnly: false
    };

    // SVG Ring Progress Calculations
    $scope.circleRadius = 36;
    $scope.circleCircumference = 2 * Math.PI * $scope.circleRadius; // ~226.2

    $scope.getDashOffset = function () {
      var rate = $scope.stats.rate || 0;
      return $scope.circleCircumference - ($scope.circleCircumference * (rate / 100));
    };

    // -----------------------------------------------------------
    // Initialization
    // -----------------------------------------------------------
    $scope.init = function () {
      // Apply theme
      document.documentElement.setAttribute('data-theme', $scope.theme);

      // Load Taxonomy
      Api.getTaxonomy().then(function (res) {
        if (res.data && res.data.taxonomy) {
          $scope.taxonomy = res.data.taxonomy;
          $scope.categoriesList = res.data.categories || Object.keys(res.data.taxonomy);
        }
      }).catch(function (err) {
        console.warn("Could not load remote taxonomy, fallback ready", err);
      });

      // Check if user is logged in
      var storedUser = localStorage.getItem('ym_user');
      if ($scope.token && storedUser) {
        try {
          $scope.currentUser = JSON.parse(storedUser);
          $scope.syncProfileFormFromUser();
          $scope.loadDashboardData();
          $scope.currentScreen = 'dashboard';
        } catch (e) {
          $scope.currentUser = null;
          $scope.currentScreen = 'welcome';
        }
      } else {
        $scope.currentScreen = 'welcome';
      }
    };

    // -----------------------------------------------------------
    // Theme Management
    // -----------------------------------------------------------
    $scope.toggleTheme = function () {
      $scope.theme = ($scope.theme === 'light') ? 'dark' : 'light';
      localStorage.setItem('ym_theme', $scope.theme);
      document.documentElement.setAttribute('data-theme', $scope.theme);
      $scope.showToast('Theme switched to ' + $scope.theme + ' mode', 'info');
    };

    // -----------------------------------------------------------
    // Toast Messages
    // -----------------------------------------------------------
    $scope.showToast = function (text, type) {
      var toast = { id: Date.now(), text: text, type: type || 'info' };
      $scope.toasts.push(toast);
      $timeout(function () {
        var idx = $scope.toasts.indexOf(toast);
        if (idx !== -1) {
          $scope.toasts.splice(idx, 1);
        }
      }, 4000);
    };

    // -----------------------------------------------------------
    // Authentication Handlers
    // -----------------------------------------------------------
    $scope.requestOtp = function () {
      if (!$scope.authForm.email) {
        $scope.authForm.errorMsg = "Please enter your Gmail address.";
        return;
      }
      var email = $scope.authForm.email.trim().toLowerCase();
      if (!email.endsWith('@gmail.com')) {
        $scope.authForm.errorMsg = "Only @gmail.com addresses are permitted (e.g. citizen@gmail.com).";
        return;
      }

      $scope.authForm.loading = true;
      $scope.authForm.errorMsg = null;
      $scope.authForm.successMsg = null;

      Api.requestOtp(email).then(function (res) {
        $scope.authForm.loading = false;
        $scope.authForm.otpRequested = true;
        $scope.authForm.successMsg = res.data.message || "OTP generated successfully.";
        if (res.data.dev_otp) {
          $scope.authForm.devOtp = res.data.dev_otp;
          $scope.showToast("Development OTP: " + res.data.dev_otp, 'info');
        } else {
          $scope.showToast("Verification OTP sent to your Gmail inbox.", 'success');
        }
      }).catch(function (err) {
        $scope.authForm.loading = false;
        var msg = (err.data && err.data.message) ? err.data.message : "Failed to generate OTP.";
        $scope.authForm.errorMsg = msg;
        $scope.showToast(msg, 'error');
      });
    };

    $scope.fillDevOtp = function () {
      if ($scope.authForm.devOtp) {
        $scope.authForm.code = $scope.authForm.devOtp;
      }
    };

    $scope.verifyOtp = function () {
      if (!$scope.authForm.code || $scope.authForm.code.length !== 6) {
        $scope.authForm.errorMsg = "Please enter the 6-digit verification code.";
        return;
      }

      $scope.authForm.loading = true;
      $scope.authForm.errorMsg = null;

      Api.verifyOtp($scope.authForm.email, $scope.authForm.code).then(function (res) {
        $scope.authForm.loading = false;
        $scope.token = res.data.token;
        $scope.currentUser = res.data.user;
        localStorage.setItem('ym_token', $scope.token);
        localStorage.setItem('ym_user', JSON.stringify($scope.currentUser));

        $scope.showToast("Namaste! Successfully logged in.", 'success');

        // Check if user has an existing complete profile
        var profile = $scope.currentUser.profile;
        var hasProfile = profile && profile.name && profile.categories && profile.categories.length > 0;

        if (hasProfile) {
          $scope.syncProfileFormFromUser();
          $scope.loadDashboardData();
          $scope.currentScreen = 'dashboard';
        } else {
          // Send to eligibility wizard form
          $scope.syncProfileFormFromUser();
          $scope.formStep = 1;
          $scope.currentScreen = 'form';
        }
      }).catch(function (err) {
        $scope.authForm.loading = false;
        var msg = (err.data && err.data.message) ? err.data.message : "Verification failed. Check your OTP.";
        $scope.authForm.errorMsg = msg;
        $scope.showToast(msg, 'error');
      });
    };

    $scope.logout = function () {
      localStorage.removeItem('ym_token');
      localStorage.removeItem('ym_user');
      $scope.token = null;
      $scope.currentUser = null;
      $scope.schemes = [];
      $scope.authForm = {
        email: '',
        code: '',
        otpRequested: false,
        devOtp: null,
        loading: false,
        errorMsg: null,
        successMsg: null
      };
      $scope.currentScreen = 'welcome';
      $scope.showToast("You have been signed out.", 'info');
    };

    // -----------------------------------------------------------
    // Wizard & Profile Form
    // -----------------------------------------------------------
    $scope.syncProfileFormFromUser = function () {
      if ($scope.currentUser && $scope.currentUser.profile) {
        var p = $scope.currentUser.profile;
        $scope.profileForm.name = p.name || '';
        $scope.profileForm.age = p.age || 28;
        $scope.profileForm.gender = p.gender || 'Male';
        $scope.profileForm.state = p.state || 'Uttar Pradesh';
        $scope.profileForm.area = p.area || 'Rural';
        $scope.profileForm.income = (p.income !== undefined) ? p.income : 150000;
        $scope.profileForm.land = p.land || 'Small/Marginal (< 5 Acres)';
        $scope.profileForm.bpl = !!p.bpl;
        $scope.profileForm.categories = angular.copy(p.categories || []);
        $scope.profileForm.subCategories = angular.copy(p.subCategories || []);
        $scope.profileForm.occupation = p.occupation || '';
        $scope.profileForm.interest = p.interest || '';
      }
    };

    $scope.setFormStep = function (step) {
      if (step >= 1 && step <= 3) {
        $scope.formStep = step;
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    };

    // Multi-Select Category Logic
    $scope.isCategorySelected = function (cat) {
      return $scope.profileForm.categories.indexOf(cat) !== -1;
    };

    $scope.toggleCategory = function (cat) {
      var idx = $scope.profileForm.categories.indexOf(cat);
      if (idx !== -1) {
        $scope.profileForm.categories.splice(idx, 1);
        // Also remove any subcategories belonging to this unselected category
        if ($scope.taxonomy[cat]) {
          var subs = $scope.taxonomy[cat];
          $scope.profileForm.subCategories = $scope.profileForm.subCategories.filter(function (sc) {
            return subs.indexOf(sc) === -1;
          });
        }
      } else {
        $scope.profileForm.categories.push(cat);
      }
    };

    // Multi-Select Subcategory Logic
    $scope.isSubCategorySelected = function (subCat) {
      return $scope.profileForm.subCategories.indexOf(subCat) !== -1;
    };

    $scope.toggleSubCategory = function (subCat) {
      var idx = $scope.profileForm.subCategories.indexOf(subCat);
      if (idx !== -1) {
        $scope.profileForm.subCategories.splice(idx, 1);
      } else {
        $scope.profileForm.subCategories.push(subCat);
      }
    };

    $scope.saveProfile = function () {
      if (!$scope.profileForm.name) {
        $scope.showToast("Please enter your full name.", 'error');
        $scope.formStep = 1;
        return;
      }
      if ($scope.profileForm.categories.length === 0) {
        $scope.showToast("Please select at least one identity category.", 'error');
        $scope.formStep = 3;
        return;
      }

      Api.updateProfile($scope.profileForm).then(function (res) {
        $scope.currentUser = res.data.user;
        localStorage.setItem('ym_user', JSON.stringify($scope.currentUser));
        $scope.showToast("Citizen profile successfully saved! Refreshing eligibility...", 'success');
        $scope.loadDashboardData();
        $scope.currentScreen = 'dashboard';
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }).catch(function (err) {
        var msg = (err.data && err.data.message) ? err.data.message : "Failed to update profile.";
        $scope.showToast(msg, 'error');
      });
    };

    // -----------------------------------------------------------
    // Dashboard & Schemes
    // -----------------------------------------------------------
    $scope.loadDashboardData = function () {
      Api.getSchemes().then(function (res) {
        if (res.data) {
          $scope.schemes = res.data.schemes || [];
          $scope.stats.total = res.data.total || $scope.schemes.length;
          $scope.stats.eligible = res.data.eligible_count || 0;
          $scope.stats.mismatch = res.data.criteria_mismatch_count || 0;
          $scope.stats.rate = res.data.overall_match_rate || 0;

          // Compute saved count
          $scope.stats.saved = $scope.schemes.filter(function (s) {
            return s.is_saved;
          }).length;
        }
      }).catch(function (err) {
        $scope.showToast("Error retrieving schemes data.", 'error');
      });
    };

    // Toggle Saved Scheme
    $scope.toggleSavedScheme = function (scheme, $event) {
      if ($event) {
        $event.stopPropagation();
      }
      if (!$scope.token) {
        $scope.showToast("Please log in to save schemes.", 'error');
        return;
      }

      Api.toggleSaved(scheme.slug).then(function (res) {
        scheme.is_saved = res.data.is_saved;
        if ($scope.currentUser) {
          $scope.currentUser.saved_schemes = res.data.saved_schemes;
          localStorage.setItem('ym_user', JSON.stringify($scope.currentUser));
        }
        $scope.stats.saved = $scope.schemes.filter(function (s) {
          return s.is_saved;
        }).length;
        $scope.showToast(res.data.message, 'success');
      }).catch(function (err) {
        $scope.showToast("Could not update bookmark.", 'error');
      });
    };

    // Filtering logic
    $scope.filterScheme = function (scheme) {
      // 1. Search Query
      if ($scope.filters.search) {
        var q = $scope.filters.search.toLowerCase();
        var matchName = scheme.name.toLowerCase().indexOf(q) !== -1;
        var matchCat = scheme.cat.toLowerCase().indexOf(q) !== -1;
        var matchTag = (scheme.tagline || '').toLowerCase().indexOf(q) !== -1;
        var matchBeneficiary = (scheme.beneficiaries || '').toLowerCase().indexOf(q) !== -1;
        if (!matchName && !matchCat && !matchTag && !matchBeneficiary) {
          return false;
        }
      }

      // 2. Category filter
      if ($scope.filters.category && $scope.filters.category !== 'All') {
        var catMatch = (scheme.cat === $scope.filters.category) ||
          (scheme.target_categories && scheme.target_categories.indexOf($scope.filters.category) !== -1);
        if (!catMatch) {
          return false;
        }
      }

      // 3. Status filter
      if ($scope.filters.status && $scope.filters.status !== 'All') {
        if (!scheme.eligibility) {
          return false;
        }
        if ($scope.filters.status === 'ELIGIBLE' && !scheme.eligibility.is_eligible) {
          return false;
        }
        if ($scope.filters.status === 'CRITERIA_MISMATCH' && scheme.eligibility.status !== 'CRITERIA_MISMATCH') {
          return false;
        }
        if ($scope.filters.status === 'NOT_ELIGIBLE' && scheme.eligibility.status !== 'NOT_ELIGIBLE') {
          return false;
        }
      }

      // 4. Saved only
      if ($scope.filters.savedOnly && !scheme.is_saved) {
        return false;
      }

      return true;
    };

    // -----------------------------------------------------------
    // Scheme Detail View
    // -----------------------------------------------------------
    $scope.viewSchemeDetail = function (scheme) {
      $scope.selectedScheme = scheme;
      $scope.currentScreen = 'detail';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    $scope.backToDashboard = function () {
      $scope.currentScreen = 'dashboard';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    $scope.openProfile = function () {
      $scope.syncProfileFormFromUser();
      $scope.currentScreen = 'profile';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    $scope.openEditProfileWizard = function () {
      $scope.syncProfileFormFromUser();
      $scope.formStep = 1;
      $scope.currentScreen = 'form';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Category filter in Step 3
    $scope.filterCategoryName = function (cat) {
      if (!$scope.categorySearch) return true;
      return cat.toLowerCase().indexOf($scope.categorySearch.toLowerCase()) !== -1;
    };

    // Start App
    $scope.init();
  }]);

})();
