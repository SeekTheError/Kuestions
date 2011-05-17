/** ************question section********** */

function loadQuestionTags(questionContent) {
	questionContent = replaceAll(questionContent, ' +', ' ');
	questionContent=questionContent.replace("?","");
	// words = replaceAll(questionContent, '\u003F', '').split(" ");
	words = questionContent.split(" ");
	zone = document.getElementById('tagsZone');
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
		class : "tag"
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
	title = $(".popup #questionTitleInput").val();
	title= replaceAll(title,"  +"," ");
	if(title == "" | title ==" "){
		displayMessagePop("A question needs words");
	  return;
  }
  description = $(".popup #questionDescriptionInput").val();
  description = replaceAll(description, "  +", " ");

	// retrieve tags
	tags=[];
	arr=$(".popup #tagsZone .tag");
	i=0;
	$.each(arr,function (){tags[i]=$(this).text();i++; });
	console.log(tags);

  // retrieve csrf token
	tokenValue = $("#security_csrf input:first").val();

  // concatenate data
	data= "title=" + title + "&description=" + description + "&csrfmiddlewaretoken="+tokenValue;
	if( tags.length > 0)
		data=data+"&tags="+tags;
	
	$.ajax({
		type : "POST",
		url : "/question/post/",
		data : data,
		success : function(data, textStatus, jhxqr) {
			postQuestionCallback(data, jhxqr);
		}
	});
}

function postQuestionCallback(data, textStatus){
	$.facebox.close();
	displayMessage(textStatus.getResponseHeader("message"),"messageContainer");
}

/** *********Display Questions (Search/timeline/followed)*********** */

function enhanceSearch(search) {
	if (search.substr(-1) !== " ") {
		search += '*';
	}
	//search= replaceAll(search,' +',' ');
    console.log(search);
	return search;
}

function replaceAll(text, toReplace, replacement) {
	return text.replace(new RegExp(toReplace, 'g'), replacement);
}
function searchQuestions(search) {
	if(search==null){
		search = document.getElementById("searchBar").value;
	}

	if (search != "") {
		search=enhanceSearch(search);
    var url = '/api/_fti/_design/question/by_title?';
    $.ajax({
      url : url,
      data : 'q=' + search,
      dataType : 'json',
      success : function(data) {
        displayQuestionList(data.rows, 'search');
      }
    });
	} else {
		cleanQuestionList();
	}
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
      if (data.length > 0 ){
        displayQuestionList(data, 'followed');
      } else{
        $('#questionList_followed').text('no followed questions...yet');
      }
    }
  });
}
function displayRecommendedQuestions(){
	  if(!user_session.isOpen){
	    console.log('need to log in first');
	    return;
	  }
	  if(user_session.topics.length==0){
		  console.log("user has no topics");
		  return;
	  }
	  
	  topicsParam='';
	  for (i in user_session.topics){
		  topicsParam+=user_session.topics[i]+'+';
	  }
	  url='/api/_fti/_design/question/by_topics?&q='+topicsParam;
	  $.ajax({
	    url: url,
	    dataType: "JSON",
	    success: function(data){
	      if (data.rows.length > 0 ){
          questions=data.rows;

          //filter out questions that belong to the current user... we don't want to recommend their own question to them!
          var filteredList = [];
          for (i = 0; i < questions.length; i++){
            if (questions[i].fields.asker != user_session.login){
              filteredList.push(questions[i]);
            }
          }
	        displayQuestionList(filteredList, 'recommended');
	      } else{
	        $('#questionList_followed').text('no recommendation available yet... Did you edit your profile?');
	      }
	    }
	  });
	}

function displayPopularQuestions(){
  if(!user_session.isOpen){
    console.log('need to log in first');
    return;
  }

  $.ajax({
    url: '/api/_design/question/_view/popular?descending=true&limit=15',
    dataType: "JSON",
    success: function(data){
      displayQuestionList(data.rows, 'popular');
    }
  });
}

//display questions that are asked by a particular user
function displayUserQuestions(userLogin){
  console.log(userLogin);
  $.ajax({
    url: '/api/_design/question/_view/asker?key="'+ userLogin +'"&limit=15&descending=true',
    dataType: "JSON",
    success: function(data){
      displayQuestionList(data.rows, 'user');
    }
  });
}

// displayQuestionList: accepts json list of questions, displays them as list on
// left side of the page
// filterType = (search/timeline/followed/popular/recommended/user)
function displayQuestionList(questionList, filterType){
  console.log('questionlist');
  console.log(questionList);
  cleanQuestionList();

  // determine container to display questions
  var containerId = '#questionList_' + filterType;
  console.log(questionList);
  // generate styled question list
  for (var i = 0; i < questionList.length; i++){
    //create html
	  
    $(containerId).append('<div id="questionList'+i+'" class="speech_wrapper"> <div class="profile question"><a class="userLink'+i+'"><img id="questionProfileImg' + i +'"></div> <div class="speech"></a><div class="question"> <p class="bubble"></p> <p class="question_text" id="questionTitle'+i+'"></p> </div><div class="info"> <span id="askerAndPostDate'+i+'"></span> </div> <div class="actions"> <span class="follow"><a href="#"><img id="followButton' + i +'" src="/kuestions/media/image/icon_star_off.png" title="follow"></a></span> </div> </div> </div>');

    //fill in data:
    question = questionList[i];
    questionId = "";
    title = "";
    asker = "";
    postDate = "";
    //access data differently based on filter
    if (filterType == 'search' || filterType == 'recommended'){
      questionId = question.id;
      title = question.fields.title;
      asker = question.fields.asker;
      postDate = question.fields.postDate;
    } else if (filterType == 'followed'){
      questionId = question.id;
      title = question.title;
      asker = question.asker;
      postDate = question.postDate;
    } else if (filterType == 'popular'){
      questionId = question.id;
      title = question.value.title;
      asker = question.value.asker;
      postDate = question.value.postDate;
    } else if (filterType == 'user'){
      questionId = question.id;
      title = question.value.title;
      asker = question.value.asker;
      postDate = question.value.postDate;
    }
    postDate = humane_date(postDate);
    //TODO: post date message ex: 'posted 3 days ago'
    //asker and post date
    $(containerId + ' #askerAndPostDate' + i).html('<a href="/user/'+asker+'"><b>'+asker+'</b></a> posted ' + postDate);

    //edit question profile img
    $('#questionProfileImg' + i).attr('src', '/user/picture/' + asker);
    $('#userLink' + i).attr('href', '/user/' + asker);
    
    //question title
    $(containerId + ' #questionTitle' + i).text(title);

    //click handler for question detail view
    $('#questionList'+i).click( {'questionId': questionId }, function(event){
      viewQuestion(event.data.questionId);
    });

    //set up follow button
    setFollowButton(questionId, $('#followButton' + i));
  }
}

function loadTimeline(){
	 $("#questionList_timeline #timelineList").remove();
	 $.ajax({
		    url: '/timeline/',
		    type: "GET",
		    dataType: "json",
		    success: function(data){
		      displayTimeline(data);   
		    }});
	
}

function displayTimeline(data){
	timeline=eval(data);
	console.log(timeline);
	$("#questionList_timeline").append('<ul id="timelineList"></ul>');
	for(i=0;i<timeline.length;i++){
	id=timeline[i]._id.replace(".","");
	questionId=timeline[i].question;
	console.log("#questionList_timeline #"+timeline[i]._id);
	 var li = $('<li>',{
	      id: id
	    }).appendTo($("#timelineList"));
	  $("#questionList_timeline #"+id).click({'questionId': questionId},function(event){
	   viewQuestion(event.data.questionId);
	  });
	  date= new Date();
	  date.setTime(Date.parse(timeline[i].eventDate));
	  date= date.getMonth()+"/"+date.getDay()+" "+date.getHours()+":"+date.getMinutes();
	  var p= $('<span>',{
		  text: date +" " +timeline[i].questionTitle+" "
	  }).appendTo($("#timelineList #"+id));
	  var a= $('<a>',{
		  href:'/user/'+timeline[i].user,
		  text :timeline[i].user 
	  }).appendTo($("#timelineList #"+id));;
	  var a= $('<span>',{
		  text :'  post an answer'
	  }).appendTo($("#timelineList #"+id));;
	    
	}
}

function cleanQuestionList(){
  $('#questionList_search').html('<div class="dummy">search</div>' );
  $('#questionList_timeline').html('<div class="dummy">timeline</div>' );
  $('#questionList_followed').html('<div class="dummy">followed</div>');
  $('#questionList_popular').html('<div class="dummy">popular</div>');
  $('#questionList_user').html('<div class="dummy">user</div>');
  $('#questionList_recommended').html('<div class="dummy">recommended</div>');
}

/** ********View Question*********** */


// views a question when you click one
// creates a 'question page' on the right side of the page
function viewQuestion(questionId){
	csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/view/',
    type: 'POST',
    data: 'questionId='+questionId + '&csrfmiddlewaretoken='+csrf,
    dataType: "json",
    success: function(data){
      console.log(data);
      //embed question id into question display div
      $('.question_display').attr('data-questionId', data.id);
      $('.question_display').show();

      //populate question detail display
      $('#question_profile_img').attr('src', '/user/picture/' + data.asker);
      $('.question_info .profile a').attr('href','/user/'+data.asker);
      $('.question_title').html(data.title);
      $('.questionAsker').text(data.asker);
      $('.questionAsker').attr('href','/user/'+data.asker);
      $('.detail_contents').text(data.description);

      //set follow button
      setFollowButton(data.id, $('#followButton'));
      if(data.topics.length == 0){
        $('.detail_topics').hide();
      }else{
        $('.detail_topics').show();
        $('.detail_topics .topic ul').text(" ");
        for (var i = 0; i < data.topics.length; i++){
          topic=data.topics[i];
          topicHTML='<li class="topic_item False"><a href="/?search='+topic+'"><b>'+topic+'</b></a></li>';
          $('.detail_topics .topic ul').append(topicHTML);
        }
      }

      //display answers
      viewAnswers(data.answers);
      $("#answerInput").val("");
    }
  });
}

function hideQuestionDetail(){
  $("#questionDetail").addClass("hidden");
}

function setFollowButton(questionId, button){
	if(user_session.isOpen ){
    //change image depending on whether user is following
    if(userIsFollowingQuestion(questionId)){
      button.attr('src', '/kuestions/media/image/icon_star_on.png');
      button.attr('action','un');
    } 
    else {
      button.attr('src', '/kuestions/media/image/icon_star_off.png');
  	  button.attr('action','fo');
  	}

    //set button class (used to group all buttons related to one question)
    button.removeClass();
    button.addClass('follow' + questionId);

    //set click event
    button.unbind('click');
    button.click({'questionId': questionId},function(event){
        event.stopPropagation();
        manageFollowQuestion(event.data.questionId, $(this));
    });
  }
}

//parameters:
//button = img element (follow button) to manage
function manageFollowQuestion(questionId, button){
	csrf = $("#security_csrf input:first").val();
	data="questionId=" + questionId + '&csrfmiddlewaretoken=' 
			+ csrf+"&action="+button.attr('action');
	$.ajax({
	  url: '/question/manageFollowQuestion/',
	  type: "POST",
	  data: data,
	  dataType: "json",
	  success: function(data){
	    response=eval(data);
      //if question is followed
	    if(response.followed){
		    user_session.followedQuestions.push(questionId);
	    }
      //if question is not followed
	    else {
        //find the questionId and remove it
        var index = -1;
        for (var i = 0; i < user_session.followedQuestions.length; i++){
          if (user_session.followedQuestions[i] == questionId){
            index = i;
            break;
          }
        }
        if (index >= 0){
          user_session.followedQuestions.splice(index,1);
        } else{
          console.log('error: requested questionId not found in user_session.followedQuestions');
        }

        //if currently displayed question is unfollowed while viewing followed tab, hide question display
        if ( $('#followedTab').parent().attr('className').indexOf('selected') != -1 ) {
          if ( $('.question_display').attr('data-questionId') == questionId ){
            $('.question_display').hide();
          }
        }
	    }

      //change buttons appropriately
      $('.follow' + questionId).each(function(){
        questionId = $(this).attr('className').split('follow')[1];
        setFollowButton(questionId, $(this));
      });

      //if followed tab is selected
      if ( $('#followedTab').parent().attr('className').indexOf('selected') != -1) {
        //refresh followed list in question view
        displayFollowedQuestions();
        console.log('refreshed');
      }
	  }
	});
}

function userIsFollowingQuestion(questionId){
	if(user_session.isOpen){
		length=user_session.followedQuestions.length;
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
  //clear existing answer list
  $('.answer').each(function(){
    if ( $(this).attr('id') != 'answer_template' ){
      $(this).remove();
    }
  });

  //add answer list
  for (var i = 0; i < answers.length; i++){
    var answer = $('#answer_template').clone();
    answer.show();
    answer.attr('id', 'answer'+i);
    answer.find('.profile .picture').attr('src',"/user/picture/"+answers[i].poster);
    answer.find('.rate_info').text(answers[i].score);
    answer.find('.question_text').text(answers[i].content);
    answer.find('.info').html("<b>"+answers[i].poster+"</b> answered "+humane_date(answers[i].time));
    answer.find('.rate_up').click({'answerId': answers[i].id}, function(e){
      incAnswerScore(e.data.answerId);
    });
    answer.find('.rate_down').click({'answerId': answers[i].id}, function(e){
      decAnswerScore(e.data.answerId);
    });

    $('.answers_wrapper').append(answer);
  }
}

function postAnswer(answerText){
  var answer = $("#answerInput").val();
  
  // check if answer is empty
  if (answer == ""){
	displayMessage("an answer needs words","answerMessageContainer"); 
    return;
  }

  // obtain csrftoken needed to post data
  var csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/postAnswer/',
    type: "POST",
    dataType: "JSON",
    data: "answer=" + answer + '&questionId=' + $(".question_display").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
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
    data: "type=increment" + "&answerId=" + answerId + "&questionId=" + $(".question_display").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
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
    data: "type=decrement" + "&answerId=" + answerId + "&questionId=" + $(".question_display").attr("data-questionId") + '&csrfmiddlewaretoken=' + csrf,
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
	$("#message").removeClass("#hidden").slideToggle("fast");
}

function displayMessageCallback(data, textStatus, containerId) {
	displayMessage(textStatus.getResponseHeader("message"), containerId);
}

function displayMessagePop(messageContent){
	$(".popup  .message #message").remove();
	$("<h3>", {
		text : messageContent,
		id : "message",
		class : "pop_message hidden",
		click : function() {
			$(".popup  .message #message").remove();
		}
	}).appendTo($(".popup .message"));
	$('.popup .message #message').removeClass("#hidden").slideToggle('fast');
}

function displayMessageCallbackPop(data, textStatus, containerId) {
displayMessagePop(textStatus.getResponseHeader("message"));
}

function removeMessage(containerId) {
	$("#" + containerId ).empty();
	}



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
    autoHeight: false
  });
  
  $('ul.tabs').find('li').click(function(){
      $('ul.tabs li').attr("class","");
      $(this).attr("class","radiusT selected");
  });

  // tabs onclick
  $('#searchTab').click(function(){
    searchQuestions();
  });
  $('#followedTab').click(function(){
    displayFollowedQuestions();
  });
  $('#popularTab').click(function(){
    displayPopularQuestions();
  });
  $("#timelineLink").click(function () {
	  loadTimeline();
  });
  $("#recommendedTab").click(function () {
	  console.log("recommended");
	  displayRecommendedQuestions();
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
	});
}

function init() {
  $('.question_display').hide();
  $('#answer_template').hide();
	
  $('#searchBar').keyup(function(event) {
		searchQuestions();
	});
  $('#searchBar').click(function(event){
    searchQuestions();
  });
	// from the profile page, a new search redirect to the main page
	$('#searchBarProfile').keyup(function(event) {
		 if (event.keyCode == '13') {
      search = document.getElementById("searchBarProfile").value;
	    document.location.href = '/?search='+search; 
     }
	});
	$("#searchBar").focus();
	$('#message').click(function() {
		removeMessage('messageContainer');
	});
  $('#message').click(function(){
    $(this).slideToggle("fast");
	});
	
	setInterval(maintainHeightEqual, 1000);
}



function openFacebox(size){
  $('#facebox .content').css('width',size+'px'); return false;
}


function uploadImage(){
  alert('1');
  
  return false;
}






/** ******* Utils *************** */


/** ******* 1. Pretty Date *************** */
/*
 * Javascript Humane Dates
 * Copyright (c) 2008 Dean Landolt (deanlandolt.com)
 * Re-write by Zach Leatherman (zachleat.com)
 * 
 * Adopted from the John Resig's pretty.js
 * at http://ejohn.org/blog/javascript-pretty-date
 * and henrah's proposed modification 
 * at http://ejohn.org/blog/javascript-pretty-date/#comment-297458
 * 
 * Licensed under the MIT license.
 */

function humane_date(date_str){
	var time_formats = [
		[60, 'just now'],
		[90, '1 minute'], // 60*1.5
		[3600, 'minutes', 60], // 60*60, 60
		[5400, '1 hour'], // 60*60*1.5
		[86400, 'hours', 3600], // 60*60*24, 60*60
		[129600, '1 day'], // 60*60*24*1.5
		[604800, 'days', 86400], // 60*60*24*7, 60*60*24
		[907200, '1 week'], // 60*60*24*7*1.5
		[2628000, 'weeks', 604800], // 60*60*24*(365/12), 60*60*24*7
		[3942000, '1 month'], // 60*60*24*(365/12)*1.5
		[31536000, 'months', 2628000], // 60*60*24*365, 60*60*24*(365/12)
		[47304000, '1 year'], // 60*60*24*365*1.5
		[3153600000, 'years', 31536000], // 60*60*24*365*100, 60*60*24*365
		[4730400000, '1 century'], // 60*60*24*365*100*1.5
	];

	var time = ('' + date_str).replace(/-/g,"/").replace(/[TZ]/g," "),
		dt = new Date,
		seconds = ((dt - new Date(time) + (dt.getTimezoneOffset() * 60000)) / 1000),
		token = ' ago',
		i = 0,
		format;

	if (seconds < 0) {
		seconds = Math.abs(seconds);
		token = '';
	}

	while (format = time_formats[i++]) {
		if (seconds < format[0]) {
			if (format.length == 2) {
				return format[1] + (i > 1 ? token : ''); // Conditional so we don't return Just Now Ago
			} else {
				return Math.round(seconds / format[2]) + ' ' + format[1] + (i > 1 ? token : '');
			}
		}
	}

	// overflow for centuries
	if(seconds > 4730400000)
		return Math.round(seconds / 4730400000) + ' Centuries' + token;

	return date_str;
};


function maintainHeightEqual(){
  var lHeight=$(".contents .left").height();
  var rHeight=$(".contents .right").height();
  var max=lHeight;
  if(rHeight > lHeight){
    max=rHeight;
  }
}
