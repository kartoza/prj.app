/**
 * Created by Sumandari <sumandari@kartoza.com> on 24/05/21.
 */

tinymce.init({
  selector: "textarea",  // change this value according to your HTML
  selector: "textarea",
  plugins: [
    "code advlist autolink lists link image charmap print preview anchor",
    "searchreplace visualblocks code fullscreen",
    "insertdatetime media table paste"
  ],
  toolbar: "code insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
});