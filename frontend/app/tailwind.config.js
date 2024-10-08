/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html', // Adjust this if you're using an HTML file
    './src/**/*.{vue,js,ts,jsx,tsx}', // Add paths for your Vue files
  ],
  theme: {
    extend: {
      screens: {
        'below-402': {'max': '402px'}, // Custom breakpoint for screens below 402px
      },
      fontSize: {
        'custom-small': '0.780rem', // Custom font size
      },
      color:
      {
'whatsapp-green': '#075E54'
     },
     strokeWidth: {
      '5': '5', // Adds a stroke-width of 5
    },
      
    },
  },
  plugins: [],
}
