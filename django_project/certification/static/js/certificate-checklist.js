$('a.archive').click(archiveChecklist);
$('a.activate').click(activateChecklist);

function archiveChecklist() {
  var checklist = $.map($(this).closest('li'), function(el, i){
    var item = String(el.id).split('-');
    return {
      'is_archived': true,
      'id': item[0],
      'question': item[1]
    }
  });

  var data_url = $("#sortable").data("url");

  if (data_url) {
    $.ajax({
      url: data_url,
      type: "POST",
      data: JSON.stringify(checklist),
      success: function (response) {
        console.log(response);
        if($('#archive-saved').is(":visible"))
        {
          $('#archive-saved').hide();
          showArchiveSaved();
        } else {
          showArchiveSaved();
        }
      },
      error: function (response) {
        console.log(response);
        sortableEnable();
        if($('#archive-not-saved').is(":visible"))
        {
          $('#archive-not-saved').hide();
          showArchiveNotSaved();
        } else {
          showArchiveNotSaved();
        }
      }
    })
  }
}

function activateChecklist() {
  var checklist = $.map($(this).closest('li'), function(el, i){
    var item = String(el.id).split('-');
    return {
      'is_archived': false,
      'id': item[0],
      'question': item[1]
    }
  });

  var data_url = $("#sortable").data("url");

  if (data_url) {
    $.ajax({
      url: data_url,
      type: "POST",
      data: JSON.stringify(checklist),
      success: function (response) {
        console.log(response);
        if($('#archive-saved').is(":visible"))
        {
          $('#archive-saved').hide();
          showArchiveSaved();
        } else {
          showArchiveSaved();
        }
      },
      error: function (response) {
        console.log(response);
        sortableEnable();
        if($('#archive-not-saved').is(":visible"))
        {
          $('#archive-not-saved').hide();
          showArchiveNotSaved();
        } else {
          showArchiveNotSaved();
        }
      }
    })
  }
}

function showArchiveSaved() {
    $('#archive-saved').fadeIn( "fast", function() {
        $('#archive-saved').fadeOut(2000);
    });
}

function showArchiveNotSaved() {
    $('#archive-not-saved').fadeIn( "fast", function() {
        $('#archive-not-saved').fadeOut(2000);
    });
}
