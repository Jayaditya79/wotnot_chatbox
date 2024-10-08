<template>
  <div class="content-section md:ml-64">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Broadcast Messages</h2>
        <p class="text-sm md:text-base">Send out Broadcast Messages using templates</p>
      </div>

      <div>
        <button @click="showPopup = true, fetchContacts()"
          class="bg-[#075e54] text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base rounded-md shadow-lg ">
          New Broadcast
        </button>
      </div>
    </div>

    <PopUp v-if="showPopup" @close="showPopup = false, clearForm()">

      <div></div>

      <h2 class="text-xl font-semibold mb-4">New Broadcast</h2>
      <hr class="mb-4" />


      <form @submit.prevent="handleBroadcast" id="messageForm">


        <h4><b>What message do you want to send?</b></h4>
        <p class="text-sm mb-2 ">Add broadcast name and template below</p>



        <div class="p-4 bg-[#f5f6fa] mb-4">

          <!-- Input Bradacast Name -->
          <div class="mb-2">
            <label for="broadcastName" class="block text-sm font-medium">Broadcast Name<span
                class="text-red-800">*</span></label>
            <input type="text" v-model="broadcastName" id="broadcastName" placeholder="Broadcast Name" required
              class="border border-gray-300 rounded px-3 py-2 w-full">
          </div>

          <!-- input template -->
          <div class="mb-2 ">
            <label for="templates" class="block text-sm font-medium">Choose a template<span
                class="text-red-800">*</span></label>
            <!-- <select v-model="selectedTemplate" id="templates" required
              class="border border-gray-300 rounded px-3 py-2 w-full">
              <option value="" disabled>Select your option</option>
              <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.name }}</option>
            </select> -->

            <!-- New select field-->
            <select id="template-select" v-model="selectedTemplateId" @change="onTemplateSelect"
              class="border border-gray-300 rounded px-3 py-2 w-full ">
              <option v-for="template in templates" :key="template.id" :value="template.id">
                {{ template.name }}
              </option>
            </select>

            <!-- Conditional Image URL input field -->
            <div v-if="selectedTemplateHasImage">
              <label for="" class="block text-sm font-semibold">Upload Media</label>
              <input type="file" @change="onFileChange" class="mb-2 w-[60%] mr-1">
            </div>
            <div v-if="uploadedMedia">{{ this.mediaId }}</div>

            <div v-if="selectedTemplateHasParameters">
              <label for="">Select Parameter</label>
              <select name="" id="" v-model="bodyParameter">
                <option value="Name">Cotact_Name</option>
              </select>
            </div>


          </div>

        </div>
        <h4><b>Who do you want to send it to?</b></h4>
        <p class="text-sm mb-2 ">Select contacts below or <a
            href="https://drive.google.com/file/d/1hVQErwmNN6eGN1zLBoniW_34-GzAtMwm/view?usp=sharing" target="_blank"
            class="text-blue-500"><u>Download sample format for contact upload</u></a></p>

        <div class="p-4 bg-[#f5f6fa] mb-4">

          <div class="mb-2">
            <label for="recipients" class="block text-sm font-medium">Recipients<span
                class="text-red-800">*</span></label>
            <input type="text" v-model="recipients" id="recipients" placeholder="Enter phone numbers, comma-separated"
              required class="border border-gray-300 rounded px-3 py-2 w-full">
          </div>


          <div class="mb-1">
            <label for="csvFile" class="block text-sm font-semibold">Upload CSV for Contacts:</label>
            <input type="file" @change="handleFileUpload" class="mb-2 w-[60%] mr-1" />

          </div>
        </div>
        <div v-if="csvUploaded">
          <h4><b>Imported Contacts</b></h4>
          <p class="text-sm mb-2 ">Imported contacts are not saved to your contacts directory</p>
        </div>

        <div v-else>
          <h4><b>Contacts</b></h4>
          <p class="text-sm mb-2 ">Select from your saved contacts</p>
        </div>



        <div class="p-4 bg-[#f5f6fa] mb-4">
          <div class="overflow-x-auto max-h-[20vh] custom-scrollbar">
            <table class="contact-table w-full rounded-lg border-collapse">
              <thead>
                <tr class="bg-[#dddddd] text-center">
                  <th class="z-10 p-2 bg-[#dddddd] sticky top-0">
                    <input type="checkbox" @change="selectAll($event)" v-model="allSelected"
                      class=" scale-150 m-2 z-10">Select
                  </th>
                  <th class="p-2 bg-[#dddddd]  sticky top-0">Name</th>
                  <th class="p-2 bg-[#dddddd]  sticky top-0">Phone Number</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="contact in contacts" :key="contact.id">
                  <td class="text-center p-2 md:p-4 scale-125 "><input type="checkbox" v-model="selectedContacts"
                      :value="contact.phone"></td>
                  <td class="text-center p-2 md:p-4">{{ contact.name }}</td>
                  <td class="text-center p-2 md:p-4">{{ contact.phone }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <h4><b>When do you want to send the message ?</b></h4>
        <p class="text-sm mb-2 ">Select from the options below </p>


        <div class="p-4 bg-[#f5f6fa] mb-4">


          <p class=" text-sm font-semibold mb-1"><input type="radio" v-model="isScheduled" :value="false"
              class="scale-150 text-green-500 m-2">Send Now</p>

          <p class="text-sm font-semibold mb-1"><input type="radio" v-model="isScheduled" :value="true"
              class="scale-150 text-green-500 m-2" @click="currentDateTime">Schedule </p>

          <div v-if="isScheduled" class="flex justify-between">
            <div class="w-[50%]">
              <label for="scheduleDate" class="block text-sm font-medium">Date<span
                  class="text-red-800">*</span></label>
              <input type="date" v-model="scheduleDate" id="scheduleDate" required
                class="border border-gray-300 rounded px-3 py-2 w-full">
            </div>
            <div class="w-[50%]">
              <label for="scheduleTime" class="block text-sm font-medium">Time<span class="text-red-800">*</span>(GMT
                +5:30)</label>
              <input type="time" v-model="scheduleTime" id="scheduleTime" required
                class="border border-gray-300 rounded px-3 py-2 w-full">
            </div>
          </div>
        </div>



        <button type="submit" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded">{{ isScheduled ? 'Schedule Message'
          : 'Send Message' }}</button>
      </form>
      <div id="response"></div>
    </PopUp>


    <div class=" bg-[#f5f6fa] p-4  filter-container space-x-2">
      <h3 class="text-xl md:text-2xs mb-2 text-gray-600"><b>Broadcast List</b></h3>

      <div class="flex items-center filter-container space-x-2">
        <h3><b>Filter by:</b></h3>

        <div class="w-40px">
          <select name="" id="" @change="filterBroadcastsByStatus" class="border border-gray-300 rounded px-3 py-2 ">
            <option value="">Status</option>
            <option value="Successful">Successful</option>
            <option value="Cancelled">Cancelled</option>
            <option value="Partially Successful">Partially Successful</option>
          </select>
        </div>
      </div>


    </div>


    <!-- <div class="broadcastListContainer bg-gray-100 rounded-lg p-4 max-w-full mx-auto shadow-md custom-scrollbar"> -->
    <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
      <table class="w-full rounded-lg border-collapse">
        <thead>
          <tr class="bg-[#ffffff] text-center">

            <th class="p-2 md:p-4 text-left border-b-2 bg-[#ffffff] sticky top-0 ">Broadcast Name</th>
            <th class="p-2 md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Type</th>
            <th class="p-2 md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Template</th>
            <th class="p-2 md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Contacts</th>
            <th class="p-2 md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Status</th>
            <th class="p-2 md:p-4 border-b-2 bg-[#ffffff] sticky top-0 ">Action</th>


          </tr>
        </thead>
        <tbody class="bg-white">
          <tr v-for="broadcast in broadcasts" :key="broadcast.id">

            <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.name }}</td>
            <td class="border-[#ddd] p-2 md:p-4 text-center">{{ broadcast.type }}</td>
            <td class="border-[#ddd] p-2 md:p-4 text-center">{{ broadcast.template }}</td>
            <td class="border-[#ddd] p-2 md:p-4 text-center">{{ broadcast.contacts.length }}</td>
            <td class="p-2 md:p-4 text-center">
              <div :class="{
                'bg-[#e9f6ee] text-green-600 ': broadcast.status === 'Successful',
                'bg-blue-200 text-blue-600 ': broadcast.status === 'Scheduled',
                'bg-red-200 text-red-600 ': broadcast.status === 'Cancelled',
                'bg-yellow-100 text-yellow-500 ': broadcast.status === 'Partially Successful',
                'bg-yellow-200 text-yellow-600 ': broadcast.status === 'processing...',
                'border-[#ddd]': true
              }" class="text-[80%] lg:text-[100%] rounded-lg">
                {{ broadcast.status }}
              </div>
            </td>
            <td class="border-[#ddd] p-2 md:p-4 text-center"><button
                class="my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200"
                @click="showReportPopup = true, fetchBroadcastReport(broadcast.id)"> View Report</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>


    <!-- </div> -->
    <PopUp v-if="showReportPopup" @close="showReportPopup = false, broadcastReports = ['']">

      <h3 class="text-xl md:text-2xs mb-4"><b>Broadcast Report</b></h3>

      <!-- show the overview totals -->

      <div class="grid grid-cols-4 gap-4 p-4">
        <!-- Sent -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">

          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.sent }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white"><svg width="18"
                height="14" viewBox="0 0 18 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1.66797 7L7.16797 12.5L16.3346 1.5" stroke="#23A455" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round"></path>
              </svg></div>
          </div>


          <span class="text-gray-500">Sent</span>
        </div>

        <!-- Delivered -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">

          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.delivered }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white"><svg width="22"
                height="12" viewBox="0 0 22 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1.83203 6L6.64453 10.5833L9.05078 7.83333" stroke="#23A455" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"></path>
                <path d="M7.33203 5.99984L12.1445 10.5832L20.1654 1.4165" stroke="#23A455" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"></path>
                <path d="M14.6654 1.4165L11.457 5.08317" stroke="#23A455" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round"></path>
              </svg></div>
          </div>


          <span class="text-gray-500">Delivered</span>
        </div>

        <!-- Read -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.read }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white"><svg width="22"
                height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M20.2565 6.962C20.7305 7.582 20.7305 8.419 20.2565 9.038C18.7635 10.987 15.1815 15 10.9995 15C6.81752 15 3.23552 10.987 1.74252 9.038C1.51191 8.74113 1.38672 8.37592 1.38672 8C1.38672 7.62408 1.51191 7.25887 1.74252 6.962C3.23552 5.013 6.81752 1 10.9995 1C15.1815 1 18.7635 5.013 20.2565 6.962V6.962Z"
                  stroke="#23A455" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                <path
                  d="M11 11C12.6569 11 14 9.65685 14 8C14 6.34315 12.6569 5 11 5C9.34315 5 8 6.34315 8 8C8 9.65685 9.34315 11 11 11Z"
                  stroke="#23A455" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
              </svg></div>

          </div>
          <span class="text-gray-500">Read</span>
        </div>

        <!-- Replied -->
        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.replied }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white">
              <svg width="22" height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M8.60219 0.736277C8.76965 0.805709 8.91277 0.923237 9.01344 1.074C9.11411 1.22476 9.16782 1.40199 9.16777 1.58328V3.03711L11.2697 0.935194C11.3979 0.807035 11.5612 0.719762 11.739 0.684408C11.9168 0.649055 12.1011 0.667208 12.2685 0.736572C12.436 0.805936 12.5792 0.923397 12.6799 1.07411C12.7806 1.22482 12.8344 1.40201 12.8344 1.58328V4.35986C14.5385 4.45978 15.9245 4.84203 17.0447 5.44519C18.2398 6.0821 19.2221 7.0554 19.8699 8.24469C21.0524 10.3851 21.0844 12.9023 21.0844 14.4166C21.0844 14.6597 20.9879 14.8929 20.816 15.0648C20.644 15.2367 20.4109 15.3333 20.1678 15.3333C19.9247 15.3333 19.6915 15.2367 19.5196 15.0648C19.3477 14.8929 19.2511 14.6597 19.2511 14.4166C19.2511 13.8474 19.0513 13.4257 18.7039 13.0783C18.3335 12.7089 17.7679 12.399 17.0245 12.1616C15.7925 11.7693 14.2562 11.6354 12.8344 11.6437V14.4166C12.8344 14.5979 12.7806 14.7751 12.6799 14.9258C12.5792 15.0765 12.436 15.1939 12.2685 15.2633C12.1011 15.3327 11.9168 15.3508 11.739 15.3155C11.5612 15.2801 11.3979 15.1929 11.2697 15.0647L9.16777 12.9628V14.4166C9.16773 14.5979 9.11395 14.7751 9.01322 14.9258C8.9125 15.0765 8.76935 15.1939 8.60187 15.2633C8.4344 15.3327 8.25012 15.3508 8.07233 15.3155C7.89454 15.2801 7.73122 15.1929 7.60302 15.0647L1.18636 8.64803C1.01451 8.47613 0.917969 8.24301 0.917969 7.99994C0.917969 7.75688 1.01451 7.52376 1.18636 7.35186L7.60302 0.935194C7.73121 0.806922 7.89457 0.719555 8.07243 0.684147C8.25028 0.648739 8.43465 0.666881 8.60219 0.736277ZM7.33444 11.1294L4.85302 8.64803C4.68117 8.47613 4.58464 8.24301 4.58464 7.99994C4.58464 7.75688 4.68117 7.52376 4.85302 7.35186L7.33444 4.87044V3.79611L3.13061 7.99994L7.33444 12.2038V11.1294ZM18.955 11.0011C18.8138 10.3485 18.5814 9.719 18.2648 9.13111C17.7871 8.24994 17.0601 7.5293 16.1748 7.05944C15.1866 6.52686 13.8199 6.16661 11.9178 6.16661C11.6747 6.16661 11.4415 6.07003 11.2696 5.89812C11.0977 5.72622 11.0011 5.49306 11.0011 5.24994V3.79611L6.79727 7.99994L11.0011 12.2038V10.7499C11.0011 10.514 11.0921 10.2871 11.2552 10.1165C11.4182 9.94593 11.6408 9.84481 11.8765 9.83419C13.5989 9.75628 15.787 9.84336 17.5819 10.4154C18.0584 10.5635 18.5185 10.7601 18.955 11.002V11.0011Z"
                  fill="#23A455"></path>
              </svg>
            </div>

          </div>

          <span class="text-gray-500">Replied</span>
        </div>

        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.sent }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white">
              <svg width="22" height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M8.60219 0.736277C8.76965 0.805709 8.91277 0.923237 9.01344 1.074C9.11411 1.22476 9.16782 1.40199 9.16777 1.58328V3.03711L11.2697 0.935194C11.3979 0.807035 11.5612 0.719762 11.739 0.684408C11.9168 0.649055 12.1011 0.667208 12.2685 0.736572C12.436 0.805936 12.5792 0.923397 12.6799 1.07411C12.7806 1.22482 12.8344 1.40201 12.8344 1.58328V4.35986C14.5385 4.45978 15.9245 4.84203 17.0447 5.44519C18.2398 6.0821 19.2221 7.0554 19.8699 8.24469C21.0524 10.3851 21.0844 12.9023 21.0844 14.4166C21.0844 14.6597 20.9879 14.8929 20.816 15.0648C20.644 15.2367 20.4109 15.3333 20.1678 15.3333C19.9247 15.3333 19.6915 15.2367 19.5196 15.0648C19.3477 14.8929 19.2511 14.6597 19.2511 14.4166C19.2511 13.8474 19.0513 13.4257 18.7039 13.0783C18.3335 12.7089 17.7679 12.399 17.0245 12.1616C15.7925 11.7693 14.2562 11.6354 12.8344 11.6437V14.4166C12.8344 14.5979 12.7806 14.7751 12.6799 14.9258C12.5792 15.0765 12.436 15.1939 12.2685 15.2633C12.1011 15.3327 11.9168 15.3508 11.739 15.3155C11.5612 15.2801 11.3979 15.1929 11.2697 15.0647L9.16777 12.9628V14.4166C9.16773 14.5979 9.11395 14.7751 9.01322 14.9258C8.9125 15.0765 8.76935 15.1939 8.60187 15.2633C8.4344 15.3327 8.25012 15.3508 8.07233 15.3155C7.89454 15.2801 7.73122 15.1929 7.60302 15.0647L1.18636 8.64803C1.01451 8.47613 0.917969 8.24301 0.917969 7.99994C0.917969 7.75688 1.01451 7.52376 1.18636 7.35186L7.60302 0.935194C7.73121 0.806922 7.89457 0.719555 8.07243 0.684147C8.25028 0.648739 8.43465 0.666881 8.60219 0.736277ZM7.33444 11.1294L4.85302 8.64803C4.68117 8.47613 4.58464 8.24301 4.58464 7.99994C4.58464 7.75688 4.68117 7.52376 4.85302 7.35186L7.33444 4.87044V3.79611L3.13061 7.99994L7.33444 12.2038V11.1294ZM18.955 11.0011C18.8138 10.3485 18.5814 9.719 18.2648 9.13111C17.7871 8.24994 17.0601 7.5293 16.1748 7.05944C15.1866 6.52686 13.8199 6.16661 11.9178 6.16661C11.6747 6.16661 11.4415 6.07003 11.2696 5.89812C11.0977 5.72622 11.0011 5.49306 11.0011 5.24994V3.79611L6.79727 7.99994L11.0011 12.2038V10.7499C11.0011 10.514 11.0921 10.2871 11.2552 10.1165C11.4182 9.94593 11.6408 9.84481 11.8765 9.83419C13.5989 9.75628 15.787 9.84336 17.5819 10.4154C18.0584 10.5635 18.5185 10.7601 18.955 11.002V11.0011Z"
                  fill="#23A455"></path>
              </svg>
            </div>

          </div>

          <span class="text-gray-500">Success</span>
        </div>

        <div class="bg-gray-100 p-4 rounded-md shadow-sm flex flex-col items-left border-2 border-green-600">
          <div class="flex justify-between items-center">
            <span class="text-3xl font-semibold">{{ totals.failed }}</span>
            <div class="w-10 h-10 flex items-center justify-center mb-auto rounded-full bg-white">
              <svg width="22" height="16" viewBox="0 0 22 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M8.60219 0.736277C8.76965 0.805709 8.91277 0.923237 9.01344 1.074C9.11411 1.22476 9.16782 1.40199 9.16777 1.58328V3.03711L11.2697 0.935194C11.3979 0.807035 11.5612 0.719762 11.739 0.684408C11.9168 0.649055 12.1011 0.667208 12.2685 0.736572C12.436 0.805936 12.5792 0.923397 12.6799 1.07411C12.7806 1.22482 12.8344 1.40201 12.8344 1.58328V4.35986C14.5385 4.45978 15.9245 4.84203 17.0447 5.44519C18.2398 6.0821 19.2221 7.0554 19.8699 8.24469C21.0524 10.3851 21.0844 12.9023 21.0844 14.4166C21.0844 14.6597 20.9879 14.8929 20.816 15.0648C20.644 15.2367 20.4109 15.3333 20.1678 15.3333C19.9247 15.3333 19.6915 15.2367 19.5196 15.0648C19.3477 14.8929 19.2511 14.6597 19.2511 14.4166C19.2511 13.8474 19.0513 13.4257 18.7039 13.0783C18.3335 12.7089 17.7679 12.399 17.0245 12.1616C15.7925 11.7693 14.2562 11.6354 12.8344 11.6437V14.4166C12.8344 14.5979 12.7806 14.7751 12.6799 14.9258C12.5792 15.0765 12.436 15.1939 12.2685 15.2633C12.1011 15.3327 11.9168 15.3508 11.739 15.3155C11.5612 15.2801 11.3979 15.1929 11.2697 15.0647L9.16777 12.9628V14.4166C9.16773 14.5979 9.11395 14.7751 9.01322 14.9258C8.9125 15.0765 8.76935 15.1939 8.60187 15.2633C8.4344 15.3327 8.25012 15.3508 8.07233 15.3155C7.89454 15.2801 7.73122 15.1929 7.60302 15.0647L1.18636 8.64803C1.01451 8.47613 0.917969 8.24301 0.917969 7.99994C0.917969 7.75688 1.01451 7.52376 1.18636 7.35186L7.60302 0.935194C7.73121 0.806922 7.89457 0.719555 8.07243 0.684147C8.25028 0.648739 8.43465 0.666881 8.60219 0.736277ZM7.33444 11.1294L4.85302 8.64803C4.68117 8.47613 4.58464 8.24301 4.58464 7.99994C4.58464 7.75688 4.68117 7.52376 4.85302 7.35186L7.33444 4.87044V3.79611L3.13061 7.99994L7.33444 12.2038V11.1294ZM18.955 11.0011C18.8138 10.3485 18.5814 9.719 18.2648 9.13111C17.7871 8.24994 17.0601 7.5293 16.1748 7.05944C15.1866 6.52686 13.8199 6.16661 11.9178 6.16661C11.6747 6.16661 11.4415 6.07003 11.2696 5.89812C11.0977 5.72622 11.0011 5.49306 11.0011 5.24994V3.79611L6.79727 7.99994L11.0011 12.2038V10.7499C11.0011 10.514 11.0921 10.2871 11.2552 10.1165C11.4182 9.94593 11.6408 9.84481 11.8765 9.83419C13.5989 9.75628 15.787 9.84336 17.5819 10.4154C18.0584 10.5635 18.5185 10.7601 18.955 11.002V11.0011Z"
                  fill="#23A455"></path>
              </svg>
            </div>

          </div>

          <span class="text-gray-500">Failed</span>
        </div>
      </div>

      <div class="broadcastListContainer bg-gray-100 rounded-lg p-4 max-w-full mx-auto shadow-md custom-scrollbar">
        <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
          <table class="w-full rounded-lg border-collapse">
            <thead>
              <tr class="bg-[#dddddd] text-center">
                <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Name</th>
                <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Phone No</th>
                <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Status</th>
                <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Sent</th>
                <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Delivered</th>
                <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Read</th>
                <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Replied</th>

              </tr>
            </thead>
            <tbody class="bg-white">
              <tr v-for="contactReport in broadcastReports" :key="contactReport.id">
                <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.contact_name}}</td>
                <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.phone_no }}</td>
                
                <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.status }}</td>
                <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.sent }}</td>
                <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.delivered }}</td>
                <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.read }}</td>
                <td class="border-[#ddd] p-2 md:p-4 text-center">{{ contactReport.replied }}</td>

              </tr>
            </tbody>
          </table>
        </div>


      </div>

    </PopUp>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification';
import PopUp from "../popups/popup"
export default {
  name: 'BroadCast2',

  components: {
    PopUp
  }
  ,
  data() {
    return {
      mediafile: null,
      mediaId: "",
      uploadedMedia: false,

      broadcastName: '',
      recipients: '',
      selectedTemplate: '',
      templates: [],
      contacts: [],
      broadcasts: [],
      // broadcast report
      broadcastReports: [],
      totalRead: '',
      totalSent: '',
      totalDelivered: '',
      csvUploaded: false,

      allSelected: false,


      csvFile: null,
      selectedContacts: [],
      showPopup: false,
      showReportPopup: false,
      scheduleDate: '',  // New data property for schedule date
      scheduleTime: '',
      isScheduled: false,


      selectedTemplateId: null, // Holds the selected template's ID
      selectedTemplateHasImage: false, // Boolean to control if image URL input should appear
      imageUrl: '',// To store the input value for the image URL
      selectedTemplateHasParameters: false,
      bodyParameters:[],
      bodyParameter:''

    };
  },
  async mounted() {
    // await this.fetchTemplates();
    await this.fetchContacts();
    await this.fetchBroadcastList();
    await this.fetchtemplateList();



    // Fetch contacts when the component is mounted
  },
  methods: {


    // async fetchTemplates() {
    //   try {
    //     const token = localStorage.getItem('token');
    //     const response = await fetch('http://localhost:8000/templates/', {
    //       method: 'GET',
    //       headers: {
    //         'Authorization': `Bearer ${token}`,
    //         'Content-Type': 'application/json',
    //       },
    //     });

    //     if (!response.ok) {
    //       throw new Error('Network response was not ok');
    //     }

    //     const templateNames = await response.json();
    //     this.templates = templateNames.map(name => ({ id: name, name }));
    //   } catch (error) {
    //     console.error('Error fetching templates:', error);
    //   }
    // },

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

    onTemplateSelect() {
      // Find the selected template
      const selectedTemplate = this.templates.find(template => template.id === this.selectedTemplateId);

      // Check if the selected template has a HEADER with IMAGE format
      const headerComponent = selectedTemplate.components.find(
        component => component.type === 'HEADER' && component.format === 'IMAGE'

      );

      if (headerComponent) {
        // Show the image input field and pre-fill with the example image URL if available
        this.selectedTemplateHasImage = true;
        this.imageUrl = headerComponent.example?.header_handle?.[0] || ''; // Use the first example image if available
      } else {
        // Hide the image input field if no image is found in the template
        this.selectedTemplateHasImage = false;
        this.imageUrl = '';
      }


      // Check if the selected template has BODY parameters
      const bodyComponent = selectedTemplate.components.find(component => component.type === 'BODY');

      if (bodyComponent && bodyComponent.text.includes('{{')) {
        // Extract the parameters from the body text if there are placeholders
        const parameterMatches = bodyComponent.text.match(/{{\d+}}/g);
        if (parameterMatches) {
          this.selectedTemplateHasParameters = true;
          this.bodyParameters = parameterMatches.map((param, index) => ({
            name: `Parameter ${index + 1}`,
            value: ''
          }));
        } else {
          this.selectedTemplateHasParameters = false;
          this.bodyParameters = [];
        }
      } else {
        // Hide the parameter input fields if no parameters are found
        this.selectedTemplateHasParameters = false;
        this.bodyParameters = [];
      }
    },



    async fetchContacts() {

      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/contacts/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const contactList = await response.json();
        this.contacts = contactList.map(contact => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone
        }));
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },

    async fetchBroadcastList(statusFilter = null) {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://localhost:8000/broadcast/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const broadcastList = await response.json();

        // Filter broadcasts based on the statusFilter if it's provided
        this.broadcasts = broadcastList
          .map(broadcast => ({
            id: broadcast.id,
            name: broadcast.name,
            type: broadcast.type,
            template: broadcast.template,
            contacts: broadcast.contacts,
            success: broadcast.success,
            failed: broadcast.failed,
            status: broadcast.status
          }))
          .filter(broadcast => {
            return statusFilter ? broadcast.status === statusFilter : true;
          });

      } catch (error) {
        console.error('Error fetching broadcasts:', error);
      }

    },

    filterBroadcastsByStatus(event) {
      const status = event.target.value;
      this.fetchBroadcastList(status);
    },

    formatDateTime(date) {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');

      return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    },

    updateRecipients() {
      this.recipients = this.selectedContacts.join(', ');
    },


    onFileChange(event) {
      this.file = event.target.files[0];
      this.uploadMedia();
    },


    async uploadMedia() {
      const token = localStorage.getItem('token');
      this.mediafile = event.target.files[0];
      const formData = new FormData();
      formData.append('file', this.mediafile);

      try {

        const response = await fetch("http://localhost:8000/upload-media", {
          method: "POST",
          headers: {

            'Authorization': `Bearer ${token}`,
            // 'Content-Type': 'multipart/form-data',

          },
          body: formData,
        });

        const media = await response.json()
        this.mediaId = media.whatsapp_media_id
        console.log(this.mediaId)

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        else {
          this.uploadedMedia = true
          alert("Media Uploaded Successfully")
        }
      } catch (error) {
        console.error('Error uploading media:', error);
      }
    },


    // async sendBroadcast() {
    //   // Logic for scheduling a broadcast

    //   const toast = useToast();
    //   const phoneNumbers = this.recipients.split(',').map(num => num.trim());
    //   const Template = this.templates.find(template => template.id === this.selectedTemplateId);
    //   const selectedTemplate = Template.name
    //   const formattedDate = this.formatDateTime(new Date());
    //   const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;
    //   const responseDiv = document.getElementById('response');
    //   const mediaID = this.mediaId
    //   // responseDiv.textContent = 'Scheduling...';
    //   const token = localStorage.getItem('token');
    //   try {

    //     this.showPopup = false;
    //     this.clearForm();
    //     this.fetchBroadcastList();

    //     const requestBody = {
    //       name: broadcastNameWithDate,
    //       recipients: phoneNumbers,
    //       template: selectedTemplate,
    //       type: "Broadcast",
    //       status: 'Save',
    //     };

    //     // Add image header if user has selected one
    //     if (mediaID) {
    //       requestBody.image_id = mediaID;
    //     }

    //     // Add body parameters if provided (array of parameters)
    //     // if (this.bodyParameters && this.bodyParameters.length > 0) {
    //     //     requestBody.body_parameters = this.bodyParameters;
    //     // }


    //     const response = await fetch('http://localhost:8000/send-template-message/', {
    //       method: 'POST',
    //       headers: {
    //         'Authorization': `Bearer ${token}`,
    //         'Content-Type': 'application/json',
    //       },
    //       body: JSON.stringify(requestBody),


    //     });

    //     if (!response.ok) {
    //       throw new Error('Network response was not ok');
    //     }
    //     else {
    //       this.fetchBroadcastList();
    //       toast.success("'Broadcast sent successfully");
    //       responseDiv.textContent = 'Broadcast sent successfully.';
    //     }

    //     const result = await response.json();
    //     responseDiv.textContent = `Success: ${result.successful_messages}, Errors: ${result.errors.length}`;

    //   } catch (error) {
    //     console.error('Error sending broadcast:', error);
    //     responseDiv.textContent = 'Error sending broadcast.';
    //   }
    // },
    async sendBroadcast() {
      const toast = useToast();

      // Assuming recipients have both name and number in format 'Name:1234567890'
      const contacts = this.recipients.split(',').map(entry => {
        const phone = entry.trim();
        return { name: name, phone };
      });

      const Template = this.templates.find(template => template.id === this.selectedTemplateId);
      const selectedTemplate = Template.name;
      const formattedDate = this.formatDateTime(new Date());
      const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;
      const responseDiv = document.getElementById('response');
      const mediaID = this.mediaId;
      const token = localStorage.getItem('token');
      const bodyparamter=this.bodyParameter

      try {
        this.showPopup = false;
        this.clearForm();
        this.fetchBroadcastList();

        const requestBody = {
          name: broadcastNameWithDate,
          recipients: contacts, // Now sending both name and number
          template: selectedTemplate,
          type: "Broadcast",
          status: 'Saved',
        };

        if (mediaID) {
          requestBody.image_id = mediaID;
        }

        if (bodyparamter) {
          requestBody.body_parameters = bodyparamter;
        }

        const response = await fetch('http://localhost:8000/send-template-message/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        } else {
          this.fetchBroadcastList();
          toast.success('Broadcast sent successfully');
        }

        const result = await response.json();
        responseDiv.textContent = `Success: ${result.successful_messages}, Errors: ${result.errors.length}`;

      } catch (error) {
        console.error('Error sending broadcast:', error);
        responseDiv.textContent = 'Error sending broadcast.';
      }
    },
    async fetchBroadcastReport(broadcast_id) {


      const token = localStorage.getItem('token');
      try {

        const response = await fetch(`http://localhost:8000/broadcast-report/${broadcast_id}`, {
          method: "GET",
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const result = await response.json()
        this.broadcastReports = result.map(report => ({

          phone_no: report.phone_no,
          contact_name: report.contact_name,
          status: report.status,
          sent: report.sent,
          delivered: report.delivered,
          read: report.read,
          replied: report.replied


        }));

      } catch (error) {
        console.error("Error fetching report for the broadcast", error)
      }
    },

    handleBroadcast() {
      if (this.isScheduled) {
        this.scheduleBroadcast2();

      } else {
        this.sendBroadcast();
      }
    },
    async scheduleBroadcast2() {

      const contacts = this.recipients.split(',').map(entry => {
        const phone = entry.trim();
        return { name:phone , phone };
      });


      // Logic for scheduling a broadcast
      const toast = useToast();
      // const phoneNumbers = this.recipients.split(',').map(num => num.trim());
      const Template = this.templates.find(template => template.id === this.selectedTemplateId);
      const selectedTemplate = Template.name;
      const formattedDate = this.formatDateTime(new Date());
      const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;
      const responseDiv = document.getElementById('response');
      // responseDiv.textContent = 'Scheduling...';
      const token = localStorage.getItem('token');
      const mediaID = this.mediaId;
      const bodyparamter=this.bodyParameter

      // Combine date and time for scheduling
      const scheduledDatetime = new Date(`${this.scheduleDate}T${this.scheduleTime}`).toISOString();

      try {

        this.showPopup = false;
        this.clearForm();
        this.fetchBroadcastList();

        this.showPopup = false;
        this.clearForm();
        this.fetchBroadcastList();

        const requestBody = {
          name: broadcastNameWithDate,
            recipients: contacts,
            template: selectedTemplate,
            type: "Scheduled",
            status: 'Saved',
            scheduled_time: scheduledDatetime
        };

        if (mediaID) {
          requestBody.image_id = mediaID;
        }

        if (bodyparamter) {

          requestBody.body_parameters = bodyparamter;
        }

        const response = await fetch(`http://localhost:8000/schedule-template-message/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }


        toast.success("Broadcast scheduled successfully");
        this.fetchBroadcastList();
      } catch (error) {
        console.error('Error scheduling broadcast:', error);
        responseDiv.textContent = 'Error scheduling broadcast.';
      }
    },


    clearForm() {
      this.contact = "",
        this.broadcastName = '',
        this.selectedTemplateHasParameters='',
        this.selectedTemplateHasImage=false,
        this.selectedTemplateId='',
        this.bodyParameter='',
        this.recipients = '',
        this.selectedTemplate = '',
        this.csvFile = null,
        this.mediaId = "",
        this.mediafile = null,
        this.uploadedMedia = false,
        this.selectedContacts = [],
        this.scheduleDate = '',  // New data property for schedule date
        this.scheduleTime = '',
        this.isScheduled = false,
        this.contacts = [],
        this.csvUploaded = false

    },

    handleFileUpload(event) {
      this.csvFile = event.target.files[0];
      this.importCSV();

    },

    async importCSV() {
      const toast = useToast();
      if (!this.csvFile) {
        alert('Please select a file to import.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.csvFile);

      try {
        const response = await fetch('http://localhost:8000/import-contacts', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.contacts = data.contacts;
        this.csvUploaded = true;
        toast.success('Contacts imported successfully!');

        // Format and append contacts in the required format 'Name:1234567890'
        const formattedContacts = this.contacts.map(contact => `${contact.name}:${contact.phone}`).join(',');

        // Update recipients with formatted contact list
        this.recipients = this.recipients ? `${this.recipients},${formattedContacts}` : formattedContacts;

      } catch (error) {
        console.error(error);
        toast.error('Failed to import contacts.');
      }
    },


    // async importCSV() {
    //   const toast = useToast();
    //   if (!this.csvFile) {
    //     alert('Please select a file to import.');
    //     return;
    //   }

    //   const formData = new FormData();
    //   formData.append('file', this.csvFile);

    //   try {
    //     const response = await fetch('http://localhost:8000/import-contacts', {
    //       method: 'POST',
    //       body: formData,
    //     });

    //     if (!response.ok) {
    //       throw new Error('Network response was not ok');
    //     }

    //     const data = await response.json();
    //     this.contacts = data.contacts;
    //     this.csvUploaded = true
    //     toast.success('Contacts imported successfully!');

    //     // Append phone numbers to the recipients input field
    //     const phoneNumbers = this.contacts.map(contact => contact.phone).join(',');
    //     this.recipients = this.recipients ? this.recipients + ',' + phoneNumbers : phoneNumbers;
    //   } catch (error) {
    //     console.error(error);
    //     toast.error('Failed to import contacts.');
    //   }
    // },

    selectAll(event) {
      // Check if the "Select All" checkbox is checked or unchecked
      if (event.target.checked) {
        // Select all contacts by pushing all contact phone numbers to the selectedContacts array
        this.selectedContacts = this.contacts.map(contact => contact.phone);
      } else {
        // Deselect all contacts by clearing the selectedContacts array
        this.selectedContacts = [];
      }
    },

    currentDateTime() {
      const now = new Date();

      // Format the date as YYYY-MM-DD
      const year = now.getFullYear();
      const month = (now.getMonth() + 1).toString().padStart(2, '0');
      const day = now.getDate().toString().padStart(2, '0');
      this.scheduleDate = `${year}-${month}-${day}`;

      // Add 5 minutes to the current time
      now.setMinutes(now.getMinutes() + 2);
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      this.scheduleTime = `${hours}:${minutes}`;
    }


  },
  computed: {
    totals() {
      return this.broadcastReports.reduce(
        (acc, report) => {
          acc.sent += report.sent ? 1 : 0;
          acc.delivered += report.delivered ? 1 : 0;
          acc.read += report.read ? 1 : 0;
          acc.replied += report.replied ? 1 : 0;
          acc.failed += report.status === "failed" ? 1 : 0;
          return acc;
        },
        { sent: 0, delivered: 0, read: 0, replied: 0, failed: 0 } // Initial count set to 0 for all
      );
    }
  },
  watch: {
    selectedContacts: function () {
      this.updateRecipients();
    },
    selectedContactsAll(newSelectedContacts) {
      // Check if all contacts are selected
      this.updateRecipients();
      this.allSelected = newSelectedContacts.length === this.contacts.length;
    },
    mounted() {
      // Get the current date and time

    }
  }
};
</script>

<style scoped>
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

.my-custom-toast {
  background-color: #4caf50;
  /* Custom background */
  color: white;
  font-size: 16px;
  border-radius: 10px;
}
</style>
