<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>ecAEPS</title>

        <script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

        <style type="text/css" title="currentStyle" media="screen">
            @import "${tg.url('/static/css/userprofile.css')}";
        </style>

        <script type="text/javascript">

            function userUpdate(field, value, type){
                var opt = {
                    method: 'post',
                    postBody: 'field='+escape(field)+'&amp;value='+escape(value)+'&amp;type='+escape(type),
                    on500: function(t) {
                        document.getElementById('message').innerHTML = field + ' "' + value + '" already exists!';
                        new Effect.Appear('message');
                    }
                }			
                new Effect.Highlight(field);
                new Ajax.Request('userUpdate', opt);
            }

            function programUpdate(name, value)
            {
                new Effect.Highlight(name);
                new Ajax.Request('programUpdate', {method:'post', postBody:'value='+escape(value)});
            }

            function groupUpdate(name, value)
            {
                new Effect.Highlight(name);
                new Ajax.Request('groupUpdate', {method:'post', postBody:'name='+escape(name)+'&amp;value='+escape(value)});
            }

            function changeUser()
            {
                window.location="${tg.url('/userprofile/changeUser')}"
            }

            var DUR = 0.1;

            function changePassword()
            {
                document.getElementById('failure').innerHTML = "";
                Effect.Fade('change',
                {duration: DUR, afterFinish: function (){
                        new Effect.Appear('passwordbox', {duration: DUR});	
                }});
            }

            function cancelChange()
            {
                Effect.Fade('passwordbox',
                {duration: DUR, afterFinish: function (){
                        new Effect.Appear('change', {duration: DUR});	
                }});
            }

            function submitChange()
            {
                var old = document.getElementById('old').value
                var _new = document.getElementById('new').value
                var retype = document.getElementById('retype').value
                new Ajax.Request('changePassword', 
                {
                    method:'post',
                    postBody:'old='+escape(old)+'&amp;new='+escape(_new)+'&amp;retype='+escape(retype), 
                    onFailure: function (r)
                    {
                        document.getElementById('failure').innerHTML=r.responseText;
                        new Effect.Highlight('failure')
                    },
                    onSuccess: function (r)
                    {
                        document.getElementById('success').innerHTML=r.responseText;
                        document.getElementById('failure').innerHTML="";
                        document.getElementById('old').value = "";
                        document.getElementById('new').value = "";
                        document.getElementById('retype').value = "";
                        new Effect.Highlight('success')
                        Effect.Fade('passwordbox',
                        {
                            duration: DUR,
                            afterFinish: function (){
                                new Effect.Appear('change', {duration: DUR});	
                            }
                        }
                        );
                    }
                });
            }

        </script>

    </head>
    <body>	
        <div id="user_profile">
            <h2>User profile</h2>
            <input py:if="'global_admin' in tg.identity.groups" type="button" value="Log in as this user" onclick="changeUser()" />
            

            <table>
                <tr>
                    <td class="label">
            <label for="lname">Last</label>
        </td>
        <td>
            <input id="lname" name="lname" type="text" value="${user.lname}" onchange="userUpdate(this.name, this.value, 'string')" />
        </td>
    </tr>
    <tr>
        <td class="label">
            <label for="fname">First</label>
        </td>
        <td>
            <input id="fname" name="fname" type="text" value="${user.fname}" onchange="userUpdate(this.name, this.value, 'string')" />
        </td>
    </tr>
    <tr>
        <td class="label">

            

            <label for="email_address">Email</label>
        </td>
        <td>
            <input id="email_address" name="email_address" type="text" value="${user.email_address}" onchange="userUpdate(this.name, this.value, 'string')" />

        </td>
    </tr>
    <tr>
        <td class="label">
            <label for="phone">Phone</label>
        </td>
        <td>
            <input id="phone" name="phone" type="text" value="${user.phone}" onchange="userUpdate(this.name, this.value, 'string')" />
        </td>
    </tr>
    <tr>
        <td class="label">

            

            <label for="user_name">Username</label>
        </td>
        <td>
            <input id="user_name" name="user_name" type="text" value="${user.user_name}" onchange="userUpdate(this.name, this.value, 'string')" />
        </td>
    </tr>
</table>
          
            <input id="change" type="button" value="Change password" onclick="changePassword()"/>
						<div id="success"></div>
            <table id="passwordbox" style="display: none;">
                    <tr>
											<td class="label">
												<label for="old">Old password</label>
                    	</td>
											<td>
												<input id="old" name="old" type="password" />
                    	</td>
										</tr>
										<tr>
											<td class="label">
                    		<label for="new">New password</label>
                    	</td>
											<td>
												<input id="new" name="new" type="password" />
											</td>
										</tr>
                    <tr>
											<td class="label">
                    		<label for="retype">Retype</label>
                    	</td>
											<td>
												<input id="retype" name="retype" type="password" />
                    	</td>
										</tr>
										<tr>
                    	<td colspan="2" id="failure">
                     	</td>
										</tr>
										<tr>
											<td colspan="2">
                    		<input type="button" value="Change" onclick="submitChange()" />
                    		<input type="button" value="Cancel" onclick="cancelChange()" />
											</td>
										</tr>
            </table>
						
						<table>
            <tr py:if="'global_admin' in tg.identity.groups">
            	<td class="label">
								<label for="program">Program</label>
              </td>
							<td>
  							<select id="program" name="program" onchange="programUpdate(this.name, this.value)">
                    <option py:for="p in programlist" py:attrs="curProg(p.id)" value="${p.id}">${p.name}</option>
                </select>
                (Required)
							</td>
            </tr>
            <tr py:if="'global_admin' not in tg.identity.groups">
            	<td class="label">
								<label for="program">Program</label>
              </td>
							<td>
  							<label class="disabledProgram">${user.program.name}</label>
            	</td>
						</tr>
						</table>

            <div py:if="'admin' in tg.identity.groups or 'global_admin' in tg.identity.groups">
                <input id="admin" name="admin" type="checkbox" value="admin" py:attrs="curGroup('admin')" onchange="groupUpdate(this.name, this.checked)" />
                <label for="admin">Program Administrator</label>
            </div>

            <div py:if="'global_admin' in tg.identity.groups">
                <input id="global_admin" name="global_admin" type="checkbox" value="global_admin" py:attrs="curGroup('global_admin')" onchange="groupUpdate(this.name, this.checked)" />
                <label for="global_admin">Global Administrator</label>
            </div>

            <div id="man_users" py:if="'admin' in tg.identity.groups or 'global_admin' in tg.identity.groups">
                <input type="button" value="Manage users" onclick="window.location='${tg.url('/userlist')}'" />
            </div>
        </div>

    </body>
</html>
