import { initDarkMode, toggleDarkMode } from './dark_mode_support.js';
import { initLibrary, showHome, showChapters, prevChapter, nextChapter } from './app.js';

// Initialization
initDarkMode();
initLibrary();

// Binding events
document.getElementById('theme-toggle').onclick = toggleDarkMode;

document.getElementById('back-to-home').onclick = showHome;
document.getElementById('back-to-chapters').onclick = showChapters;
document.getElementById('nav-back-chapters').onclick = showChapters;

document.getElementById('prev-btn').onclick = prevChapter;
document.getElementById('next-btn').onclick = nextChapter;