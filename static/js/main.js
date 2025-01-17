$('#notif').click(function() {
    $.ajax({
        method:'post',
        url:'/request/getReplies',
        data:{},
        success:function(data){$('#notif-panel').html(data);}
    });
});

// fade in and fade out for response flash
$(".flash").hide().slideDown(500).delay(20000).fadeOut(500);
// Search results
function search(search_term){
    if ($.trim(search_term)!=''){
        $.ajax({
            method:'post',
            url:'/request/search',
            data:{'search_term':search_term},
            success:function(data){$('#coin-search-menu').html(data);}
        });
    }
};
$(function(){
    $('#coin-search-form').focusin(function(){$('#coin-search-menu').show();});
    $('#coin-search-form').focusout(function(){window.setTimeout(function(){$('#coin-search-menu').hide();}, 100);});
    $('#coin-search-form').keyup(function(){var search_term=$('#coin-search-form').val();search(search_term);});
    $('#coin-search-form').keypress(function(event){if(event.which==13){var url = $('#coin-search-menu').find('.first-result').attr('href');window.event.returnValue = false;document.location.href = url;}});
    htmlString = '<a class="dropdown-item active first-result" href="/coin/bitcoin"><img src="/static/_0.0.0/image_thumb/master.image_thumb.a5da6685a1e7c51c.626974636f696e2e706e67.png">  Bitcoin (BTC)</a><a class="dropdown-item" href="/coin/ethereum"><img src="/static/_0.0.0/image_thumb/master.image_thumb.8d54ce07ae6d9538.657468657265756d2e706e67.png">  Ethereum (ETH)</a><a class="dropdown-item" href="/coin/ripple"><img src="/static/_0.0.0/image_thumb/master.image_thumb.a2dda5226826605b.726970706c652e706e67.png">  XRP (XRP)</a><a class="dropdown-item" href="/coin/eos"><img src="/static/_0.0.0/image_thumb/master.image_thumb.b6c3e1e5f39b0cbd.656f732e706e67.png">  EOS (EOS)</a><a class="dropdown-item" href="/coin/litecoin"><img src="/static/_0.0.0/image_thumb/master.image_thumb.a61e9aea0f05909d.6c697465636f696e2e706e67.png">  Litecoin (LTC)</a><a class="dropdown-item" href="/coin/bitcoin-cash"><img src="/static/_0.0.0/image_thumb/master.image_thumb.81f6ab8263c952ce.626974636f696e2d636173682e706e67.png">  Bitcoin Cash (BCH)</a><a class="dropdown-item" href="/coin/binancecoin"><img src="/static/_0.0.0/image_thumb/master.image_thumb.9838637debc27791.62696e616e6365636f696e2e706e67.png">  Binance Coin (BNB)</a><a class="dropdown-item" href="/coin/stellar"><img src="/static/_0.0.0/image_thumb/master.image_thumb.bcb7c11581304385.7374656c6c61722e706e67.png">  Stellar (XLM)</a><a class="dropdown-item" href="/coin/tether"><img src="/static/_0.0.0/image_thumb/master.image_thumb.b5015abefe479ece.7465746865722e706e67.png">  Tether (USDT)</a><a class="dropdown-item" href="/coin/cardano"><img src="/static/_0.0.0/image_thumb/master.image_thumb.bd8870cac16366f4.63617264616e6f2e706e67.png">  Cardano (ADA)</a><a class="dropdown-item" href="/coin/tron"><img src="/static/_0.0.0/image_thumb/master.image_thumb.8f21f6ddb2fda2b8.74726f6e2e706e67.png">  TRON (TRX)</a><a class="dropdown-item" href="/coin/bitcoin-cash-sv"><img src="/static/_0.0.0/image_thumb/master.image_thumb.9ab1e21e60f035da.626974636f696e2d636173682d73762e706e67.png">  Bitcoin SV (BSV)</a></div>';
    $('#coin-search-menu').html(htmlString);
});

// Check if username exists
function checkUsername(){
    var username = $('.registerUsername').val();
    if (username.length > 3){
        var re = /^\w+$/;
        if (re.test(username)) {
            $.ajax({
                method:'post',
                url:'/request/check_username',
                data:{'username':username},
                success:function(data){
                    if (data=='taken'){
                        $('.registerUsernameMessage').html('<span style="color:red;">Username has been taken</span>').attr("accept","false");
                    } else if (data=='available') {
                        $('.registerUsernameMessage').html('<span style="color:green;">Username is available!</span>').attr("accept","true");
                    } else {
                        $('.registerUsernameMessage').html('').attr("accept","true");
                    };
                }
            });
        } else {
            $('.registerUsernameMessage').html("<span style='color:red;'>Only use letters, numbers and '_'</span>").attr("accept","false");
        }
    } else {
        $('.registerUsernameMessage').html('<span style="color:red;">Username needs to be at least 4 characters</span>').attr("accept","false");
    }
};
$(function(){
    $('.registerUsername').keyup(function(){checkUsername();});
});

// Check if email address exists
function checkEmail(email){
    $.ajax({
        method:'post',
        url:'/request/check_email',
        data:{'email':email},
        success:function(data){$('.registerEmailMessage').html(data);}
    });
};

// Check if email is valid
function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}
function validate() {
    var email = $(".registerEmail").val();
    if (validateEmail(email)) {
        checkEmail(email);
    } else {
        $(".registerEmailMessage").html("<span style='color:red;'>Invalid email</span>");
    }
    return false;
}
$(function(){
    $('.registerEmail').keyup(function(){validate();});
});
