// Adjust textarea height based on content
function textAreaAdjust(o) {o.style.height="1px";o.style.height=(22+o.scrollHeight)+"px";}

function InsertComment() {
    var body = $('#body').val();
    $.ajax({
        method:'post',
        url:'/request/upload',
        data:{'body':body},
        success:function(data){setTimeout(window.location.reload(), 500);} // refresh page after 0.5 seconds
    });
};

if (loggedin == true) {
    $('#my-submit').click(function() {
        if ($('#body').val().length < 5) {
            alert('Please enter a minimum of 4 characters')
        } else {
            InsertComment();
        };
    });
};

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}



function like(t){
    if (loggedin==false){return;}
    var id = $(t).attr('id'); // retrieves data-id
    var like_count = parseInt($(t).find('#score').text(), 10);
    if (isNaN(like_count)){like_count = 0};
    if ($(t).hasClass("voted")) {
        $(t).removeClass('voted');
        if (like_count > 1) {$(t).find('#score').html(String(like_count-1));} else {$(t).find('#score').html('');};
        $.ajax({
            method:'post',
            url:'/request/comment_like',
            data:{'id':id},
            success: function(data){}
        });
    } else {
        $(t).addClass('voted');
        $(t).find('#score').html(String(like_count+1));
        // Update dislike button if user has voted dislike previously
        if($(t).parent().find('.dislike').hasClass("voted")){
            $(t).parent().find('.dislike').removeClass('voted');
            var dislike_score = $(t).parent().find('.dislike').find('#score');
            var dislike_count = parseInt(dislike_score.text(),10);
            if (dislike_count > 1) {dislike_score.html(String(dislike_count-1));} else {dislike_score.html('');};
        };
        $.ajax({
            method:'post',
            url:'/request/comment_like',
            data:{'id':id},
            success: function(data){}
        });
    };
}
$(".like").click(function(){like(this);});

function confirm_delete(t){
    var id = $(t).closest('div').attr('id'); //this retrieves data-id
    $.ajax({
        method:'post',
        url:'/request/delete',
        data:{'id':id},
        success: function(data){
            $(".alert_placeholder").html(data);
            setTimeout(window.location.reload(), 500);
        }
    });
};
$(".confirm-delete").click(function(){confirm_delete(this);});

function change_deleteModal_id(t){
    var id = $(t).closest('div').attr('id'); //this retrieves data-id
    $(".deleteModal").attr("id",id);
};
$(".delete").click(function(){change_deleteModal_id(this);});
