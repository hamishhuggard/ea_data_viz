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


// NIGHT MODE AND DAY MODE

function setNightMode() {
    document.body.classList.add("nightmode");
	const button = document.getElementById("nightmode-button");
    button.src = "/assets/sun.svg"
    button.title = "Day mode"
}

function setDayMode() {
    document.body.classList.remove("nightmode");
	const button = document.getElementById("nightmode-button");
    button.src = "/assets/moon.svg"
    button.title = "Night mode"
}

function toggleNightMode() {
    if (document.body.classList.contains("nightmode")) 
        setDayMode();
    else 
        setNightMode();
}

if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    setDayMode();
}

// To watch for changes:
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (e.matches) 
        setNightMode();
    else 
        setDayMode();
});

