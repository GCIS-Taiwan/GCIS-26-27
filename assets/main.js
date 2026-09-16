document.addEventListener('DOMContentLoaded', () => {
    // --- DARK MODE TOGGLE ---
    const toggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (toggleBtn) toggleBtn.textContent = 'Light';
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');
            if (theme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                toggleBtn.textContent = 'Dark';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                toggleBtn.textContent = 'Light';
            }
        });
    }

    // --- MOBILE PHOTO EXPAND TOGGLE ---
    document.querySelectorAll('.newsletter-img').forEach(img => {
        img.addEventListener('click', () => {
            img.classList.toggle('expanded');
        });
    });
});