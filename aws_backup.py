import boto3
import botocore
import os
import os.path
from os import path
import sys
import argparse
import hashlib
from pathlib import Path
from settings import cfg
###################################################################################################
# Program variables
###################################################################################################
if(cfg['CWD']=='DEFAULT'):
	cwd = get_cwd()
else:
	cwd = cfg['CWD']
###################################################################################################
# End user variables
###################################################################################################
proxy_c = boto3.client(
		's3',
	    aws_access_key_id = 'AKIAIK5MTANAEZARXJIQ',
	    aws_secret_access_key = '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',
	    #aws_session_token=SESSION_TOKEN,
		)
proxy_r = boto3.resource(
		's3',
	    aws_access_key_id = 'AKIAIK5MTANAEZARXJIQ',
	    aws_secret_access_key = '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',
	    #aws_session_token=SESSION_TOKEN,
		)
s3_c = boto3.client(
		's3',
	    aws_access_key_id = 'AKIAJON5HWX7WVBLPTXQ',
	    aws_secret_access_key = '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',
	    #aws_session_token=SESSION_TOKEN,
		)
s3_r = boto3.resource(
		's3',
	    aws_access_key_id = 'AKIAJON5HWX7WVBLPTXQ',
	    aws_secret_access_key = '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',
	    #aws_session_token=SESSION_TOKEN,
		)

###################################################################################################
# End user interactions
###################################################################################################
# The User's actual bucket for storage.
def add_update_new_device(bucket):
	last_update = '0000'
	passcode = input('Please enter your 8 letter passcode: ')
	account = read_object(proxy_r, 'passcode-iiitd', passcode+".txt")
	print('account', account)
	if_backup = read_object(proxy_r, 'backup-iiitd', account+".txt")
	if(if_backup>last_update):
		sync(s3_c, s3_r, bucket)
		set_user_timestamp('user', if_backup)
		set_user_account('user', account)
	else:
		print('Already up to date...')

def update_device(bucket):
	timestamp = get_user_timestamp('user1')
	account = get_user_account('user1')
	if_backup = read_object(proxy_r, 'backup-iiitd', account+".txt")
	if(if_backup>last_update):
		sync(s3_c, s3_r, bucket)
		set_user_timestamp('user1', if_backup)
		set_user_account('user1', account)
	else:
		print('Already up to date...')	
###################################################################################################
# s3 User Managment
###################################################################################################
def if_new_user(name, ID, key):
	old_file_path = save_old_dir()
	_path = cwd+"\\"+name
	if not path.exists(_path):
		os.makedirs(_path)
		os.chdir(_path)	
		make_cred_file(ID, key)
	reset_working_dir(old_file_path)

def make_cred_file(ID, key):
	f = open("credentials", "w")
	f.write("[default]\naws_access_key_id = "+ID+"\naws_secret_access_key = "+key)
	f.close()
	f = open("config", "w")
	f.write("[default]\nregion = us-west-2\noutput = json")
	f.close()

# String input - user id
def get_user_cred(input):
	old_file_path = save_old_dir()
	os.chdir(cwd+'\\'+input)
	f = open('credentials', 'r')
	id_key = []
	if f.mode=='r':
		contents = f.readlines()
	for s in contents:
		if 'aws_access_key_id' in s or 'aws_secret_access_key' in s:
			a = s.split(" = ")
			print(a)
			a = a[1]
			a = a.replace("\n", "")
			id_key.append(a)

	#print(id_key)	
	#print(os.getcwd())
	print("Resetting working dir...")
	reset_working_dir(old_file_path)
	return id_key

def get_user_timestamp(input):
	old_file_path = save_old_dir()
	os.chdir('C:\\Users\\dell\\.aws\\'+input)
	with open('timestamp.txt', 'r') as f:
		timestamp = f.readlines()
	print("Resetting working dir...")
	reset_working_dir(old_file_path)
	return timestamp

def set_user_timestamp(input, timestamp):
	old_file_path = save_old_dir()
	os.chdir(cwd'\\'+input)
	with open('timestamp.txt', 'w') as f:
		f.write(timestamp)
	print("Resetting working dir...")
	reset_working_dir(old_file_path)

def get_user_account(input):
	old_file_path = save_old_dir()
	os.chdir('C:\\Users\\dell\\.aws\\'+input)
	with open('account.txt', 'r') as f:
		account = f.readlines()
	print("Resetting working dir...")
	reset_working_dir(old_file_path)
	return account

def set_user_account(input, account):
	old_file_path = save_old_dir()
	os.chdir('C:\\Users\\dell\\.aws\\'+input)
	with open('account.txt', 'w') as f:
		f.write(account)
	print("Resetting working dir...")
	reset_working_dir(old_file_path)

###################################################################################################
# s3 Utility
###################################################################################################
def set_client(input):
	client = boto3.client(
	's3',
    aws_access_key_id = id_key[0],
    aws_secret_access_key = id_key[1],
    #aws_session_token=SESSION_TOKEN,
	)
	return client

def set_resource(input):
	resource = boto3.resource(
    's3',
    aws_access_key_id = id_key[0],
    aws_secret_access_key = id_key[1],
    #aws_session_token=SESSION_TOKEN,
	)
	return resource
# input from save_old_dir
def reset_working_dir(input):
	os.chdir(input)
	print(os.getcwd())

def get_cwd():
	return os.getcwd()

def get_bucket_list():
	for bucket in s3.buckets.all():
		print(bucket.name)

def read_object(s3, bucket, key):
	obj = s3.Object(bucket, key)
	obj = obj.get()['Body'].read().decode('utf-8')
	#print(obj)
	return obj

# String input
def save_old_dir():
	return os.getcwd()
###################################################################################################
# Sync files from root directory
###################################################################################################
def sync(s3_c, s3_r, bucket):
	print("Syncing...")
	old_file_path = save_old_dir()
	# traverse root directory, and list directories as dirs and files as files
	#bucket = s3.Bucket(bucket)
	for root, dirs, files in os.walk(get_cwd()+"\\test_folder"):
		print('root', root)
		print('dirs', dirs)
		print('files', files)
		path = root.split(os.sep)
		print((len(path) - 1) * '---', os.path.basename(root))
		for file in files:
			#print(len(path) * '---', file)
			print(path,file)
			file_path = root
			f = open(root+"\\"+file, 'r')
			with open(root+"\\"+file, 'r'):	
				#print(path+file)
				contents = f.read()
				print('Checking if file has been modified...')
				check_and_update(s3_c, s3_r, file, contents, bucket, file_path)
	print("Synced!")
	reset_working_dir(old_file_path)

# md5 checksum has 5GB file limit.
def check_and_update(s3_c, s3_r, file, contents, bucket, file_path):
	#print('bucket', bucket)
	md5_file = hashlib.md5(contents.encode()).hexdigest()
	print('md5_file', md5_file)

	if(search_bucket(s3_r, file, bucket)):
		md5_bucket = get_bucket_md5(s3_c, file, bucket)
		print('md5_bucket', md5_bucket)
		if(md5_file!=md5_bucket):
			print('Updating files...')
			print('File_path:', file_path)
			upload(s3_r, file, bucket, file_path)
		else:
			print('File not modified!')
	else:
		print('Updating files...')
		print('File_path', file_path)
		upload(s3_r, file, bucket, file_path)

def get_bucket_md5(s3_c, file, bucket):
    key = s3_c.head_object(Bucket = bucket, Key = file)
    #print(key)
    s3_etag = key['ETag'].strip('"').strip("'")
    return s3_etag

def search_bucket(s3_r, file, bucket):
	try:
	    s3_r.Object(bucket, file).load()
	except botocore.exceptions.ClientError as e:
	    if e.response['Error']['Code'] == "404":
	        # The object does not exist.
	        print("404 Not found...")
	    else:
	        # Something else has gone wrong.
	        print("Well, shit.")
	        raise
	    return False
	else:
	    # The object does exist.
	    return True
###################################################################################################
# File Transfering
###################################################################################################
# Note resource not client..
def upload(s3, filename, bucket, file_path):
	old_file_path = save_old_dir()

	os.chdir(file_path)
	print("Uploading...")
	s3.meta.client.upload_file(filename, bucket, filename)
	print("Done uploading!")

	reset_working_dir(old_file_path)

# Uses resource...
def download(s3, filename, bucket):
	old_file_path = save_old_dir()

	download_dir = 'C:\\Users\\dell\\Downloads'
	reset_working_dir(download_dir)
	try:
		print('Downloading...')
		s3.Bucket(bucket).download_file(filename, filename)
		print('File downloaded!')
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
		else:
			raise

	reset_working_dir(old_file_path)
###################################################################################################
# Pending
###################################################################################################
def bucket_details(s3, bucket):
	pass
def list_buckets():
	pass
def make_bucket():
	pass
def parse_id_key():
	pass	
###################################################################################################
# Main Program
###################################################################################################
def parse_args():
	parser = argparse.ArgumentParser()

	# Set default profile for uploading? Last used account...
	parser.add_argument('--user', dest='user',
						default='default', type=str)
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	
	args = parse_args()

	print('Called with args:')
	print(args)


	"""
	id_key = get_user_cred(args.user)
	s3_c = set_client(id_key)
	s3_r = set_resource(id_key)
	for bucket in s3_r.buckets.all():
		print(bucket.name)
	"""
	#upload(s3_r, 'test_upload_2.txt', 'passcode-iiitd', get_cwd())
	#download(s3_r, 'passcode-userb.txt', 'passcode-iiitd')
	#print("Syncing...")
	#sync(s3_c,s3_r,'bucketiiitd')
	#print("Synced!")
	#if_new_user('priyam', '22', 'B)
	add_update_new_device('bucketiiitd')