# Alexa-BackUp
An Alexa skill to back up your devices. You can add a new device  to back up or choose from the existing list of the devices to back up.

## Usage
You are required to leave the `Alexa Backup` script running in the background. The script will periodically ping AWS and check for a backup instruction. 

First time users are required to enter the passcode in the GUI console as mentioned below. Details will be stored on file. Afterwards, the script will start automatically when ever the user logs in his computer. You can also manually restart the script by opening/executing the `BackMeUp.bat` file.

The code is a proof of concept, and will work properly on Windows OS only.

## User Settings
0. Use `pip install -r requirements.txt` to install all dependencies (assuming you have Python).

1. Alexa shall backup all content present in the directory where this folder is stored. 

2. The working directory can be changed by editting `cfg['CWD']` in the `settings.py` file.

3. The download directory can be changed by editting `cfg['DOWNLOAD']` in the `settings.py` file.

4. It is advisable to have a default bucket to upload to. This can be set in the `.\user\bucket` file.

## GUI 
1. Create a IAM account. For help, refer to [this document](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).

2. Get your Access Key, Secret Access Key and Bucket Name. The Bucket name will be from your AWS s3 account, and AWS Access Key and Secret Key will be from your AWS IAM.

3. Open/Execute `BackMeUp.bat`.

4. Fill the Access Key, Secret Key and Bucket Name fields with the above respectively.

5. Say to Alexa, `"Back me up"`.

6. If you are backing up a new device, ask Alexa to `"Add a new device"`.

7. Say to Alexa, `"The device name is {device Name}"`.

8. If you are backing up a existing device, say `"Backup {device name}"`

9. Enter the Passcode given by Alexa in the Passcode field.

10. Submit the request.
