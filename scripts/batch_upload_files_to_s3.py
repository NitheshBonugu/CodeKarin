import os
import boto3

MODE = 'UPLOAD' # upload files to specified s3 bucket
# MODE = 'DEBUG' # print local file path to objects to upload

# add boto3 aws interface for python s3
s3 = boto3.resource('s3')

# define bucket name to upload
bucket = 'karin-longterm-storage-bucket'
# other config INCLUDING KEY ACCESS TO AWS AND REGION should be specified in ~./aws/config

# path to search for files to upload
path = '../problems/test-contest'

# prefix to remmove from the path is s3
prefix = '../problems/'

# recursive function to print KARIN formatted problem files to s3 resources
def print_files_in_path(path, depth):
	# problem format for KARIN problems has a maximum depth of 6, assuming the path specified is the name of a problem_set
	if depth > 6:
		return
	# search all file in the top level path
	if os.path.isdir(path): 
		files = os.listdir(path)
		# if no deeper levels return
		if(files == []):
			return
		# for each file get the path name (from THIS path)
		for f in files:
			ret = path + '/'
			ret = ret + f
			# remove the '../' from the front of the path
			temp = ret.replace(prefix, '')
			# check if the file has an extension (i.e. '.java' / '.json' / etc.)
			if '.' in temp:
				# print file paths to upload
				if(MODE == 'DEBUG'):
					print(temp)
				# upload files to s3 bucket
				elif(MODE == 'UPLOAD'):
					s3.Bucket(bucket).upload_file(ret, temp)
			# recursive call
			print_files_in_path(path + '/' + f, depth + 1)

# initial call
print_files_in_path(path, 0)
