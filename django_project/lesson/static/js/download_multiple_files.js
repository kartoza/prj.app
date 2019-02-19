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
}

function downloadCheckedFiles() {
    var $checkedElements = $('.worksheet-checkbox:checked');
    var worksheets = {};
    $.each($checkedElements, function (index, element) {
        var pk = $(element).attr('worksheet-pk');
        var numbering = $(element).attr('worksheet-number');
        worksheets[pk] = numbering
    });

    window.open(worksheets_download_url + '?worksheet=' + JSON.stringify(worksheets))

    $('input[type="checkbox"]').prop('checked', false).hide();
    $('#toggle-checklist-btn').removeClass('btn-success').addClass('btn-default');
    $('#download-multiple-submit').hide();
}
