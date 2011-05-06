function loadQuestionTags() {
	el = document.getElementById("postBar");
	questionContent = el.value;
	words = replaceAll(questionContent, ' +', ' ').split(" ");
	zone = document.getElementById('tagsZone')
	tags = zone.getElementsByTagName('span');
	for (i = 0; i < tags.length; i++) {
		zone.removeChild(tags[i]);
	}
	checkIfTag(words);
}

function checkIfTag(words) {
	for (i = 0; i < words.length; i++) {
		if (words[i] != '') {
			word = words[i].toLowerCase();
			url = '/api/_design/topics/_view/topic?key="' + word + '"';
			$.ajax({
				type : "GET",
				dataType : "json",
				url : url,
				success : function(data) {
					appendTag(data);
				}
			});
		}
	}
}

var temp = '';
function appendTag(data) {
	json = eval(data);
	if (json.rows[0]) {
		p = document.createElement('span');
		p.id = word;
		p.className = "tag";
		p.textContent = json.rows[0].key;
		zone = document.getElementById('tagsZone')
		zone.appendChild(p);
		$(p).click(function() {
			zone = document.getElementById('tagsZone');
			tag = document.getElementById(word);
			zone.removeChild(tag);
		});
	}

}

function postQuestion() {
	question = $("#postBar").val();
	tokenValue = $("#security_csrf input:first").val();
	$.ajax({
		type : "POST",
		url : "/question/post/",
		data : "question=" + question + "&csrfmiddlewaretoken=" + tokenValue,
		success : function(data, textStatus, jhxqr) {
			displayMessageCallback(data, jhxqr, "postMessageContainer");
		}
	});
}

/** *********Search*********** */

function enhanceSearch(search) {
	if (search.substr(-1) !== " ") {
		search += '*';
	}
	// search = search.replace(new RegExp(" ", 'g'), "+");

	return search;
}

function replaceAll(text, toReplace, replacement) {
	return text.replace(new RegExp(toReplace, 'g'), replacement);
}
var lastSearch = '';
function searchQuestions() {
	search = document.getElementById("searchBar").value
	if (search != "") {
		search = enhanceSearch(search);
		console.log(search);
		if (search != lastSearch) {
			var url = '/api/_fti/_design/question/by_content';
			$.ajax({
				url : url,
				data : 'q=' + search,
				dataType : 'json',
				success : function(data) {
					displaySearchResults(data);
				}
			});
		}

	} else {
		cleanQuestionList();
	}
	lastSearch = search;

}

// the minimun score a match should have in order to be displayed
var minScore = 0.5;
function displaySearchResults(data) {
	cleanQuestionList();
	object = eval(data);
	if (object.rows) {
		// create unordered list under questionList div
		$("#questionList").append('<ul id="questionSearchResults"/>');
		// fill the search results with retrieved data
		question = object.rows;
		for (i = 0; i < object.total_rows; i++) {
			// TODO:reintegrate formatQuestion (it will be nice to have question
			// previews instead of a plain question list here)
			if (question[i].score >= minScore) {

				// append li element
				jQuery('<li/>', {
					id : question[i].id,
					text : question[i].fields.content,
					click : viewQuestion
				}).appendTo($("#questionSearchResults"));
			}
		}
	}
}

function formatQuestion(question) {
	span = document.createElement("span");
	p = document.createElement("p");
	p.id = question.id
	p.textContent = question.content;
	span.appendChild(p);
	return p;
}
function cleanQuestionList() {
	el = document.getElementById("questionList");
	child = document.getElementById("questionSearchResults");
	if (child != undefined) {
		el.removeChild(child);
	}
}

/** ********View Question*********** */

// views a question when you click one
// creates a 'question page' on the right side of the page
function viewQuestion() {
	// obtain csrftoken needed to post data
	var csrf = $("#security_csrf input:first").val();

	// send ajax request to questioncontroller's viewQuestion
	$.ajax({
		url : '/question/view/',
		type : "POST",
		data : "questionId=" + this.id + '&csrfmiddlewaretoken=' + csrf,
		dataType : "json",
		success : function(data) {
			console.log(data)
			// unhide question detail
			$("#questionDetail").removeClass("hidden");
			// embed current question ID into #questionDetail
			$("#questionDetail").attr("data-questionId", data.id);

			// set question Title
			$("#questionTitle").text(data.content);
			// display asker
			$("#questionAsker").text(data.asker);

			// clear existing answer list
			$("#answerList").empty();
			// populate answer list
			for ( var i = 0; i < data.answers.length; i++) {
				$('<li>', {
					text : data.answers[i].content
				}).appendTo($("#answerList"));
			}

			/* TODO:use javascript to produce the whole detail view? */

		}
	});
}

/** *********Answering******** */

function postAnswer(answerText) {
	var answer = $("#answerInput").val();

	// check if answer is empty
	if (answer == "") {
		displayMessage('an answer need words','answerMessageContainer')
		return;
	}

	// obtain csrftoken needed to post data
	var csrf = $("#security_csrf input:first").val();
	$.ajax({
		url : '/question/postAnswer/',
		type : "POST",
		dataType : "json",
		data : "answer=" + answer + '&questionId='
				+ $("#questionDetail").attr("data-questionId")
				+ '&csrfmiddlewaretoken=' + csrf,
		success : function(data) {
			postAnswerCallback(data);
		}
	});
	// clear answer input
	$("#answerInput").val("");
}

function postAnswerCallback(data) {
	response = eval(data);
	console.log(response);
	if (response.success) {
		console.log('true')
		$('<li>', {
			text : data.answer
		}).appendTo($("#answerList"));
	}
	else {
		displayMessage(response.message,'answerMessageContainer')
	}

}
/*
 */

/** ***Util****** */

function displayMessage(messageContent,containerId){
	removeMessage(containerId);
	
	content = document.getElementById(containerId);
	console.log(content);
	message = document.createElement("h3");
	message.className = "message nodisp";
	message.id = "message";

	message.textContent = messageContent;
	content.appendChild(message);
	$("#message").click(function() {
		removeMessage(containerId);
	});
	$("#message").addClass("#display").show("fast");
	
}

function displayMessageCallback(data, textStatus, containerId) {
	displayMessage(textStatus.getResponseHeader("message"),containerId);

}

function removeMessage(containerId) {
	content = document.getElementById(containerId);
	child = document.getElementById("message");
	if (child != undefined) {
		content.removeChild(child);
	}

}

/** ******* Init *************** */
$(document).ready(function() {
	init();
});

$(document).ready(function() {
	$(window).resize(function() {

		var height = parseInt($(window).height()) - 200;
		height = height + 'px';
		$("div.panel_contents").css({
			'height' : height
		});

		height = parseInt($(window).height()) - 130;
		height = height + 'px';
		$("div.left").css({
			'min-height' : height
		});
	});

	var height = parseInt($(window).height()) - 130;
	height = height + 'px';
	$("div.left").css({
		'min-height' : height
	});

	init();

	// for loading dialog
	$(".ld_line").fadeOut(1000);

	// for modal dialog
	$('a[rel*=facebox]').facebox();
	// $('button[rel*=facebox]').facebox();
});

function init() {
	$('#searchBar').keyup(function(event) {
		searchQuestions();

	});

	$('#postBar').change(function(event) {
		loadQuestionTags();
	});

	$('#message').click(function() {
		removeMessage('messageContainer');
	})
}
