document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const loader = document.querySelector(".loader");
    const inputInfo = document.getElementById("InputInfo");
    const loadInfo = document.getElementById("loadInfo");
    const inputTopic = document.getElementsByName('inputTopic')[0]
    
    inputInfo.addEventListener('transitionend', () => {
        loadInfo.textContent = `Getting resources on: ${inputTopic.value}`;
        loadInfo.style.visibility = "visible";
    })
    
    form.addEventListener("mouseover", () => {
        inputInfo.classList.add("input-info-hidden");
        loader.classList.remove("loader-hidden");

    });
});

