import dropbox
import api
import access_token
import picamera
from time import time, sleep, strftime
import urllib2


def dropbox_auth():
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(api.app_key, api.app_secret)
    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print '1. Go to: %s ' % authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    auth_code = raw_input("Enter the authorization code here: ").strip()

    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(auth_code)

    client = dropbox.client.DropboxClient(access_token)

    save_token(access_token)
    return client

def save_token(access_token):
    with open("access_token.py", "w") as access_token_file:
        access_token_file.write("key = '%s'" % access_token)

def can_connect_to_dropbox():
    try:
        urllib2.urlopen("http://www.dropbox.com")
        return True
    except urllib2.URLError:
        return False

def upload_to_dropbox(client, filename):
    if can_connect_to_dropbox():
        print "sending %s to dropbox" % filename
        with open(filename, 'rb') as f:
            client.put_file(filename, f)
        print "uploaded: %s" % filename
    else:
        print "Unable to connect to dropbox. No internet?"

def main():
    if access_token.key:
        client = dropbox.client.DropboxClient(access_token.key)
        print 'You are authorised!'
    else:
        client = dropbox_auth()

    with picamera.PiCamera() as camera:
        sleep(2)
        camera.resolution = (2000, 2000)
        camera.led = False
        camera.rotation = 180
        camera.awb_mode = 'off'
        camera.awb_gains = 1.9,1.45
        camera.iso = 100
        camera.shutter_speed = 15000
        camera.contrast = 80
        timestamp = strftime("%Y-%m-%d_%H-%M-%S")
        filename = 'plant_%s.jpg' % timestamp
        camera.brightness = 60
        camera.capture(filename)
        print 'Captured %s' % filename
        upload_to_dropbox(client, filename)


if __name__ == '__main__':
    main()
