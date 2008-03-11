<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
    <head><!--!{{{HEAD-->
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
        <title>ecAEPS</title>

        <script src="${tg.url('/static/javascript/prototype.js')}" type="text/javascript"></script>
        <script src="${tg.url('/static/javascript/scriptaculous.js')}" type="text/javascript"></script>

        <style type="text/css" title="currentStyle" media="print, screen">
            @import "${tg.url('/static/css/assessment2.css')}";
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

            function totalUpdate(id, percent, value){
              new Ajax.Request('scoreUpdate', 
							{
									method:'post',
									postBody:'id='+escape(id)+'&value='+escape(value),
									onComplete: function (r)
									{
											document.getElementById(percent).innerHTML = r.responseText;
											new Effect.Highlight(percent)
									}
							});
            }

            function basketUpdate(id, value){
              new Ajax.Request('scoreUpdate', 
							{
									method:'post', postBody:'id='+escape(id)+'&value='+escape(value)
							})
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

        </script>



    </head><!--! }}}HEAD-->
    <body>
        <div id="assessment">
            <h2 class="inline_header"><span class="green_under">Assessment (Level ${a.level})</span> for <a id="childname_link" name="top" href="${tg.url('/child')}?id=${child.id}">${child.firstlast()}</a> </h2>

            <table class="standard" id="a_content">
    	        <tr>
		            <td class="align_right">
		                This area last edited by:
		            </td>
		            <td class="header">
		                ${getEditor(a.id, categories[0])[0]}
		                <br />
		                ${getEditor(a.id, categories[0])[1]}
		            </td>
		            <td class="header" py:for="i in old">
		                ${getEditor(i.id, categories[0])[0]}
		                <br />
		                ${getEditor(i.id, categories[0])[1]}
		            </td>
	            </tr>
	            <tr>
	             	<td id="testdate" class="align_right">
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
						<div py:for="c in categories">
							<?python d = data[c]?>
							<tr>
								<td class="leftblank">&nbsp;</td>
								<td class="blank" colspan="${len(old)+1}">&nbsp;</td>
							</tr>
							<tr>
								<td class="category" id="leftblank" colspan="${len(old)+2}">${c}</td>
							</tr>
							<tr>
              	<td class="subtotal">
									Score possible
                </td>
                <td class="sum" id="sum" colspan="${len(old)+1}">
									${scorePossible(c, a.level)}
                </td>
              </tr>
              <tr>
              	<td class="subtotal">
									Score
                </td>
                <td class="sum" id="sum">
									<input id="${count+1}" type="text" maxlength="3" size="3" value="${d['stscore'].value}" onblur="totalUpdate(${d['stscore'].id}, 'percent_${c}', this.value)" onkeypress="enter2tab(event, this.id)" />
                </td>
                <td class="sum" py:for="i in old">
									${d['oldtotals'][i.id]}
                </td>
              </tr>
              <tr>
                <td class="subtotal">
									# of items scored NA
                </td>
                <td class="sum" id="sum">
									<input id="${count+1}" type="text" maxlength="3" size="3" value="${d['nascore'].value}" onblur="totalUpdate(${d['nascore'].id}, 'percent_${c}', this.value)" onkeypress="enter2tab(event, this.id)" />
                </td>
                <td class="sum" py:for="i in old">
									${d['oldna'][i.id]}
                </td>
              </tr>
              <tr>
              	<td class="subtotal">
									Percent score
                </td>
                <td class="sum" id="percent_${c}">
									${d['percent']}
                </td>
                <td class="sum" py:for="i in old">
									${d['percents'][i.id]}
                </td>
              </tr>
						</div>
						<tr>
							<td class="leftblank">&nbsp;</td>
							<td class="blank" colspan="${len(old)+1}">&nbsp;</td>
						</tr>
						<tr>
							<td class="category" id="leftblank" colspan="${len(old)+2}">OSEP</td>
						</tr>
						<tr py:for="i in range(3)">
							<?python b = baskets[i]?>
            	<td class="subtotal">
								Basket ${i+1}
              </td>
              <td class="sum" id="sum">
								<input id="${count+1}" type="text" maxlength="3" size="3" value="${b['val'].value}" onblur="basketUpdate(${b['val'].id}, this.value)" onkeypress="enter2tab(event, this.id)" />
              </td>
              <td class="sum" py:for="i in old">
								${b['old'][i.id].value}
              </td>
            </tr>
            </table>
            
						<div class="noprint">
								<br />
                <a href="#top">Top</a>
            </div>

				</div>
    </body>
</html>