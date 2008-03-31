<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Guildr</title>
</head>
<body>

  <div id="sidebar" py:if="tg.identity.anonymous">
    <h2>Log In</h2>
    <form method="POST" action="/login">
    <table>
        <tr><td><label for="user_name">User Name:</label></td></tr>
        <tr><td><input type="text" id="user_name" name="user_name"/></td></tr>
        <tr><td><label for="password">Password:</label></td></tr>
        <tr><td><input type="password" id="password" name="password"/></td></tr>
        <tr><td><input type="submit" name="login" value="Login"/></td></tr>
    </table>
    <input type="hidden" name="forward_url" value="/" />
    </form>
  </div>
  <table style="width:100%">
      <tr><th>Guild Name</th><th>Website</th><th>Numer of Members</th></tr>
      <tr py:for="i in guilds"><td><a href="${tg.url('/')}guild/${i.id}">${i.name}</a></td><td><a href="${i.website}">linky</a></td><td>${len(i.members)}</td></tr>
  </table>
</body>
</html>
