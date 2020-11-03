$( document ).ready(function() {

	$("#select_data").change(function(){
		if($("#select_data").val() == "Subject") {
				$("#name").show();
		}
		else if($("#select_data").val() == "Section") {
				$("#name").val("");
				$("#name").hide();
			}
	});
});	

