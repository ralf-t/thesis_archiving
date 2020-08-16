$( document ).ready(function() {

	$('#image_file').change(function(e) {
	  var file = e.target.files; 

	  $(this).next('.custom-file-label').html(file[0]['name']);

	});

});