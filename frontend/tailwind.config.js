/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Dark theme colors matching the reference image
                primary: {
                    bg: '#0f1419',      // Very dark background
                    card: '#1a1f2e',    // Dark navy cards
                    border: '#2d3748',  // Subtle borders
                },
                accent: {
                    blue: '#3b82f6',    // Bright blue for buttons
                    green: '#10b981',   // Success green
                    red: '#ef4444',     // Error red
                    purple: '#8b5cf6',  // Purple accent
                },
                text: {
                    primary: '#f3f4f6',  // Light text
                    secondary: '#9ca3af', // Muted text
                }
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'fade-in': 'fadeIn 0.3s ease-in-out',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
        },
    },
    plugins: [],
}
