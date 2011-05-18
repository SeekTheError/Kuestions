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
    dataType: "json",
		success : function(data, textStatus, jhxqr) {
      $.facebox.close();
      displayMessage(jhxqr.getResponseHeader("message"),"messageContainer");

      questionId = jhxqr.getResponseHeader("questionId");

      //add question to followed list
      user_session.followedQuestions.push( questionId );

      //display posted question
      viewQuestion( questionId );
		}
	});
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
        if (data.rows.length > 0){
          displayQuestionList(data.rows, 'search');
        } else{
          $('#questionList_search').html('<h2>No results!</h2>');
        }
      }
    });
	} else {
    $('#questionList_search').html('<h2>Please enter a question or a search term</h2>');
	}
}

function searchQuestionsHasTopic(search) {
	if(search==null){
		search = document.getElementById("searchBar").value;
	}

	if (search != "") {
		search=enhanceSearch(search);
    var url = '/api/_fti/_design/question/by_topics?';
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
        $('#questionList_followed').html('<h2>No followed questions...yet!</h2>');
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
      $('#questionList_recommended').html('<h2>For question recommendations, please update your topics of interest on your profile page!</h2>');
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

          // filter out questions that belong to the current user... we don't
			// want to recommend their own question to them!
          var filteredList = [];
          for (i = 0; i < questions.length; i++){
            if (questions[i].fields.asker != user_session.login){
              filteredList.push(questions[i]);
            }
          }
	        displayQuestionList(filteredList, 'recommended');
	      } else{
          $('#questionList_recommended').html('<h2>For question recommendations, please enter more topics of interest on your profile page!</h2>');
	      }
	    }
	  });
	}

function displayPopularQuestions(){
  $.ajax({
    url: '/api/_design/question/_view/popular?descending=true&limit=15',
    dataType: "JSON",
    success: function(data){
      displayQuestionList(data.rows, 'popular');
    }
  });
}

// display questions that are asked by a particular user
function displayUserQuestions(userLogin){
  console.log(userLogin);
  $.ajax({
    url: '/api/_design/question/_view/asker?key="'+ userLogin +'"&limit=15&descending=true',
    dataType: "JSON",
    success: function(data){
      if (data.rows.length > 0){
        displayQuestionList(data.rows, 'user');
      } else{
        $('#questionList_user').html('<h3>This user has not asked any questions!</h3>');
      }
    }
  });
}

// displayQuestionList: accepts json list of questions, displays them as list on
// left side of the page
// filterType = (search/timeline/followed/popular/recommended/user)
function displayQuestionList(questionList, filterType){
  cleanQuestionList();

  // determine container to display questions
  var containerId = '#questionList_' + filterType;
  // generate styled question list
  for (var i = 0; i < questionList.length; i++){
    // create html
	  
    $(containerId).append('<div id="questionList'+i+'" class="speech_wrapper"> <div class="profile question"><a id="userLink'+i+'"><img id="questionProfileImg' + i +'" /></div> <div class="speech"></a><div class="question"> <p class="bubble"></p> <p class="question_text" id="questionTitle'+i+'"></p> </div><div class="info"> <span id="askerAndPostDate'+i+'"></span> </div> <div class="actions"> <span class="follow"><a href="#"><img id="followButton' + i +'" src="/kuestions/media/image/icon_star_off.png" title="follow" /></a></span> </div> </div> </div>');

    // fill in data:
    question = questionList[i];
    questionId = "";
    title = "";
    asker = "";
    postDate = "";
    // access data differently based on filter
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

    // asker and post date
    postDate = humane_date(postDate);
    $(containerId + ' #askerAndPostDate' + i).html('<a href="/user/'+asker+'"><b>'+asker+'</b></a> posted ' + postDate);

    // edit question profile img
    $('#questionProfileImg' + i).attr('src', '/user/picture/' + asker);
    $('#userLink' + i).attr('href', '/user/' + asker);
    
    // question title
    var titleContainer =  $(containerId + ' #questionTitle' + i);
    titleContainer.text(title);
    if (filterType == 'search'){
      //searchword highlighting
      searchWords = $('#searchBar').val().split(" ");
      searchWords = $.grep(searchWords, function(n, i){
        return n != "";
      });
      for (var j = 0; j < searchWords.length; j++){
        titleContainer.highlight(searchWords[j]);
      }
    }

    // click handler for question detail view
    $('#questionList'+i).click( {'questionId': questionId }, function(event){
      viewQuestion(event.data.questionId);
    });

    // set up follow button
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
          if (data.length > 0){
            displayTimeline(data);   
          } else {
            $('#questionList_timeline').html('<h2>No new events! Perhaps you should follow more questions</h2>');
          }
		    }});
	
}

function displayTimeline(data){
	timeline=eval(data);
	console.log(timeline);
	$("#questionList_timeline").append('<ul id="timelineList"></ul>');
	for(i=0;i<timeline.length;i++){
    id=timeline[i]._id.replace(".","");
    questionId=timeline[i].question;
    
	  var li = $('<li>',{
	      id: id
	    }).appendTo($("#timelineList"));
	  $("#questionList_timeline #"+id).click({'questionId': questionId},function(event){
	   viewQuestion(event.data.questionId);
	  });
	  
	  date = humane_date(timeline[i].eventDate);
	  var a= $('<a>',{
		  href:'/user/'+timeline[i].user,
		  text :timeline[i].user 
	  }).appendTo($("#timelineList #"+id));;
	  var a= $('<span>',{
		  text :'  post an answer'
	  }).appendTo($("#timelineList #"+id));;
	  var p= $('<span>',{
		  text: date +" " +timeline[i].questionTitle+" "
	  }).appendTo($("#timelineList #"+id));
	  
	    
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
var lastAnswerCount;
var answerDaemon;
function viewQuestion(questionId){
	csrf = $("#security_csrf input:first").val();
  $.ajax({
    url: '/question/view/',
    type: 'GET',
    data: 'questionId='+questionId,
    dataType: "json",
    success: function(data){
      console.log(data);
      // embed question id into question display div
      $('.question_display').attr('data-questionId', data.id);
      $('.question_display').show();

      // populate question detail display
      $('#question_profile_img').attr('src', '/user/picture/' + data.asker);
      $('.question_info .profile a').attr('href','/user/'+data.asker);
      $('.question_title').html(data.title);
      $('.questionAsker').text(data.asker);
      $('.questionAsker').attr('href','/user/'+data.asker);
      $('.detail_contents').text(data.description);

         // set follow button
      setFollowButton(data.id, $('#followButton'));
      if(data.topics.length == 0){
        $('.detail_topics').hide();
      }else{
        $('.detail_topics').show();
        $('.detail_topics .topic ul').text(" ");
        for (var i = 0; i < data.topics.length; i++){
          topic=data.topics[i];
          topicHTML='<li class="topic_item False"><a href="/?search='+topic+'&topic=1"><b>'+topic+'</b></a></li>';
          $('.detail_topics .topic ul').append(topicHTML);
        }
      }

      //view answers
      viewAnswers(data.answers);
      
      //initialize answer update checker daemon
      $(".newAnswerAlert").text("");
      lastAnswerCount=data.answers.length;
      if (!answerDaemon){
        answerDaemon = runAnswerDaemon();
      }

      //clear answer input
      $("#answerInput").val("");
    }
  });
}

function runAnswerDaemon(){
  console.log("check for new answers");
  $.ajax({
      url: '/question/view/',
      type: 'GET',
      data: 'questionId='+$('.question_display').attr('data-questionId')+"&auto",
      dataType: "json",
      success: function(data){
        answers = data.answers;
        if(lastAnswerCount < answers.length){
          diff = answers.length-lastAnswerCount;
          (diff == 1) ? $(".newAnswerAlert").text(diff+ " new answer") : $(".newAnswerAlert").text(diff+ " new answers");	
        }
     }
  });	

  //keep running answer daemon once it's started
  return setTimeout("runAnswerDaemon()",2000);
}

function hideQuestionDetail(){
  $("#questionDetail").addClass("hidden");
}

function setFollowButton(questionId, button){
	if(user_session.isOpen ){
    // change image depending on whether user is following
    if(userIsFollowingQuestion(questionId)){
      button.attr('src', '/kuestions/media/image/icon_star_on.png');
      button.attr('action','un');
    } 
    else {
      button.attr('src', '/kuestions/media/image/icon_star_off.png');
  	  button.attr('action','fo');
  	}

    // set button class (used to group all buttons related to one question)
    button.removeClass();
    button.addClass('follow' + questionId);

    // set click event
    button.unbind('click');
    button.click({'questionId': questionId},function(event){
        event.stopPropagation();
        manageFollowQuestion(event.data.questionId, $(this));
    });
  }
}

// parameters:
// button = img element (follow button) to manage
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
      // if question is followed
	    if(response.followed){
		    user_session.followedQuestions.push(questionId);
	    }
      // if question is not followed
	    else {
        // find the questionId and remove it
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

        // if currently displayed question is unfollowed while viewing followed
		// tab, hide question display
        if ( $('#followedTab').parent().attr('className').indexOf('selected') != -1 ) {
          if ( $('.question_display').attr('data-questionId') == questionId ){
            $('.question_display').hide();
          }
        }
	    }

      // change buttons appropriately
      $('.follow' + questionId).each(function(){
        questionId = $(this).attr('className').split('follow')[1];
        setFollowButton(questionId, $(this));
      });

      // if followed tab is selected
      if ( $('#followedTab').parent().attr('className').indexOf('selected') != -1) {
        // refresh followed list in question view
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
  // clear existing answer list
  $('.answer').each(function(){
    if ( $(this).attr('id') != 'answer_template' ){
      $(this).remove();
    }
  });

  //if answers list is empty, hide answers header
  if (answers.length == 0){
    $('#answers_header').hide();
  } else{
    $('#answers_header').show();
  }

  //sort answers by rank
  answers = answers.sort(function(answer1, answer2){
    return answer2.score - answer1.score;
  });

  //add answer list
  for (var i = 0; i < answers.length; i++){
    var answer = $('#answer_template').clone();
    answer.show();
    answer.attr('id', 'answer'+i);
    answer.find('.profile .userLink').attr('href',"/user/"+answers[i].poster);
    answer.find('.profile .picture').attr('src',"/user/picture/"+answers[i].poster);
    answer.find('.rate_info').text(answers[i].score);
    answer.find('.question_text').text(answers[i].content);
    answer.find('.info').html('<a href="/user/'+answers[i].poster+'"><b>'+answers[i].poster+"</b></a> answered "+humane_date(answers[i].time));
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
      
      //increment answer count
      lastAnswerCount=lastAnswerCount+1;

      //redisplay answer list
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
  $('body').click({'containerId': containerId}, function(event){
    removeMessage(event.data.containerId);
    $(this).unbind('click');
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
  $('#askQuestionButton').click(function(){
    $.facebox({div: '#question_dialog'});
    $('.popup #questionTitleInput').val( $('#searchBar').val() );
    loadQuestionTags( $('.popup #questionTitleInput').val() );
  });


	// Display a search comming from the profile page
  vars=getUrlVars();
	if(vars["search"]){
		search=vars["search"];
		$('#searchBar').attr('value',decodeURIComponent(search));
		if(vars["topic"] && vars["topic"] == '1'){
		  searchQuestionsHasTopic(vars["search"]);
		}
		else{
		  searchQuestions(vars["search"]);		
	  }
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
  
  if(vars["show"]){
	  if(vars["show"] == 'ask'){
	    $(".ask_wrapper a").click();
      var left=parseInt($("#facebox").css('left'));
      $("#facebox").css('left',(left-215)+'px');
	  }
	}
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
	
	
	var size=$(window).height()-140;
	$(".right").css('max-height',size+'px');
	$(window).resize(function(){
	 var size=$(window).height()-140;
	 $(".right").css('max-height',size+'px');
	});

$('.newAnswerAlert').click(
    function () {
      $('.newAnswerAlert').text("");
      viewQuestion($('.question_display').attr('data-questionId'));
    }
  );
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
 * JavaScript Pretty Date Copyright (c) 2008 John Resig (jquery.com) Licensed
 * under the MIT license.
 */

// Takes an ISO time and returns a string representing how
// long ago the date represents.
function humane_date(time){
	var date = new Date((time || "").replace(/-/g,"/").replace(/[TZ]/g," ")),
		diff = (((new Date()).getTime() - date.getTime()) / 1000),
		day_diff = Math.floor(diff / 86400);
			
	if ( isNaN(day_diff) || day_diff < 0 || day_diff >= 31 )
		return;
			
	return day_diff == 0 && (
			diff < 60 && "just now" ||
			diff < 120 && "1 minute ago" ||
			diff < 3600 && Math.floor( diff / 60 ) + " minutes ago" ||
			diff < 7200 && "1 hour ago" ||
			diff < 86400 && Math.floor( diff / 3600 ) + " hours ago") ||
		day_diff == 1 && "Yesterday" ||
		day_diff < 7 && day_diff + " days ago" ||
		day_diff < 31 && Math.ceil( day_diff / 7 ) + " weeks ago";
}

// If jQuery is included in the page, adds a jQuery plugin to handle it as well
if ( typeof jQuery != "undefined" )
	jQuery.fn.prettyDate = function(){
		return this.each(function(){
			var date = humane_date(this.title);
			if ( date )
				jQuery(this).text( date );
		});
	};
