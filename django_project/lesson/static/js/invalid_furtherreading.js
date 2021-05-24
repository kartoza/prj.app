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

function checkAbsoluteRelativePath(urlString){
  return (urlString.indexOf('http://') === 0 || urlString.indexOf('https://') === 0) ? urlString : window.location.origin + urlString;
}

// https://stackoverflow.com/a/5717133/10268058
function validURL(str) {
  var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!pattern.test(str);
}