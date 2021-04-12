function toggleCheckList(that) {
    var $element = $(that);
    if($element.hasClass('btn-default')){
        $element.removeClass('btn-default').addClass('btn-success');
        $('input[type="checkbox"]').show();
        $('#download-multiple-submit').show();
    }else {
        $element.removeClass('btn-success').addClass('btn-default');
        $('input[type="checkbox"]').hide();
        $('#download-multiple-submit').hide();
    }
}

function toggleCheckAllWorksheet(that) {
    var $element = $(that);
    var elementId = $element.parent().attr('id');
    var $checkbox = $('.' + elementId + '-checkbox');
    if($element.is(":checked")){
        $checkbox.prop('checked', true)
    }else {
        $checkbox.prop('checked', false)
    }
    updatePaginationLink()
}

// ----------------------------------------------------------------------------
// pagination support
function getWorksheetListPage(){
    // get the list of checked worksheet for pagination support
    const urlParams = new URLSearchParams(window.location.search);
    var page = urlParams.get('page');
    if (page == null){
        page = "1"
    }
    var $checkedElements = $('.worksheet-checkbox:checked');
    var worksheets = {};
    $.each($checkedElements, function (index, element) {
        let pk = $(element).attr('worksheet-pk');
        let numbering = $(element).attr('worksheet-number');
        worksheets[pk] = numbering
    });
    var result = {}
    result[page] = worksheets
    return result
}

function addWorksheetList(newWorksheet){
    // merge worksheet dictionary for pagination support
    // newWorksheet is a dictionary
    const urlParams = new URLSearchParams(window.location.search);
    const worksheet_all = urlParams.get('worksheet_all');
    let worksheetQueryParam = JSON.parse(worksheet_all);
    return  {...worksheetQueryParam, ...newWorksheet}
}

function updatePaginationLink(){
    // add query parameter for pagination support
    const urlParams = new URLSearchParams(window.location.search);
    const worksheet_all = urlParams.get('worksheet_all');
    let worksheetListPage = getWorksheetListPage();
    let worksheetList = JSON.stringify(addWorksheetList(worksheetListPage));
    let paginationElement = $('.pagination>li>a');
    $.each(paginationElement, function (index, element) {
        let href = $(element).attr('href');
        if (worksheet_all !== '') {
            href = href.replace(/&worksheet_all=.*/, '')
        }
        let newHref = `${href}&worksheet_all=${worksheetList}`;
        element.href = newHref;
    })
}

function updateCheckedWorksheet(){
    const urlParams = new URLSearchParams(window.location.search);
    const worksheet_all = urlParams.get('worksheet_all');
    var page = urlParams.get('page');
    var parsedWorksheets = JSON.parse(worksheet_all);
    for (let key in parsedWorksheets){
        if (key == page) {
            let worksheet = parsedWorksheets[key];
            for (let pk in worksheet){
                let $checkbox = $('[worksheet-pk='+ pk +']');
                $checkbox.prop('checked', true);
            }
        }
    }
}

// add to onLoad
if(window.addEventListener) {
    window.addEventListener('load', updatePaginationLink,false); //W3C
    window.addEventListener('load', updateCheckedWorksheet,false); //W3C
} else {
    window.attachEvent('onload', updatePaginationLink); //IE
    window.attachEvent('onload', updateCheckedWorksheet); //IE
}

function parseWorksheetAllList(){
    const urlParams = new URLSearchParams(window.location.search);
    const worksheet_all = urlParams.get('worksheet_all');
    const page = urlParams.get('page');
    var parsedWorksheets = JSON.parse(worksheet_all);
    var worksheets = {}
    for (let key in parsedWorksheets){
        if (key != page){
            let worksheet = parsedWorksheets[key];
            for (let k in worksheet){
                worksheets[k] = worksheet[k]
            }
        }
    }
    return worksheets
}
//-----------------------------------------------------------------------------

function downloadCheckedFiles() {
    var $checkedElements = $('.worksheet-checkbox:checked');
    var worksheets = {};
    $.each($checkedElements, function (index, element) {
        var pk = $(element).attr('worksheet-pk');
        var numbering = $(element).attr('worksheet-number');
        worksheets[pk] = numbering
    });

    // get worksheet from another page
    var parsingWorksheet = parseWorksheetAllList();
    worksheets = {...worksheets, ...parsingWorksheet}

    window.open(worksheets_download_url + '?worksheet=' + JSON.stringify(worksheets))

    $('input[type="checkbox"]').prop('checked', false).hide();
    $('#toggle-checklist-btn').removeClass('btn-success').addClass('btn-default');
    $('#download-multiple-submit').hide();
}
