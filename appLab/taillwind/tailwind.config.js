/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../apps/attendance/form.py',
    '../apps/report/forms.py'
  ],
  theme: {
    extend: {
      screens: {
        print: {raw : 'print'},
      }
    },
    fontFamily: {
      "exo": ['"exo 2"'],
      "rale": ['"Raleway"'],
    },
  },
  plugins: [],
}

