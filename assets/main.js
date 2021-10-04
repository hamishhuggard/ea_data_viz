function toggleSidebarVisible() {

	const sidebar = document.getElementById("sidebar");
	const buttress = document.getElementById("sidebar-buttress");

    if (sidebar.classList.contains("hidden")) {
        sidebar.classList.remove("hidden");
        buttress.style.display = "block";
    } else {
        sidebar.classList.add("hidden");
        buttress.style.display = "none";
    }

}
