$( document ).ready(function() {

	// instantiate token plugin
	// wag gawing global variable dahil di lang iisa ang magiging tokenfield
	
	$('.summernote').summernote({
	  toolbar: [
	    // [groupName, [list of button]]
	    ['style', ['style','bold', 'italic', 'underline', 'clear']],
	    ['font', ['strikethrough', 'superscript', 'subscript']],
	    ['fontsize', ['fontsize']],
	    ['para', ['ul', 'ol', 'paragraph']],
	    ['height', ['height']]
	  ]
	});

	$('#form_file').change(function(e) {
	  var file = e.target.files; 

	  $(this).next('.custom-file-label').html(file[0]['name']);

	});


	$("[name$='keywords']").tokenfield({
		limit:10,
		beautify:false
	});

	// setting name for infield token input for dom purposes
	$("[id^='keywords'].token-input").attr('name','keywords')

	$("[name$='area'], [name$='keywords']").keyup( function(){
		const input = $(this)
		const val = input.val();
		var name = input.attr('name');
		var tags_div;					

		// endsWith dahil may prefix sya for every entry iteration
		if(name.endsWith('area')){
			name = 'area'	// reassign dahil if not, the name is 'prefix-area'
			tags_div = $('#'+input.attr('id')+'tags');			
		}

		if(name.endsWith('keywords')){
			name = 'keywords'
			tags_div = $('#'+input.attr('id').split('-')[0]+'tags');	// para makuha yung id niya w/o 'tokenfield' 			
		}
		
		// ajax
		req = $.ajax({
			url:'/admin/register/thesis/fuzz_tags',
			type: 'POST',
			data: {val:val, name:name}
		});

		req.done(function(tags){
			tags_div.html(tags).slideDown();

			// append clicked tag
			// hide div
			
			// unbind to make sure walang unneeded listeners
			tags_div.find("button[name='areatag']").click(function(){
				input.val( $(this).val() );

				tags_div.slideUp();

				$(this).unbind('click');
				
			});

			tags_div.find("button[name='keywordstag']").click(function(){
				
				// dom climbing para maget yung element kung san nainstantiate yung tokenfield()
				tokenfield_parent = input.parent().find('[id^=keywords');

				// set the infield val to empty
				input.val('');

				tokenfield_parent.tokenfield('createToken', $(this).val());

				tags_div.slideUp();

				$(this).unbind('click');
				
			});

		});
	});

	$("[name$='area'], [name$='keywords']").blur( function(){
		const input = $(this)
		var name = input.attr('name');
		var tags_div;					

		if(name.endsWith('area')){
			name = 'area'	// reassign dahil if not, the name is 'prefix-area'
			tags_div = $('#'+input.attr('id')+'tags');			
		}

		if(name.endsWith('keywords')){
			name = 'keywords'
			tags_div = $('#'+input.attr('id').split('-')[0]+'tags');	// para makuha yung id niya w/o 'tokenfield' 			
		}
		
		tags_div.slideUp();
	});

	$("[name^='accept']").hide();
	$("[name^='edit']").hide();

	$("[name^='search']").click(function(){

		fieldset = $(this).closest("fieldset");

		query_div = $("#query")

		entry_index = $(this).attr('id').split('-')[1];

		title_id = '#' + 'title' + entry_index
		title_val = $(title_id).val().trim() ? $(title_id).val().trim() : null;

		area_id = '#' + 'area' + entry_index
		area_val = $(area_id).val().trim() ? $(area_id).val().trim() : null;

		keywords_id = '#' + 'keywords' + entry_index
		keywords_val = $(keywords_id).tokenfield('getTokensList').trim()
		keywords_arr = keywords_val.trim() ? keywords_val.split(',') : null;

		req = $.ajax({
			url:'/admin/register/thesis/advanced_search',
			type: 'POST',
			data: JSON.stringify({title:title_val, area:area_val, keywords:keywords_arr})
		});

		req.done(function(query){
			query_div.html(query)
		});
		// send values to ajax
		// returned must be filtered html

		fieldset.find("[name^='accept']").show();
	});


	$("[name^='accept']").click(function(){
		const fieldset = $(this).closest("fieldset");
		fieldset.find('input, textarea').attr('readonly','');
		fieldset.find("[name^='search']").hide();
		fieldset.find("[name^='edit']").show();
		// hide tags div
		$(this).hide();
	});

	$("[name^='edit']").click(function(){
		const fieldset = $(this).closest("fieldset");
		fieldset.find('input, textarea').removeAttr('readonly','');
		fieldset.find("[name^='accept']").show();
		fieldset.find("[name^='search']").show();
		$(this).hide();
	});

	$("[name^='author']").keyup( function(){
		const field = $(this);
		const val = field.val();
		const valid_feedback = $("#"+field.attr("id") + "valid");
		const invalid_feedback = $("#"+field.attr("id") + "invalid");
		
		req = $.ajax({
			url:'/validate_sn',
			type: 'POST',
			data: {val:val}
		});

		req.done(function(found){
			if(found){
				field.attr('class','form-control is-valid');
				valid_feedback.html("Student found with name: "+found);
			}else{
				field.attr('class','form-control is-invalid');
				invalid_feedback.html('Student number does not exist');
			}
		});
	});

});