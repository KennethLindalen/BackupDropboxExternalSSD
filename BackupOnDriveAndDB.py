import sys
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

TOKEN = ''
FOLDER_CHOICE=''
FOLDER_TO_UPLOAD='/Users/kenneth/Documents/arbeidsplass/forOpplastning/'
FOLDER_TO_MOVE_UPLOAD_FOLDER='/Users/kenneth/Documents/arbeidsplass/harBlittOpplastet/'
DRIVE_PATH='/Volumes/NO\ NAME'
FILE_LIST=[]
dbx = dropbox.Dropbox(TOKEN)

#Lager liste over alle filene i FOLDER_TO_UPLOAD/FOLDER_CHOICE
def fileLooper():
    for root, dirs, files in os.walk(FOLDER_TO_UPLOAD + FOLDER_CHOICE):  
        for filename in files:
            print(filename)
            FILE_LIST = []
            FILE_LIST.append(filename)


#MOpplastnings og send til drive metode
def upload():
    fileLooper()
    print("Upload")
    for i in FILE_LIST:
        with open(i, 'rb') as f:
            print("Laster opp " + f + " til Dropbox...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Kan ikke laste opp; ikke nok plass i dropbox mappen")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

        os.system("mv " + FOLDER_TO_UPLOAD + " " + DRIVE_PATH)
        os.system("mv " + FOLDER_TO_UPLOAD + " " + FOLDER_TO_MOVE_UPLOAD_FOLDER)


if __name__ == '__main__':
    # Ser om access token er oppgitt
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Access token eksisterer ikke")

    # Sjekk om access token fungerer
    try:
        dbx.users_get_current_account()
    except AuthError:
        sys.exit("ERROR: Access token fungerer ikke, prov aa opprett en ny token")
        
    fileLooper()
    FOLDER_CHOICE = input("Mappenavn paa mappen du vil laste opp: ")

    upload()