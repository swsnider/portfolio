<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
	<title>Whitepages Search Function</title>
	<style type="text/css">
		.searchBox{
			text-align:center;
			border: thin solid green;
			width: 20%;
		}
		.centered{
			margin-left: auto;
			margin-right: auto;
			padding-bottom: 1em;
		}
		#whitepages{
		    margin-top: 1em;
			width:50%;
			text-align: center;
			border: thin solid red;
		}
	</style>
</head>
<body>
    <div class="centered" style="width: 50%; color: red;" py:if="flash">${flash}</div>
	<div class="searchBox centered">
		<form action="whitepages.cgi" method="post">
			<h2>White Pages Search</h2>
			<label for="q">Search: </label><input type="text" name="q" /><input type="submit" value="Search!" />
			<p><a href="http://lucene.apache.org/java/2_3_1/queryparsersyntax.html">Search Syntax</a><br/>NOTE: There are two possible search fields: '<strong>data</strong>', which has the full text from the phonebook, and '<strong>source</strong>', which has the name of the file from which the data was taken.</p>
		</form>
	</div>
	<div id="whitepages" class="centered">
	    <span py:if="extras">${extras}</span>
		<h2>Or, Browse the data</h2>
		<span py:for="i in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']"><a href="whitepages.cgi?letter=${i}">${i}</a> </span>
	</div>
	<div id="bookContents">
		<table border="1">
			<tr py:for="i in entries"><td>${i.data}</td><td><a href="http://hopper.uoregon.edu/~ssnider/swfs/${i.realSource()}">Linky</a></td></tr>
		</table>
	</div>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-3926876-1");
pageTracker._initData();
pageTracker._trackPageview();
</script>
</body>
</html>
