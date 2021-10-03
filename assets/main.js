function toggleSidebarVisible() {
	const sidebar = document.getElementById("sidebar");
    let display;
    if (sidebar.classList.contains("hidden")) {
        sidebar.style.display = "initial";
        sidebar.classList.add("hidden");
        sidebar.classList.remove("hidden");
        display = "initial";
    } else {
        sidebar.classList.add("hidden");
        setTimeout(function()
            {
                sidebar.style.display = "none";

        }, 600);
    }
}
