

import json,boto3,random,datetime

passcodeBucketName = 'passcode-iiitd'
backupBucketName='backup-iiitd'
id_key = ''
sec_key = ''
def lambda_handler(event, context):
    #credentials.txt contains AWS credentials for reading and writting to buckets 'backup-iiitd' and 'passcode-iiitd'
    fil = open('credentials.txt','r')
    id_key = fil.readline()[:-1]
    sec_key = fil.readline()
    s3_c = boto3.client('s3', aws_access_key_id = id_key, aws_secret_access_key = sec_key)
    s3_r = boto3.resource('s3', aws_access_key_id = id_key, aws_secret_access_key = sec_key)
    print('savit',id_key,sec_key)
    #if event["session"]["new"]:
    #    on_session_started({"requestId": event["request"]["requestId"]}, event["session"])
    
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"],s3_c,s3_r)
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
        
def gen_code():
    letter="abcdefghijklmnopqrstuvwxyz"
    hashc=[]
    for q in range(8):
        hashc.append(random.randint(0,25))
    passcode=""
    for w in hashc:
        passcode+=letter[w]
    return passcode 

def addDots(s):
    ret =''
    for i in s:
        ret += i + '. '
    return ret[:-2]
    
def on_session_started(session_started_request, session):
    print("Starting new session.")
def on_launch(launch_request, session):
    return get_welcome_response()
def on_session_ended(session_ended_request, session):
    print("Ending session.")
    # Cleanup goes here...
    
def on_intent(intent_request, session,s3_c,s3_r):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "backUpDevice":
        return get_backUp_message(session['user'],intent,s3_r)
    elif intent_name == "addDevice":
        return get_addDevice_message(session["user"],intent,s3_r)
    elif intent_name == "showDeviceList":
        return get_deviceList(session["user"],s3_c)
    elif intent_name == "getDeviceName":
        return get_addDevice_message(session["user"],intent,s3_r)
    
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.RepeatIntent":
        return repeat_pass(session)
    else:
        print(intent_name)
        raise ValueError("Invalid intent" + intent_name)
        
        
def handle_session_end_request():
    card_title = "Thanks"
    speech_output = "Thank you for using the BackMeUp skill.  See you next time!"
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "BackMeUp"
    speech_output = "Welcome to BackMeUp. " \
                    "You can ask me to backup existing devices, or add new device on AWS"
    reprompt_text = "Please tell me backup exisisting devices " \
                    "for example backup my devicename."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def get_backUp_message(user,intent,s3_r):
    session_attributes = {}
    card_title = "Backup system"
    reprompt_text = ""
    should_end_session = False
    userId=user["userId"]
    if(intent["confirmationStatus"]=='NONE'):
        speech_output="Confirm your intent to backup " + str(intent["slots"]["deviceName"]["value"])
        return build_response(session_attributes, build_speechlet_response_confirm(
        card_title, speech_output, reprompt_text, should_end_session)) 
    
    speech_output="backing up device " + str(intent["slots"]["deviceName"]["value"])
    
    curdate = datetime.datetime.now()
    filBody = str(curdate).encode("utf-8")
    s3_path = userId + '-' + intent["slots"]["deviceName"]["value"] +'.txt'
    s3_r.Bucket(backupBucketName).put_object(Key=s3_path, Body=filBody)
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def get_addDevice_message(user,intent,s3_r):
    session_attributes = {}
    reprompt_text = ""
    card_title = "Add device Status"
    should_end_session = False
    print(intent['slots'])
    try:
        deviceName = intent["slots"]["deviceName"]["value"]
    except:
        print('here')
        speech_output = "Please speak the name of the device to be added, say the name of my device is : followed by the device name"
        
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
    userId=user["userId"]
    userId.replace('.','')
    filBody = (userId + '-' + deviceName).encode("utf-8")
    passcode = gen_code()
    s3_path = passcode + '.txt'
    s3_r.Bucket(passcodeBucketName).put_object(Key=s3_path, Body=filBody)
    s3_path = userId + '-' + deviceName
    s3_path.replace('.','')
    s3_path += '.txt'
    curdate = datetime.datetime.now(datetime.timezone.utc)
    filBody = str(curdate).encode('utf-8')
    s3_r.Bucket(backupBucketName).put_object(Key=s3_path, Body=filBody)
    spoken = '<say-as interpret-as="spell-out">' +  str(passcode) + '</say-as>'
    speech_output = "open the script in your device to add device and enter this passcode in it " + spoken
    session_attributes['passcode'] = spoken
    reprompt_text = ' the passcode is ' + spoken
    return build_response(session_attributes, build_speechlet_response_SSML(
        card_title, speech_output, reprompt_text, should_end_session))

def get_deviceList(user,s3_c):
    
    
    ret = ''
    userId=user["userId"]
    len1 = len(userId)
    for key in s3_c.list_objects(Bucket=backupBucketName)['Contents']:
        if(userId in key['Key']):
            
            ret += key['Key'][len1 + 1:-4] +  ', '
       
    
    session_attributes = {}
    card_title = "B"
    reprompt_text=''
    should_end_session = False
    if(ret == ''):
        speech_output = "there are no devices"
        
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    speech_output = "the devices are : "  + ret
    

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def repeat_pass(session):
    card_title = "LastPasscode"
    should_end_session = False
    reprompt_text = ''
    session_attributes = session['attributes']
    try:
        speech_output = session_attributes['passcode']
        reprompt_text = speech_output
        return build_response(session_attributes, build_speechlet_response_SSML(
        card_title, speech_output, reprompt_text, should_end_session))
    except:
        speech_output = 'there seems to be no passcode here, please try adding the device again'
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

    
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_speechlet_response_SSML(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": "<speak>" + output + '</speak>'
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "SSML",
                "ssml":"<speak>" + reprompt_text + '</speak>'
            }
        },
        "shouldEndSession": should_end_session
    }
def build_speechlet_response_confirm(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },

 
        "shouldEndSession": should_end_session,
        "directives": [
        {
            "type": "Dialog.ConfirmIntent",
            
        }
        ]
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }