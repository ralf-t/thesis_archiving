$( document ).ready(function() {

	$("#select_data").change(function(){
		if($("#select_data").val() == "Subject"){
			$("#name").show();
		}
		else{
			$("#name").val("");
			$("#name").hide();
		}
	});
});	

