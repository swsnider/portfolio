<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>ecAEPS</title>

        <script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

        <style type="text/css" title="currentStyle" media="screen">
            @import "${tg.url('/static/css/search.css')}";
        </style>

        <script type="text/javascript">

            var DUR = 0.1;

            function deleteCheck(id)
            {
                Effect.Fade('delete_'+id, 
                {duration: DUR, afterFinish: function (){
                        new Effect.Appear('del_check_'+id, {duration: DUR});
                        new Effect.Highlight('child_'+id);}});
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

            function cancelDelete(id){
                Effect.Fade('del_check_'+id, 
                {duration: DUR, afterFinish: function(){
                        new Effect.Appear('delete_'+id, {duration: DUR});
                }});
            }

            function createNewChild()
            {
                window.location="${tg.url('/child/createNewChild')}"
            }

            function deleteChild(id){
                new Effect.Highlight('child_'+id);
                Effect.Fade('child_'+id);
                new Ajax.Request('deleteChild', {method:'post', postBody:'id='+escape(id)});
            }

            function addChild(id){
                new Ajax.Request('addChild', {method:'post', postBody:'id='+escape(id)});
                new Effect.Highlight('add_'+id, {endcolor:document.getElementById('add_'+id).style.backgroundColor});
                Effect.Fade('a_'+id,
                {duration: DUR, afterFinish: function (){
                        new Effect.Appear('r_'+id, {duration: DUR});	
                }});

            }

            function remChild(id){
                new Ajax.Request('removeChild', {method:'post', postBody:'id='+escape(id)});
                new Effect.Highlight('add_'+id, {endcolor:document.getElementById('add_'+id).style.backgroundColor});
                Effect.Fade('r_'+id,
                {duration: DUR, afterFinish: function (){
                        new Effect.Appear('a_'+id, {duration: DUR});	
                }});
            }

        </script>

    </head>
    <body>
        <h2 class="section_header">Search</h2>

        <form method="post" action="search">
            <label for="search_ssid">SSID</label>
            <input id="search_ssid" name="search_ssid" type="text" />

            <label for="search_name">Name</label>
            <input id="search_name" name="search_name" type="text" />

            <label for="search_birthdate">Birthdate</label>
            <input id="search_birthdate" name="search_birthdate" type="text" />

            <input type="submit" value="Search" />
        </form>
        <br />

        <div py:if="size > -1">
            <h2 class="inline_header">Results</h2>
            <input py:if="'admin' in tg.identity.groups or 'global_admin' in tg.identity.groups" type="button" value="Create new child record" onclick="createNewChild()" />

            <table class="standard" id="search" py:if="size > 0">
                <tr>
                    <th><a class="sort_link" href="${tg.url('/search',sort='lname,fname')}">Name ${sym('lname')}</a></th>
                    <th><a class="sort_link" href="${tg.url('/search',sort='bdate,lname,fname')}">Birthdate ${sym('bdate')}</a></th>
                    <th><a class="sort_link" href="${tg.url('/search',sort='ssid')}">SSID ${sym('ssid')}</a></th>
                    <th>Last assessment</th>
										<th>New assessment</th>
                    <th>Child List</th>
                    <th class="last">&nbsp;</th>
                </tr>
                <?python rownum=0?>
                <tr py:for="r in results" id="child_${r.id}" py:attrs="shaded(rownum)">
                    <?python rownum+=1?>
                    <td><a href="${tg.url('/child',id=r.id)}">${r.firstlast()}</a></td>
                    <td>${r.display_bdate}</td>
                    <td>${r.ssid}</td>
                    <td py:if="r.lastAssessment.id != 0"><a href="${tg.url('/assessment',id=r.lastAssessment.id)}">${str(r.lastAssessment.display_dateEntered)}</a></td>
                    <td py:if="r.lastAssessment.id == 0">&nbsp;</td>
										<td><a href="${tg.url('/assessment/newAssessment',level='I',childid=r.id)}">Level I</a> | <a href="${tg.url('/assessment/newAssessment',level='II',childid=r.id)}">Level II</a></td>
                    <td id="add_${r.id}" py:if="r.id not in childlist">
                        <a id="a_${r.id}" onclick="addChild(${r.id})">Add</a>
                        <a id="r_${r.id}" onclick="remChild(${r.id})" style="display:none;">Remove</a>
                    </td>
                    <td id="add_${r.id}" py:if="r.id in childlist">
                        <a id="a_${r.id}" onclick="addChild(${r.id})" style="display:none;">Add</a>
                        <a id="r_${r.id}" onclick="remChild(${r.id})">Remove</a>
                    </td>
                    <td class="last">
                        <div py:if="'admin' in tg.identity.groups or 'global_admin' in tg.identity.groups">
                            <a id="delete_${r.id}" onclick="deleteCheck(${r.id})">Delete</a>
                            <label name='del_check' class="unclicked" id="del_check_${r.id}" style="display: none;">
                                Permanently delete this child from the database? 
                                <a onclick="deleteChild(${r.id})">Yes</a> 
                                <a onclick="cancelDelete(${r.id})">No</a>
                            </label>
                        </div>
                    </td>
                </tr>
            </table>
            <p py:if="size == 0">No results found.</p>
        </div>
    </body>
</html>
