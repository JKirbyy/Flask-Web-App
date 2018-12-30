$(document).ready(function() {
	console.log("here")
	var alert = $("div.alerttwo");
	alert.hide();

	$("button.new").on("click", function() { //when user opts to change password
		var clicked_obj = $(this);
		console.log("clicked");
		// Which idea was clicked? Fetch the idea ID
		var password_one = document.getElementById("passoneone").value;
		var password_two = document.getElementById("passtwotwo").value;

		if (password_one != password_two)
		{
			console.log("passwords do not match")
			alert.html("Passwords do not match.");
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

		else
		{
			document.newpassform.submit(); //change password 
		}

	});

});
