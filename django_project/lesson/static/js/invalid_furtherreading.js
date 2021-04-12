function showInvalidLink(projectSlug){
    $("li.invalid-link").remove();
    $("#loadingGif").css("display", "block");
    let url = `/${projectSlug}/lessons/invalid_further_reading`
    $.getJSON(url, function(data){
        $("#loadingGif").css("display", "none");
        data.data ? data.data.map(item => $("#invalidLinkList").append(`<li class="invalid-link">${item}</li>`)) : $("#invalidLinkList").append(`<li>No invalid link.</li>`);
    })
}