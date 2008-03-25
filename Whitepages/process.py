#!/usr/bin/env python
import re, sys, os.path
from sqlobject import *

connection_string = "mysql://user:password@server/db"
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

alphas = {u'220.swf': u'M', u'65.swf': u'C', u'113.swf': u'G', u'47.swf': u'C', u'151.swf': u'H', u'107.swf': u'F', u'169.swf': u'K', u'48.swf': u'C', u'171.swf': u'K', u'295.swf': u'S', u'319.swf': u'T', u'262.swf': u'P', u'83.swf': u'D', u'197.swf': u'L', u'206.swf': u'M', u'360.swf': u'Z', u'190.swf': u'L', u'123.swf': u'G', u'54.swf': u'C', u'166.swf': u'J', u'193.swf': u'L', u'86.swf': u'D', u'104.swf': u'F', u'331.swf': u'U', u'157.swf': u'I', u'94.swf': u'E', u'268.swf': u'R', u'38.swf': u'B', u'204.swf': u'M', u'134.swf': u'H', u'235.swf': u'N', u'95.swf': u'E', u'58.swf': u'C', u'23.swf': u'B', u'246.swf': u'O', u'184.swf': u'L', u'347.swf': u'W', u'63.swf': u'C', u'247.swf': u'P', u'314.swf': u'S', u'177.swf': u'K', u'337.swf': u'U', u'251.swf': u'P', u'330.swf': u'U', u'267.swf': u'R', u'71.swf': u'C', u'333.swf': u'U', u'172.swf': u'K', u'96.swf': u'E', u'115.swf': u'G', u'203.swf': u'M', u'195.swf': u'L', u'271.swf': u'R', u'6.swf': u'A', u'211.swf': u'M', u'359.swf': u'Y', u'43.swf': u'B', u'57.swf': u'C', u'1.swf': u'A', u'266.swf': u'R', u'7.swf': u'A', u'324.swf': u'T', u'140.swf': u'H', u'265.swf': u'Q', u'269.swf': u'R', u'127.swf': u'G', u'16.swf': u'A', u'285.swf': u'S', u'335.swf': u'U', u'299.swf': u'S', u'258.swf': u'P', u'307.swf': u'S', u'142.swf': u'H', u'318.swf': u'T', u'128.swf': u'G', u'224.swf': u'M', u'182.swf': u'L', u'105.swf': u'F', u'111.swf': u'F', u'62.swf': u'C', u'259.swf': u'P', u'250.swf': u'P', u'178.swf': u'K', u'82.swf': u'D', u'288.swf': u'S', u'214.swf': u'M', u'186.swf': u'L', u'59.swf': u'C', u'338.swf': u'U', u'74.swf': u'D', u'228.swf': u'N', u'256.swf': u'P', u'158.swf': u'I', u'287.swf': u'S', u'357.swf': u'Y', u'129.swf': u'H', u'146.swf': u'H', u'39.swf': u'B', u'275.swf': u'R', u'351.swf': u'W', u'209.swf': u'M', u'294.swf': u'S', u'10.swf': u'A', u'249.swf': u'P', u'322.swf': u'T', u'97.swf': u'E', u'11.swf': u'A', u'276.swf': u'R', u'176.swf': u'K', u'248.swf': u'P', u'56.swf': u'C', u'33.swf': u'B', u'254.swf': u'P', u'37.swf': u'B', u'98.swf': u'E', u'326.swf': u'T', u'34.swf': u'B', u'293.swf': u'S', u'122.swf': u'G', u'219.swf': u'M', u'81.swf': u'D', u'229.swf': u'N', u'260.swf': u'P', u'225.swf': u'M', u'50.swf': u'C', u'281.swf': u'R', u'189.swf': u'L', u'42.swf': u'B', u'361.swf': u'Z', u'41.swf': u'B', u'284.swf': u'S', u'132.swf': u'H', u'164.swf': u'J', u'156.swf': u'I', u'301.swf': u'S', u'180.swf': u'L', u'22.swf': u'B', u'185.swf': u'L', u'252.swf': u'P', u'69.swf': u'C', u'194.swf': u'L', u'32.swf': u'B', u'165.swf': u'J', u'257.swf': u'P', u'356.swf': u'Y', u'239.swf': u'O', u'329.swf': u'U', u'270.swf': u'R', u'147.swf': u'H', u'117.swf': u'G', u'215.swf': u'M', u'187.swf': u'L', u'3.swf': u'A', u'101.swf': u'E', u'12.swf': u'A', u'116.swf': u'G', u'320.swf': u'T', u'296.swf': u'S', u'153.swf': u'I', u'188.swf': u'L', u'325.swf': u'T', u'310.swf': u'S', u'99.swf': u'E', u'207.swf': u'M', u'119.swf': u'G', u'334.swf': u'U', u'27.swf': u'B', u'264.swf': u'Q', u'136.swf': u'H', u'348.swf': u'W', u'78.swf': u'D', u'8.swf': u'A', u'205.swf': u'M', u'327.swf': u'T', u'290.swf': u'S', u'274.swf': u'R', u'135.swf': u'H', u'66.swf': u'C', u'29.swf': u'B', u'31.swf': u'B', u'345.swf': u'W', u'26.swf': u'B', u'245.swf': u'O', u'181.swf': u'L', u'328.swf': u'U', u'280.swf': u'R', u'233.swf': u'N', u'100.swf': u'E', u'201.swf': u'M', u'40.swf': u'B', u'286.swf': u'S', u'317.swf': u'T', u'303.swf': u'S', u'68.swf': u'C', u'253.swf': u'P', u'306.swf': u'S', u'53.swf': u'C', u'292.swf': u'S', u'321.swf': u'T', u'261.swf': u'P', u'212.swf': u'M', u'145.swf': u'H', u'311.swf': u'S', u'316.swf': u'T', u'92.swf': u'E', u'315.swf': u'S', u'118.swf': u'G', u'13.swf': u'A', u'133.swf': u'H', u'298.swf': u'S', u'297.swf': u'S', u'349.swf': u'W', u'149.swf': u'H', u'152.swf': u'H', u'227.swf': u'N', u'160.swf': u'J', u'289.swf': u'S', u'79.swf': u'D', u'238.swf': u'O', u'179.swf': u'K', u'161.swf': u'J', u'30.swf': u'B', u'19.swf': u'B', u'76.swf': u'D', u'217.swf': u'M', u'300.swf': u'S', u'192.swf': u'L', u'244.swf': u'O', u'84.swf': u'D', u'226.swf': u'N', u'109.swf': u'F', u'36.swf': u'B', u'44.swf': u'B', u'45.swf': u'B', u'162.swf': u'J', u'28.swf': u'B', u'200.swf': u'M', u'354.swf': u'X', u'20.swf': u'B', u'93.swf': u'E', u'272.swf': u'R', u'305.swf': u'S', u'137.swf': u'H', u'273.swf': u'R', u'112.swf': u'G', u'120.swf': u'G', u'358.swf': u'Y', u'5.swf': u'A', u'332.swf': u'U', u'237.swf': u'O', u'170.swf': u'K', u'241.swf': u'O', u'213.swf': u'M', u'282.swf': u'R', u'313.swf': u'S', u'60.swf': u'C', u'14.swf': u'A', u'240.swf': u'O', u'342.swf': u'W', u'9.swf': u'A', u'4.swf': u'A', u'155.swf': u'I', u'138.swf': u'H', u'243.swf': u'O', u'218.swf': u'M', u'353.swf': u'W', u'102.swf': u'F', u'163.swf': u'J', u'236.swf': u'N', u'52.swf': u'C', u'49.swf': u'C', u'150.swf': u'H', u'283.swf': u'S', u'25.swf': u'B', u'121.swf': u'G', u'202.swf': u'M', u'278.swf': u'R', u'352.swf': u'W', u'141.swf': u'H', u'230.swf': u'N', u'80.swf': u'D', u'72.swf': u'C', u'103.swf': u'F', u'77.swf': u'D', u'64.swf': u'C', u'17.swf': u'A', u'131.swf': u'H', u'90.swf': u'E', u'223.swf': u'M', u'344.swf': u'W', u'67.swf': u'C', u'143.swf': u'H', u'139.swf': u'H', u'216.swf': u'M', u'222.swf': u'M', u'35.swf': u'B', u'2.swf': u'A', u'183.swf': u'L', u'73.swf': u'D', u'232.swf': u'N', u'340.swf': u'W', u'15.swf': u'A', u'304.swf': u'S', u'108.swf': u'F', u'199.swf': u'M', u'312.swf': u'S', u'174.swf': u'K', u'124.swf': u'G', u'70.swf': u'C', u'154.swf': u'I', u'91.swf': u'E', u'308.swf': u'S', u'355.swf': u'Y', u'21.swf': u'B', u'221.swf': u'M', u'144.swf': u'H', u'350.swf': u'W', u'89.swf': u'E', u'114.swf': u'G', u'210.swf': u'M', u'88.swf': u'D', u'277.swf': u'R', u'148.swf': u'H', u'323.swf': u'T', u'125.swf': u'G', u'263.swf': u'P', u'130.swf': u'H', u'196.swf': u'L', u'339.swf': u'W', u'234.swf': u'N', u'87.swf': u'D', u'255.swf': u'P', u'24.swf': u'B', u'126.swf': u'G', u'231.swf': u'N', u'46.swf': u'C', u'61.swf': u'C', u'208.swf': u'M', u'167.swf': u'J', u'175.swf': u'K', u'279.swf': u'R', u'346.swf': u'W', u'55.swf': u'C', u'85.swf': u'D', u'51.swf': u'C', u'291.swf': u'S', u'343.swf': u'W', u'18.swf': u'A', u'336.swf': u'U', u'173.swf': u'K', u'168.swf': u'J', u'75.swf': u'D', u'198.swf': u'L', u'242.swf': u'O', u'110.swf': u'F', u'309.swf': u'S', u'159.swf': u'J', u'191.swf': u'L', u'341.swf': u'W', u'302.swf': u'S', u'106.swf': u'F'}
revAlphas = {u'A': [u'1.swf.txt', u'2.swf.txt', u'3.swf.txt', u'4.swf.txt', u'5.swf.txt', u'6.swf.txt', u'7.swf.txt', u'8.swf.txt', u'9.swf.txt', u'10.swf.txt', u'11.swf.txt', u'12.swf.txt', u'13.swf.txt', u'14.swf.txt', u'15.swf.txt', u'16.swf.txt', u'17.swf.txt', u'18.swf.txt'], u'C': [u'46.swf.txt', u'47.swf.txt', u'48.swf.txt', u'49.swf.txt', u'50.swf.txt', u'51.swf.txt', u'52.swf.txt', u'53.swf.txt', u'54.swf.txt', u'55.swf.txt', u'56.swf.txt', u'57.swf.txt', u'58.swf.txt', u'59.swf.txt', u'60.swf.txt', u'61.swf.txt', u'62.swf.txt', u'63.swf.txt', u'64.swf.txt', u'65.swf.txt', u'66.swf.txt', u'67.swf.txt', u'68.swf.txt', u'69.swf.txt', u'70.swf.txt', u'71.swf.txt', u'72.swf.txt'], u'B': [u'19.swf.txt', u'20.swf.txt', u'21.swf.txt', u'22.swf.txt', u'23.swf.txt', u'24.swf.txt', u'25.swf.txt', u'26.swf.txt', u'27.swf.txt', u'28.swf.txt', u'29.swf.txt', u'30.swf.txt', u'31.swf.txt', u'32.swf.txt', u'33.swf.txt', u'34.swf.txt', u'35.swf.txt', u'36.swf.txt', u'37.swf.txt', u'38.swf.txt', u'39.swf.txt', u'40.swf.txt', u'41.swf.txt', u'42.swf.txt', u'43.swf.txt', u'44.swf.txt', u'45.swf.txt'], u'E': [u'89.swf.txt', u'90.swf.txt', u'91.swf.txt', u'92.swf.txt', u'93.swf.txt', u'94.swf.txt', u'95.swf.txt', u'96.swf.txt', u'97.swf.txt', u'98.swf.txt', u'99.swf.txt', u'100.swf.txt', u'101.swf.txt'], u'D': [u'73.swf.txt', u'74.swf.txt', u'75.swf.txt', u'76.swf.txt', u'77.swf.txt', u'78.swf.txt', u'79.swf.txt', u'80.swf.txt', u'81.swf.txt', u'82.swf.txt', u'83.swf.txt', u'84.swf.txt', u'85.swf.txt', u'86.swf.txt', u'87.swf.txt', u'88.swf.txt'], u'G': [u'112.swf.txt', u'113.swf.txt', u'114.swf.txt', u'115.swf.txt', u'116.swf.txt', u'117.swf.txt', u'118.swf.txt', u'119.swf.txt', u'120.swf.txt', u'121.swf.txt', u'122.swf.txt', u'123.swf.txt', u'124.swf.txt', u'125.swf.txt', u'126.swf.txt', u'127.swf.txt', u'128.swf.txt'], u'F': [u'102.swf.txt', u'103.swf.txt', u'104.swf.txt', u'105.swf.txt', u'106.swf.txt', u'107.swf.txt', u'108.swf.txt', u'109.swf.txt', u'110.swf.txt', u'111.swf.txt'], u'I': [u'153.swf.txt', u'154.swf.txt', u'155.swf.txt', u'156.swf.txt', u'157.swf.txt', u'158.swf.txt'], u'H': [u'129.swf.txt', u'130.swf.txt', u'131.swf.txt', u'132.swf.txt', u'133.swf.txt', u'134.swf.txt', u'135.swf.txt', u'136.swf.txt', u'137.swf.txt', u'138.swf.txt', u'139.swf.txt', u'140.swf.txt', u'141.swf.txt', u'142.swf.txt', u'143.swf.txt', u'144.swf.txt', u'145.swf.txt', u'146.swf.txt', u'147.swf.txt', u'148.swf.txt', u'149.swf.txt', u'150.swf.txt', u'151.swf.txt', u'152.swf.txt'], u'K': [u'169.swf.txt', u'170.swf.txt', u'171.swf.txt', u'172.swf.txt', u'173.swf.txt', u'174.swf.txt', u'175.swf.txt', u'176.swf.txt', u'177.swf.txt', u'178.swf.txt', u'179.swf.txt'], u'J': [u'159.swf.txt', u'160.swf.txt', u'161.swf.txt', u'162.swf.txt', u'163.swf.txt', u'164.swf.txt', u'165.swf.txt', u'166.swf.txt', u'167.swf.txt', u'168.swf.txt'], u'M': [u'199.swf.txt', u'200.swf.txt', u'201.swf.txt', u'202.swf.txt', u'203.swf.txt', u'204.swf.txt', u'205.swf.txt', u'206.swf.txt', u'207.swf.txt', u'208.swf.txt', u'209.swf.txt', u'210.swf.txt', u'211.swf.txt', u'212.swf.txt', u'213.swf.txt', u'214.swf.txt', u'215.swf.txt', u'216.swf.txt', u'217.swf.txt', u'218.swf.txt', u'219.swf.txt', u'220.swf.txt', u'221.swf.txt', u'222.swf.txt', u'223.swf.txt', u'224.swf.txt', u'225.swf.txt'], u'L': [u'180.swf.txt', u'181.swf.txt', u'182.swf.txt', u'183.swf.txt', u'184.swf.txt', u'185.swf.txt', u'186.swf.txt', u'187.swf.txt', u'188.swf.txt', u'189.swf.txt', u'190.swf.txt', u'191.swf.txt', u'192.swf.txt', u'193.swf.txt', u'194.swf.txt', u'195.swf.txt', u'196.swf.txt', u'197.swf.txt', u'198.swf.txt'], u'O': [u'237.swf.txt', u'238.swf.txt', u'239.swf.txt', u'240.swf.txt', u'241.swf.txt', u'242.swf.txt', u'243.swf.txt', u'244.swf.txt', u'245.swf.txt', u'246.swf.txt'], u'N': [u'226.swf.txt', u'227.swf.txt', u'228.swf.txt', u'229.swf.txt', u'230.swf.txt', u'231.swf.txt', u'232.swf.txt', u'233.swf.txt', u'234.swf.txt', u'235.swf.txt', u'236.swf.txt'], u'Q': [u'264.swf.txt', u'265.swf.txt'], u'P': [u'247.swf.txt', u'248.swf.txt', u'249.swf.txt', u'250.swf.txt', u'251.swf.txt', u'252.swf.txt', u'253.swf.txt', u'254.swf.txt', u'255.swf.txt', u'256.swf.txt', u'257.swf.txt', u'258.swf.txt', u'259.swf.txt', u'260.swf.txt', u'261.swf.txt', u'262.swf.txt', u'263.swf.txt'], u'S': [u'283.swf.txt', u'284.swf.txt', u'285.swf.txt', u'286.swf.txt', u'287.swf.txt', u'288.swf.txt', u'289.swf.txt', u'290.swf.txt', u'291.swf.txt', u'292.swf.txt', u'293.swf.txt', u'294.swf.txt', u'295.swf.txt', u'296.swf.txt', u'297.swf.txt', u'298.swf.txt', u'299.swf.txt', u'300.swf.txt', u'301.swf.txt', u'302.swf.txt', u'303.swf.txt', u'304.swf.txt', u'305.swf.txt', u'306.swf.txt', u'307.swf.txt', u'308.swf.txt', u'309.swf.txt', u'310.swf.txt', u'311.swf.txt', u'312.swf.txt', u'313.swf.txt', u'314.swf.txt', u'315.swf.txt'], u'R': [u'266.swf.txt', u'267.swf.txt', u'268.swf.txt', u'269.swf.txt', u'270.swf.txt', u'271.swf.txt', u'272.swf.txt', u'273.swf.txt', u'274.swf.txt', u'275.swf.txt', u'276.swf.txt', u'277.swf.txt', u'278.swf.txt', u'279.swf.txt', u'280.swf.txt', u'281.swf.txt', u'282.swf.txt'], u'U': [u'328.swf.txt', u'329.swf.txt', u'330.swf.txt', u'331.swf.txt', u'332.swf.txt', u'333.swf.txt', u'334.swf.txt', u'335.swf.txt', u'336.swf.txt', u'337.swf.txt', u'338.swf.txt'], u'T': [u'316.swf.txt', u'317.swf.txt', u'318.swf.txt', u'319.swf.txt', u'320.swf.txt', u'321.swf.txt', u'322.swf.txt', u'323.swf.txt', u'324.swf.txt', u'325.swf.txt', u'326.swf.txt', u'327.swf.txt'], u'W': [u'339.swf.txt', u'340.swf.txt', u'341.swf.txt', u'342.swf.txt', u'343.swf.txt', u'344.swf.txt', u'345.swf.txt', u'346.swf.txt', u'347.swf.txt', u'348.swf.txt', u'349.swf.txt', u'350.swf.txt', u'351.swf.txt', u'352.swf.txt', u'353.swf.txt'], u'Y': [u'355.swf.txt', u'356.swf.txt', u'357.swf.txt', u'358.swf.txt', u'359.swf.txt'], u'X': [u'354.swf.txt'], u'Z': [u'360.swf.txt', u'361.swf.txt']}


class Entry(SQLObject):
    data = UnicodeCol(notNone=True)
    source = UnicodeCol(notNone=True)
    def alphaPos(self):
        if self.source in alphas:
            return alphas[self.source]
        else:
            return "A"
    def realSource(self):
        return ".".join(self.source.split(".")[:2])


def main():
    if len(sys.argv) != 2:
    	print "please provide a file to use"
    	sys.exit(1)
    f = open(sys.argv[1].strip())

    textRe = r"^[^#]+#[0-9A-Fa-f]{8}>(.*)$"
    allCaps = r"\b([A-Z][A-Z]+)\b"


    begin = False
    processText = False
    curr = []
    currLast = ""
    isFirst = True
    for line in f:
        if line.startswith("[021]"):
            processText = True
            continue
        if processText:
            if "---" in line:
                begin = False
                Entry(data = " ".join(curr), source = os.path.basename(sys.argv[1]))
                curr=[]
                processText=False
                isFirst=True
                continue
            result = re.match(textRe, line.strip())
            if result == None:
                sys.stderr.write("[" + sys.argv[1] + "] Error! Line: " + line + "\n")
                processText=False
                continue
            txt = result.group(1).strip()
            if isFirst:
                maybeLast = re.match(allCaps, txt.split()[0].strip())
                if maybeLast:
                    currLast = maybeLast.group(1)
                    curr.append(txt)
                else:
                    curr.append(currLast + " " + txt)
            else:
                curr.append(txt)
            processText = False
            isFirst = False
    Entry(data = " ".join(curr), source = os.path.basename(sys.argv[1]))
    f.close()
if __name__ == "__main__":
    main()
