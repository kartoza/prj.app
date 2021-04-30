function showInvalidLink(projectSlug){
    $("li.invalid-link").remove();
    $("#btnDownloadPDF").remove();
    $("#loadingGif").css("display", "block");
    let url = `/${projectSlug}/lessons/invalid_further_reading/`
    let context;
    $.ajax({
      url: url,
      success: function(data){
        $("#loadingGif").css("display", "none");
        data.data ? data.data.forEach(el => $("#invalidLinkList").append(`<li class="invalid-link"><a href="${el.worksheet_url}">${el.worksheet}</a> has invalid link or unavailable link: ${el.invalid_url}</li>`)) : $("#invalidLinkList").append(`<li class="invalid-link">No invalid link.</li>`);

        let cleanedData = []
        data.data.forEach(el => {
          cleanedData.push({
            'worksheet_url':  el.worksheet_url.replace(/\&nbsp;/g, ''),
            'worksheet': el.worksheet,
            'invalid_url': el.invalid_url
          })
        })
        context = {
          'data': cleanedData,
          'loc': window.location.origin,
          'project_name': data.project_name
        };

        pdfUrl = `/${projectSlug}/lessons/print_invalid_further_reading/?data=${JSON.stringify(context)}`;
        $("#downloadPDF").append(`<button type="button" class="btn btn-primary btn-sm" id="btnDownloadPDF" data-dismiss="modal"><span class="fa fa-download"></span></button>`);
        $("#btnDownloadPDF").on("click", () => window.open(pdfUrl, "_blank"));
      },
      error: function(){
        $("#loadingGif").css("display", "none");
        $("#invalidLinkList").append(`<li class="invalid-link">Cannot check the invalid urls.</li>`);
      }
    });
}

