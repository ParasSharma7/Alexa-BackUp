import json,boto3
def read_object(s3, bucket, key):
	obj = s3.Object(bucket, key)
	obj = obj.get()['Body'].read().decode('utf-8')
	#print(obj)
	return obj

def lambda_handler(event, context):
    #credentials.txt contains AWS credentials for reading and writting to buckets 'backup-iiitd' and 'passcode-iiitd'
    fil = open('credentials.txt','r')
    id_key = fil.readline()[:-1]
    sec_key = fil.readline()
    proxy_r = boto3.resource('s3', aws_access_key_id = 'AKIAIK5MTANAEZARXJIQ',aws_secret_access_key = '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',)
    passcode = event['queryStringParameters']['passcode']
    account = read_object(proxy_r, 'passcode-iiitd', passcode+".txt")
    if(account != event['queryStringParameters']['account']):
        return {
        "statusCode": 200,
        "body": json.dumps('The account ID does not match')
        }
    
    date = read_object(proxy_r, 'backup-iiitd' , account + '.txt')
    
    
    return {
        "statusCode": 200,
        "body": json.dumps(date)
    }
