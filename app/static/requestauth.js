$(document).ready(function() {

	// Set the CSRF token so that we are not rejected by server
	var csrf_token = $('meta[name=csrf-token]').attr('content');
	// Configure ajaxSetupso that the CSRF token is added to the header of every request
  $.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrf_token);
	        }
	    }
	});


	$("#parent").on("click", "a.follow", function() {
		var clicked_obj = $(this);
		var requesting_user = $(this).attr('id');
		var requested_story = $("a.requested").attr('id');


		$.ajax({
			url: '/follow',
			type: 'POST',
			data: JSON.stringify({ requesting_user: requesting_user, requested_story: requested_story}),
			contentType: "application/json; charset=utf-8",
        	dataType: "json",
          success: function(response)
					{
                clicked_obj.innerHTML = "Requested";
								var req = document.getElementById(requesting_user);
								req.innerHTML = "Requested"; //show user they have requested authorship
								req.classList.remove('follow'); //remove the request button

			    },
			error: function(error){
				console.log(error);
			}
		});
	});
});
