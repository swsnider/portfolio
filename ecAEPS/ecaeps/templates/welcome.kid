<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>ecAEPS</title>

        <script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

        <script type="text/javascript">
            function remChild(id){
                new Effect.Highlight('child_'+id);
                Effect.Fade('child_'+id);
                new Ajax.Request('removeChild', {method:'post', postBody:'id='+escape(id), onFailure:function(){window.location="";}});
            }
        </script>
        <style type="text/css">
            @import "${tg.url('static/css/welcome.css')}";
        </style>
    </head>

    <body>
        <div id="child_list">
            <h2 class="section_header">Child list</h2>

            <table class="standard" id="cl" py:if="len(childList)>0">
                <tr class="childheaderrow">
                    <th>Name</th>
                    <th>Birthdate</th>
                    <th>SSID</th>
                    <th>Last assessment</th>
										<th>New assessment</th>
                    <th class="last">&nbsp;</th>
                </tr>
                <?python rownum=0 ?>
                <tr py:for="i in childList" id="child_${i.id}" class="childrow" py:attrs="shaded(rownum)">
                    <?python rownum+=1 ?>
                    <td><a href="${tg.url('child',id=i.id)}">${i.fname} ${i.lname}</a></td>
                    <td>${i.display_bdate}</td>
                    <td>${i.ssid}</td>
                    <td py:if="i.lastAssessment.id != 0"><a href="${tg.url('assessment',id=i.lastAssessment.id)}">${str(i.lastAssessment.display_dateEntered)}</a></td>
                    <td py:if="i.lastAssessment.id == 0">&nbsp;</td>
										<td><a href="${tg.url('assessment/newAssessment',level='I',childid=i.id)}">Level I</a> | <a href="${tg.url('assessment/newAssessment',level='II',childid=i.id)}">Level II</a></td>
                    <td class="last"><a onclick="remChild('${i.id}')">Remove</a></td>
                </tr>
            </table>
            <p py:if="len(childList)==0">Your Child List is empty.  To find children to add to your list, use the <a href="${tg.url('search')}">search</a>.</p>
        </div>
    </body>
</html>
