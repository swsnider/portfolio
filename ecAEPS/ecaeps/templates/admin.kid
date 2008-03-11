<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>ecAEPS</title>

<script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
<script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

<script type="text/javascript">
	function uploadCriteria()
	{
		var filename = document.getElementById('file').value
		window.location="${tg.url('uploadCriteria')}?filename="+filename
	}
	function uploadChildren()
	{
		var filename = document.getElementById('file').value
		window.location="${tg.url('uploadChildren')}?filename="+filename
	}
	function addProgram()
	{
		var name = document.getElementById('program').value
		window.location="${tg.url('addProgram')}?name="+name
	}
</script>

<style type="text/css">
    @import "${tg.url('static/css/admin.css')}";
</style>
</head>
<body>	
	<div id="user_profile">
		<h2>Admin Tools</h2>
		
		${message}
		<br />
		<input id="program" type="text" />
		<input type="button" value="Add program" onclick="addProgram()" />
		<br />
		<br />
		<input id="file" type="file" />
		<br />
		Upload Criteria<input type="button" value="upload" onclick="uploadCriteria()" />
		<br />
		Upload Children<input type="button" value="upload" onclick="uploadChildren()" />
	</div>
</body>
</html>
