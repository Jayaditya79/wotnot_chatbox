<template>
  <div class="content-section p-4">
    <!-- Section Header -->
    <div class="flex flex-col md:flex-row justify-between mb-4">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Conversation Analytics</h2>
        <p class="text-sm md:text-base">Your data for conversation analytics goes here.</p>
      </div>
      <button @click="goToDashboard"
        class="bg-[#075e54] text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base rounded-md shadow-lg">
        Go to Dashboard
      </button>
    </div>

    <!-- Analytics List Table -->
    <div class="bg-[#f5f6fa] rounded-md p-4 mb-4 shadow-lg">
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-[#dddddd] text-center">
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Start Time</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">End Time</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Conversation Type</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Conversation Category</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Cost</th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="(item, index) in sortedAnalyticsData" :key="index" class="text-center">
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ item.start_time }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ item.end_time }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ item.conversation_type }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ item.conversation_category }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ item.cost }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      localUser: {
        whatsapp_business_id: '',
      },
      analyticsData: [], // Holds the conversation data
      loading: true, // Loading indicator
      error: null, // Error message if any
    };
  },
  async mounted() {
    await this.fetchUserDetails();
    await this.fetchConversationHistory(this.localUser.whatsapp_business_id);
  },
  computed: {
  // Computed property to return a sorted copy of analyticsData in descending order of start_time
  sortedAnalyticsData() {
    return [...this.analyticsData].sort((a, b) => new Date(b.start_time) - new Date(a.start_time));
  },
},

  methods: {
    async fetchUserDetails() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        const data = await response.json();
        console.log(data);
        this.localUser.whatsapp_business_id = data['Whatsapp_Business_Id'];
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },
    async fetchConversationHistory(accountId) {
      try {
        const response = await fetch(
          `http://localhost:8000/conversation-cost-history/${accountId}`,
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );
        const data = await response.json();
        this.analyticsData = data.conversation_analytics;
        this.loading = false;
      } catch (err) {
        this.error = err.message || 'Failed to fetch data';
        this.loading = false;
      }
    },
    goToDashboard() {
      this.$router.push('/dashboard');
    },
  },
};
</script>

<style scoped>
/* Custom scrollbar for table overflow */
.custom-scrollbar::-webkit-scrollbar {
  width: 10px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #888;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Responsive Table Styles */
@media (max-width: 768px) {
  table thead {
    display: none;
  }

  table tbody tr {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
    border-bottom: 2px solid #ddd;
  }

  table tbody tr td {
    display: block;
    text-align: right;
    position: relative;
    padding-left: 50%;
  }

  table tbody tr td::before {
    content: attr(data-label);
    position: absolute;
    left: 0;
    padding-left: 10px;
    font-weight: bold;
    text-transform: uppercase;
  }
}
</style>
