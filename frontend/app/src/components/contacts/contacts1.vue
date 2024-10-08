<template>
  <div class="content-section md:ml-64">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold ">Manage Contacts</h2>
        <p class="text-xsm md:text-base">Contact list stores the list of numbers that you've interacted with.
          You can even manually export or import contacts.</p>
      </div>
      

      <div>
        <button @click="showPopup = true"
          class="bg-[#075e54] text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base rounded-md shadow-lg">
          + Add Contact
        </button>
      </div>
    </div>
    <PopUp1 v-if="showPopup" @close="closePopup">
      <form @submit.prevent="submitForm" id="contactForm" class="p-6 w-[400px]">
        <h2 class="text-xl font-semibold mb-4">{{ isEditing ? 'Edit Contact' : 'Add Contact' }}</h2>
        <hr class="mb-4" />

        <div class="mb-4">
          <label for="name" class="block text-sm font-medium">Name<span class="text-red-800">*</span></label>
          <input type="text" v-model="contact.name" id="name" placeholder="Name" required class="border border-gray-300 rounded px-3 py-2 w-full">
        </div>

        <div class="mb-4">
          <label for="phone" class="block text-sm font-medium">Phone Number<span class="text-red-800">*</span></label>
          <div class="flex">
            <select v-model="contact.countryCode" class="border border-gray-300 rounded-l px-3 py-2 w-20 mr-2">
              <option value="+1">+1</option>
              <option value="+44">+44</option>
              <option value="+91">+91</option>
            </select>
            <input type="text" v-model="contact.phone" id="phone" placeholder="Phone Number" required class="border border-gray-300 rounded-r px-3 py-2 w-full">
          </div>
        </div>
        <label for="email" class="block text-sm font-medium">Email<span class="text-red-800">*</span></label>
        <input type="email" v-model="contact.email" id="email" placeholder="Email" required class="border border-gray-300 rounded px-3 py-2 mb-2 w-full">
        
        <div class="mb-4">
  <label class="block text-sm font-medium">Tags</label>
  <div class="custom-scrollbar tags-container-container">

  <div class="tags-container">
    <div class="tag-input" v-for="(tag, index) in contact.tags" :key="index" style="display: flex; align-items: center;">
      <input type="text" v-model="tag.key" placeholder="Key" required class="border border-gray-300 rounded px-3 py-2 mb-2 w-full" style="width: 60%;">
      <input type="text" v-model="tag.value" placeholder="Value" required class="border border-gray-300 rounded px-3 py-2 mb-2 w-full" style="width: 60%; margin-left: 10px;">
      <button type="button" @click="removeTag(index)" class="hover:bg-gray-100 rounded-full p-2 transition">
        <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover" colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px"></lord-icon>
      </button>
    </div>
  </div>
<button type="button" @click="addTag" class="my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200">Add Tag</button>

  </div>
</div>


        <div class="flex justify-between mt-2">
          <button @click="closePopup" type="button" class="border-[2px] border-gray-300 hover:bg-gray-200 text-black rounded-lg px-4 py-2">
            Cancel
          </button>
          <button type="submit" class="bg-[#23a455] text-white px-4 py-2 rounded">
            {{ isEditing ? 'Update Contact' : 'Add Contact' }}
          </button>
        </div>
      </form>
    </PopUp1>

    
    
    <div class="bg-[#f5f6fa] p-5  filter-container space-x-2">

      <h3 class="text-xl md:text-2xs mb-0 text-gray-600"><b>Contact List</b></h3>
      <!-- <div class="dropdown-container">
        <b><label for="sort-by">Sort by:</label></b>
        <select v-model="sortBy" @change="fetchContactList">
          <option value="created_at">Created At</option>
          <option value="updated_at">Updated_at</option>
        </select>
      </div>

      <div class="dropdown-container">
        <b><label for="order">Order:</label></b>
        <select v-model="order" @change="fetchContactList">
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>

      <div class="search-container">
      <b><label for="search">Search by phone number:</label></b>
      <input type="text" v-model="searchQuery" placeholder="Search by phone number" @input="fetchContactList">
      </div> -->


      
      <div class="flex items-center space-x-2   tags-search-container">
        <h3 class="text-l"><b>Filter by tags:</b></h3>
        
        <input type="text" v-model="tag_key" placeholder="Key" class="border border-gray-300 rounded px-3 py-2 w-40px">
        <input type="text" v-model="tag_value" placeholder="Value" class="border border-gray-300 rounded px-3 py-2 w-40px">
        
        <button @click="fiterBytTags" class="relative my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200">Apply filter</button>
      </div>
    </div> 

    
    
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        <table class="w-full rounded-lg border-collapse block">
          <thead>
            <tr class="bg-[#ffffff] border-b-2 border-gray-300" >
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Id</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Name</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Phone Number</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Email</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Tags</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Created at</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0 z-10">Action</th>
            </tr>
          </thead>

          <tbody class="bg-white">
            <tr v-for="contact in contacts" :key="contact.id">
              <td class="border-gray-300 py-5 px-3 contact-id-column">{{ contact.id }}</td>
              <td class="border-gray-300 py-5 px-3 name-column">{{ contact.name }}</td>
              <td class="border-gray-300 py-5 px-3">{{ contact.phone }}</td>
              <td class="border-gray-300 py-5 px-3 contact-email-column">{{ contact.email }}</td>
              <td class="border-gray-300 py-5 px-4 contact-tag-column">
                <div v-for="(tag, index) in contact.tags" :key="index">
                  <span class="font-bold">{{ tag.key }}:</span> {{ tag.value }}
                </div>
              </td>
              <td class="border-gray-300 py-5 px-3">{{ formatDate(contact.created_at) }}</td>
              <td class="border-gray-300 py-5 px-3">
                <div class="flex justify-left">
                  <button @click="modifyContact(contact)" class="hover:bg-white rounded-full p-2 transition">
                    <lord-icon src="https://cdn.lordicon.com/wuvorxbv.json" trigger="hover"
                      style="width:32px;height:32px">
                    </lord-icon>
                  </button>
                  <button @click="deleteContact(contact.phone)"
                    class="hover:bg-white rounded-full p-2 transition">
                    <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                      colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                    </lord-icon>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification';
import PopUp1 from "../popups/popup1";

export default {
  components: {
    PopUp1,
  },
  async mounted() {
    await this.fetchContactList();

    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },
  name: "ContActs1",
  data() {
    return {
      showPopup: false,
      showActionPopup: false,
      contact: {
        id: "",
        name: "",
        email: "",
        phone: "",
        countryCode: "+91",
        tags: [],

      // Search Bar
        tag_key: '',
        tag_value:'',
      },
      selectedContact: null,
      contacts: [],
      isEditing: false,
      searchQuery: '',  // This will be used for searching by phone number
      selectedTag: null,
      sortBy: 'updated_at', // Default sorting criteria
      order: 'desc', // Default sorting order
      searchTerm: '', // For searching by contact name
    };
  },
  computed: {
    filteredContacts() {
      const searchPhone = this.searchQuery.toLowerCase(); // Updated to use searchQuery for phone numbers
      const searchName = this.searchTerm.toLowerCase(); // For contact name search

      return this.contacts
        .filter(contact => {
          const matchesPhone = contact.phone.toLowerCase().includes(searchPhone); // Searching by phone number
          const matchesName = contact.name.toLowerCase().includes(searchName); // Searching by contact name
          const matchesTag = this.selectedTag
            ? contact.tags.some(tag => tag.key.toLowerCase() === this.selectedTag.toLowerCase())
            : true;
          return (matchesPhone || matchesName) && matchesTag; // Filtering by phone number, name, and tags
        });
    },
    uniqueTags() {
      const allTags = this.contacts.flatMap(contact => contact.tags.map(tag => tag.key));
      return [...new Set(allTags)];
    },
    formattedTags() {
      return this.contacts.map(contact => ({
        ...contact,
        formattedTags: contact.tags.map(tag => `${tag.key}: ${tag.value}`).join(', '),
      }));
    }
  },
  methods: {
    async submitForm() {
      const toast = useToast();
      const { id, name, email, phone, countryCode, tags } = this.contact;

      let fullPhoneNumber = phone;
      if (countryCode && countryCode.trim() !== '') {
        fullPhoneNumber = `${countryCode} ${phone}`;
      }

      if (tags.some(tag => tag.key === '' || tag.value === '')) {
        alert("Please fill in all key-value pairs");
        return;
      }

      const tagArray = tags.map(tag => `${tag.key}:${tag.value}`);

      const url = id ? `http://localhost:8000/contacts/${id}` : "http://localhost:8000/contacts/";
      const method = id ? "PUT" : "POST";
      const token = localStorage.getItem("token");

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name, email, phone: fullPhoneNumber, tags: tagArray }), // Send full phone number
        });

        if (response.ok) {
          toast.success(id ? "Contact updated successfully" : "Contact created successfully");
          this.clearForm();
          this.fetchContactList();
        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error saving contact:", error);
        alert("Error saving contact");
      }
    },
    clearForm() {
      this.contact = {
        id: "",
        name: "",
        email: "",
        phone: "",
        tags: [],
      };
      this.showPopup = false;
    },
    closePopup() {
      this.showPopup = false;
      this.clearForm();  // Clear the form when closing the popup
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', options).replace(/,/g, '');
    },
    async fetchContactList() {
      const token = localStorage.getItem("token");
      const url = `http://localhost:8000/contacts/?sort_by=${this.sortBy}&order=${this.order}`;

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const contactsList = await response.json();
        console.log(contactsList);
        this.contacts = contactsList.map((contact) => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          email: contact.email,
          tags: contact.tags.map(tag => {
            const [key, value] = tag.split(":");
            return { key, value };
          }),
          created_at: contact.created_at, // Store raw dates for sorting
          updated_at: contact.updated_at // Store updated_at too
        }));
      } catch (error) {
        console.error("Error fetching contacts:", error);
      }
    },

    // Contacts Tags Filter
    async fiterBytTags(){
      const token = localStorage.getItem("token");
      const tagValue=this.tag_value
      const tagKey=this.tag_key
      try{
        
        const response=await fetch(`http://localhost:8000/contacts-filter/filter?tag_key=${tagKey}&tag_value=${tagValue}`,{
          method:"GET",
          headers:{
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }});


          const contactsList= await response.json()
          this.contacts = contactsList.map((contact) => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          email: contact.email,
          tags: contact.tags.map(tag => {
            const [key, value] = tag.split(":");
            return { key, value };
          }),
          created_at: contact.created_at, // Store raw dates for sorting
          updated_at: contact.updated_at // Store updated_at too
        }));

          if(!response.ok){
            throw new Error("Network response not ok")
          }

      }catch(error){
        console.error("Error filtering contacts",error)
      }
    },
    closeActionPopup() {
      this.showActionPopup = false;
      this.selectedContact = null;
    },
    modifyContact(contact) {
      this.selectedContact = contact;
      this.contact = { ...this.selectedContact };
      this.showPopup = true;
      this.closeActionPopup();
    },
    async deleteContact(phone) {
      const toast = useToast();
      const confirmDelete = confirm("Are you sure you want to delete this contact?");
      if (!confirmDelete) return;

      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`http://localhost:8000/contacts/${phone}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          toast.success("Contact deleted successfully");
          this.fetchContactList();
          this.closeActionPopup();
        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error deleting contact:", error);
        alert("Error deleting contact");
      }
    },
    addTag() {
      const lastTag = this.contact.tags[this.contact.tags.length - 1];
      if (this.contact.tags.length === 0 || (lastTag.key !== '' && lastTag.value !== '')) {
        this.contact.tags.push({ key: "", value: "" });
      } else {
        alert("Please enter key and value for the previous tag");
      }
    },
    removeTag(index) {
      this.contact.tags.splice(index, 1);
    },
    filterContacts() {
      this.fetchContactList();
    }
  },
};
</script>

<style scoped>
/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  border-radius: 16px;
  background-color: #e7e7e7;
  border: 1px solid #cacaca;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 3px solid transparent;
  background-clip: content-box;
  background-color: #075e54;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555;
}
.tags-container {
  max-height: 120px; /* adjust this value based on the height of your attribute rows */
  overflow-y: auto;
}

.tags-container::-webkit-scrollbar {
  width: 8px;
}

.tags-container::-webkit-scrollbar-track {
  border-radius: 16px;
  background-color: #e7e7e7;
  border: 1px solid #cacaca;
}

.tags-container::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 3px solid transparent;
  background-clip: content-box;
  background-color: #075e54;
}

.tags-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
table {
  width: 100%;
  border-collapse: collapse;
}

thead, tbody {
  width: 100%;
}

thead th, tbody td {
  width: 2.28%; /* 100% / 7 columns */
  padding: 10px;
  text-align: left;
  border: 1px solid #ffffff;
}

tbody td {
  height: 50px; /* adjust this value to change the row height */
}

td {
  word-break: keep-all;
}
.name-column {
  max-width: 130px; /* Adjust based on your needs */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.contact-id-column {
    font-size: 1.0rem; /* Adjust the font size as needed */
    max-width: 20px; /* Optional: Adjust width if needed */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .controls-container {
  @apply flex items-center p-5 gap-5 shadow;
}

.dropdown-container {
  @apply p-1 flex flex-col items-start w-1/5;
}

.search-container {
  @apply p-1 flex flex-col items-start w-1/3;
}

.controls-container label, 
.search-container label {
  @apply text-sm mb-1;
}

.controls-container select, 
.search-container input[type="text"] {
  @apply w-full p-2 text-sm border border-gray-300 rounded;
} 

</style>










<!-- <div class="mb-4">
          <label for="attributes" class="block text-sm font-medium">Custom Attribute (Optional)</label>
          <button @click="addAttribute" type="button" class="border border-green-500 text-green-500 px-4 py-2 rounded">
            + Add Attribute
          </button>
        </div> -->

<!-- <PopUpSmall v-if="showActionPopup" @close="closeActionPopup">
      <div class="bg-white shadow-lg rounded-lg p-4">
        <p class="text-lg mb-4">What action do you want to take?</p>
        <div class="flex space-x-4">
          <button @click="modifyContact" class="bg-yellow-500 text-white py-2 px-4 rounded">Modify</button>
          <button @click="deleteContact(selectedContact.phone)"
            class="bg-red-500 text-white py-2 px-4 rounded">Delete</button>
        </div>
      </div>
    </PopUpSmall> -->
<!-- <button @click="openActionPopup(contact)"
                  class="bg-[#075e54] text-white py-2 px-4 rounded">Action
                </button> -->
















<!-- <style scoped>
 .contactsListContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

}

.contactsList-table {
  width: 100%;
  border-radius: 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;

}

th {
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;


}

.contactsList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.contactsList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.contactsList-table tbody {
  background-color: white; 
}


</style>  -->
