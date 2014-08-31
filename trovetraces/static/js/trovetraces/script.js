$(function() {
	$("#order_by").change(function() {
		var href = window.location.href;
		if (href.indexOf("?") == -1) {
			href = href + "?";
		}
		href = href.replace(/page=\d+/, "page=1");
		href = href.replace(/&*order_by=[a-z_-]+/, "");
		var order_by = $("#order_by").val();
		if (order_by !== "") {
			href = href + "&order_by=" + order_by;
		}
		window.location.href = href;
	});
});