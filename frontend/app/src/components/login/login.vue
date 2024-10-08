<template>
  <main class="bg-container" >
    <div class="w-full max-w-sm bg-white p-8 rounded-lg shadow-md">


      <div class="flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
          <path fill="#075e54"
            d="M160 368c26.5 0 48 21.5 48 48l0 16 72.5-54.4c8.3-6.2 18.4-9.6 28.8-9.6L448 368c8.8 0 16-7.2 16-16l0-288c0-8.8-7.2-16-16-16L64 48c-8.8 0-16 7.2-16 16l0 288c0 8.8 7.2 16 16 16l96 0zm48 124l-.2 .2-5.1 3.8-17.1 12.8c-4.8 3.6-11.3 4.2-16.8 1.5s-8.8-8.2-8.8-14.3l0-21.3 0-6.4 0-.3 0-4 0-48-48 0-48 0c-35.3 0-64-28.7-64-64L0 64C0 28.7 28.7 0 64 0L448 0c35.3 0 64 28.7 64 64l0 288c0 35.3-28.7 64-64 64l-138.7 0L208 492z" />
        </svg>
        <div class="logo"> WotNot</div>
      </div>

      
      <p class="text-xl sm:text-xl font-semibold text-center text-gray-800 mb pb-0">Login to your Wotnot account</p>

      <hr class="my-6 border-gray-300" />

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Email</label>
          <input type="text" id="username" v-model="username" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" v-model="password" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
        </div>
        <button type="submit"
          class="w-full bg-[#075e54] text-white py-2 rounded-md hover:bg-[#2d988c] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
          Login
        </button>
        <p v-if="errorMessage" class="text-red-500 text-sm mt-2">{{ errorMessage }}</p>
      </form>

      <p class="mt-4 text-center text-sm">
        Don't have an account?
        <a href="" class="text-[#075e54] font-semibold mb-4" @click.prevent="redirectSignup">Sign Up</a>
      </p>
    </div>
  </main>
</template>


<script>
export default {
  name: "LoginPage",
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async handleLogin() {
      fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: this.username,
          password: this.password
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.access_token) {
            // Store the token in localStorage or Vuex (if using Vuex)
            localStorage.setItem('token', data.access_token);
            // Redirect to the dashboard
            console.log()
            this.$router.push('/dashboard');
          } else {
            // Handle login error
            alert('Login failed');
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    redirectSignup(){
      this.$router.push("/signup");
    }
  },
};
</script>


<style scoped>
.logo {
  font-weight: 800;
  margin: 8px 0;
  padding-right: 30px;
  font-size: xx-large;
  color: #075e54;
}

.bg-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh; /* equivalent to min-h-screen */
  
  background-image: url("@/assets/LoginPage.png");
  background-position: center; /* equivalent to bg-gray-100 */
  padding: 0 16px; /* equivalent to px-4 */
}

/* Responsive padding for different screen sizes */
@media (min-width: 640px) { /* equivalent to sm:px-6 */
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 1024px) { /* equivalent to lg:px-8 */
  .container {
    padding: 0 32px;
  }
}
</style>