/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        primary: '#2c3e50',
        accent: '#f4d03f',
        'pale-yellow': '#ffeeb0',
        'dark-gold': '#fcd670',
      },
      fontFamily: {
        sans: ['Inter', 'Open Sans', 'sans-serif'],
        heading: ['Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
