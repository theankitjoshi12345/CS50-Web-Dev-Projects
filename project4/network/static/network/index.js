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
    
    // Global Click Event Delegation
    document.addEventListener('click', (event) => {
        const target = event.target; // FIXED: Added const keyword

        // --- DELETE POST ACTION ---
        if (target.matches('.post-delete-button')){ // FIXED: Changed from ID (#) to Class (.)
            const post_id = target.dataset.id;
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/delete/${post_id}`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": csrf
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                const post = target.closest('.individual-post');
                post.classList.add('hide-deleted-post');
                post.addEventListener('animationend', () => {
                    post.remove();
                });
            })
            .catch(error => console.log('Error deleting post:', error));
        }
        
        // --- EDIT POST ACTION ---
        else if (target.matches('.post-edit-button')){
            if (document.querySelector('#editpost-container')){
                document.querySelector('#editpost-container').remove();                
            }

            const content = target.dataset.content;
            const id = target.dataset.id;

            const editpost = document.createElement('div');
            editpost.className = "newpost-container";
            editpost.id = "editpost-container";
            editpost.innerHTML = `
                <textarea id="editpost-content" required autofocus>${content}</textarea>
                <button id="editpost-save-button" class=" btn btn-success btn-sm" data-id="${id}">Save</button>
                <button id="editpost-cancel-button" class=" btn btn-light btn-sm">Cancel</button>            
            `
            target.parentElement.prepend(editpost);

            const textarea = document.querySelector('#editpost-content');
            textarea.focus();

            const length = textarea.value.length;
            textarea.setSelectionRange(0, length);
        }
        
        // --- FOLLOW / UNFOLLOW ACTION ---
        else if (target.matches('#followButton')){ // FIXED: Removed redundant inner if condition
            const username = target.dataset.username;
            let url; 
            
            const followers = document.querySelector('#followers');
            let currentcount = +followers.textContent.trim(); // Using textContent instead of innerHTML
            
            if (target.textContent.trim() === "Follow") {
                url = "follow";
                target.textContent = "Unfollow";
                currentcount++;
            } else {
                url = "unfollow";
                target.textContent = "Follow";
                currentcount--;
            }
            
            followers.textContent = currentcount;            
            
            fetch(`/${url}/${username}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
            })
            .catch(error => console.error("Error updating relationship:", error));
        }
        else if(target.matches("#editpost-save-button")){
            const content = document.querySelector('#editpost-content').value;
            const id = target.dataset.id;
             
            fetch(`/edit/${id}`, {
                method:"PUT",
                headers: {
                    "X-CSRFToken":getCookie('csrftoken'),
                    "Content-Type":"application/json",
                },
                body:JSON.stringify({
                    content:content,
                })
            })
            .then(response=>response.json())
            .then(data=>{
                console.log(data.message);
                target.parentElement.parentElement.querySelector('.post-content').innerHTML = content;

                target.parentElement.remove();
            })

        }
        else if(target.matches("#editpost-cancel-button")){
            target.parentElement.remove();
        }
        else if(target.matches('.likebutton')){
            const id = target.dataset.id;
            fetch(`/likes/${id}`, {
                method:"PUT",
                headers:{
                    "Content-Type":"application/json",
                    "X-CSRFToken":getCookie('csrftoken')
                }
            })
            .then(response=>response.json())
            .then(data => {
                if(data.likes !== undefined){
                    target.parentElement.querySelector('.likescount').textContent = data.likes;                
                }
                console.log(data.message)
            })
            .catch(error => console.error("Error with like/unlike button:", error));
        }

    });

    // --- NEW POST FORM SUBMISSION ---
    document.querySelector('#newpost').onsubmit = (event) => {
        event.preventDefault(); 

        const content = document.querySelector('#newpost-content').value;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/newpost', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken 
            },
            body: JSON.stringify({
                content: content
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.querySelector('#newpost-content').value = '';
            
            const newpost = document.createElement('div');
            newpost.className = "individual-post";
            
            const post = data.post;
            
            newpost.innerHTML = `
                <small style="color:blueviolet;">${post.timestamp}</small><br>
                <strong><a href="/profile/${post.username}">${post.username}</a></strong>: <span class="post-content">${post.content}</span> <br>
                <small style="color:red;"><span class="likescount">${post.likes} </span><button data-id="${post.id}" class="likebutton">❤️</button></small>
                &emsp;
                <small style="color:blue;">${post.comments} 📨</small>
                &emsp;
                <button class="btn btn-primary post-edit-button" data-content="${post.content}" data-id="${post.id}">Edit</button> 
                &emsp;
                <button class="btn btn-primary post-delete-button" data-id="${post.id}">Delete</button>    
            `;

            document.querySelector('#posts-container').prepend(newpost);
        });
    }
});