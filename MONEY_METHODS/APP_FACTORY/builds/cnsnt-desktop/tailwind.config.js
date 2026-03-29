/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#1a1a2e',
          light: '#16213e',
          dark: '#0f0f23',
        },
        coral: {
          DEFAULT: '#e94560',
          light: '#ff6b81',
          dark: '#c23152',
        },
        ocean: '#0f3460',
      },
      borderRadius: {
        xl: '12px',
      },
      fontFamily: {
        sans: ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
