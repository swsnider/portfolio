
import cherrypy
import datetime

def session(name, default, replacement=None):
	# If not in session, use default
	if name not in cherrypy.session:
		cherrypy.session[name] = default
	# If replacement given, use replacement
	if replacement is not None:
		cherrypy.session[name] = replacement
	return cherrypy.session[name]

def shaded(num):
	if int(num) % 2 == 0:
		return {'style':'background-color: #eee'}
	else:
		return {'style':None}
		
def color(val):
	if val == '#':
		return {'class':'error_score'}
	else:
		return {'class':'score'}

def percent(score, possible, na):
	score = float(score)
	possible = float(possible)
	na = float(na)
	return int(round(score / (possible - (2 * na)) * 100))

def scorePossible(category, level):
	if category == 'Cognitive':
		return 184
	elif category == 'Social-Communication':
		return 98
	elif category == 'Social':
		return 66
	elif category == 'Adaptive':
		return 78
	elif category == 'Fine Motor':
		return 28
	elif category == 'Gross Motor':
		return 36	

# VALI-DATE & HELPER FUNCTIONS
def validate(parts):
	for i in [0,1,2]:
		if parts[i][0] + parts[i][1] + parts[i][2] != 1:
			return False
		if parts[0][i] + parts[1][i] + parts[2][i] != 1:
			return False
	return True
	
def resolveDateParts(parts):
	for i in [0,1,2]:
		for j in [0,1,2]:
			if parts[i][j] == 1:
				row = [0,1,2]
				row.remove(i)
				col = [0,1,2]
				col.remove(j)
				if parts[row[0]][j] + parts[row[1]][j] == 0:
					parts[i][col[0]] = 0
					parts[i][col[1]] = 0
				if parts[i][col[0]] + parts[i][col[1]] == 0:
					parts[row[0]][j] = 0
					parts[row[1]][j] = 0
	return parts	

def evalDatePart(part):
	part = str(part)
	if len(part) == 4 or int(part) > 31:
		return [0,0,1]
	if int(part) > 12:
		return [0,1,1]
	return [1,1,1]

def dateString(month, day, year):
	month = int(month)
	day = int(day)
	year = str(year)
	if len(year) == 2 and int(year) > 50:
		year = "19" + year
	if len(year) == 2 and int(year) <= 50:
		year = "20" + year
	if len(year) == 3:
		year = "2" + year
	return datetime.date(int(year),month,day)

def valiDate(date):
	print type(date)
	start = 0;
	end = 0;
	getting = False
	nums = []
	for i in range(len(date)):
		if date[i].isdigit() and getting:
			end = i
		elif date[i].isdigit():
			start = i
			getting = True
		elif getting:
			end = i
			nums.append(date[start:end])
			getting = False
	if getting:
		nums.append(date[start:])
	
	today = datetime.date.today()
	year = today.year
	month = today.month
	day = today.day
	
	for num in nums:
		if len(num) > 4:
			return None
	
	if len(nums) == 0:
		return dateString(month,day,year)
	elif len(nums) == 1:
		return None
	elif len(nums) in [2,3]:
		if len(nums) == 2:
			nums.append(str(year))
		num0 = evalDatePart(nums[0])
		num1 = evalDatePart(nums[1])
		num2 = evalDatePart(nums[2])
		res = resolveDateParts([num0,num1,num2])
		
		if not validate(res):
			if res[0][0] == 1 and res[1][1] == 1 and res[2][2] == 1:
				month = nums[0]
				day = nums[1]
				year = nums[2]
				return dateString(month,day,year)
			else:
				return None
			
		for i in [0,1,2]:
			if res[i][0] == 1:
				month = nums[i]
			elif res[i][1] == 1:
				day = nums[i]
			else:
				year = nums[i]
		
		return dateString(month,day,year)
	else:
		return None
		
		