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
