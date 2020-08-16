$( document ).ready(function() {
	$('input').attr('autocomplete','off');

	// name generator ajax
	$('#acad_role, #admin_role').change(function(){
		const role = $(this).val();
		
		req = $.ajax({
			url: '/thesis_archiving/admin/register/user/generated_user',
			type: 'POST',
			data : {role:role}
		});

		req.done(function(username) {	
			const student_role = ( $('#acad_role').val() === 'Student' ) ? true : false;

			// Student role overrides usernames
			if (student_role){
				$('#username').removeAttr('readonly');
				$('#username').val('');

			} else {
				$('#username').attr('readonly','');
				$('#username').val(username);
			}
			
		});
	});

});