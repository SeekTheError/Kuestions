function searchQuestion() {

	var searchParameter = document.getElementById("searchParameter").value;
	var url = '/api/_fti/_design/question/by_content?q=' + searchParameter;
	$.ajax({
		url : url,
		dataType : 'json',
		success : function(data) {
			displaySearchResults(data);
		}
	});
}

function displaySearchResults(data) {
	object = eval(data);
	rows = object.rows;
	if (object.rows) {
		el = document.getElementById("questionList");
		child = document.getElementById("questionSearchResults");
		if (child != undefined) {
			el.removeChild(child);
		}
		ul = document.createElement("ul");
		ul.id = "questionSearchResults";
		el.appendChild(ul);
		rows = object.rows;
		length = rows.length;
		for (i = 0; i < length; i++) {
			question = rows[i].fields;
			question.id = rows[i].id;
			li = document.createElement("li");
			li.appendChild(formatQuestion(question));
			ul.appendChild(li);
		}
	}
}
function formatQuestion(question) {
	span = document.createElement("span");
	p = document.createElement("p");
	p.textContent = question.default;
	span.appendChild(p);
	return p;
}
