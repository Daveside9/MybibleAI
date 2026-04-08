import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // MatchHang Brand Colors
        navy: {
          DEFAULT: '#071226',
          50: '#0A1B3D',
          100: '#0D2454',
          200: '#102D6B',
        },
        primary: {
          DEFAULT: '#0B6CF1',
          50: '#E6F2FF',
          100: '#CCE5FF',
          200: '#99CBFF',
          300: '#66B1FF',
          400: '#3397FF',
          500: '#0B6CF1',
          600: '#0956C1',
          700: '#074091',
          800: '#052B61',
          900: '#031530',
        },
        cyan: {
          DEFAULT: '#00C2FF',
          50: '#E6F9FF',
          100: '#CCF3FF',
          200: '#99E7FF',
          300: '#66DBFF',
          400: '#33CFFF',
          500: '#00C2FF',
          600: '#009BCC',
          700: '#007499',
          800: '#004D66',
          900: '#002633',
        },
        success: '#32D583',
        danger: '#FF5964',
        warning: '#FFA500',
        text: {
          primary: '#EAF2FF',
          muted: '#93A5C4',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Inter', 'system-ui', 'sans-serif'], // Temporarily using Inter instead of Poppins
      },
      borderRadius: {
        'card': '12px',
      },
      animation: {
        'marquee': 'marquee 25s linear infinite',
        'marquee-slow': 'marquee 35s linear infinite',
      },
      keyframes: {
        marquee: {
          '0%': { transform: 'translateX(0%)' },
          '100%': { transform: 'translateX(-100%)' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
