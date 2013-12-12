// get csrf
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




$(document).ready(function(){

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // active
    var cateactive = null,
        siteactive = null,
        baseurl = window.location.href;
        activeurl = [baseurl.split('/')[0],baseurl.split('/')[1],baseurl.split('/')[2]].join('/') 


    if(baseurl.indexOf('site')>=0){
        siteactive = baseurl.split('=')[1]
        $('#'+siteactive).addClass('active')
    }
    if(baseurl.split('/').length>4){
        cateactive = baseurl.split('/')[3]
        $('#'+cateactive).addClass('active')
    }


    // site filter
    $('#chinaluxus').click(function(){
        $('#siteswitch').val('chinaluxus');
    });
    $('#527motor').click(function(){
        $('#siteswitch').val('527motor');
    });
    $('#autohome').click(function(){
        $('#siteswitch').val('autohome');
    });
    $('#neeu').click(function(){
        $('#siteswitch').val('neeu');
    });


    // login and register
    $('form#loginform').submit(function() {
        var data = null;
            username = $('form#loginform input[name="username"]').val();
            password = $('form#loginform input[name="password"]').val();
            csrftoken = getCookie('csrftoken');
            status = null;

        data = {
            'username':username,
            'password':password
        };

        // console.log('username',username,'password',password,'csrftoken',csrftoken,activeurl+"login/")

        $.post(activeurl+"/account/login/",data,function(json){
            // returndata = eval("("+json+")"); 
            status = json['status']
            if(status=='already'){
                // console.log(json)
                $('ul.nav.navbar-nav.navbar-right').eq(0).replaceWith(
                        '<ul class="nav navbar-nav navbar-right"><li><a href="/account/logout/">'+json['username']+'</a></li></ul>'
                    )
                $('div#login button[data-dismiss="modal"]').eq(0).click();
            }else if(status=='not exist'){
                // console.log(json)
                $('form#loginform span').eq(0).replaceWith(
                        '<span class="label label-warning">邮箱或密码错误，请重新输入</span>'
                    )

            }else if(status=='type worong'){
                // console.log(json)
                $('form#loginform span').eq(0).replaceWith(
                        '<span class="label label-warning">邮箱或密码格式不正确，请重新输入</span>'
                    )
            }else{
                // console.log(json)
            }
            

        })
        // window.location.reload()
        
        return false;
    });

    $('form#regform').submit(function() {
        var data = null;
            username = $('form#regform input[name="username"]').val();
            screen_name = $('form#regform input[name="screen_name"]').val();
            password = $('form#regform input[name="password"]').val();
            csrftoken = getCookie('csrftoken');
            status = null;

        data = {
            'screen_name':screen_name,
            'username':username,
            'password':password
        };

        // console.log('username',username,'password',password,'csrftoken',csrftoken,activeurl+"login/")

        $.post(activeurl+"/account/regist/",data,function(json){
            // returndata = eval("("+json+")"); 
            status = json['status']
            if(status=='success'){
                console.log(json)
                $('div#reg button[data-dismiss="modal"]').eq(0).click();
                $('ul.navbar-right a[data-target="#login"]').eq(0).click();

            }else if(status=='already exist'){
                console.log(json)
                $('form#regform span').eq(0).replaceWith(
                        '<span class="label label-warning">该用户已存在，请重新输入用户名密码</span>'
                    )

            }else if(status=='type worong'){
                console.log(json)
                $('form#regform span').eq(0).replaceWith(
                        '<span class="label label-warning">昵称、邮箱或密码格式不正确，请重新输入</span>'
                    )
            }else{
                console.log(json)
            }
            

        })
        // window.location.reload()
        
        return false;
    });


    bindPostCommentHandler();
});

// ajax
function bindPostCommentHandler() {
    var loadtime = 0,
        num = 10,
        category = null,
        query = null,
        site = null,
        data = null;
    $(window).scroll(function() {
        var h0 = $(window).scrollTop(),
            h2 = $(window).height(),
            h3 = $(document).height(),
            h4 = $('div.span12 p.text-center a').height() + 400,
            url = window.location.href;
            base_url = [url.split('/')[0],url.split('/')[1],url.split('/')[2],'v1','list'].join('/') 

        if(url.split('/').length>4){
            category = url.split('/')[3]
        }
        if(url.indexOf('query')>=0){
            query = url.split('=')[1]
        }
        if(url.indexOf('site')>=0){
            site = url.split('=')[1]
        }
        data = {
            nums:num,
            query:query,
            category:category,
            site:site
        };
        if(h0+h2>=h3-h4){
            loadtime=0;
        }

        if(h0+h2>=h3-h4&&loadtime==0){
            $.get(base_url,data,function(html){
                        $('div.col-sm-9 ul.main-list').eq(0).append(html)
                    }

            ).fail(function(){
                        console.log('i,m wrong')
                    })
            loadtime=loadtime+1;
            num = num + 10;
        }
    });
}


// django send
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



