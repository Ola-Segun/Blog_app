document.getElementById("id_title").addEventListener("keyup", createSlug);


function createSlug() {
    var title = document.getElementById("id_title").value;
    var slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
    document.getElementById("id_slug").value = slug;
}

