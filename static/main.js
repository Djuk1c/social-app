var likesModal = document.getElementById("likesModal");

isEditing = false;
likesShowing = false;

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

function onLikesClick(e)
{
    console.log(e);
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

window.onclick = function(event) 
{
    if (event.target == likesModal) {
        likesModal.style.display = "none";
    }
  }