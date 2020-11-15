$( document ).ready(function() {
	
	$('#date_deploy').attr('data-provide','datepicker');
	$('#date_deploy').datepicker({
	    startDate: "01/01/2010",
	    todayBtn: 'linked',
	    clearBtn: true
	});

	$("[name$='keywords']").tokenfield({
		limit:10,
		beautify:false
	});

	$('#form_file,#thesis_file').change(function(e) {
	  var file = e.target.files; 

	  $(this).next('.custom-file-label').html(file[0]['name']);

	});

	// for tags and shit
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
			url:'/thesis_archiving/admin/register/thesis/fuzz_tags',
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
	
	$("#username").keyup( function(){
		const field = $(this);
		const val = field.val();
		const valid_feedback = $("#username-valid");
		const invalid_feedback = $("#username-invalid");
		
		req = $.ajax({
			url:'/thesis_archiving/validate_sn',
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