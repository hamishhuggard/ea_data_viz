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

function toggleNightMode() {

	const body = document.body;
	const button = document.getElementById("nightmode-button");

    if (body.classList.contains("nightmode")) {
        body.classList.remove("nightmode");
        button.src = "/assets/moon.svg"
        button.title = "Night mode"
    } else {
        body.classList.add("nightmode");
        button.src = "/assets/sun.svg"
        button.title = "Day mode"
    }

}

function toggleAboutVisibility() {

	const about = document.getElementById("about");

    if (about.classList.contains("hidden")) {
        about.classList.remove("hidden");
    } else {
        about.classList.add("hidden");
    }

}
