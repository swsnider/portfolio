<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>ecAEPS</title>

        <script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

        <style type="text/css" title="currentStyle" media="screen">
            @import "${tg.url('/static/css/child.css')}";
        </style>

        <script type="text/javascript">

            var DUR = 0.1;

            function deleteCheck(id)
            {
                Effect.Fade('delete_'+id, 
                {duration: DUR, afterFinish: function (){
                        new Effect.Appear('del_check_'+id, {duration: DUR});
                        new Effect.Highlight('assessment_'+id);}});
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

            function childUpdate(field, value, type, message){
                new Ajax.Request('childUpdate', 
                {
                    method:'post',
                    postBody:'field='+escape(field)+'&amp;value='+escape(value)+'&amp;type='+escape(type), 
                    onFailure: function (r)
                    {
                        document.getElementById(message).innerHTML=r.responseText;
                        new Effect.Highlight(message)
                    },
                    onSuccess: function (r)
                    {
                        document.getElementById(field).value=r.responseText;
                        document.getElementById(message).innerHTML="";
                        new Effect.Highlight(field)
                    }
                });
            }

            function deleteAssessment(id){
                new Effect.Highlight('assessment_'+id);
                Effect.Fade('assessment_'+id);
                new Ajax.Request('deleteAssessment', {method:'post', postBody:'id='+escape(id), onFailure:function(){window.location="";}});
            }

            function keepAssessment(id){
                Effect.Fade('del_check_'+id, 
                {duration: DUR, afterFinish: function(){
                        new Effect.Appear('delete_'+id, {duration: DUR});
                }});
            }
        </script>

    </head>
    <body>
        <div id="child_profile">
            <h2>Child Profile</h2>
            <div id="message"></div>
            <table id="childprofile">
                <tr><td>
                        <label for="lname">Last</label>
                        <input type="text" name="lname" id="lname" value="${child.lname}" onchange="childUpdate(this.name, this.value, 'string', 'message')" />
                        </td><td>
                </td></tr>
                <tr><td>
                        <label for="fname">First</label>
                        <input type="text" name="fname" id="fname" value="${child.fname}" onchange="childUpdate(this.name, this.value, 'string', 'message')" />
                        </td><td>
                </td></tr>
                <tr><td>
                        <label for="mname">Middle</label>
                        <input type="text" name="mname" id="mname" value="${child.mname}" onchange="childUpdate(this.name, this.value, 'string', 'message')" />
                        </td><td>
                </td></tr>
                <tr><td>
                        <label for="bdate">Birthdate</label>
                        <input type="text" name="bdate" id="bdate" value="${child.display_bdate}" onchange="childUpdate(this.name, this.value, 'date', 'bday_message')" />
                        </td><td style="display: inline;" id="bday_message">
                </td></tr>
                <tr><td>
                        <label for="ssid">SSID</label>
                        <input type="text" name="ssid" id="ssid" size="10" maxlength="10" value="${child.ssid}" onchange="childUpdate(this.name, this.value, 'string', 'ssid_message')" />
                        </td><td id="ssid_message">(Required)
                </td></tr>	
            </table>
        </div>
        <div class="assessments">
            <div class="level">
                <h2>Assessments</h2>

                Create new assessment record:
                <a href="${tg.url('/assessment/newAssessment')}?level=I">Level I</a>
                <a href="${tg.url('/assessment/newAssessment')}?level=II">Level II</a>
            </div>
            <table class="standard" id="chiass" py:if="len(child.assessments) > 0">
                <tr>
                    <th>
                        Date
                    </th>
                    <th>
                        Level
                    </th>
                    <th>
                        Created by
                    </th>
                    <th></th><th class="last"></th>
                </tr>
                <?python rownum=0?>
                <tr py:for="i in child.assessments" id="assessment_${i.id}" py:attrs="shaded(rownum)">
                    <?python rownum+=1?>
                    <td>
                        <a href="${tg.url('/assessment')}?id=${i.id}">${i.display_dateEntered}</a>
                    </td>
                    <td class="level">
                        ${i.level}
                    </td>
                    <td>
                        ${i.owner.firstlast()	}, ${i.owner.program.name}
                    </td>
                  <!--  <td>
	                    <a onclick="print('${newloc}')">Print area</a>
	              		</td> -->
                    <td class="last"> 
                        <a id="delete_${i.id}" onclick="deleteCheck(${i.id})">
                            Delete
                        </a>
                        <label name='del_check' class='unclicked' id="del_check_${i.id}" style="display: none;">
                            Are you sure?&nbsp;
                            <a onclick="deleteAssessment(${i.id})">Yes</a>&nbsp;
                            <a onclick="keepAssessment(${i.id})">No</a>
                        </label>
                    </td>
                </tr>
            </table>
            <p py:if="len(child.assessments) == 0">There are no assessments for this child.</p>
        </div>
        <div id="user_lists" py:if="'admin' in tg.identity.groups or 'global_admin' in tg.identity.groups">
            <h2>User lists</h2>			
            <table class="standard" id="chiuse" py:if="len(child.listedOn) > 0">
                <tr>
                    <th>
                        Program
                    </th>
                    <th>
                        Name
                    </th>
                    <th>
                        Email
                    </th>
                    <th class="last">
                        Phone
                    </th>
                </tr>
                <?python rownum=0?>
                <tr py:for="i in child.listedOn" py:attrs="shaded(rownum)">
                    <?python rownum+=1?>
                    <td>
                        ${i.program.name}
                    </td>
                    <td>
                        ${i.firstlast()}
                    </td>
                    <td>
                        ${i.email_address}
                    </td>
                    <td class="last">
                        ${i.phone}
                    </td>
                </tr>
            </table>
            <p py:if="len(child.listedOn) == 0">This child is not on any user's Child List.</p>
        </div>
    </body>
</html>
