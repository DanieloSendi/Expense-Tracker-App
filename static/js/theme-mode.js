function setTheme(theme) {
    localStorage.setItem("theme", theme);
    applyTheme();
}

function applyTheme() {
    let theme = localStorage.getItem("theme") || "auto";

    // If the user has not previously set a theme, we use “auto” by default.
    if (!theme) {
        theme = "auto";
        localStorage.setItem("theme", "auto");
    }

    let themeIcon = document.getElementById("themeIcon");

    // Resetowanie aktywnych klas w dropdownie
    document.getElementById("lightMode").classList.remove("active");
    document.getElementById("darkMode").classList.remove("active");
    document.getElementById("autoMode").classList.remove("active");

    if (theme === "dark") {
        document.documentElement.setAttribute("data-bs-theme", "dark");
        themeIcon.innerText = "🌙";
        document.getElementById("darkMode").classList.add("active");
    } else if (theme === "light") {
        document.documentElement.setAttribute("data-bs-theme", "light");
        themeIcon.innerText = "☀️";
        document.getElementById("lightMode").classList.add("active");
    } else {
        // Tryb AUTO → używa ustawień systemowych
        if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
            document.documentElement.setAttribute("data-bs-theme", "dark");
            themeIcon.innerText = "🌓";
        } else {
            document.documentElement.setAttribute("data-bs-theme", "light");
            themeIcon.innerText = "🌓";
        }
        document.getElementById("autoMode").classList.add("active");
    }
}

// Listening for changes in system settings
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (localStorage.getItem("theme") === "auto") {
        applyTheme();
    }
});

// Setting the theme at the start
document.addEventListener("DOMContentLoaded", applyTheme);
