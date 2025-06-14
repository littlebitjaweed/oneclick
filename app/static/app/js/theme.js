<<<<<<< HEAD
// theme.js
const themeToggleButton = document.getElementById("theme-toggle");

// Check if dark mode was previously enabled in localStorage
if (localStorage.getItem('theme') === 'dark') {
  document.body.classList.add('dark');
} else {
  document.body.classList.remove('dark');
}

// Toggle dark mode on button click
themeToggleButton.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  
  // Save the theme preference in localStorage
  if (document.body.classList.contains("dark")) {
    localStorage.setItem('theme', 'dark');
  } else {
    localStorage.setItem('theme', 'light');
  }
});
=======
// Toggle Navbar Menu on Mobile
function toggleMenu() {
    const navbarMenu = document.getElementById('navbarMenu');
    navbarMenu.classList.toggle('active');
  }
  
  // Dark Mode Toggle
  const themeToggleBtn = document.getElementById('theme-toggle');
  const body = document.body;
  
  themeToggleBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDarkMode = body.classList.contains('dark-mode');
    themeToggleBtn.textContent = isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode';
    localStorage.setItem('darkMode', isDarkMode);
  });
  
  // Check Local Storage for Dark Mode Preference
  if (localStorage.getItem('darkMode') === 'true') {
    body.classList.add('dark-mode');
    themeToggleBtn.textContent = '☀️ Light Mode';
  }
>>>>>>> c32b2ba38f68d6d961bdd4dc00a7cd7874bf8545
