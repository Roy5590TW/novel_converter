export function initDarkMode() {
    const savedTheme = localStorage.getItem('theme');
    const html = document.documentElement;
    
    // Initialization judgment
    if (savedTheme === 'dark') {
        html.classList.add('dark-mode');
        updateThemeUI(true);
    } else if (savedTheme === 'light') {
        html.classList.add('light-mode');
        updateThemeUI(false);
    } else {
        // Follow the system
        const isSystemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        updateThemeUI(isSystemDark);
    }
}

export function toggleDarkMode() {
    const html = document.documentElement;
    const isCurrentlyDark = getComputedStyle(html).getPropertyValue('--bg-color').trim() === '#121212';

    if (isCurrentlyDark) {
        html.classList.remove('dark-mode');
        html.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
        updateThemeUI(false);
    } else {
        html.classList.remove('light-mode');
        html.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
        updateThemeUI(true);
    }
}

function updateThemeUI(isDark) {
    const icon = document.getElementById('theme-icon');
    const text = document.getElementById('theme-text');
    if (icon && text) {
        icon.innerText = isDark ? '☀️' : '🌙';
        text.innerText = isDark ? '淺色模式' : '深色模式';
    }
}