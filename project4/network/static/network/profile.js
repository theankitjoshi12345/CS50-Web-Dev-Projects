function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', (event) => {
        const target = event.target;
        
        // Grab username from the dataset attribute
        const username = target.dataset.username;
        
        if (target.id === "followButton") {
            let url; // FIXED: Changed const to let so it can be reassigned
            const followers = document.querySelector('#followers');
            let currentcount = +followers.innerHTML.trim();
            
            if (target.innerHTML.trim() === "Follow") {
                url = "follow";
                target.innerHTML = "Unfollow";
                currentcount++;

            } else {
                url = "unfollow";
                target.innerHTML = "Follow";
                currentcount--;
            }
            followers.innerHTML = currentcount;            
            fetch(`/${url}/${username}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie('csrftoken'),
                }
            })
            .then(response => response.json()) // FIXED: Added parentheses ()
            .then(data => {
                console.log(data.message);
            })
            .catch(error => console.error("Error updating relationship:", error)); // FIXED: Added error handling argument
        }
    });
});