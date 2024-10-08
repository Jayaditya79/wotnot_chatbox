<template>
  <div class="content-section md:ml-64">

    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-2xl font-bold ">Integration</h2>
        <p>Integrate other application with WotNot</p>
      </div>

    </div>



    <div class="woocommerceBox cursor-pointer p-4  hover:bg-gray-300 rounded-lg mb-4">
      <img src="@/assets/woocommerce.png" alt="Woocommerce" @click="showPopup = true">
    </div>

    <PopUp v-if="showPopup" @close="showPopup = false"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 custom-scrollbar">

      <div class="popup-content custom-scrollbar p-4">
        <form class="space-y-4" @submit.prevent="submitTemplate">
          <h2 class="text-xl font-bold ">Woocommerce</h2>
          <hr class="mb-4" />

          <div>
            <label class="block text-gray-700 font-semibold mb-2" required>Select action<span
                class="text-red-800">*</span></label>
            <select v-model="SelectedAction"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option value="" disabled>Select your option</option>
              <option value="woo/order_confirmation">Send Order Confirmation</option>
              <option value="Abandoned Cart">Abandoned Cart</option>
            </select>
          </div>

          <div v-if="SelectedAction === 'woo/order_confirmation'">
            <label class="block text-gray-700 font-semibold mb-2">Select template<span
                class="text-red-800">*</span></label>
            <select v-model="selectedTemplate"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option value="" disabled>Select your template</option>
              <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.name }}</option>
            </select>
          </div>

          <div v-if="selectedTemplate !== null">
            <label for="" class="block text-gray-700 font-semibold mb-2">Add Parameters<span
                class="text-red-800">*</span></label>
            <div v-for="(parameter, index) in parameters" :key="index" class="flex items-center space-x-2 mb-2">

              <select v-model="parameter.key" class="w-full p-2 border rounded-md bg-gray-100">
                <option value="" disabled>Select your parameter</option>
                <option v-for="option in parameterOptions" :key="option" :value="option.key">{{ option.label }}</option>
              </select>
              <button @click.prevent="removeParameter(index)"
                class="relative my-2 h-8 w-24 border-2 border-solid border-red-500 text-red-500 hover:text-gray-200 hover:bg-red-700">
                Remove
              </button>
            </div>
            <button @click.prevent="addParameter"
              class="relative my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200">
              Add Parameter
            </button>



            <div class="webhookConfig" v-if="selectedTemplate !== null">


            </div>
            <h3 class="text-lg font-bold mb-2">Woocommerce Setup</h3>
            <input type="text" v-model="webhookLink" class="w-full p-2 border rounded-md bg-gray-100" disabled>

            <ul class="list-disc pl-5 mt-4 space-y-2 text-sm">
              <li>Navigate to <b>WooCommerce > Settings</b></li>
              <li>Click on the <b>Advanced tab</b></li>
              <li>In the <b>Advanced settings</b>, click on <b>Webhook</b></li>
              <li>Click the <b>Add Webhook</b> button.</li>
              <li><b>Configure Webhook Settings</b></li>
              <li><b>Name</b>: Give your webhook a name to identify it.</li>
              <li><b>Status:</b> Set this to Active.</li>
              <li>Topic: Choose the event you want the webhook to listen to</li>
              <li><b>Delivery URL: use the above given webhook URL</b></li>
              <li><b>Secret:</b> leave blank</li>
              <li><b>API Version:</b> Leave the default version</li>
              <li>Click Save Webhook to activate the integration</li>
            </ul>
          </div>


          <button type="submit" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded">Save Integration</button>

        </form>
      </div>


    </PopUp>
    <h3 class="text-xl md:text-2xs mb-4 text-gray-600"><b>Integration List</b></h3>
    <div class="broadcastListContainer bg-gray-100 rounded-lg p-4 max-w-full mx-auto shadow-md custom-scrollbar">
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        <table class="w-full rounded-lg border-collapse">
          <thead>
            <tr class="bg-[#dddddd] text-center">
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">ID</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Application</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Type</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">API Key</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Action</th>

            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="integration in integrations" :key="integration.id">
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.id }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.app }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.type }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.api_key }}</td>
              <button @click="deleteIntegration(integration.id)" class="hover:bg-white rounded-full p-2 transition center">
                <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                  colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                </lord-icon>
              </button>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>


<script>
import PopUp from "../popups/popup";
import { useToast } from 'vue-toastification';

export default {

  name: 'AppIntegration',
  data() {

    return {
      showPopup: false,
      SelectedAction: null,
      templates: [],
      selectedTemplate: null,
      webhookLink: '',
      integrations: [],
      templateParams: [],
      parameters: [],  // List of parameters for the template
      parameterOptions: [{ label: "Customer Name", key: "billing.first_name" },
      { label: "Order ID", key: "id" },
      { label: "Order Total", key: "total" },
      { label: "Customer Phone", key: "billing.phone" },
      { label: "Payment Method", key: "payment_method" },],

      parameterFields: [{ selected: '' }]

    }

  },
  components: {
    PopUp
  },
  async mounted() {
    await this.fetchTemplates()
    await this.fetchapiKey();
    await this.fetchIntegrationList();
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);



    // Fetch contacts when the component is mounted
  },

  methods: {

    addParameter() {
      this.parameters.push({ key: this.parameterOptions[0] }); // Add a new parameter with default value
    },

    removeParameter(index) {
      this.parameters.splice(index, 1); // Remove parameter by index
    },
    togglepopup() {
      console.log("event")
    },
    async fetchTemplates() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/templates/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templateNames = await response.json();
        this.templates = templateNames.map(name => ({ id: name, name }));
      } catch (error) {
        console.error('Error fetching templates:', error);
      }
    },

    async fetchapiKey() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch("http://localhost:8000/webhooklink",
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          });


        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const result = await response.json()
        this.webhookLink = result.webkook_link
      } catch (error) {
        console.error('Error fetching API key:', error);
      }

    },
    async submitTemplate() {
      const payload = {
        template_id: this.selectedTemplate,
        parameters: this.parameters,
        type: this.SelectedAction

      };

      // Replace with your API endpoint
      try {
        const toast = useToast();
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/integrate/woocommerce', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          toast.success("Integration saved successfully");
          this.fetchIntegrationList();

        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
        // Handle successful submission
      } catch (error) {
        console.error('Failed to submit the template: ', error);
      }
    },

    async deleteIntegration(integration_id) {
      try {

        const toast = useToast();
        const token = localStorage.getItem('token');
        const confirmDelete=confirm("Are you sure you want to delete this contact?                           Note:Make sure to also delete the webhook from woocommece.")
        if (!confirmDelete) return;
        const response = await fetch(`http://localhost:8000/integration/${integration_id}`, 
          {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );

  
        if(response.ok){
          toast.success("Integration deleted successfully")
          this.fetchIntegrationList();
        }
        else{
          const errordata=await response.json()
          toast.error(`Error:${errordata.detail}`)
        }


      } catch (error) {
        console.error('Failed to delete the integration: ', error)

      }
    },

    async fetchIntegrationList() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch("http://localhost:8000/integration/list", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const IntegrationList = await response.json();
        this.integrations = IntegrationList.map(integration => ({
          id: integration.id,
          app: integration.app,
          type: integration.type,
          api_key: integration.api_key
        }));
      } catch (error) {
        console.error('Failed to submit the template: ', error);
      }
    }
  }
}
</script>

<style scoped>
/* Add your styles here */
.woocommerceBox {
  padding: 10px;
  border-radius: 10px;
  border: solid;
  width: fit-content;
}

.webhookConfig ul li {
  margin-bottom: 5px;
}

.popup-content {
  max-height: 700px;
  /* Limit the height of the popup */
  overflow-y: auto;
  /* Enable vertical scrolling if content exceeds max-height */
}

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