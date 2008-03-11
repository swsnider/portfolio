<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
    <head><!--!{{{HEAD-->
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>ecAEPS</title>

        <script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

        <style type="text/css" title="currentStyle" media="print, screen">
            @import "${tg.url('/static/css/assessment.css')}";
        </style>
        <style type="text/css" title="currentStyle" media="print">
            @import "${tg.url('/static/css/print.css')}";
        </style>

        <script type="text/javascript">
            //<![CDATA[	
            function assessmentUpdate(field, value, type){
	            new Ajax.Request('assessmentUpdate', 
              {
                  method:'post',
                  postBody:'field='+escape(field)+'&amp;value='+escape(value)+'&amp;type='+escape(type),
                  onComplete: function (r)
                  {
                      document.getElementById(field).value=r.responseText;
                      new Effect.Highlight(field)
                  }
              });
            }
            function scoreUpdate(id, value){
                new Ajax.Request('${tg.url('/assessment/scoreUpdate')}', {method:'post', postBody:'id='+escape(id)+'&value='+escape(value)});
            }

            function totalUpdate(id, value){
              new Ajax.Request('scoreUpdate', 
							{
									method:'post',
									postBody:'id='+escape(id)+'&value='+escape(value),
									onComplete: function (r)
									{
											document.getElementById('percent').innerHTML = r.responseText;
											new Effect.Highlight('percent')
									}
							});
            }

            function overwrite(input)
            {
                if(input.value == '`' || input.value == '~')
                input.value = 0;
                if(input.value != "0" && input.value != "1" && input.value != "2")
                {
                    input.value = "#";
                    input.style.color = "red";
                    }else{
                    input.style.color = "black";
                }
            }

            // Adapted from w3schools example
            function enter2tab(e, id)
            {
                var keynum
                if(window.event) // IE
                keynum = e.keyCode
                else if(e.which) // Netscape/Firefox/Opera
                keynum = e.which

                if(keynum == 13)
                {
                    var i = parseInt(id)
                    document.getElementById(i).blur()
                    var next = document.getElementById(i+1)
                    if(next == null) {
                    	document.getElementById(1).focus()
											document.getElementById(1).select()
                    } else {
                    	next.focus()
											next.select()
                		}
								}		
            }

            //]]>

            //Hovis's positioning script for the "popups"
            function findPos(obj) {
                var curleft = curtop = 0;
                if (obj.offsetParent) {
                    curleft = obj.offsetLeft
                    curtop = obj.offsetTop
                    while (obj = obj.offsetParent) {
                        curleft += obj.offsetLeft
                        curtop += obj.offsetTop
                    }
                }
                return [curleft,curtop];
            }

        </script>



    </head><!--! }}}HEAD-->
    <body>
        <div id="assessment">
            <h2 class="inline_header"><span class="green_under">Assessment (Level ${a.level})</span> for <a id="childname_link" name="top" href="${tg.url('/child')}?id=${child.id}">${child.firstlast()}</a> </h2>

            <div id="overtable">
                <table id="print_link"><tr><td>
                    <a onclick="window.print();">Print area</a>
                </td></tr></table>

                <table id="categories"><tr>
                        <?python temp = [{'id':None},{'id':'current'}] ?>
                        <td class="category" py:for="c in catlist" py:attrs="temp[int(c==category)]">
                                <a py:if="c == category">${c}</a>
                                <a py:if="c != category" href="?category=${c}">${c}</a>
                        </td>
                </tr></table>

                <div class="right" id="fillval">
                    <form id="fillform" action="fillUpdate" method="post">
                        <label for="fill">Fill</label>
                        <div id="fill" class="box">
                            <input type="radio" id="missing" name="fill" value="missing" py:attrs="pcheck('fill','missing')" />
                            <label for="missing">missing</label>
                            <input type="radio" id="all" name="fill" value="all" py:attrs="pcheck('fill','all')" />
                            <label for="all">all</label>
                        </div>

                        <label for="values">&nbsp;values with</label>
                        <div id="values" class="box">
                            <input py:if="len(old) > 0" type="radio" id="previous" name="values" py:attrs="pcheck('values','previous')" value="previous" />
                            <label py:if="len(old) > 0" for="previous">previous test</label>
                            <input type="radio" id="zeros" name="values" py:attrs="pcheck('values','zeros')" value="zeros" />
                            <label for="zeros">0's</label>
                            <input type="radio" id="twos" name="values" value="twos" py:attrs="pcheck('values','twos')" />
                            <label for="twos">2's</label>
                        </div>
&nbsp;
                        <input type="submit" value="Go" />
                    </form>
                </div>
            </div>
        </div>
						<h3>${category}</h3>
            
            <table class="standard" id="a_content">
                <tr>
                    <td class="align_right" colspan="2">
                        This area last edited by:
                    </td>
                    <td onMouseOver="getElementById('column3').style.display = 'block';" class="header">
                        ${getEditor(a.id, category)[0]}
                        <br />
                        ${getEditor(a.id, category)[1]}
                    </td>
                    <td class="header" py:for="i in old">
                        ${getEditor(i.id, category)[0]}
                        <br />
                        ${getEditor(i.id, category)[1]}
                    </td>
                </tr>
                <tr>
									<td class="empty">&nbsp;</td>
	                <td id="testdate">
                      Test date:
                  </td>
                  <td class="header">
          					<input type="text" size="8" name="dateEntered" id="dateEntered" value="${a.display_dateEntered}" onblur="assessmentUpdate(this.name, this.value, 'date')" />
                  </td>
									<td class="header" py:for="i in old">
                      ${i.display_dateEntered}
                  </td>
                </tr>
                <?python count=0; rownum=0 ?>
                <tr class="criteria" py:for="c in criteria" py:attrs="shaded(rownum)">
                    <?python rownum+=1 ?>
										<td class="empty">&nbsp;</td>
                    <td class="level${c.rank}">
                        <span class="noprint" id="prefix">${c.prefix}</span>
                    </td>
                    <td py:if="c.rank!='1'" class="score">
                        <?python
													val = ""
													sid = 0
													for s in a.scores:
														if s.criterionID == c.id:
															val = s.value
															sid = s.id
													count = count+1
												?>
                        
                        <input id="${count}" type="text" maxlength="1" size="1" name="score" value="${val}" onblur="overwrite(this);scoreUpdate(${sid}, this.value)" onkeypress="enter2tab(event, this.id)" py:attrs="scoreclass(val)"/>
                    </td>
                    <td py:if="c.rank=='1'" class="area">
												&nbsp;
                    </td>
							      <td py:if="c.rank!='1'" py:for="i in old" class="score">
							      	<?python
												val = ""
												for s in i.scores:
													if s.criterionID == c.id:
														val = s.value
											?>
							      	<span py:attrs="scoreclass(val)">${val}</span>
							      </td>
							      <td py:if="c.rank=='1'" py:for="i in old" class="score">
                        &nbsp;
                    </td>
                </tr>
								<tr>
										<td id="leftblank" colspan="2">&nbsp;</td>
										<td id="blank">&nbsp;</td>
										<td id="blank" py:for="i in old">&nbsp;</td>
								</tr>
								<tr>
                    <td class="subtotal" colspan="2">
											Domain score possible
                    </td>
                    <td class="sum" id="sum" colspan="${len(old)+1}">
											${scorePossible(category, a.level)}
                    </td>
                </tr>
                <tr>
                    <td class="subtotal" colspan="2">
											Domain subtotal (all items)
                    </td>
                    <td class="sum" id="sum">
											<input id="${count+1}" type="text" maxlength="3" size="3" value="${subtotal.value}" onblur="totalUpdate(${subtotal.id}, this.value)" onkeypress="enter2tab(event, this.id)" />
                    </td>
                    <td class="sum" py:for="i in old">
											${oldtotals[i.id]}
                    </td>
                </tr>
                <tr>
                    <td class="subtotal" colspan="2">
											# of items scored NA
                    </td>
                    <td class="sum" id="sum">
											<input id="${count+1}" type="text" maxlength="3" size="3" value="${na.value}" onblur="totalUpdate(${na.id}, this.value)" onkeypress="enter2tab(event, this.id)" />
                    </td>
                    <td class="sum" py:for="i in old">
											${oldna[i.id]}
                    </td>
                </tr>
                <tr>
                    <td class="subtotal" colspan="2">
											Percent score
                    </td>
                    <td class="sum" id="percent">
											${percent}
                    </td>
                    <td class="sum" py:for="i in old">
											${percents[i.id]}
                    </td>
                </tr>
            </table>
            <div class="noprint">
								<br />
                <a href="#top">Top</a>
                <a href="${tg.url('/assessment/')}?category=${nextCategory()}">Next</a>
            </div>



    </body>
</html>
