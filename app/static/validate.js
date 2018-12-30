$(document).ready(function() {
	console.log("here")
	var alert = $("div.alert");
	alert.hide();

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

	$("button.sub").on("click", function() {
		var clicked_obj = $(this);
		var username = document.getElementById("username").value;
		var password_one = document.getElementById("passone").value;
		var password_two = document.getElementById("passtwo").value;

			url: '/validate',
			type: 'POST',
			data: JSON.stringify({ username: username}), //let server check if user exist already
			contentType: "application/json; charset=utf-8",
        	dataType: "json",
          success: function(response)
					{

						if (response == 2)
						{
							alert.html("User already exists.");
							alert.show();
						}

						else if (password_one != password_two)
						{
							console.log("passwords do not match")
							alert.html("Passwords do not match.");
							alert.show();
						}

						else if (username.length > 12)
						{
							console.log("username too long")
							alert.html("Username too long. Must be between 5 and 12 characters.");
							alert.show();
						}

						else if (username.length < 5)
						{
							console.log("username too short")
							alert.html("Username too short. Must be between 5 and 12 characters.");
							alert.show();
						}

						else if (password_one.length < 5)
						{
							console.log("password too short")
							alert.html("Password too short. Must be between 5 and 12 characters.");
							alert.show();
						}

						else if (password_one.length > 12)
						{
							console.log("password too long")
							alert.html("Password too long. Must be between 5 and 12 characters.");
							alert.show();
						}

						else //if valid then submit form to server
						{
							document.form.submit();
						}


			    },
			error: function(error){
				console.log(error);
			}
		});
	});

});
