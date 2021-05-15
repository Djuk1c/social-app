var upload = document.getElementById("file_upload");
if (upload)
    upload.value=null;

var likesModal
isEditing = false;
likesShowing = false;

let drag = false;
document.addEventListener('mousedown', () => drag = false);
document.addEventListener('mousemove', () => drag = true);
document.addEventListener('mouseup', () => console.log(drag ? 'drag' : 'click'));

window.onclick = function(event) 
{
    if (event.target == likesModal && likesShowing) {
        likesModal.style.display = "none";
        likesShowing = !likesShowing;
    }
}

function onEditClick(e)
{
    // XDDDDDDDDD
    postDiv = e.target.parentNode.parentNode.parentNode;
    for (i = 0; i < postDiv.childNodes.length; i++)
    {
        if (!isEditing)
        {
            if (postDiv.childNodes[i].id == "edit-post-div")
            {
                postDiv.childNodes[i].style.display = "block";
            }
            if (postDiv.childNodes[i].id == "post-text")
            {
                postDiv.childNodes[i].style.display = "none";
            }
        }
        else
        {
            if (postDiv.childNodes[i].id == "edit-post-div")
            {
                postDiv.childNodes[i].style.display = "none";
            }
            if (postDiv.childNodes[i].id == "post-text")
            {
                postDiv.childNodes[i].style.display = "block";
            }
        }
    }
    isEditing = !isEditing;
}

function onLikesClick(e, id)
{
    likesModal = document.getElementById("likesModal" + id);
    if (!likesShowing)
    {
        likesModal.style.display = "block";
    }
    else
    {
        likesModal.style.display = "none";
    }
    likesShowing = !likesShowing;
}

function onPostClick(e, id)
{
    var elm = e.target;
    var filter = ['avatar', 'poster-name', 'postComments', 'postLikes', 'likePost', 'postEditIcons']
    
    if (filter.includes(elm.id) || elm.id.includes('likesModal') || drag)
    {
        return;
    }

    if (window.location.pathname != "/post")
    {
        window.location.href="post?id=" + id;
    }
}

function openCommentBox()
{
    commentBox = document.getElementById('comment-post-div')
    if (commentBox)
    {
        commentBox.style.display = 'block';
    }
}