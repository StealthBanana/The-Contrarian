document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const loader = document.querySelector(".loader");
    const inputInfo = document.getElementById("InputInfo");
    const loadInfo = document.getElementById("loadInfo");
    const inputTopic = document.getElementsByName('inputTopic')[0]

    form.addEventListener("submit", () => {
        inputInfo.classList.add("input-info-hidden");
        inputInfo.addEventListener("transitionend", () => {
            inputInfo.remove()
        }, { once: true });
        loader.classList.remove("loader-hidden");
        loadInfo.textContent = `Getting resources on: ${inputTopic.value}`;
        loadInfo.style.visibility = "visible";
    });
});

