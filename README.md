# Alexa-BackUp
A Alexa skill to back up your devices. You can add a new device  to back up or choose from the existing list of the devices to back up.

## User Settings
0. Use `pip install -r requirements.txt` to install all dependencies (assuming you have Python).

1. Alexa shall backup all content present in the directory where this folder is stored. 

2. The working directory can be changed by editting `cfg['CWD']` in the `settings.py` file.

3. The download directory can be changed by editting `cfg['DOWNLOAD']` in the `settings.py` file.

4. It is advisable to have a default bucket to upload to. This can be set in the `.\user\bucket` file.

## GUI 
1. Create a IAM account.

2. Get your Access Key, Secret Access Key and Bucket Name.

3. Run backup.py .

4. Fill the ID, Access Key and Bucket Name with them respectively.

5. Say to Alexa, `"Back me up"`.

6. If you are backing up a new device, ask Alexa to `"Add a new device"`.

7. Say to Alexa, `"The device name is {device Name}`"

8. Enter the Passcode given by Alexa in the Passcode field.

9. Submit the request.
