document.addEventListener('DOMContentLoaded', function() {

    // load_posts()
    document.querySelector('#submit_post').addEventListener('click', submit_post);



    document.querySelectorAll('button.edit').forEach(function(button) {
        button.onclick = function() {
            console.log(button.dataset.post)
            fetch('/posts/'+button.dataset.post)
                .then(response => response.json())
                .then(post => {
                    console.log(post);
                    var text_area = '<textarea class="form-control" id="compose_'+button.dataset.post+ '">'+ post.text+'</textarea>'
                    document.querySelector("#post_text"+button.dataset.post).innerHTML = text_area;
                    document.querySelector("#"+button.id).style.display = 'none';
                    document.querySelector("#save_button_"+button.dataset.post).style.display = 'block';
                });
        }
    });


    document.querySelectorAll('button.save').forEach(function(button) {
        button.style.display = 'none';

        button.onclick = function() {
            fetch('/posts/'+button.dataset.post)
                .then(response => response.json())
                .then(post => {
                    save_post(button.dataset.post)
                    var text_area =  post.text
                    document.querySelector("#post_text"+button.dataset.post).innerHTML = text_area;
                    document.querySelector("#edit_button_"+button.dataset.post).style.display = 'block';
                    document.querySelector("#save_button_"+button.dataset.post).style.display = 'none';
                });
        }
    });


    document.querySelectorAll('button.like').forEach(function(button) {
        button.onclick = function() {
            fetch('/posts/'+button.dataset.post)
                .then(response => response.json())
                .then(post => {
                    like_post(button.dataset.post)
                });
        }
    });


    document.querySelectorAll('button.unlike').forEach(function(button) {
        button.style.display = 'none';
        button.onclick = function() {
            fetch('/posts/'+button.dataset.post)
                .then(response => response.json())
                .then(post => {
                    un_like_post(button.dataset.post)
                });
        }
    });



} )



function like_post(post_id) {
    var count = parseInt(document.querySelector('#count_like_'+post_id).innerHTML, 10);
    fetch('/posts/'+post_id, {
        credentials: 'include',
        method: 'PUT',
        body: JSON.stringify({
            likes: "True"
        })
    })
        .then(response => response)
        .then(result => {
            document.querySelector('#count_like_'+post_id).innerHTML = count+1;
            document.querySelector("#unlike_"+post_id).style.display = 'block';
            document.querySelector("#like_"+post_id).style.display = 'none';
        });
};

function un_like_post(post_id) {

    var count = parseInt(document.querySelector('#count_like_'+post_id).innerHTML, 10);
    fetch('/posts/'+post_id, {
        credentials: 'include',
        method: 'PUT',
        body: JSON.stringify({
            unlikes: "True"
        })
    })
        .then(response => response)
        .then(result => {
            document.querySelector('#count_like_'+post_id).innerHTML = count-1;

            document.querySelector("#unlike_"+post_id).style.display = 'none';
            document.querySelector("#like_"+post_id).style.display = 'block';
        });


};

function load_posts() {
//document.querySelector('#posts-view').innerHTML = `<h3>Posts</h3>`;

  //Show the post list

  fetch('/posts/')
        .then(response => response.json())
        .then(posts => {
            // Print posts
            console.log(posts);
            posts.forEach(add_posts);
        });
};

function add_posts(contents) {
    var post = document.createElement('div');
    post.innerHTML ="<strong>"+ contents.user_name+ ": </strong>";
    document.querySelector('#post_list').append(post);
     }

function submit_post() {

        fetch('/post_submit', {
           credentials: 'include',
          method: 'POST',
          body: JSON.stringify({
              text: document.querySelector('#compose-post').value
          })
        })
        .then(response => response.json())
            .then(result => {
                console.log(result);
                location.reload()
            });

}


function save_post(post_id) {
    new_text = document.querySelector('#compose_'+post_id).value;

    fetch('/posts/'+post_id, {
        credentials: 'include',
        method: 'PUT',
        body: JSON.stringify({
            text: new_text
        })
    })
        .then(response => response)
        .then(result => {
            document.querySelector('#post_text'+post_id).innerHTML = new_text;
        });


};







