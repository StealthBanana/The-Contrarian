document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const loader = document.querySelector(".loader");
    const inputInfo = document.getElementById("InputInfo");

    form.addEventListener("submit", () => {
        // Fade the loader in and the input section out at the same time.
        // No need to reverse this afterward -- submitting the form navigates
        // the browser to /results/<topic>, which unloads this page entirely.
        loader.classList.remove("loader-hidden");
        inputInfo.classList.add("input-info-hidden");
    });
});