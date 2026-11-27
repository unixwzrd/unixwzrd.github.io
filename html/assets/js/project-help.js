// Enhance the already usable project links; never collect or submit inquiry data.
document.addEventListener("DOMContentLoaded", function () {
    var picker = document.querySelector("[data-project-help-picker]");
    if (!picker) return;
    var filter = picker.querySelector("[data-project-help-filter]");
    var select = picker.querySelector("#project-help-select");
    var projects = Array.from(picker.querySelectorAll("[data-project-name]"));
    if (!filter || !select || !projects.length) return;

    function showSelectedProject() {
        projects.forEach(function (project) {
            project.hidden = Boolean(select.value && project.dataset.projectName !== select.value);
        });
    }

    select.addEventListener("change", showSelectedProject);
    showSelectedProject();
    filter.hidden = false;
});

