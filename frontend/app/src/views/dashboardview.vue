<template>
  <div id="app">
    <div class="navbar">

      <div class="nav-left">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
          <path fill="#075e54"
            d="M160 368c26.5 0 48 21.5 48 48l0 16 72.5-54.4c8.3-6.2 18.4-9.6 28.8-9.6L448 368c8.8 0 16-7.2 16-16l0-288c0-8.8-7.2-16-16-16L64 48c-8.8 0-16 7.2-16 16l0 288c0 8.8 7.2 16 16 16l96 0zm48 124l-.2 .2-5.1 3.8-17.1 12.8c-4.8 3.6-11.3 4.2-16.8 1.5s-8.8-8.2-8.8-14.3l0-21.3 0-6.4 0-.3 0-4 0-48-48 0-48 0c-35.3 0-64-28.7-64-64L0 64C0 28.7 28.7 0 64 0L448 0c35.3 0 64 28.7 64 64l0 288c0 35.3-28.7 64-64 64l-138.7 0L208 492z" />
        </svg>
        <div class="logo"> WotNot</div>
        <div class="nav-item" v-for="section in navItems" :key="section.name" @click="navigate(section.path)"
          :class="{ active: isActive(section.path)}">
          <i :class="section.icon"></i>{{ section.label }}        
        </div>
      </div>

      <div class="nav-right">

        <!-- Wallet Button with Icon -->
        <div class="wallet-section">
          <button @click="toggleWalletModal" class="wallet-btn">
            <i class="bi bi-wallet2"></i>
          </button>
        </div>

        <div class="flex" v-if="user">

          <p class="text-green-700"> {{ user.email }}</p>
        </div>
        <div v-else>
          <p class="text-gray-600">Session Expired</p>
        </div>


        <div class="profile-dropdown" @click="toggleDropdown" ref="profileDropdown">
          <!-- <img src="../assets/—Pngtree—avatar icon profile icon member_5247852.png" alt="Profile"
            class="profile-icon" /> -->
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
              <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
              <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
            </svg>

          <div v-if="dropdownOpen" class="dropdown-menu" ref="dropdownMenu">
            <ul>
              <li @click="goToProfile"><i class="bi bi-person-circle"></i> View Profile</li>
              <li @click="goToPurchaseHistory"><i class="bi bi-currency-rupee"></i> Purchase History </li>
              <li @click="goToSettings"><i class="bi bi-gear-fill"></i> Settings</li>
              <li @click="logout"><i class="bi bi-box-arrow-right"></i> Logout</li>
            </ul>
          </div>
        </div>

        
      </div>


    </div>

    <!-- Wallet Modal Pop-up -->
    <div v-if="walletModalOpen" class="modal-overlay" >
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Wallet</h2>
          <!-- X Close Button -->
          <span class="close-btn" @click="toggleWalletModal">&times;</span>
        </div>
        <p><strong>Current Balance:</strong> {{ currentBalance }}</p>
        <button @click="topUpBalance" class="topup-btn">Top Up Balance</button>
      </div>
    </div>

    <div class="flex flex-1">
      <!-- Hamburger button for mobile view -->
      <button @click="isMenuOpen = !isMenuOpen" class="p-2 md:hidden">
        <i class="bi bi-list text-2xl z-[1000] absolute top-[60px]"></i>
      </button>

      <!-- Broadcast Section Sidebar -->
      <div
        class="fixed top-12 left-0 w-64 h-[calc(100vh-65px)] bg-gray-100 p-4 overflow-y-auto mt-4 z-50 transform md:transform-none transition-transform duration-300 ease-in-out"
        :class="{ '-translate-x-full': !isMenuOpen, 'translate-x-0': isMenuOpen }"
        v-if="currentSection === 'broadcast'">
        <a href="#" @click.prevent="navigate('/broadcast/broadcast2')"
          :class="{ 'text-green-900 font-semibold': isActive('/broadcast/broadcast2'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/broadcast/broadcast2')}"
          class="block p-3 text-gray-600 rounded-lg ">
          <i class="bi bi-broadcast mr-2"></i>Broadcast Messages
        </a>
        <a href="#" @click.prevent="navigate('/broadcast/broadcast1')"
          :class="{ 'text-green-900 font-semibold': isActive('/broadcast/broadcast1') ,'hover:bg-gray-200 hover:font-semibold': !isActive('/broadcast/broadcast1') }"
          class="block p-3 text-gray-600 rounded-lg ">
          <i class="bi bi-chat-right-text-fill mr-2"></i>Manage Templates
        </a>
        <a href="#" @click.prevent="navigate('/broadcast/broadcast3')"
          :class="{ 'text-green-900 font-semibold': isActive('/broadcast/broadcast3'),'hover:bg-gray-200 hover:font-semibold': !isActive('/broadcast/broadcast3') }"
          class="block p-3 text-gray-600 rounded-lg ">
          <i class="bi bi-calendar2-range-fill mr-2"></i>Scheduled Broadcasts
        </a>
      </div>

      <!-- Contacts Section Sidebar -->
      <div
        class="fixed top-12 left-0 w-64 h-[calc(100vh-65px)] bg-gray-100 p-4  overflow-y-auto mt-4 z-50 transform md:transform-none transition-transform duration-300 ease-in-out"
        :class="{ '-translate-x-full': !isMenuOpen, 'translate-x-0': isMenuOpen }" v-if="currentSection === 'Contacts'">
        <a href="#" @click.prevent="navigate('/contacts/contacts1')"
          :class="{ 'text-green-900 font-semibold': isActive('/contacts/contacts1'), 'hover:bg-gray-200 hover:font-semibold': !isActive('/contacts/contacts1')  }"
          class="block p-3 text-gray-600 rounded-lg ">
          <i class="bi bi-journal-bookmark-fill mr-2 "></i>Manage Contacts
        </a>
        <a href="#" @click.prevent="navigate('/contacts/contacts2')"
          :class="{ 'text-green-900 font-semibold': isActive('/contacts/contacts2'),'hover:bg-gray-200 hover:font-semibold': !isActive('/contacts/contacts2')  }"
          class="block p-3 text-gray-600 rounded-lg ">
          <i class="bi bi-tags-fill mr-2"></i>Manage Tags
        </a>
      </div>

      <!-- Integration Section Sidebar -->
      <div
        class="fixed top-12 left-0 w-64 h-[calc(100vh-65px)] bg-gray-100 p-4  overflow-y-auto mt-4 z-50 transform md:transform-none transition-transform duration-300 ease-in-out"
        :class="{ '-translate-x-full': !isMenuOpen, 'translate-x-0': isMenuOpen }" v-if="currentSection === 'Integration'">
        <a href="#" @click.prevent="navigate('/integration/integration1')"
          :class="{ 'text-green-900 font-semibold': isActive('/integration/integration1') ,'hover:bg-gray-200 hover:font-semibold': !isActive('/integration/integration1') }"
          class="block p-3 text-gray-600 rounded-lg  "><i class="bi bi-link-45deg"></i>
          Integration
        </a>
      </div>
  <!--    <div v-if="currentSection === 'Chatbot'" class="flex-1 mt-16 p-8 bg-white overflow-y-auto h-[calc(100vh-65px)]">
  <router-view></router-view>
</div>-->
<!--<ActiveChatsSidebar v-if="currentSection === 'Chatbot'" class="fixed top-12 left-0 w-64 h-[calc(100vh-65px)] bg-gray-100 p-4 overflow-y-auto mt-4 z-50 transform md:transform-none transition-transform duration-300 ease-in-out" :class="{ '-translate-x-full': !isMenuOpen, 'translate-x-0': isMenuOpen }" />-->



      <!-- Main Content-->
      <div class="flex-1 mt-16  p-8 bg-white overflow-y-auto h-[calc(100vh-65px)] ">
        <router-view></router-view>
      </div>

      <!-- Profile Popup -->
      <ProfilePopup :visible="showProfilePopup" :user="user" @close="showProfilePopup = false" />
    </div>

  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router';
import ProfilePopup from './profile.vue';

export default {
  name: 'DashboardView',
  components: {
    ProfilePopup
  },
  data() {
    return {
      localUser: {
        whatsapp_business_id: '', 
        // currentBalance: 0 ,
      },
      navItems: [
        { name: 'broadcast', label: 'Broadcast', icon: 'bi bi-broadcast', path: '/broadcast/broadcast2' },
        { name: 'Contacts', label: 'Contacts', icon: 'bi bi-person-video2', path: '/contacts/contacts1' },
        { name: 'Integration', label: 'Integration', icon: 'bi bi-plugin', path: '/integration/integration1' },
        { name: 'chatbot', label: 'Chatbot', path: '/chatbot/chatbotview', icon: 'bi bi-robot' }
      ],
      user: null,
      dropdownOpen: false,
      showProfilePopup: false,
      isMenuOpen: false,
      walletModalOpen: false ,
      currentBalance: 0
    }
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const isActive = (path) => route.path === path;
    const navigate = (path) => {
      router.push(path);
    }

    return {
      navigate,
      isActive,
      currentSection: getSectionFromRoute(route.path),


    };
  },
  watch: {
    '$route.path': function (newPath) {
      this.currentSection = getSectionFromRoute(newPath);
    }
  },




  async mounted() {
    await this.fetchUserDetails() ;
    await this.created();
    document.addEventListener('click', this.handleOutsideClick);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleOutsideClick);
  },

  methods: {
    async created() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        this.user = await response.json();
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },

    async fetchUserDetails() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        const data = await response.json();
        this.localUser.whatsapp_business_id = data['Whatsapp_Business_Id'];
        
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },

    async fetchWalletDetails(accountId) {
    try {
        
        const response = await fetch(`http://localhost:8000/conversations-cost/${accountId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        
        // Check if the response is ok (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        // Parse the JSON data from the response
        const costData = await response.json();
        
        // Set the current balance using the response data
        this.currentBalance = costData;
        this.currentBalance = this.currentBalance.toFixed(3) ; // Assuming the response directly gives the balance
        
        
    } catch (error) {
        console.error('Error fetching wallet details:', error);
        // Handle errors accordingly, e.g., show an error message to the user
        return null; // Or any default value or error handling logic
    }
},

    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    async toggleWalletModal() {
      this.walletModalOpen = !this.walletModalOpen;
      const walletOpen= this.walletModalOpen

      if(walletOpen){
        await this.fetchWalletDetails(this.localUser.whatsapp_business_id)
      }
      

    },
    topUpBalance() {
      alert('Coming Soon...');
    },
    goToProfile() {
      this.showProfilePopup = true;
    },
    goToSettings() {
      this.$router.push('/settings');
    },
    goToPurchaseHistory() {
      this.$router.push('/purchase-history');
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },

    handleOutsideClick(event) {
    // Check if the click is outside the dropdown element
    const dropdownMenu = this.$refs.dropdownMenu; // Use $refs to access the dropdown menu element
    const profileDropdown = this.$refs.profileDropdown; // Use $refs to access the profile dropdown element

    if (dropdownMenu && !dropdownMenu.contains(event.target) && profileDropdown && !profileDropdown.contains(event.target)) {
      this.dropdownOpen = false; // Close dropdown
    }
  },
 
  }
}

function getSectionFromRoute(path) {
  if (path.startsWith('/broadcast')) return 'broadcast';
  if (path.startsWith('/contacts')) return 'Contacts';
  if (path.startsWith('/integration')) return 'Integration';
  if (path.startsWith('/chatbot')) return 'Chatbot'; // Add this line
  return 'broadcast';
}
</script>








<style>

body {
  font-family: Arial, sans-serif;
  margin: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  background-color: #f8f9fa;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-left,
.nav-right {
  display: flex;
}

.nav-right {
  align-items: center;
}

.logo {
  font-weight: 800;
  margin: 8px 0;
  padding-right: 30px;
  font-size: xx-large;
  color: #075e54;
}

svg {
  width: 62px;
  height: 62px;
  padding: 15px 10px 10px 10px;
  color: #075e54;
}

.nav-right svg {
  
  width: 36px;
  height: 36px;
  padding: 0;
  margin: 0 9px 0 9px;
  color: #525252;
  transition: all 0.3s ease;
}
.nav-right svg:hover{
  border-radius: 100%;
  padding: 0;
  width: 36px;
  height: 36px;
  transform: translateY(-3px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.nav-item {
  padding: 15px;
  cursor: pointer;
  color:#525252;
  text-align: center;
  margin: 8px 0;
  border-right: 1px solid #e9ecef;
  font-size: medium;
}

.userDetails {
  display: flex;
  margin-left: 300px;
}

.userDetails p {
  padding-left: 5px;
}

.profile-icon {
  width: 60px;
  height: 60px;
  cursor: pointer;
  margin-right: 5px;
}

.profile-dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 75px;
  right: 30px;
  width: 200px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  color: #525252;
}

.dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu li {
  padding: 10px;
  cursor: pointer;
  font-size: 18px;
}

.dropdown-menu li:hover {
  background-color: #f1f1f1;
}

.dropdown-menu li i {
  margin-right: 9px;
}

.logout {
  align-self: flex-end;
}

.nav-item i {
  padding-right: 9px;
}

.nav-item:hover {
  font-weight: 600;
  border-radius: 5px;
  color: #075e54;
}

.container-contacts {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  padding: 20px;
  text-align: left;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

form {
  display: flex;
  flex-direction: column;
}

select {
  width: 100%;
  padding: 10px;
  margin: 8px 0 20px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
}

h2 {
  color: #075e54;
  margin-bottom: 20px;
}


button {
  background-color: #075e54;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1ebd5b;
}
.wallet-section{
  margin-right:9px;
}
.wallet-btn {
  background: linear-gradient(45deg, #34eb83, #2ebf91);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px 10px;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.wallet-btn i {
  margin-left: 3px;
  margin-right: 3px;
}

.wallet-btn:hover {
  transform: translateY(-3px);
  background: linear-gradient(45deg, #28b479, #249e85);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Modal Content */
.modal-content {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  width: 400px;
  text-align: center;
  position: relative;
  animation: fadeIn 0.3s ease;
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

/* Close Button (X) */
.close-btn {
  position: absolute;
  right: 15px;
  top: 15px;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  color: #333;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #ff0000;
}

/* Top-Up Button */
.topup-btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px 30px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.topup-btn:hover {
  background-color: #218838;
}

/* Fade-in Animation for Modal */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

</style>