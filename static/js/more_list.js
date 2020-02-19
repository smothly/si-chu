document.addEventListener('DOMContentLoaded', () => {
    more_buttons = document.querySelectorAll(".more-btn");
    more_buttons.forEach(button => {
        button.addEventListener('click', open_more_list);
    });
});

function open_more_list(event) {
    let target = document.getElementById(event.target.name);
    target.style.display = "";
    event.target.innerText = "접기";
    event.target.addEventListener('click', close_more_list);
    event.target.removeEventListener('click', open_more_list);
}

function close_more_list(event) {
    let target = document.getElementById(event.target.name);
    target.style.display = "none";
    event.target.innerText = "더보기";
    event.target.addEventListener('click', open_more_list);
    event.target.removeEventListener('click', close_more_list);
}
