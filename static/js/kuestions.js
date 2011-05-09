/** ************question section********** */

function loadQuestionTags(questionContent) {
	questionContent = replaceAll(questionContent, ' +', ' ');
	questionContent=questionContent.replace("?","");
	// words = replaceAll(questionContent, '\u003F', '').split(" ");
	words = questionContent.split(" ");
	zone = document.getElementById('tagsZone')
	tags = zone.getElementsByTagName('span');
	for (i = 0; i < tags.length; i++) {
		zone.removeChild(tags[i]);
	}
	checkIfTag(words);
}

function checkIfTag(words) {

	$(".popup #tagsZone .tag").remove();
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

function addTag(value){
	$(".popup #tagBar").attr("value","");
	d=new Date();
	id=  d.getMilliseconds();
	$('<span>', {
		id : id,
		text : value,
		class : "tag",
	}).appendTo(".popup #tagsZone");
	$("#"+id).click(function(){$("#"+this.id).remove();});
	
}

function appendTag(data) {
	json = eval(data);
	
	if (json.rows[0]) {
		addTag(json.rows[0].key);
		console.log(json.rows[0].key);
	}
}

function postQuestion() {	
	// retrieve question
	question = $(".popup #postQuestionBar").val();
	question= replaceAll(question,"  +"," ");
	if(question == "" | question ==" "){
		displayMessagePop("A question needs words");
	    return;
	    }
	console.log('posting:' +question);
	// retrieve tags
	tags=[];
	arr=$(".popup #tagsZone .tag");
	i=0
	$.each(arr,function (){tags[i]=$(this).text();i++; });
	console.log(tags);
	tokenValue = $("#security_csrf input:first").val();
	
	data= "question=" + question + "&csrfmiddlewaretoken="+tokenValue;
	if( tags.length > 0)
		data=data+"&tags="+tags;
	
	$.ajax({
		type : "POST",
		url : "/question/post/",
		data : data,
		success : function(data, textStatus, jhxqr) {
			questionCallBack(data, jhxqr);
			// displayMessageCallbackPop(data, jhxqr, "postMessageContainer");
		}
	});
}

function questionCallBack(data, textStatus){
	$.facebox.close();
	displayMessage(textStatus.getResponseHeader("message"),"messageContainer");
}

/** *********Display Questions (Search/timeline/followed)*********** */

function enhanceSearch(search) {
	if (search.substr(-1) !== " ") {
		search += '*';
	}
	return search;
}

function replaceAll(text, toReplace, replacement) {
	return text.replace(new RegExp(toReplace, 'g'), replacement);
}
var lastSearch = '';
function searchQuestions(search) {
	if(search==null){
		search = document.getElementById("searchBar").value;
	}
	if (search != "") {
		search=enhanceSearch(search);
		if (search != lastSearch) {
			var url = '/api/_fti/_design/question/by_content';
			$.ajax({
				url : url,
				data : 'q=' + search,
				dataType : 'json',
				success : function(data) {
					displayQuestionList(data.rows, 'search');
				}
			});
		}
	} else {
		cleanQuestionList();
	}
	lastSearch = search;
}

function displayFollowedQuestions(){
  if(!user_session.isOpen){
    console.log('need to log in first');
    return;
  }

  $.ajax({
    url: '/question/display/followed/',
    dataType: "JSON",
    success: function(data){
      displayQuestionList(data, 'followed');
    }
  });
}


// the minimun score a match should have in order to be displayed
var minScore = 0.5;

//displayQuestionList: accepts json list of questions, displays them as list on left side of the page
//filterType = (search/timeline/followed)
function displayQuestionList(questionList, filterType){
  cleanQuestionList();

  //determine container to display questions
  var containerId = '#questionList_' + filterType;

  //create ul
  $(containerId).append('<ul id="questionSearchResults"></ul>');

  //question data is not always consistent...need to parse data case by case
  if (filterType == 'search'){
    //fill search results
    for (i = 0; i < questionList.length; i++){
      if (questionList[i].score >= minScore){
        var li = $('<li>',{
          id: questionList[i].id,
          text: questionList[i].fields.content,
        }).appendTo($("#questionSearchResults"));

        li.click({'questionId': questionList[i].id}, function(event){
          viewQuestion(event.data.questionId);
        });
      }
    }
  } else if (filterType == 'followed'){
    //fill search results
    for (i = 0; i < questionList.length; i++){
      var li = $('<li>',{
        id: questionList[i].id,
        text: questionList[i].content,
      }).appendTo($("#questionSearchResults"));

      li.click({'questionId': questionList[i].id}, function(event){
        viewQuestion(event.data.questionId);
      });
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

function cleanQuestionList(){
  $("#questionSearchResults").remove();
}

/** ********View Question*********** */


// views a question when you click one
// creates a 'question page' on the right side of the page
function viewQuestion(questionId){
  removeMessage("answerMessageContainer");
  $.ajax({
    url: '/question/view/',
    type: "GET",
    data: "questionId=" + questionId ,
    dataType: "json",
    success: function(data) { // data is question json data
      // unhide question detail
      $("#questionDetail").removeClass("hidden");
      // embed current question ID into #questionDetail
      $("#questionDetail").attr("data-questionId", data.id);
      // set question Title
      $("#questionTitle").text(data.content);
      // display asker
      $("#questionAsker").attr("href","/user/"+ data.asker);
      $("#questionAsker").text(data.asker);
      // display follow or unfollow on the button, and set it action
      setManageFollowButton(questionId);
      viewAnswers(data.answers);
	$("#answerInput").val("");}
  });
}

function hideQuestionDetail(){
  $("#questionDetail").addClass("hidden");
}

function setManageFollowButton(questionId){
	if(user_session.isOpen ){
	  $("#manageFollow").removeAttr('disabled');
  	$("#manageFollow").removeClass("hidden");
    if(userIsFollowingQuestion(questionId)){
     console.log('user is following');
      $("#manageFollow").text('Unfollow');
      $("#manageFollow").attr('action','un');
    } 
    else {
  	  console.log('user is NOT following');
  	  $("#manageFollow").text('Follow');
  	  $("#manageFollow").attr('action','fo');
  	}
  }
  else {
    $("#manageFollow").addClass("hidden");
  }
}

function manageFollowQuestion(){
	csrf = $("#security_csrf input:first").val();
	questionId=$("#questionDetail").attr("data-questionId")
	data="questionId=" + questionId + '&csrfmiddlewaretoken=' 
			+ csrf+"&action="+$("#manageFollow").attr('action');
	$.ajax({
	  url: '/question/manageFollowQuestion/',
	  type: "POST",
	  data: data,
	  dataType: "json",
	  success: function(data){
	    response=eval(data);
	    console.log(response);
	    if(response.followed){
		    user_session.followedQuestions.push(questionId);
	    }
	    else {
	      user_session.followedQuestions.pop(questionId);
	    }
	    setManageFollowButton(questionId);
	  }
	});
}

function userIsFollowingQuestion(questionId){
	if(user_session.isOpen){
		length=user_session.followedQuestions.length
	for (i=0;i<length;i++){
		if(questionId == user_session.followedQuestions[i])
			{return true;}
	}
		return false;
	}
	else 
		{return false;}
}

/** ********Answer functions*********** */

// takes list of answers as input and displays them on #answerList
function viewAnswers(answers){
  // clear existing answer list
  $("#answerList").empty();
  // populate answer list
  for (var i = 0; i < answers.length; i++){
    var li = $('<li>',{
      text: answers[i].content + ": " + answers[i].score,
      id: answers[i].id
    }).appendTo($("#answerList"));

    // rating buttons
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
  
  // check if answer is empty
  if (answer == ""){
	displayMessage("an answer needs word","answerMessageContainer"); 
    return;
  }

  // obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/postAnswer/',
    type: "POST",
    dataType: "JSON",
    data: "answer=" + answer + '&questionId=' + $("#questionDetail").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
    success: function(data){
      if (data.error){
        displayMessage(data.errorMessage,'answerMessageContainer');
        return;
      }
      viewAnswers(data);
    }
  });

  // clear answer input
  $("#answerInput").val("");
}

function incAnswerScore(answerId){
  // obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/rateAnswer/',
    type: "POST",
    data: "type=increment" + "&answerId=" + answerId + "&questionId=" + $("#questionDetail").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
    dataType: "json",
    success: function(data, textStatus, jqxhr){    
      displayMessage(jqxhr.getResponseHeader('message'),"answerMessageContainer");
      viewAnswers(data);
    }
  });
}

function decAnswerScore(answerId){
  // obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/rateAnswer/',
    type: "POST",
    data: "type=decrement" + "&answerId=" + answerId + "&questionId=" + $("#questionDetail").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
    dataType: "json",
    success: function(data, textStatus, jqXHR){
      displayMessage(jqXHR.getResponseHeader('message'),"answerMessageContainer");
      viewAnswers(data);     
    }
  });
}

/** **********Message functions ************* */

function displayMessage(messageContent, containerId) {
	removeMessage(containerId);
	content = document.getElementById(containerId);
	message = document.createElement("h3");
	message.id = "message";
	message.className = "message hidden";
	message.textContent = messageContent;
	content.appendChild(message);
	$("#" + containerId + " .message").click(function() {
		removeMessage(containerId);
	});
	$("#message").removeClass("#hidden").show("fast");
}

function displayMessageCallback(data, textStatus, containerId) {
	displayMessage(textStatus.getResponseHeader("message"), containerId);
}

function displayMessagePop(messageContent){
	$(".popup  .message #message").remove()
	$("<h3>", {
		text : messageContent,
		id : "message",
		class : "pop_message hidden",
		click : function() {
			$(".popup  .message #message").remove();
		}
	}).appendTo($(".popup .message"));
	$('.popup .message #message').removeClass("#hidden").show('fast');
}

function displayMessageCallbackPop(data, textStatus, containerId) {
displayMessagePop(textStatus.getResponseHeader("message"));
}

function removeMessage(containerId) {
	$("#" + containerId ).empty();
	}

/*
 * use to display a search comming from the profile page
 * 
 * 
 */

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

/** ******* Init *************** */
var user_session=null;
$(document).ready(function() {
	loadSession();
	init();
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
	// for loading dialog
	$(".ld_line").fadeOut(1000);
	// for modal dialog
	$('a[rel*=facebox]').facebox();	
	// Display a search comming from the profile page
	 vars=getUrlVars();
	if(vars["search"]){
		search=vars["search"];
		$('#searchBar').attr('value',unescape(search));
		searchQuestions(vars["search"]);		
	}
	if(vars["question"]){
		viewQuestion(vars["question"]);
	}
  $('#coda-slider-1').codaSlider({
    dynamicArrows: false,
    dynamicTabs: false,
    firstPanelToLoad: 1,
    autoHeight: false,
  });
  
  $('ul.tabs').find('li').click(function(){
      $('ul.tabs li').attr("class","");
      $(this).attr("class","radiusT selected");
  });
  
  $('#followedTab').click(function(){
    displayFollowedQuestions();
  });
});

function loadSession(){
	$.ajax({
		url:'/security/session/',
		TYPE : 'GET',
		dataType : 'json',
		success: function(data){
			user_session=eval(data);
		}	
	})
}

function init() {
	$('#searchBar').keyup(function(event) {
		searchQuestions();
	});
	// from the profile page, a new search redirect to the main page
	$('#searchBarProfile').keyup(function(event) {
		 if (event.keyCode == '13') {
		search = document.getElementById("searchBarProfile").value;
	    document.location.href = '/?search='+search; }
	});
	$('#message').click(function() {
		removeMessage('messageContainer');
	});
	$("#manageFollow").click(function(){
   	 $("#manageFollow").attr('disabled','disabled'); 
 	     manageFollowQuestion();
    });
	$("#searchBar").focus();
}
