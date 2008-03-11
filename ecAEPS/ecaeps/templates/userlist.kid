<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>ecAEPS</title>

<script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
<script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

<style type="text/css" title="currentStyle" media="screen">
		@import "${tg.url('/static/css/userlist.css')}";
</style>

<script type="text/javascript">

	var DUR = 0.1;

	function deleteCheck(id)
	{
		Effect.Fade('delete_'+id, 
								{duration: DUR, afterFinish: function (){
															new Effect.Appear('del_check_'+id, {duration: DUR});
															new Effect.Highlight('user_'+id);}});
		var nodes = document.getElementsByName('del_check');
		for(i in nodes)
			if(nodes[i].className=='clicked')
			{
				nodes[i].className = 'unclicked';
				var temp = (nodes[i].id).split('_');
				var nid = temp[temp.length-1];
				Effect.Fade(nodes[i].id,
										{duration: DUR, afterFinish: function (){
													new Effect.Appear('delete_'+nid, {duration: DUR});	
										}});
			}
		document.getElementById('del_check_'+id).className = 'clicked';
	}
	
	function deleteUser(id){
		new Effect.Highlight('user_'+id);
		Effect.Fade('user_'+id);
		new Ajax.Request('deleteUser', {method:'post', postBody:'id='+escape(id)});
	}
	
	function keepUser(id){
		Effect.Fade('del_check_'+id, 
								{duration: DUR, afterFinish: function(){
									new Effect.Appear('delete_'+id, {duration: DUR});
								}});
	}
	
</script>


</head>
<body>
	<h2 class="inline_header">User list</h2>
	<input type="button" value="Create new user record" onclick="window.location='${tg.url('/userprofile/createUser')}'" />
	<div id="progdiv">
		<label for="program">Program</label>
		<select py:if="'global_admin' in tg.identity.groups" id="program" onchange="window.location='?program='+this.options[this.selectedIndex].value">
			<option selected="selected" value="0">All</option>
			<option py:for="p in programlist" py:attrs="curProg(p.id)" value="${p.id}">${p.name}</option>
		</select>
		<label py:if="'global_admin' not in tg.identity.groups">${program.name}</label>
	</div>
	
	<table class="standard" id="users">
		<tr>
			<th>
				Name
			</th>
			<th>
				Username
			</th>
			<th>
				Email
			</th>
			<th>
				Phone
			</th>
			<th class="last"></th>
		</tr>
		<?python rownum=0?>
		<tr py:for="u in userlist" id="user_${u.id}" py:attrs="shaded(rownum)">
			<?python rownum+=1?>
			<td>
				<a href="${tg.url('/userprofile',id=u.id)}">${u.firstlast()}</a>
			</td>
			<td>
				${u.user_name}
			</td>
			<td>
				${u.email_address}
			</td>
			<td>
				${u.phone}
			</td>
			<td class="last">
				<a id="delete_${u.id}" onclick="deleteCheck(${u.id})">
						Delete
				</a>
				<label name='del_check' class='unclicked' id="del_check_${u.id}" style="display: none;">
					Delete this user from the database?&nbsp;
					<a onclick="deleteUser(${u.id})">Yes</a>&nbsp;
					<a onclick="keepUser(${u.id})">No</a>
				</label>
			</td>
		</tr>
	</table>
</body>
</html>