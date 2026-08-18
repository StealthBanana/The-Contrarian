document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const loader = document.querySelector(".loader");
    const inputInfo = document.getElementById("InputInfo");
    const loadInfo = document.getElementById("loadInfo");
    const inputTopic = document.getElementsByName('inputTopic')[0]

    form.addEventListener("submit", () => {
        loader.classList.remove("loader-hidden");
        inputInfo.classList.add("input-info-hidden");
        loadInfo.textContent = `Getting resources on the topic ${inputTopic.value}.`;
        loadInfo.style.visibility = "visible";
    });
});


