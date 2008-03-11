<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

    <head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
        <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
        <title py:replace="''">Your title goes here</title>
        <meta py:replace="item[:]"/>
        <style type="text/css">
            #pageLogin
            {
                font-size: 10px;
                font-family: verdana;
                text-align: right;
            }
        </style>
        <style type="text/css" media="all">
            @import "${tg.url('/static/css/master.css')}";
        </style>
    </head>

    <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

        <div class="header">
            <div class="noprint" py:if="tg.config('identity.on') and not defined('logging_in')" id="pageLogin">
                <span py:if="tg.identity.anonymous">
                    <a href="${tg.url('/login')}">Login</a>
                </span>
                <span py:if="not tg.identity.anonymous">
                    ${tg.identity.user.firstlast()}, ${tg.identity.user.program.name} |
                    <a href="${tg.url('/logout')}">Logout</a>
                </span>
            </div>
            <h1 class="noprint">ec<span id="aeps">AEPS</span></h1>
        </div>
        <div class="menu" py:if="tg.config('identity.on') and not defined('logging_in')"><div class="noprint"><a href="${tg.url('/userprofile')}">User profile</a> <a href="${tg.url('/')}">Child list</a> <a href="${tg.url('/search')}">Search</a> <a href="${tg.url('/unimplemented')}">Reports</a> <a py:if="not tg.identity.user.basketmode" href="${tg.url('/bmode')}">Assessment mode: A</a><a py:if="tg.identity.user.basketmode" href="${tg.url('/amode')}">Assessment mode: B</a></div></div>
        <div class="content">
                <div id="status_block" class="flash" py:if="value_of('tg_flash', None)" py:content="tg_flash"></div>

                <div py:replace="[item.text]+item[:]"/>
                    <!-- End of main_content -->
                </div>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-3491345-1");
pageTracker._initData();
pageTracker._trackPageview();
</script>
        </body>

    </html>
