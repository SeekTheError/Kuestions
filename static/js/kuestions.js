
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
			displayMessage(data, jhxqr, "postMessageContainer");
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
		search=enhanceSearch(search);
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

var temp;

// the minimun score a match should have in order to be displayed
var minScore = 0.5;
function displaySearchResults(data) {
	cleanQuestionList();
	object = eval(data);
	if (object.rows) {
    //create unordered list under questionList div
    $("#questionList").append('<ul id="questionSearchResults"/>');
    //fill the search results with retrieved data
		question = object.rows;
		for (i = 0; i < object.total_rows; i++) {
      //TODO:reintegrate formatQuestion (it will be nice to have question previews instead of a plain question list here)
			if (question[i].score >= minScore) {
        //obtain csrftoken
        var csrf = $("#security_csrf input:first").val();

        //append li element
        jQuery('<li/>',{
          id: question[i].id,
          text: question[i].fields.content,
          click: function(e){
            $.ajax({
              url: '/question/view/',
              type: "POST",
              data: "questionId=" + this.id + '&csrfmiddlewaretoken=' + csrf,
              success: function(data) {
                $(".right").empty();
                jQuery('<h1>',{
                  text: data
                }).appendTo($(".right"));
              }
            });
          }
        }).appendTo($("#questionSearchResults"));
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
function cleanQuestionList() {
	el = document.getElementById("questionList");
	child = document.getElementById("questionSearchResults");
	if (child != undefined) {
		el.removeChild(child);
	}
}

/** ***Util****** */

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

/** ******* Init *************** */
$(document).ready(function() {
	init();
});

function init() {
	$('#searchBar').keyup(function(event) {
		searchQuestions();

	});

	/***************************************************************************
	 * $('#searchBar').change(function(event) {
	 * searchQuestion(document.getElementById("searchBar").value); });
	 **************************************************************************/

	$('#postBar').change(function(event) {
		loadQuestionTags();
	});

}
