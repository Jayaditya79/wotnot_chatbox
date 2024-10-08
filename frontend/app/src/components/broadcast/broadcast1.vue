<template>
  <div class="content-section md:ml-64 ">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Manage Templates</h2>
        <p class="text-sm md:text-base">Your content for scheduled broadcasts goes here.</p>
      </div>

      <div class="bg-[#075e54] rounded-md shadow-lg mt-2 md:mt-0">
        <button @click="showPopup = true"
          class="text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base w-full md:w-auto">
          Create New Template
        </button>

      </div>
    </div>

    <h3 class="text-xl md:text-2xs mb-4 text-gray-600"><b>Template List</b></h3>
    
      
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        
        <table class="w-full rounded-md border-collapse">
          <thead>
            <tr class="border-b-2 bg-[#ffffff] text-center">
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Name</th>
              <th class="p-2 text-center md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Language</th>
              <th class="p-2 text-center md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Status</th>
              <th class="p-2 text-center md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Category</th>
              <th class="p-2 text-center md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Sub Category</th>
              <th class="p-2 text-center md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">ID</th>
              <th class="p-2 text-center md:p-4 border-b-2 bg-[#ffffff] sticky top-0 z-10">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="template in templates" :key="template.id">
              <td class=" border-[#ddd] p-2 md:p-4 text-left">{{ template.name }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.language }}</td>
              <!-- <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.status }}</td> -->
              <td class="p-2 md:p-4 text-center">
                <div :class="{
                  'bg-[#e9f6ee] text-green-500 ': template.status === 'APPROVED',
                  'bg-blue-100 text-blue-500 ': template.status === 'PENDING',
                  'bg-red-100 text-red-500 ': template.status === 'REJECTED',
                  'border-[#ddd]': true
                }" class="text-[80%] lg:text-[100%] rounded-lg">
                  {{ template.status }}
                </div>
              </td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.category }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.sub_category }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.id }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">
                <button @click="deleteTemplate(template.id)" class="hover:bg-white rounded-full p-2 transition">
                  <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                    colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                  </lord-icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    

    <div v-if="showPopup" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[1000]"
      @click.self="closePopup">
      <div class="max-w-3xl mx-auto p-6 bg-white shadow rounded-lg">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold">Create Message Template</h2>
          <hr class="mb-4"/>
          <span class="relative bottom-1 text-4xl cursor-pointer text-black" @click="closePopup">&times;</span>
        </div>

        <form>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block below-402:text-custom-small text-sm font-medium">Template Name
                <span class="text-red-800">*</span>
              </label>
              <div class="relative mb-2">
                <input v-model="template.name" :placeholder="nameError || 'Template Name'" @blur="validateTemplateName"
                  :class="[
                    'border border-[#ddd] p-2 rounded-md w-full',
                    { 'border-red-500': nameError, 'placeholder-red-500': nameError }
                  ]" required />

              </div>
            </div>

            <div>
              <label class="block text-sm font-medium">Category<span class="text-red-800">*</span></label>
              <select v-model="selectedCategory" class="mt-1 p-2 w-full border border-gray-300 rounded-md h-10" required>
                <option value="Marketing">Marketing</option>
                <option value="Utility">Utility</option>
              </select>
            </div>

            <!-- Language -->
            <div class="mb-4">
              <label class="block text-sm font-medium">Language</label>
              <select class="mt-1 p-2 w-full border border-gray-300 rounded-md h-10" >
                <option>English</option>
                <!-- Add other languages here -->
              </select>
            </div>

          </div>



       

          <label for="">Header</label>
          <input v-model="headerComponent.text" placeholder="Header Text (optional)"
            class="border border-[#ddd] p-2 rounded-md w-full mb-2" />

          <div class="mb-4">
            <label class="block text-sm font-medium">Body<span class="text-red-800">*</span></label>
            <textarea v-model="bodyComponent.text" class="mt-1 p-2 w-full border border-gray-300 rounded-md h-12"
              placeholder="Template Message..." rows="4" required></textarea>
          </div>

          <label for="">Footer</label>
          <input v-model="footerComponent.text" placeholder="Footer Text (optional)"
            class="border border-[#ddd] p-2 rounded-md w-full mb-2" />

          <span>
            <button
              class="relative my-2 h-8 w-24 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200"
              @click.prevent="addbutton">
              Add Button
            </button>
          </span>

          <!-- Button Text and URL Inputs -->
          <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.text"
            placeholder="Button Text (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />
          <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.url"
            placeholder="Button URL (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />


          <!-- Sub-Category Selection -->
          <label v-if="selectedCategory === 'Marketing'" for="">Sub-Category</label>
          <select v-model="selectedSubCategory" v-if="selectedCategory === 'Marketing'" required
            class="border border-[#ddd] p-2 rounded-md w-full mb-2">
            <option value="" disabled>Select Sub-Category</option>
            <option value="ORDER_DETAILS">Order Details</option>
            <!-- <option value="ORDER_STATUS">Order Status</option> -->
          </select>
          <!-- Actions -->
          <div class="flex space-x-4">
            <button @click="submitTemplate" class="px-4 py-2 bg-green-600 text-white rounded-md">Save</button>
            <button @click="closePopup" class="px-4 py-2 bg-gray-400 text-white rounded-md">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'BroadCast1',
  data() {
    return {
      templateName: '',
      isTemplateNameValid: true,
      templates: [],
      showPopup: false,
      addButton: false,
      showSelectionPopup: false,
      selectedCategory: 'Marketing',
      selectedSubCategory: '',
      template: {
        name: '',
        components: []
      },
      bodyComponent: {
        type: 'BODY',
        text: ''
      },
      headerComponent: {
        type: 'HEADER',
        format: 'TEXT',
        text: ''
      },
      footerComponent: {
        type: 'FOOTER',
        text: ''
      },
      button: {
        type: 'URL',
        text: '',
        url: ''
      },
      nameError: ''
    };
  },

  async mounted() {
    await this.fetchtemplateList();

    // Dynamically load the Lordicon script
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },

  methods: {
    addbutton() {
      this.addButton = !this.addButton;
    },

    openPopup() {
      this.showPopup = true;
      this.selectedType = 'MARKETING';  // Ensure Marketing is default when opening
    },


    async fetchtemplateList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch("http://localhost:8000/template", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data;
      } catch (error) {
        console.error("There was an error fetching the templates:", error);
      }
    },

    async submitTemplate() {
      if (this.nameError) {
        return; // Prevent form submission if there are validation errors
      }

      this.template.components = [this.bodyComponent];

      if (this.selectedSubCategory !== 'ORDER_STATUS') {
        if (this.headerComponent.text) {
          this.template.components.push(this.headerComponent);
        }

        if (this.footerComponent.text) {
          this.template.components.push(this.footerComponent);
        }

        if (this.button.text && this.button.url) {
          this.template.components.push({
            type: 'BUTTONS',
            buttons: [this.button]
          });
        }
      } else {
        if (this.footerComponent.text) {
          this.template.components.push(this.footerComponent);
        }
      }

      const payload = {
        name: this.template.name,
        components: this.template.components,
        language: 'en_US',
        category: this.selectedCategory,
        sub_category: this.selectedSubCategory
      };

      const token = localStorage.getItem('token');

      if (!token) {
        console.error('No access token found in local storage');
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/create-template', payload, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        console.log('Template created successfully:', response.data);

        await this.fetchtemplateList();
        this.closePopup();
      } catch (error) {
        console.error('Error creating template:', error.response ? error.response.data : error.message);
      }
    },

    // 
    validateTemplateName() {
      // Updated regex to allow lowercase letters and underscores
      const regex = /^[a-z_0-9]+$/;

      if (this.template.name.trim() === '') {
        this.nameError = 'Template name is required';
      } else if (!regex.test(this.template.name)) {
        this.template.name = '';
        this.nameError = 'Template name must contain only lowercase letters and underscores.';
      } else {
        this.nameError = '';
      }
    },

    watch: {
      templateName() {
        this.validateTemplateName();
      },
    },

    selectType(type) {
      this.selectedType = type;
      this.showSelectionPopup = false;
      this.showPopup = true;
    },

    closePopup() {
      this.template.name = '';
      this.showPopup = false;
    },

    closeSelectionPopup() {
      this.showSelectionPopup = false;
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
</style>

<!-- <style scoped>

.error {
  border-color: red;
}

.error-message {
  color: red;
  font-size: 0.875em;
  margin-top: 0.5em;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}

.CreateTemplateContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.CreateTemplateContainer button {
  margin-left: 805px;
}

.templateList_container {
  background-color: #f5f6fa;
  border-radius: 12px 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.templateList-table {
  width: 100%;
  border-radius: 12px 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
}

th {
  padding: 20px 43px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table td {
  border: 1px solid #ddd;
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.templateList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table tbody {
  background-color: white;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.template-type-options {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.template-type-options button {
  flex: 1;
  padding: 10px;
  border: none;
  background-color: #075e54;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.template-type-options button:hover {
  background-color: #075e54;
}

.discard-button {
  margin-top: 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button {
  background-color: 5;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #218838;
}
</style>  -->
