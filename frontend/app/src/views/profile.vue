
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-end z-50" v-if="visible" @click.self="close">
    <div class="w-80 h-full bg-white shadow-lg transform transition-transform duration-300" :class="visible ? 'translate-x-0' : 'translate-x-full'">
      <div class="flex justify-between items-center p-4 border-b border-gray-200">
        <h2 class="text-xl font-semibold text-gray-900">Profile Details</h2>
        <button @click="close" class="text-gray-600 hover:text-gray-900">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <form @submit.prevent="saveProfile" class="p-4 space-y-4">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email:</label>
          <div class="relative mt-1">
            <input type="email" id="email" v-model="localUser.email" :readonly="isEmailReadonly"
              class="block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Username:</label>
          <div class="relative mt-1">
            <input type="text" id="name" v-model="localUser.name" :readonly="isNameReadonly"
              class="block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
            
          </div>
        </div>

        <div>
          <label for="whatsapp_business_id" class="block text-sm font-medium text-gray-700">WhatsApp Business ID:</label>
          <input type="text" id="whatsapp_business_id" v-model="localUser.whatsapp_business_id" readonly
            class="block w-full p-2 mt-1 border border-gray-300 rounded-md shadow-sm sm:text-sm"
          />
        </div>

        <div>
          <label for="phone_id" class="block text-sm font-medium text-gray-700">Phone ID:</label>
          <input type="text" id="phone_id" v-model="localUser.phone_id" readonly
            class="block w-full p-2 mt-1 border border-gray-300 rounded-md shadow-sm sm:text-sm"
          />
        </div>

        <div>
          <label for="access_token" class="block text-sm font-medium text-gray-700">Access Token:</label>
          <input type="text" id="access_token" v-model="localUser.access_token" readonly
            class="block w-full p-2 mt-1 border border-gray-300 rounded-md shadow-sm sm:text-sm"
          />
        </div>

        <div class="mt-4">
          <button type="submit" class="w-full px-4 py-2 text-white bg-teal-600 hover:bg-teal-700 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2">
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ProfileSidebar',
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localUser: { ...this.user },
      isEmailReadonly: true,
      isNameReadonly: true
    };
  },
  watch: {
    visible: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchUserDetails();
        }
      }
    },
    user: {
      immediate: true,
      handler(newVal) {
        this.localUser = { ...newVal };
      }
    }
  },
  methods: {
    close() {
      this.$emit('close');
    },
    toggleEmailReadonly() {
      this.isEmailReadonly = !this.isEmailReadonly;
    },
    toggleNameReadonly() {
      this.isNameReadonly = !this.isNameReadonly;
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
        this.localUser.email = data.email;
        this.localUser.name = data.name;
        this.localUser.whatsapp_business_id = data['Whatsapp_Business_Id'];
        this.localUser.phone_id = data['Phone_id'];
        this.localUser.access_token = data['Access_Token'];
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },
    async saveProfile() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            email: this.localUser.email,
            name: this.localUser.name,
            Whatsapp_Business_Id: this.localUser.whatsapp_business_id,
            Phone_id: this.localUser.phone_id,
            Access_Token: this.localUser.access_token
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to save user details');
        }

        console.log('Profile saved', this.localUser);
        this.$emit('update:user', this.localUser);
        this.close();
      } catch (error) {
        console.error('Error saving user details:', error);
      }
    }
  }
};
</script>

<style scoped>

.profile-sidebar-overlay {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  z-index: 1000;
}

.profile-sidebar {
  width: 300px;
  right: 0;
  height: 100%;
  background: white;
  padding: 20px;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
}

.profile-sidebar-overlay .profile-sidebar {
  transform: translateX(0);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 2vw 0 4vw 0;
}

h2 {
  margin: 0;
}

.cancel-icon {
  cursor: pointer;
  color: #075e54; 
  font-size: 18px; 
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 10px;
}

input {
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-group {
    display: flex;
    align-items: center;
    position: relative;
}

.edit-icon {
    position: absolute;
    right: 10px; 
    cursor: pointer;
    color: #007bff; 
}

input#email,
input#name {
  padding-right: 30px; 
}

button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

button[type="submit"] {
  background-color: #075e54;
  color: white;
}

button[type="button"] {
  background-color: #ddd;
  color: #075e54;
}
</style>