<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>ecAEPS</title>

<script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
<script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

<style type="text/css" title="currentStyle" media="screen">
		@import "${tg.url('/static/css/createuser.css')}";
</style>

</head>
<body>
	<div id="create_user">
		<h2>Create User</h2>
		
		<form id="f" action="validateUser" method="post">
			${message}
			<table>
				<tr>
					<td>
						<label for="username">Username</label>
					</td>
					<td>
						<input id="username" name="username" type="text" />
						Usually name in email address, like 'jdoe' or 'jane_doe'.
					</td>
				</tr>
				<tr>
					<td>
						<label for="password">Password</label>
					</td>
					<td>
						<input id="password" name="password" type="password" />
					</td>
				</tr>
				<tr>
					<td>
						<label for="retype">Retype password</label>
					</td>
					<td>
						<input id="retype" name="retype" type="password" />
					</td>
				</tr>
			</table>
			<input type="submit" value="Save Changes" />
			<input type="button" value="Cancel" onclick="window.location='${tg.url('/userlist')}'" />
		</form>
	</div>
		
</body>
</html>