/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './layouts/**/*.html',
    './content/**/*.md',
    './assets/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary:      '#CC0000',
        'primary-dark': '#990000',
        gold:         '#F0A500',
        dark:         '#1C1C1C',
        surface:      '#F8F8F8',
      },
      fontFamily: {
        headline: ['Oswald', 'sans-serif'],
        body:     ['Inter', 'sans-serif'],
      },
      fontSize: {
        'xs':  '12px',
        'sm':  '14px',
        'base':'16px',
        'lg':  '20px',
        'xl':  '24px',
        '2xl': '30px',
        '3xl': '36px',
        '4xl': '48px',
      },
    },
  },
  safelist: ['opacity-0'],
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
