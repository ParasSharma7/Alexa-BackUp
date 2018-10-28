# Alexa-BackUp
A Alexa skill to back up your devices. You can add a new device  to back up or choose from the existing list of the devices to back up.

## Usage
You are required to leave the `backup.py` script running in the background. The script will periodically ping AWS and check for a backup instruction. 

First time users are required to enter the passcode in the GUI console as mentioned below. Details will be stored on file.

## User Settings
0. Use `pip install -r requirements.txt` to install all dependencies (assuming you have Python).

1. Alexa shall backup all content present in the directory where this folder is stored. 

2. The working directory can be changed by editting `cfg['CWD']` in the `settings.py` file.

3. The download directory can be changed by editting `cfg['DOWNLOAD']` in the `settings.py` file.

4. It is advisable to have a default bucket to upload to. This can be set in the `.\user\bucket` file.

## GUI 
1. Create a IAM account. For help, refer to [this document](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).

2. Get your Access Key, Secret Access Key and Bucket Name. The Bucket name will come from your AWS s3 account, and AWS Access Key and Secret Key from your AWS IAM.

3. Run backup.py .

4. Fill the ID (IAM access key), Access Key (IAM secret key) and Bucket Name with them respectively.

5. Say to Alexa, `"Back me up"`.

6. If you are backing up a new device, ask Alexa to `"Add a new device"`.

7. Say to Alexa, `"The device name is {device Name}"`.

8. If you are backing up a existing device, say `"Backup {device name}"`

9. Run `backup.py` and fill in details of your AWS credentials and s3 storage bucket.

10. Enter the Passcode given by Alexa in the Passcode field.

11. Submit the request.
