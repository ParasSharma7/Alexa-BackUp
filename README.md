# Alexa-BackUp
A Alexa skill to back up your devices. You can add a new device  to back up or choose from the existing list of the devices to back up.

## Usage
0. Use `pip install -r requirements.txt` to install all dependencies (assuming you have Python).

1. Alexa shall backup all content present in the directory where this folder is stored. 

2. The working directory can be changed by editting the `settings.py` file.

3. It is advisable to have a default bucket to upload to. This can be set in the `bucket` file.

4. Ensure `cfg['B_BUCKET']` is modified.
