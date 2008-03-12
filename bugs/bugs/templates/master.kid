<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="sitetemplate">
    <head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
        <script type="text/javascript" src="http://yui.yahooapis.com/2.5.0/build/yuiloader/yuiloader-beta-min.js" />
        <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.0/build/reset-fonts-grids/reset-fonts-grids.css" /> 
        <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.5.0/build/base/base-min.css" /> 
        <script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript" />
        <script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript" />
        <script src="${tg.url('/static/javascript/modalbox.js')}" type="text/javascript" />
        <link rel="stylesheet" href="${tg.url('/static/css/modalbox.css')}" type="text/css" media="screen" />
        <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
        <title py:replace="''">Your title goes here</title>
        <meta py:replace="item[:]" name="description" content="master template"/>
        <link rel="stylesheet" type="text/css" media="screen" href="../static/css/style.css"
            py:attrs="href=tg.url('/static/css/style.css')"/>
        <script src="${tg.url('/static/javascript/bugsJs.js')}" type="text/javascript" />
        <script type="text/javascript">
            function dispose_flash(){
                Effect.SwitchOff('status_block');
            }
            function loginSuccess(transport){
                
            }
            function loginFailure(transport){
                //Note: This should actually do registration instead
                var tr = Builder.node("span", {id:'loginError'}, "An authentication error occurred!");
                $('loginTable').descendants()[2].insert(Builder.node("br"), {position: 'after'});
                $('loginTable').descendants()[2].insert(tr, {position: 'after'});
            }
            function doLogin(){
                new Ajax.Request("${tg.url('/ajaxLogin')}", {
                    method: "post",
                    onSuccess: loginSuccess,
                    onFailure: loginFailure,
                    parameters: {
                        user_name: $("user_name").value,
                        password: $("password").value,
                        login:"login"
                    }
                });
            }
        </script>
    </head>
    <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
        <div id="doc3" class="yui-t6">
            <div id="hd"><h1>[Logo]: ${page_title()}</h1></div>
            <div id="bd">
                <div id="yui-main">
                    <div class="yui-b">
                        <div class="yui-g">
                            <div id="status_block" class="flash" py:if="value_of('tg_flash', None)" onclick="dispose_flash()"><div><span py:replace="tg_flash"></span><br/><span class="directions">[click to remove]</span></div></div>
                            <div py:replace="[item.text]+item[:]">page content</div>
                        </div>
                    </div>
                </div>
                <div class="yui-b" py:if="tg.config('identity.on') and not defined('logging_in')" id="pageLogin">
                    <span py:if="tg.identity.anonymous">
                        <table id="loginTable">
                            <tr><th colspan="2">Login or Register</th></tr>
                            <tr><td><label for="user_name">User Name:</label></td><td><input type="text" id="user_name" name="user_name"/></td></tr>
                            <tr><td><label for="password">Password:</label></td><td><input type="password" id="password" name="password"/></td></tr>
                            <tr><td colspan="2"><button type="button" onclick="doLogin();">Login/Register</button></td></tr>
                        </table>
                    </span>
                    <span py:if="not tg.identity.anonymous">
                        Welcome ${tg.identity.user.display_name or tg.identity.user.user_name}.
                        <a href="${tg.url('/logout')}">Logout</a>
                    </span>
                </div>
            </div>
            <div id="ft">Powered by <a href="http://swsnider.com/projects/bugs">Bugs</a>.</div>
        </div>
    </body>
</html>
