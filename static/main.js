isEditing = false;

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

function onDeleteClick(e)
{

}