<template>
  <div id="app" class="main-container">
    <!-- Sidebar for Active Chats -->
    <div class="sidebar">
  <b><h2>Active Chats</h2></b>
  <ul class="chat-list">
    <li v-for="chat in chats" :key="chat.message_id">
      <a @click="loadChat(chat.message_id)">
        {{ chat.contact_details.name }} ({{ chat.contact_details.phone }})
      </a>
    </li>
  </ul>
</div>


    <!-- Chat Area -->
    <div class="chat-area">
      <div class="chat-header">
        <div class="timer">
          <svg width="60" height="60">
            <circle cx="30" cy="30" r="25" stroke="white" stroke-width="5" fill="none"></circle>
            <circle id="progressCircle" class="progress-circle" cx="30" cy="30" r="25" stroke-dasharray="157.08" :stroke-dashoffset="progressSeconds" />
          </svg>
          <span id="currentTime">{{ currentTime }}</span>
        </div>
        <div>
          <i class="fas fa-user-circle"></i>
          <h6 id="chatTitle">{{ chatTitle }} <br> <span class="available-text">Available</span></h6>
        </div>
        <select id="userDropdown" @change="selectUser">
          <option value="" disabled selected>Select User</option>
          <option v-for="chat in chats" :key="chat.message_id" :value="chat.message_id">{{ chat.contact_details.name }}</option>
        </select>
      </div>

      <div class="chat-content" id="chatContent">
        <div v-html="chatContent"></div>
        <div id="messages">
          <div v-for="message in messages" :key="message.id" class="message">
            <p class="user-message">{{ message.text }}</p>
          </div>
        </div>
      </div>

      <!-- Message Input Area -->
      <div class="message-input-area">
        <input type="text" v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
        <label for="file-upload" class="upload-label">
          <i class="fas fa-paperclip"></i>
        </label>
        <input type="file" id="file-upload" @change="handleFileUpload" class="file-input" />
        <button @click="sendMessage">Send</button>
      </div>
    </div>

    <!-- Contact Information -->
    <div class="contact-info">
      <h3>{{ contactInfo.name }}</h3>
      <p><strong>Phone Number:</strong> {{ contactInfo.phone }}</p>
      <h4>Contact Attributes</h4>
      <table class="contact-table">
        <tbody>
          <tr>
            <td><strong>Email:</strong></td>
            <td>{{ contactInfo.email }}</td>
          </tr>
          <tr>
            <td><strong>Created at:</strong></td>
            <td>{{ contactInfo.created }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatbotView',
  data() {
    return {
      chats: [],
      chatTitle: "",
      chatContent: "",
      contactInfo: {},
      messages: [],
      newMessage: "",
      currentTime: "",
      progressSeconds: 0,
    };
  },
  mounted() {
    this.fetchActiveChats().catch((error) => {
      console.error("Error fetching active chats:", error);
    });
    this.updateCurrentTime();
    setInterval(() => this.updateCurrentTime(), 1000);
  },
  methods: {
    async fetchActiveChats() {
      try {
        const response = await fetch("http://localhost:8000/api/chats");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        // Remove duplicates based on phone number
        const uniqueChats = [];
        const phoneNumbers = new Set();
        data.forEach((chat) => {
          if (!phoneNumbers.has(chat.contact_details.phone)) {
            phoneNumbers.add(chat.contact_details.phone);
            uniqueChats.push(chat);
          }
        });
        
        this.chats = uniqueChats;
      } catch (error) {
        console.error("Error fetching active chats:", error);
      }
    },
    updateCurrentTime() {
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      this.currentTime = `${hours}:${minutes}`;
      this.updateProgressBar(now.getSeconds());
    },
    updateProgressBar(seconds) {
      const circumference = 125.66;
      const offset = circumference - (circumference * (seconds / 60));
      this.progressSeconds = offset;
    },
    loadChat(chatId) {
      const chat = this.chats.find(chat => chat.message_id === chatId);
      if (chat) {
        this.chatTitle = `Chat with ${chat.contact_details.name}`;
        this.contactInfo = chat.contact_details;
        this.chatContent = chat.latest_message;
        this.messages = [];
      } else {
        console.error(`Chat with ID "${chatId}" not found.`);
      }
    },
    selectUser(event) {
      const selectedUser = event.target.value;
      if (selectedUser) {
        this.loadChat(selectedUser);
      }
    },
    sendMessage() {
      if (this.newMessage.trim()) {
        this.messages.push({ id: this.messages.length, text: this.newMessage });
        this.newMessage = '';
      }
    },
    // handleFileUpload(event) {
    // Handle file upload logic here
    // }
  }
};
</script>





  <style scoped>
  /* Main container layout */
  .main-container {
    display: flex;
    height: 90vh;
    background-color: #f4f4f4;
    font-family: Arial, sans-serif;
    width: 100%;
  }
  
  /* Sidebar styling */
  .sidebar {
    width: 20%;
    background-color: #075E54;
    color: #ffffff;
    padding: 15px;
    overflow-y: auto;
  }
  
  .sidebar h2 {
    color: #fff;
    margin-bottom: 10px;
  }
  
  .chat-list {
    list-style: none;
    padding: 0;
  }
  
  .chat-list li {
    margin-bottom: 15px;
  }
  
  .chat-list li a {
    text-decoration: none;
    color: #ffffff;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .chat-list li a:hover {
    background-color: #25d366;
    padding: 5px;
    border-radius: 5px;
  }
  
  /* Chat area styling */
  .chat-area {
    flex-grow: 1;
    background-color: #ffffff;
  
    border-left: 1px solid #ccc;
    height: 90vh;
  }
  
  .chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #f8f9fa;
  width: 100%; /* Make sure it occupies the full width of the container */
  max-width: 100%; /* Remove any width restrictions if necessary */
  box-sizing: border-box;
  border-bottom: 1px solid #ccc; /* Optional: add a bottom border */
  height:105px;
}

  
  .status {
    color: #4caf50;
    font-weight: bold;
  }
  
  .chat-content {
    height: calc(100vh - 200px);
    overflow-y: auto;
  }
  
  .message {
    margin: 10px 0;
  }
  
  .user-message {
    background-color: #dcf8c6;
    padding: 10px;
    border-radius: 10px;
    max-width: 70%;
  }
  
  /* Message Input Area */
  .message-input-area {
    display: flex;
    align-items: center;
  }
  
  .message-input-area input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .message-input-area button {
    margin-left: 10px;
    padding: 10px;
    background-color: #075E54;
    color: rgb(255, 255, 255);
  }
  .chat-list li {
    margin-bottom: 15px;
  }
  
  .chat-list a {
    color: #ffffff;
    text-decoration: none;
    padding: 10px;
    display: block;
    background-color: #128C7E;
    border-radius: 5px;
    transition: background-color 0.3s;
  }
  
  .chat-list a:hover {
    background-color: #25D366;
  }
  
  /* Chat area styling */
  .chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    border-left: 1px solid #ddd;
  }
  
  .chat-header {
    padding: 10px;
    background-color: #128c7e;
    color: white;
    text-align: center;
    font-size: 1.5em;
    width:100%;
  }
  /* Style for the select dropdown */
  #userDropdown {
    background-color: #128c7e; /* Green background */
    color: white; /* White text color */
    padding: 1px;
    border: 1px solid #ccc;
    border-radius: 10px;
    width:30%;
  }
  
  /* Optional: Change text color for options */
  #userDropdown option {
    background-color: #128c7e; /* Green background for options */
    color: white; /* White text color for options */
  }
  
  .status {
    display: block;
    font-size: 0.8em;
    color: #c1c1c1;
    margin-top: 5px;
  }
  
  .chat-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background-color: #f9f9f9;
  }
  
  .message {
    background-color: #dcf8c6;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 10px;
    width: fit-content;
    max-width: 60%;
  }
  
  .user-message {
    margin: 0;
    font-size: 1em;
  }
  /* Timer styling */
  .timer {
              display: flex;
              align-items: center;
              justify-content: center;
              margin-right: 10px; /* Space between timer and title */
          }
  
          .timer-circle {
              position: relative;
              width: 50px;
              height: 50px;
          }
  
          .timer-circle span {
              font-size: 0.8em; /* Adjusted font size */
              color: #4caf50; /* Text color */
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
          }
  
          .status {
              margin-left: auto; /* Push status to the right */
          }
  
          .timer i {
              margin-right: 5px;
              color: #FFD700; /* Gold color for the icon */
          }
  
          /* Circular progress bar styles */
          .progress-circle {
              stroke: #4caf50;
              stroke-width: 5;
              fill: none;
              transform: rotate(-90deg);
              transform-origin: 50% 50%;
          }
  /* Message input area styling */
  .message-input-area {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #f1f1f1;
  }
  
  .message-input-area input[type="text"] {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .upload-label {
    cursor: pointer;
    margin-left: 10px;
  }
  
  .upload-label i {
    font-size: 18px;
    color: #666;
  }
  
  .upload-label:hover i {
    color: #25d366;
  }
  
  .file-input {
    display: none;
  }
  
  button {
    margin-left: 10px;
    padding: 10px 15px;
    background-color: #25d366; /* Change background to a darker color */
    color: rgb(255, 255, 255); /* Text color is white */
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #1da857; /* Darker green on hover */
  }
  
  
  /* Contact information styling */
  .contact-info {
    width: 30%;
    padding: 20px;
    background-color: #f0f0f0;
    border-left: 1px solid #ddd;
  }
  
  .contact-info h3 {
    margin-top: 0;
  }
  
  .tags {
    margin-top: 20px;
  }
  
  .tags h4 {
    margin-bottom: 10px;
  }
  
  .tags ul {
    list-style: none;
    padding: 0;
  }
  
  .tags ul li {
    background-color: #128C7E;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    margin-bottom: 5px;
    display: inline-block;
  }
  
  .tags ul li button {
    margin-left: 10px;
    background: none;
    border: none;
    color: white;
    cursor: pointer;
  }
  
  .tags input {
    padding: 5px;
    margin-top: 10px;
    width: 80%;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  .tags button {
    padding: 5px 10px;
    background-color: #128C7E;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .tags button:hover {
    background-color: #25D366;
  }
  
  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .sidebar {
      width: 100%;
    }
  
    .chat-area,
    .contact-info {
      width: 100%;
      margin-top: 10px;
    }
  
    .chat-area {
      order: 2;
    }
  
    .contact-info {
      order: 1;
    }
  
    .main-container {
      flex-direction: column;
    }
  }
  .contact-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
  }
  
  .contact-table th,
  .contact-table td {
      border: 1px solid #4c4b4b;
      padding: 8px;
      text-align: left;
  }
  
  .contact-table th {
      background-color: #f2f2f2;
  }
  .available-text {
  font-size: 12px;  /* Adjust the size as needed */
  color: #ffffff;   
  top:2px;   /* Optional: Change color if needed */
}
  
  
  </style>