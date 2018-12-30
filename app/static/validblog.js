$(document).ready(function() {
	var alert = $("div.alertthree");
	alert.hide();

	$("button.blog").on("click", function() {
		var clicked_obj = $(this);
		var title = document.getElementById("title").value;
		var mainbody = document.getElementById("mainbody").value;
		var comment = document.getElementById("comment").value;

		if (title.length > 99)
		{
			console.log("Title too long.")
			alert.html("Title too long.");
			alert.show();
		}

		else if (mainbody.length > 49999)
		{
			console.log("Body too long.")
			alert.html("Body too long.");
			alert.show();
		}

		else if (comment.length > 499)
		{
			console.log("Comment too long.")
			alert.html("Comment too long.");
			alert.show();
		}

		else
		{
			document.blogform.submit();
		}
	});
});
