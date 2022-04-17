const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};


/////////////////////////////////////////////////////////   SUGGESTIONS   ///////////////////////////////////////////////////////////////////

const toggleFollow = ev => {
    const elem = ev.currentTarget;
    
    if (elem.getAttribute('aria-checked') === 'false') {
        followUser(elem.dataset.userId, elem);
    } else {
        unfollowUser(elem.dataset.followingId, elem);
    }
};

const followUser = (userId, elem) => {
    const postData = {
        "user_id": userId
    };
    
    fetch("/api/following/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => { 
            console.log(data);
            elem.innerHTML = 'unfollow';
            elem.setAttribute('aria-checked', 'true');
            elem.classList.add('unfollow');
            elem.classList.remove('follow');
            elem.setAttribute('data-following-id', data.id);
        });
};

const unfollowUser = (followingId, elem) => {
    const deleteURL = `/api/following/${followingId}`;
    fetch(deleteURL, {
        method: "DELETE",
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        elem.innerHTML = 'follow'
        elem.setAttribute('aria-checked', 'false');
        elem.classList.add('follow');
        elem.classList.remove('unfollow');
        elem.removeAttribute('data-following-id');
    });
};

const user2Html = user => {
    return `<div class = "suggestion">
                <img src="${user.thumb_url}" />
                <div>
                    <p class = "username">${user.username}</p>
                    <p class = "suggestion-text">suggested for you</p>
                </div>
                <div>
                    <button 
                    class = "follow" 
                    aria-label="Follow"
                    aria-checked="false"
                    data-user-id = "${user.id}" 
                    onclick = "toggleFollow(event);"> follow </button>
                </div>
            </div>`;
};

// fetch data from your API endpoint:
const displaySuggestions = () => {
    fetch('/api/suggestions')
        .then(response => response.json())
        .then(users => {
            console.log(users);
            const html = users.map(user2Html).join('\n');
            document.querySelector('.suggestions').innerHTML = html;
        })
};

/////////////////////////////////////////////////////////   POSTS   ///////////////////////////////////////////////////////////////////
const destroyModal = ev => {
    document.querySelector('#modal-container').innerHTML = "";
};

const displayAllComments = (comments) => {
    let html_ ='';
    for(i=0; i< comments.length; i++){
        curr = comments[i];
        html_+= `
        <div>
            <strong>${curr.user.username}</strong>
            ${curr.text}
            <div>${curr.display_time}</div>
        </div>
        `
    }
    return html_;
};

const showPostDetail = ev => {
    const postId = ev.currentTarget.dataset.postId;
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post => {
            const html = `
                <div class="modal-bg">
                    <button onclick ="destroyModal(event)"> Close </button>
                    <div class ="modal">
                        <img src = "${post.image_url}" />
                    </div>
                    <div class = "modal">
                        <section id = "comments">
                            ${displayAllComments(post.comments)}
                        </section>
                    </div>
                </div>`;
            document.querySelector('#modal-container').innerHTML = html;
        })
};


const displayComments = (comments, postID) => {
    let html = '';
    if (comments.length > 1){
        html += `
            <button class="viewcomments" data-post-id = "${postID}" onclick="showPostDetail(event);"> 
                view all ${comments.length} comments 
            </button>
        `;
    }
    if (comments && comments.length>0) {
        const lastComment = comments[comments.length - 1];
        html += `
            <div> 
                <strong>${lastComment.user.username}</strong>
                ${lastComment.text}
                <div>${lastComment.display_time}</div>
            </div>
        `
    }
    html += `
    <section id= "addcomment">
        <section id="comment">
            <section id="emoji">
                <i class="far fa-smile"></i>
            </section>
            <section id="actualcomment">
                <input type="text" aria-label="Add a comment" placeholder = "Add a comment..." id="${postID}">
            </section>
        </section>
        <section id="post">
            <button data-post-id = "${postID}" data-all-comments="${comments}" onclick="sendComment(event)">Post</button>
        </section>
    </section>
    `
    return html;
};


function getInputValue(idofpost){
    // Selecting the input element and get its value 
    var inputVal = document.getElementById(idofpost).value;
    
    // Returning the value
    return (inputVal);
};

const sendComment = ev => {
    console.log('Post comment button clicked');
    const elem = ev.currentTarget;
    comment_topost = getInputValue(elem.dataset.postId);
    postComment(elem.dataset.postId, comment_topost);
    const to_fetch = `/api/posts/${elem.dataset.postId}`;
    const post = fetch(to_fetch);
    elem.dataset.allComments = comments;
    displayComments(post.comments, elem.dataset.postId);

};

const postComment = (postId, text) => {
    const postData = {
        "post_id": postId,
        "text": text
    };
    
    fetch("api/comments", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
};



const likeUnlike = ev => {
    console.log('like/unlike button clicked');
    const elem = ev.currentTarget;
    if (elem.getAttribute('aria-checked') === 'false') {
        likePost(elem.dataset.postId, elem);
    } else { 
        unlikePost(elem.dataset.postId, elem.dataset.likeId, elem);
    }
};
const likePost = (postId, elem) => {
    const postData = {
    };
    const followURL = `/api/posts/${postId}/likes/`;
    fetch(followURL, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
        body: JSON.stringify(postData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        elem.innerHTML = `<section id="like">
            <i class="fas fa-heart"></i>
            </section>
            `;
        elem.setAttribute('aria-checked', 'true');
        elem.classList.add('unlike');
        elem.classList.remove('like');
        elem.setAttribute('data-like-id', data.id);
    });
};

const unlikePost = (postId, likeId, elem) => {
    const unfollowURL = `/api/posts/${postId}/likes/${likeId}`;
    fetch(unfollowURL, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        elem.innerHTML = `<section id="like">
        <i class="far fa-heart"></i>
        </section>
        `;
        elem.setAttribute('aria-checked', 'false');
        elem.classList.add('like');
        elem.classList.remove('unlike');
        elem.removeAttribute('data-following-id');
    });
};

const post2Html = post => {
    return `
        <section id = "POST">
            <section id="userp">
                <section id="name">
                    <h3>${post.user.username }</h3>
                </section>
                <section id="dots">
                    <h2>...</h2>
                </section>
            </section>
            <section id="imgpost">
                <img src="${post.image_url}" alt="${post.title}">
            </section>

            <section id="actions">
                <section id="lcs">
                    <button aria-checked = "${post.current_user_like_id ? 'true' : 'false'}" data-post-id = "${post.id}"  data-like-id = "${post.current_user_like_id}"
                    aria-label="Like" class = "like"  onclick = "likeUnlike(event)">
                        <section id="like">
                            <i class="fa${post.current_user_like_id ? 's' : 'r'} fa-heart"></i>
                        </section>
                    </button>
                    <section id="commentt">
                        <i class="far fa-comment"></i>
                    </section>
                    <section id="share">
                        <i class="far fa-paper-plane"></i>
                    </section>
                </section>
                <section id= "save">
                    <button aria-checked = "${post.current_user_bookmark_id ? 'true' : 'false'}" data-post-id = "${post.id}" data-bookmark-id = "${post.current_user_bookmark_id}"
                    aria-label="Bookmark" class = "bookmark" onclick = "bookmarkUnbookmark(event)">
                    <i class="fa${post.current_user_bookmark_id ? 's' : 'r'} fa-bookmark"></i>
                </button>
                </section>
            </section>

            <section>
                <section id="likes">
                    <h4>${post.likes.length} like${post.likes.length != 1 ? 's' : ''}</h4>
                </section>

                <section id="comment1">
                    <section id="userr">
                    <p>
                        <strong>${post.user.username}</strong>
                        ${post.caption}
                    </p>
                    </section>
                </section>

            </section>
            <section id = "comments">
                ${ displayComments(post.comments, post.id) }
            </section>
        </section>
    `;
};

const bookmarkUnbookmark = ev => {
    console.log('Bookmark button clicked');
    const elem = ev.currentTarget;
    if (elem.getAttribute('aria-checked') === 'false') {
        bookmarkPost(elem.dataset.postId, elem);
    } else { 
        unbookmarkPost(elem.dataset.bookmarkId, elem);
    }
};

const bookmarkPost = (postId, elem) => {
    const postData = {
        "post_id": postId
    };
    
    fetch("/api/bookmarks/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            elem.innerHTML = `<section id="save">
            <i class="fas fa-bookmark"></i>
            </section>
            `;
            elem.setAttribute('aria-checked', 'true');
            elem.classList.add('unbookmark');
            elem.classList.remove('bookmark');
            elem.setAttribute('data-bookmark-id', data.id);
        });
};

const unbookmarkPost = (bookmarkId, elem) => {
    const unbookmarkurl = `/api/bookmarks/${bookmarkId}`;
    fetch(unbookmarkurl, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        elem.innerHTML = `<section id="save">
            <i class="far fa-bookmark"></i>
            </section>
            `;
        elem.setAttribute('aria-checked', 'false');
        elem.classList.add('bookmark');
        elem.classList.remove('unbookmark');
        elem.removeAttribute('data-bookmark-id');
    });
};

const getCookie = key => {
    let name = key + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
};


// fetch data from your API endpoint:
const displayPosts = () => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};


const initPage = () => {
    displayStories();
    displaySuggestions();
    displayPosts();
};


// invoke init page to display stories:
initPage();