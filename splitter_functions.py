from __future__ import print_function
import pickle
import os.path
import glob, os
import pdftotext
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from apiclient import errors
from apiclient import http
import io
import sys
import PyPDF2
import send_email
import tempfile
from googleapiclient.http import MediaIoBaseDownload



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.appdata','https://www.googleapis.com/auth/drive']
SUCCESS = 0
FAIL = -1
main_directory = "/tmp/pdfs"

def convert_pdf_to_txt(pdf_path, debug, log_file):
    pdfFileObj = open(pdf_path,'rb')
    #The pdfReader variable is a readable object that will be parsed
    with open(os.devnull, "w") as fp:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj, warndest=fp)
    #discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    names = []
    count = 0
    text = ""
    #The while loop will read each page
    os.system("pdftotext downloaded.pdf")
    filepath = 'downloaded.txt'
    getNextLine = False
    getTwoLines = False
    i = 0
    with open(filepath, encoding='utf-8') as fp:
        for line in fp:
            if getNextLine:
                if(len(line) > 1):
                   # print(line)
                    if "FRGP-" in line:
                        #print("case success")
                        names.append(line[line.index("FRGP-"):].rstrip())
                        getNextLine = False
                        continue
                    else:
                        #print("doesn't ecist")
                        getNextLine = True
                        continue
                if "Please make checks" in line:
                    #print("case suceeded")
                    getNextLine = False
                    names.append("Unidentified" + str(i))
                    i = i+1
                    #print("Unidentified")
                    continue
            if ("PO/ Contract Number" in line) or ("P/O Contract" in line)  or ("Contract Number" in line) or ("PO/Contract" in line):
                if(len(line) > 1):
                    try:
                        if(line.index("FRGP-")):
                            newLine = line[line.index("FRGP-"):]
                            names.append(newLine.rstrip())
                            #print(newLine.rstrip())
                    except ValueError:
                        #print("Failed")
                        getNextLine = True
        return names






def pdf_split(names):
    #try:
    infile = PdfFileReader(open('downloaded.pdf', 'rb'))
    for i in range(infile.getNumPages()):
        p = infile.getPage(i)
        outfile = PdfFileWriter()
        outfile.addPage(p)
        filename = main_directory+'/'+names[i]+'.pdf'
        try:
            with open(filename, 'wb') as f:
                outfile.write(f)
        except IOError:
            return "failed to open file %s %s"%(filename, sys.exc_info()), FAIL
    return "succeeded to pdf_split", SUCCESS
    #except:
'''        #        try: 
        infile = PdfFileReader(open('downloaded.pdf', 'rb'))
        #return "Failed to open PDFFileReader", FAIL
        count = 0
        for i in range(infile.getNumPages()):
#            return str(infile.getNumPages()), FAIL
            p = infile.getPage(i)
            outfile = PdfFileWriter()
            outfile.addPage(p)
            filename = main_directory+'/Unidentified'+str(i)+'.pdf'
            try:
                with open(filename, 'wb') as f:
                    outfile.write(f)
            except IOError:
                return "failed to open file", FAIL
        return "suceeded to pdf split", SUCCESS
    #except:    
     #           return "pdf_split failed", FAIL'''
            
def split_pdf_file(path, month, year, log_file, debug):
    """
    """
#    year = str(year).strip()
#    month = str(month).strip()
    creds = get_creds()
    service = build('drive', 'v3', credentials=creds)

    filename = os.path.splitext(path)[0]
    filename = os.path.split(filename)[1]
    if debug:
        log_file.write(filename)
    try: 
        os.mkdir(main_directory)
    except FileExistsError:
        pass
    except: 
        return "unable to mkdir directory named %s %s"%(main_directory, sys.exc_info()), year, FAIL

    names = convert_pdf_to_txt(path, debug, log_file)
    if debug:
        log_file.write("    split_pdf_file: file_name = %s\n"%names)
    message, status = pdf_split(names)
    if status == FAIL:
        return message, year, status
    parent_folder = "1s8NxVCzRL8DwndZAm07dD9wtPysmYjsv"
    folder_id = ''
    if(year == "2019"):
        folder_id = "1Rh-LmLJhadFwXtYiXCTS32w-he_BjTLM"
        year = "2019-2020"
    elif(year == "2020"):
        folder_id = "1xt-8GBY7aTdlyJo9XyR1m8o1kwWXFFFl"
        year = "2020-2021"
    elif(year == "2021"):
        folder_id = "1jvO-Qd-ZbtSWG8RYx-DIda4JCXzmpu2Z"
        year = "2021-2022"
    elif(year == "2022"):
        folder_id = "1uyLba5jHbUhxf35d6I3Uc-4YFi3YM4uu"
        year = "2022-2023"
    elif(year =="2023"):
        folder_id = "1C3A2C7xBxEmNUU1htYwuBMWvzW8POmwy"
        year = "2023-2024"    
    
    folder_metadata = {
    'name': month,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [folder_id]
    }
#    try:
    folder=service.files().create(body=folder_metadata,fields='webViewLink,id').execute()
    folder_id = folder.get('id')
 #   except:
 #       folder = service.files().create(fields='webViewLink,id').execute()
 #       folder_id = folder.get('id')
    if debug:
        log_file.write("    split_pdf_file: folder = %s\n"%folder.get('webViewLink'))

    for file_name in glob.glob(main_directory+"/*.pdf"):
        if debug:
            log_file.write("    split_pdf_file: file_name = %s\n"%file_name)
        file_metadata = {'name': os.path.split(file_name)[1],'parents': [folder_id]}
        media = MediaFileUpload(file_name,
                        mimetype='application/pdf', resumable=True)
        service.files().create(body=file_metadata, fields='id',
                                    media_body=media).execute()
        if debug:
            log_file.write("    split_pdf_file: File ID: %s added\n" % file_metadata.get('name'))
    try:
        shutil.rmtree(main_directory)
    except:
        return "error removing directory %s" %(main_directory), FAIL
    return folder.get('webViewLink'), year, SUCCESS

def get_creds():
    """Reconstitute the credentials that are stored in the token.pickle file.
       If the file doesn't exist, ask the user for credentials.
       Return the credentials.
       The file token.pickle stores the user's access and refresh tokens, and is
       created automatically when the authorization flow completes for the first
       time.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def fetch_and_split_file(file_id, year, month, log_file, debug):
    """Shows basic usage of the Drive
    """
    if debug:
        log_file.write("  fetch_and_split_file: called\n")
    creds = get_creds()
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO('downloaded.pdf', mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if debug:
            log_file.write("  fetch_and_split_file: Download %d%%.\n" % int(status.progress() * 100))
    link, year, status = split_pdf_file("downloaded.pdf", month, year, log_file, debug)
    send_email.send_email(link, year, month)
    if debug:
        log_file.write("  fetch_and_split_file: returning\n")
    return link, status
