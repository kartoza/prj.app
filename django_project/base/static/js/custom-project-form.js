$(document).ready(function () {
    $('#id_project_representative').css('cssText', 'display: none !important;');
    $('#preview-certificate').appendTo($('#div_id_template_certifying_organisation_certificate'));
    $('#error-submit').appendTo($('#div_id_template_certifying_organisation_certificate'));
    $('#preview-template-load').appendTo($('#div_id_template_certifying_organisation_certificate'));
    readExistingFile('project_representative_signature-clear_id', 'project_representative_signature', false);
    readExistingFile('image_file-clear_id', 'project_logo', false);
    readExistingFile('template_certifying_organisation_certificate-clear_id', 'template_certificate', true);

    //check if browser supports file api and filereader features
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        function humanFileSize(bytes, si) {
            var thresh = si ? 1000 : 1024;
            if(bytes < thresh) return bytes + ' B';
            var units = si ? ['kB','MB','GB','TB','PB','EB','ZB','YB'] : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
            var u = -1;
            do {
                bytes /= thresh;
                ++u;
            } while(bytes >= thresh);
            return bytes.toFixed(1)+' '+units[u];
        }

        //this function is called when the input loads an image
        function renderImage(file){
            var reader = new FileReader();
            reader.onload = function(event){
                var the_url = event.target.result;
                $('#preview-photo').html("<img src='"+the_url+"' / height='150px'>");
                $('#preview-form input[name=template_certificate]').val(the_url);
                $('#name').html(file.name);
                $('#size').html(humanFileSize(file.size, "MB"));
                $('#type').html(file.type)
            };

            //when the file is read it triggers the onload event above.
            reader.readAsDataURL(file);
        }

        function renderUrl(file, form_id) {
            var reader = new FileReader();
            reader.onload = function(event){
                var url = event.target.result;
                $(form_id).val(url);
            };
            reader.readAsDataURL(file);
        }


        //watch for change on the image placeholders
        $( "#id_template_certifying_organisation_certificate" ).change(function() {
            renderImage(this.files[0])
        });

        $( "#id_project_representative_signature" ).change(function() {
            renderUrl(this.files[0], '#preview-form input[name=project_representative_signature]')
        });

        $( "#id_image_file" ).change(function() {
            renderUrl(this.files[0], '#preview-form input[name=project_logo]')
        });
    }
});

function previewCertificate() {
    $('#error-submit').html('');

    if($('input[name=name]').val() === ''){
        $('#error-submit').html('Please input project name.');
        return false
    }else if($('select[name=project_representative]').val() === ''){
        $('#error-submit').html('Please choose a project representative.');
        return false
    }

    $('#preview-form input[name=project_name]').val($('input[name=name]').val());
    $('#preview-form input[name=project_representative]').val($('select[name=project_representative]').val());
}

function getDataUri(url, callback) {
    var image = new Image();

    image.onload = function () {
        var canvas = document.createElement('canvas');
        canvas.width = this.naturalWidth; // or 'width' if you want a special/scaled size
        canvas.height = this.naturalHeight; // or 'height' if you want a special/scaled size

        canvas.getContext('2d').drawImage(this, 0, 0);

        // Get raw image data
        callback(canvas.toDataURL('image/png').replace(/^data:image\/(png|jpg);base64,/, ''));

        // ... or get as Data URI
        callback(canvas.toDataURL('image/png'));
    };

    image.src = url;
}

function readExistingFile(placeholder, form_id, preview) {
    if($('#' + placeholder).length){
        var file_url = $('#' + placeholder).prev().attr('href');
        file_url = file_url.replace('/media/', '');
        var file = media_url + file_url;
        if(preview) {
            $('#preview-photo').html("<img src='" + file + "' / height='150px'>");
        }

        getDataUri(file, function(dataUri) {
            $('#preview-form input[name=' + form_id + ']').val(dataUri);
        });
    }
}
