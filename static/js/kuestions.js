$(document).ready(function() {
	init();
});

function init() {
	// google instant style
	$('#searchBar').keyup(function(event) {
		if (event.which > 47 | event.which == 8)
			searchQuestion();
	});

	$('#postBar').change(function(event) {
		postQuestionSequence();
	});
}

function postQuestionSequence() {
	questionContent = document.getElementById("postBar").value;

	/*
	 * $.ajax({ url : url, data : data });
	 */
	postQuestion(questionContent, undefined);

}

function postQuestion(question, tags) {
	// retrieve the csrf tokken
	tokenValue = document.getElementById("extra").getElementsByTagName("input")[0]
			.getAttribute("value");
	$.ajax({
		type : "POST",
		url : "/question/post/",
		data : "question=" + question + "&csrfmiddlewaretoken=" + tokenValue,
		success : function(data, textStatus, jqxhr) {
			displayMessage(data, jqxhr, "postMessageContainer");
		}
	});
}
var temp;
function displayMessage(data, textStatus, containerId) {
	removeMessage(containerId);
	
	content = document.getElementById(containerId);

	message = document.createElement("h3");
	message.className = "message nodisp";
	message.id = "message";

	message.textContent = textStatus.getResponseHeader("message");
	content.appendChild(message);
	$("#message").click(function() {
		removeMessage(containerId);
	});
	$("#message").addClass("#display").show("fast");
}

function removeMessage(containerId) {
	content = document.getElementById(containerId);
	child = document.getElementById("message");
	if (child != undefined) {
		content.removeChild(child);
	}

}

function searchQuestion() {
	var searchParameter = document.getElementById("searchBar").value;

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
		// clean the current questions
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
			if (rows[i].score >= 0.6) {
				question = rows[i].fields;
				question.id = rows[i].id;
				li = document.createElement("li");
				li.appendChild(formatQuestion(question));
				ul.appendChild(li);
			}
		}
	}
}
function formatQuestion(question) {
	span = document.createElement("span");
	p = document.createElement("p");
	p.textContent = question.content;
	span.appendChild(p);
	return p;
}
