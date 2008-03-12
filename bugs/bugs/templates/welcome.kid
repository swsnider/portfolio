<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Welcome to TurboGears</title>
</head>
<body>
	<div class='warning' style="display:none;" id="domexample"><p>Are you sure to delete this item?</p> <input type='button' value='Yes, delete!' onclick='Modalbox.hide()' /> or <input type='button' value='No, leave it!' onclick='Modalbox.hide()' /></div>
	<script type="text/javascript">
		Modalbox.show($('domexample'),
		{title: this.title, width: 300});
	</script>
</body>
</html>
