import os
import sys
script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'api', 'backend_lambda_python' )
sys.path.append( mymodule_dir )
from backend.handler import lambda_handler as bh

# REQUEST_NO:
	# 0 - 3 : codebuild interfaces
	# 10 - 12 : class interfaces
	# 20 - 25 : user interfaces
	# 30 - 33 : problem interfaces
	# 100 + prev nubmer : test interfaces


def userInterface(request_no, user_list):
	get_user = {
	  "request_no": 21,
	  "user_id":"user1",
	  "uid_to_get":""
	}

	add_user_list = {
	  "request_no": 23,
	  "user_id":"user1",
	  "new_users":[]
	}

	delete_user_list = {
	  "request_no": 24,
	  "user_id":"user1",
	  "del_users":[]
	}

	context = {}

	if(request_no == 21):
		for user in user_list:
			event = get_user
			event['uid_to_get'] = user['new_user_id']
			print(bh(event, context))
	elif (request_no == 23):
		event = add_user_list
		event['new_users'] = user_list
		print(bh(event, context))
	elif(request_no == 24):
		event = delete_user_list
		tmp_list = []
		for user in user_list:
			tmp_item = {}
			tmp_item['del_user_id'] = user['new_user_id']
			tmp_item['del_cog_id'] = 'example_tmp'
			tmp_list.append(tmp_item)
		event['del_users'] = tmp_list
		print(bh(event, context))



def classInterface(request_no, class_list):
	add_class={
	  "request_no": 10,
	  "user_id": "user1",
	  "new_class_id":"class1",
	  "end_date":"04-22-2022",
	  "problem_sets":["test-problems"],
	  "contest_sets":["test-problems"],
	  "students":["user2"]
	}

	get_class={
	  "request_no": 11,
	  "user_id": "user1",
	  "cid_to_get": "class1"
	}

	delete_class={
	  "request_no": 12,
	  "user_id":"user1",
	  "del_class_id":"class1"
	}


	context = {}

	for cl in class_list:

		if(request_no == 10):
			event = add_class
			event['user_id'] = cl['user_id']
			event['new_class_id'] = cl['class_id']
			event['end_date'] = cl['end_date']
			event['problem_sets'] = cl['problem_sets']
			event['contest_sets'] = cl['contest_sets']
			event['students'] = cl['students']
			print(bh(event, context))
		elif (request_no == 11):
			event = get_class
			event['cid_to_get'] = cl['class_id']
			print(bh(event, context))
		elif(request_no == 12):
			event = delete_class
			event['del_class_id'] = cl['class_id']
			print(bh(event, context))
		

def problemInterface(request_no, problem_list):
	add_problem_set={
	  "request_no": 30,
	  "user_id":"backend_test_user1",
	  "problem_set": "test-problems",
	  "end_date": "f"
	}

	get_problem_set={
	  "request_no": 31,
	  "user_id":"backend_test_user1",
	  "problem_set":"test-problems"
	}

	delete_problem_set={
	  "request_no": 32,
	  "user_id": "backend_test_user1",
	  "problem_set": "test-problems"
	}

	get_problem_by_id={
	  "request_no": 33,
	  "user_id": "backend_test_user1",
	  "problem_id": "test-problems/test-5"
	}

	for p in problem_list:

		if(request_no == 30):
			event = add_problem_set
			event['problem_set'] = p['problem_set']
			event['end_date'] = p['end_date']
			event['classroom_id'] = p['classroom_id']
			event['professor_id'] = p['professor_id']
			print(bh(event, context))
		elif (request_no == 31):
			event = get_problem_set
			event['problem_set'] = p['problem_set']
			print(bh(event, context))
		elif(request_no == 32):
			event = delete_problem_set
			event['problem_set'] = p['problem_set']
			print(bh(event, context))
		elif(request_no == 33):
			event = get_problem_by_id
			event['problem_set'] = p['problem_set']
			print(bh(event, context))

if __name__ == "__main__":

	# event = {"request_no": 500}
	context = {}
	# print(bh(event, context))

	user_list = [
	    {
	      "new_user_id":"AnonBear",
	      "new_user_classrooms": ["COSC10104:IntroToProgramming"],
	      "new_user_group":"student",
	      "new_user_email": "dylanwulfson@gmail.com",
	      "is_test" : False
	    }
	]
	# print(userInterface(23, user_list))

	class_list = [
		{
		  	"class_id":"COSC10104:IntroToProgramming",
		  	"user_id": "KrishnaKadiyala",
		  	"end_date":"05-08-2022",
		  	"problem_sets":["test-problems"],
		  	"contest_sets":["test-contest"],
		  	"students":["AnonGirrafe","AnonAngel","AnonFish","AnonBear","AnonPinapple","AnonGecko"]
		}
	]

	print(classInterface(10, class_list))


	problem_list = [
		{
		  	"problem_set":"test-problems",
		  	"problem_id":"test-problems/test-0",
		  	"end_date":"05-08-2022",
		  	"classroom_id": "COSC10104:IntroToProgramming",
		  	"professor_id": "KrishnaKadiyala"
		}
	]

	# print(problemInterface(30, problem_list))


