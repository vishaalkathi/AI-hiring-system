/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#00685f",
          container: "#008378",
        },

        secondary: {
          DEFAULT: "#006c4c",
        },

        tertiary: {
          DEFAULT: "#0058be",
        },

        surface: {
          DEFAULT: "#faf8ff",
          low: "#f2f3ff",
          high: "#e2e7ff",
        },

        "on-surface": "#131b2e",

        outline: {
          DEFAULT: "#6d7a77",
        },
      },

      fontFamily: {
        sans: ["Plus Jakarta Sans", "sans-serif"],
      },

      width: {
        sidebar: "260px",
      },

      spacing: {
        gutter: "1.25rem",
      },

      borderRadius: {
        card: "1rem",
        button: "0.75rem",
      },

      inset: {
        sidebar: "260px",
      },
      
      margin: {
        sidebar: "260px",
      },
    },
  },

  plugins: [],
};