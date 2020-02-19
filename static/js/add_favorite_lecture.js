document.addEventListener('DOMContentLoaded', () => {
    favorite_buttons = document.querySelectorAll(".favorite-button");
    favorite_buttons.forEach(button => {
        button.addEventListener('click', favorite);
    });
});

function favorite(event) {
    event.preventDefault();
    let url = favorite_url;
    let id = event.target.name;
    let formData = new URLSearchParams();
    formData.set("id", id);
    fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie("csrftoken"),
            "X-Requested-With": "XMLHttpRequest"
        },
        body: formData
    }).then((res) => {
        res.json()
            .then((json) => {
                    render(json["target"], json["data"], json["msg"]);
                }
            )
    }).catch(err => console.error(err));
}

// 데이터를 가져와서 target을 렌더링한 HTML 데이터로 치환
function render(target, data, messages) {
    console.log("reload")
    target_dom = document.querySelector(target);
    target_dom.innerHTML = data;
    target_button = document.querySelector(target);
    target_button.addEventListener('click', favorite);

    message_dom = document.querySelector(`#messages`);
    message_dom.innerHTML = messages;
    reconnect_notification_delete_onclick();
}

// Cookie를 가져와 POST요청에 필요한 csrf token을 가져올 때 사용한다.
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function reconnect_notification_delete_onclick() {
    console.log("reload");
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        $notification = $delete.parentNode;
        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
}