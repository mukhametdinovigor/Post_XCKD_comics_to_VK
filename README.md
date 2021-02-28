# Post XCKD's comics to VK.
This script downloading random XCKD's comic from [XKCD](https://xkcd.com) and publish it on the wall to 
your VK group.

### How to install.


Comics downloading does not require any keys. To upload comic you need vk access token and vk group id.

 - To get vk access token you need:
    - create application [here](https://vk.com/dev) and get its client_id. You can find out client_id by pressing
      button 'Редактировать' and you will see it in browser address bar.
    - follow the link - [Implicit Flow Procedure](https://vk.com/dev/implicit_flow_user)
 - To get group id follow the link [get group_id](https://regvk.com/id/). 

Put vk access token and vk group id into `.env` file, and assign vk access token to the `VK_ACCESS_TOKEN` variable, 
assign vk group id to the `VK_GROUP_ID` variable. Your group id should be with minus sign.

It should look like this:

```
VK_ACCESS_TOKEN='22043fd3dc99f242dd836b9adacb9ed16570f062a39c8ba9f12557d8b0d18b0e8279a6d2abb0c5f8'
VK_GROUP_ID='-202785554'
```

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Run script in command line:
```
python3 main.py
```
After successful posting you will get your post_id number in a console:

```
Your post_id - 15
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
