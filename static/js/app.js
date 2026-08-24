document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const loader = document.querySelector(".loader");
    const inputInfo = document.querySelector(".inputInfo");
    const loadInfo = document.getElementById("loadInfo");
    const inputTopic = document.getElementsByName('inputTopic')[0];

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        inputInfo.addEventListener("transitionend", () => {
            inputInfo.style.display = "none";

            loader.classList.remove("loader-hidden");
            loadInfo.textContent = `Getting resources on: ${inputTopic.value}`;
            loadInfo.style.visibility = "visible";

            form.submit();

        }, { once: true });

        inputInfo.classList.add("input-info-hidden");
    });
});