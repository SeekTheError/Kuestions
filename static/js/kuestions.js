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
			displayMessage(data);
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
    //create unordered list under questionList div
    $("#questionList").append('<ul id="questionSearchResults"/>');
    //fill the search results with retrieved data
		question = object.rows;
		for (i = 0; i < object.total_rows; i++) {
      //TODO:reintegrate formatQuestion (it will be nice to have question previews instead of a plain question list here)
			if (question[i].score >= minScore) {

        //append li element
        var li = $('<li>',{
          id: question[i].id,
          text: question[i].fields.content,
        }).appendTo($("#questionSearchResults"));

        //add click event
        li.click({'questionId': question[i].id}, function(event){
          viewQuestion(event.data.questionId);
        });
			}
		}
	}
}

function formatQuestion(question) {
	span = document.createElement("span");
	p = document.createElement("p");
	p.id=question.id
	p.textContent = question.content;
	span.appendChild(p);
	return p;
}

function cleanQuestionList(){
  $("#questionList").empty();
}

/** ********View Question*********** */

// views a question when you click one
// creates a 'question page' on the right side of the page
function viewQuestion(questionId){
  //obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();

  //send ajax request to questioncontroller's viewQuestion
  $.ajax({
    url: '/question/view/',
    type: "POST",
    data: "questionId=" + questionId + '&csrfmiddlewaretoken=' + csrf,
    dataType: "json",
    success: function(data) { //data is question json data
      //unhide question detail
      $("#questionDetail").removeClass("hidden");
      //embed current question ID into #questionDetail
      $("#questionDetail").attr("data-questionId", data.id);

      //set question Title
      $("#questionTitle").text(data.content);
      //display asker
      $("#questionAsker").text("asker: " + data.asker);

      viewAnswers(data.answers);

      /* TODO:use javascript to produce the whole detail view? */
      
    }
  });
}

/** *********Answering******** */

//takes list of answers as input and displays them on #answerList
function viewAnswers(answers){
  //clear existing answer list
  $("#answerList").empty();
  //populate answer list
  for (var i = 0; i < answers.length; i++){
    var li = $('<li>',{
      text: answers[i].content + ": " + answers[i].score,
      id: answers[i].id
    }).appendTo($("#answerList"));

    //rating buttons
    var plusButton = $('<input>',{
      type: "button",
      value: "+",
    }).appendTo(li);

    plusButton.click({'answerId': answers[i].id}, function(e){
      incAnswerScore(e.data.answerId);
    });

    var minusButton = $('<input>',{
      type: "button",
      value: "-",
    }).appendTo(li);

    minusButton.click({'answerId': answers[i].id}, function(e){
      decAnswerScore(e.data.answerId);
    });
  }
}

function postAnswer(answerText){
  var answer = $("#answerInput").val();
  
  //check if answer is empty
  if (answer == ""){
    return;
  }

  //obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/postAnswer/',
    type: "POST",
    dataType: "JSON",
    data: "answer=" + answer + '&questionId=' + $("#questionDetail").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
    success: function(data){
      if (data.error){
        displayMessage(data.errorMessage);
        return;
      }
      viewAnswers(data);
    }
  });

  //clear answer input
  $("#answerInput").val("");
}

function incAnswerScore(answerId){
  //obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/rateAnswer/',
    type: "POST",
    data: "type=increment" + "&answerId=" + answerId + "&questionId=" + $("#questionDetail").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
    dataType: "json",
    success: function(data, textStatus, jqxhr){
      viewAnswers(data);
      displayMessage(jqxhr.getResponseHeader('message'));
    }
  });
}

function decAnswerScore(answerId){
  //obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/rateAnswer/',
    type: "POST",
    data: "type=decrement" + "&answerId=" + answerId + "&questionId=" + $("#questionDetail").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
    dataType: "json",
    success: function(data, textStatus, jqXHR){
      viewAnswers(data);
      displayMessage(jqXHR.getResponseHeader('message'));
    }
  });
}

/** ***Util****** */


function displayMessage(message){
  removeMessage();

  $('<h3>',{
    id: "message",
    className: "message nodisp:",
    text: message,
    click: function(){
      removeMessage()
    }
  }).appendTo($("#messageContainer"));
}

function removeMessage(){
  $("#messageContainer").empty();
}


/** ******* Init *************** */
$(document).ready(function() {
	init();
});

function init() {
	$('#searchBar').keyup(function(event) {
		searchQuestions();

	});
	
	$('#postBar').change(function(event) {
		loadQuestionTags();
	});
 
    $('#message').click(function () {removeMessage('messageContainer');})
}
