
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    // Match root level source files (App.tsx, index.tsx, etc.)
    // Explicitly avoids "./**" to prevent scanning node_modules which slows down builds
    "./*.{js,ts,jsx,tsx}",
    // Match components directory
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
