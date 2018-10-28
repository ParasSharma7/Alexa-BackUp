# Alexa-BackUp
A Alexa skill to back up your devices. You can add a new device  to back up or choose from the existing list of the devices to back up.

## User Settings
0. Use `pip install -r requirements.txt` to install all dependencies (assuming you have Python).

1. Alexa shall backup all content present in the directory where this folder is stored. 

2. The working directory can be changed by editting the `settings.py` file.

3. It is advisable to have a default bucket to upload to. This can be set in the `bucket` file.

4. Ensure `cfg['B_BUCKET']` is modified. The value under it is a bucket meant to store timestamps of previous backups.


## GUI 
1. Create a IAM account.

2. Get your Access Key, Secret Access Key and Bucket Name.

3. Fill the ID, Access Key and Bucket Name with them respectively.

4. Say to Alexa, "Back me up".

5. If you are backing up a new device, ask Alexa to "Add a new device".

6. Say to Alexa, "The device name is {device Name}"

7. Enter the Passcode given by Alexa in the Passcode field.

8. Submit the request.
