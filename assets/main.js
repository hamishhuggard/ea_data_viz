function toggleSidebarVisible() {

	const sidebar = document.getElementById("sidebar");
	const buttress = document.getElementById("sidebar-buttress");

    if (sidebar.classList.contains("toggled")) {
        sidebar.classList.remove("toggled");
        buttress.classList.remove("toggled");
    } else {
        sidebar.classList.add("toggled");
        buttress.classList.add("toggled");
    }

}

function toggleAboutVisibility() {

	const about = document.getElementById("about-box");

    if (about.classList.contains("hidden")) {
        about.classList.remove("hidden");
    } else {
        about.classList.add("hidden");
    }

}


if (window.matchMedia("(max-media: 700px)").matches) {
    function mobileSidebar() {
        
        toggleSidebarVisible();

    }
}


// NIGHT MODE AND DAY MODE

function setDarkMode() {
    document.body.classList.add("darkmode");
	const button = document.getElementById("darkmode-button");
    button.src = "/assets/sun.svg"
    button.classList.add("noprefer");
}

function setLightMode() {
    document.body.classList.remove("darkmode");
	const button = document.getElementById("darkmode-button");
    button.src = "/assets/moon.svg";
    button.classList.add("noprefer");
}

function toggleDarkMode() {
    if (document.body.classList.contains("darkmode")) 
        setLightMode();
    else 
        setDarkMode();
}

// Initial dark mode preference
window.onload = () => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setDarkMode();
    }
}

// Detect changes in dark mode preferences
window.matchMedia('(prefers-color-scheme: dark)').addListener(function (e) {
    if (e.matches) 
        setDarkMode();
    else 
        setLightMode();
});

