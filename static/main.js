document.getElementById("file_upload").value=null; 
var likesModal

isEditing = false;
likesShowing = false;

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
    if (window.location.pathname != "/post" && e.target==this)
    {
        window.location.href="post?id=" + id;
    }
}