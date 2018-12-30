$(document).ready(function() {

	var csrf_token = $('meta[name=csrf-token]').attr('content');
  $.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrf_token);
	        }
	    }
	});

	$("a.ans").on("click", function() {
		var clicked_obj = $(this);
		var request_id = $(document.getElementsByClassName("req")).attr('id');
		var decision = $(this).attr("data-answer"); //+ and - buttons have different answer attributes
			url: '/requests',
			type: 'POST',
			data: JSON.stringify({ request_id: request_id, decision: decision}),
			contentType: "application/json; charset=utf-8",
        	dataType: "json",
          success: function(response)
					{
    						clicked_obj.parent().remove(); //remove request
								var count = document.getElementById("req");
								count_number = parseFloat(count.innerHTML);
								count_number--; //decrease the request count displayed
								count.innerHTML = count_number;
								if (decision == 1)
								{
									var count_two = document.getElementById("auth");
									count_number_two = parseFloat(count_two.innerHTML);
									count_number_two++; //increase the author count displayed
									count_two.innerHTML = count_number_two;
								}
			    },
			error: function(error){
				console.log(error);
			}
		});
	});

	$("a.remove").on("click", function() { //remove author
		var clicked_obj = $(this);
		var remove_id = $(document.getElementsByClassName("remove")).attr('data-id');
		var post_id = $(document.getElementsByClassName("post")).attr('id');
			url: '/remove',
			type: 'POST',
			data: JSON.stringify({ remove_id: remove_id, post_id: post_id}),
			contentType: "application/json; charset=utf-8",
        	dataType: "json",
          success: function(response)
					{
								clicked_obj.parent().remove(); //remove author name displayed
								var count = document.getElementById("auth");
								count_number = parseFloat(count.innerHTML);
								count_number--; //decrease displayed author count
								count.innerHTML = count_number;
			    },
			error: function(error){
				console.log(error);
			}
		});
	});
});
