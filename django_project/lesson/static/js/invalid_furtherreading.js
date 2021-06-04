function showInvalidLink(projectSlug){
    $("li.invalid-link").remove();
    $("#btnDownloadPDF").remove();
    $("#loadingGif").css("display", "block");
    let url = `/${projectSlug}/lessons/_further_reading_links/`
    let context;
    let cleanedData = []
    $.ajax({
      url: url,
      success: function(data){
        var promises = []
        data.data.forEach(el => {
          let url_checked = checkAbsoluteRelativePath(el.further_reading_url)

          var request = $.ajax({
            url: is_url_exist_url + '?url_string=' + url_checked,
            success: function (data) {
              if (!data.is_url_exist) {
                $("#invalidLinkList").append(`<li class="invalid-link"><a href="${el.worksheet_url}">${el.worksheet}</a> has invalid link or unavailable link: ${el.further_reading_url}</li>`);
                cleanedData.push({
                  'worksheet_url':  el.worksheet_url.replace(/\&nbsp;/g, ''),
                  'worksheet': el.worksheet,
                  'invalid_url': el.further_reading_url
                });
              }
            }
          })
          promises.push(request);
        });

        // waiting all ajax request in loop finished
        $.when.apply(null, promises).done(function(){
          console.log('done');
          console.log(cleanedData);
          context = {
            'data': cleanedData,
            'loc': window.location.origin,
            'project_name': data.project_name
          };

          pdfUrl = `/${projectSlug}/lessons/print_invalid_further_reading/?data=${JSON.stringify(context)}`;
          $("#downloadPDF").append(`<button type="button" class="btn btn-primary btn-sm" id="btnDownloadPDF" data-dismiss="modal"><span class="fa fa-download"></span></button>`);
          $("#btnDownloadPDF").on("click", () => window.open(pdfUrl, "_blank"));
          $("#loadingGif").css("display", "none");
        })

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

console.log(is_url_exist_url + '?url_string=http://google.com')
$.ajax({
  url: is_url_exist_url + '?url_string=http://google.com',
  success: function (data) {
    console.log(data)
  }
})
