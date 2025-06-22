function toggleDropdown() {
    document.getElementById("accountDropdown").classList.toggle("show");
}

// Function to toggle visibility of submenus
function toggleSubmenu(event, submenuId) {
    event.preventDefault(); // Prevent default link behavior
    event.stopPropagation(); // Stop event bubbling to prevent main menu from closing
    var submenu = document.getElementById(submenuId);
    var parentToggle = event.currentTarget; // The element that was clicked (e.g., Tenant Account)

    // Close other open submenus within the same main menu
    var allSubmenus = document.querySelectorAll('#accountDropdown .submenu-content');
    allSubmenus.forEach(function(sub) {
        if (sub.id !== submenuId && sub.classList.contains('show')) {
            sub.classList.remove('show');
            // Also remove 'active' class from the corresponding toggle
            var correspondingToggle = document.querySelector(`[onclick*='${sub.id}']`);
            if (correspondingToggle) {
                correspondingToggle.classList.remove('active');
            }
        }
    });

    // Toggle visibility of the current submenu
    submenu.classList.toggle("show");
    parentToggle.classList.toggle("active"); // Add/remove class for arrow rotation
}

// Close the main dropdown menu (and all submenus) if the user clicks outside of it
window.onclick = function(event) {
    // Check if the click was outside the main trigger and outside the dropdown content
    if (!event.target.matches('#accountTrigger') && !event.target.closest('.dropdown-content')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
                // Also close all submenus inside
                var submenus = openDropdown.querySelectorAll('.submenu-content');
                submenus.forEach(function(sub) {
                    sub.classList.remove('show');
                });
                // And remove active class from all submenu toggles
                var toggles = openDropdown.querySelectorAll('.dropdown-category-toggle');
                toggles.forEach(function(toggle) {
                    toggle.classList.remove('active');
                });
            }
        }
    }
}