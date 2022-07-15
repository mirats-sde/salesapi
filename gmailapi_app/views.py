from django.http import HttpResponse
import base64
import os
import pickle
from django.http import HttpResponse
from django.shortcuts import render
# Gmail API utils
from Google import create_service
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
import json
from django.views.decorators.csrf import csrf_exempt
import os
SCOPES = ['https://mail.google.com/']
our_email = 'lokeshwaran.naidu@miratsinsights.com'
CLIENT_SECRET_FILE=os.path.join(os.getcwd(),"client.json")
API_NAME='gmail'
API_VERSION='v1'

# service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)




# Create your views here.

def index(req):
    return render(req,'gmailapi_app/index.html')


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

@csrf_exempt
def sendMail(req):
    body=req.body
    mail_obj=json.loads(body)
  
    # email_msg=mail_obj["message"]
    mimeMessage=MIMEMultipart()
    mimeMessage['to']=mail_obj['to']
    mimeMessage['subject']=f"""RFQ - QID#{mail_obj["opportunityID"]} - {mail_obj['supplier_company_name']} - MiratsInsights"""
    mimeMessage['cc']=mail_obj['cc']
    email_msg="""
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
    <style>
        @import url("https://fonts.googleapis.com/css?family=Google+Sans_old:100,200,300,400,500,700|Roboto:400,400italic,500,500italic,700,700italic|Roboto+Mono:400,500,700&amp;display=swap");

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Google Sans, Roboto, Arial, sans-serif;
        }

        .main_container {
            width: 100%;
        }

        .main_container img {
            object-fit: cover;
        }

        .intro {
            padding: 2em 0;
        }

        .intro_logo img {
            width: 20%;
            object-fit: cover;
        }


        .intro h1 {
            font-size: 20px;
        }

        .intro p {
            margin-top: 0.3em;
            font-size: 17px;
        }

        .countries {
            background: #F8F8F8;
            border-radius: 20px;
            padding: 1em;
            margin-bottom: 1em;
        }

        .countries p,
        .target_audience p {
            text-align: center;
            font-size: 17px;
            font-weight: 500;
        }

        .cards {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-right: 1em;
            /* gap: 1em; */
            margin-bottom: 1em;
            text-align: center;
        }

        .card_body {
            width: 30%;
            background: #F8F8F8;
            border-radius: 26px;
            padding: 2em;
            margin-right:1em;

        }

        .card_body h2 {
            font-weight: 700;
            font-size: 22px;
        }

        .card_body p {
            font-size: 18px;
        }

        .target_audience {
            background: #F8F8F8;
            border-radius: 20px;
            padding: 1em;
            margin-bottom:1em;
        }

        .details {
            margin: 2em 0;
            font-weight: 500;
            font-size: 18px;
            line-height: 1.4;
        }

        .below_details {
            margin-bottom: 1em;
        }


        .portal_details {
            margin-top: 1em;
            font-size: 18px;
            width: 80%;
        }

          .bid {
            background: #3F86F0;
            border-radius: 26px;
            width: 100%;
            border: none;
            margin: 1em 0;
            font-size: 18px;
            color: white;
            padding: 0.5em;
            cursor: pointer;
            display: block;
            /* display: flex;
            justify-content: center; */
            text-decoration: none;
        }
        .center{
            text-align:center;
            color:white;
        }
  

       

        .note {
            font-size: 16px;
        }

        .managed_by {
            margin-top: 1em;
            margin-bottom: 4em;
            font-size: 18px;
        }

        .order_details {
            font-size: 18px;
            margin-bottom: 1em;
            padding-left: 1em;
        }

        .order_details p {
            font-weight: 600;
        }

        .email_footer {
            padding: 2em 2em 4em 2em;
            background: #F8F8F8;
        }

        .regards {
            font-weight: 400;
            font-size: 18px;
            color: #5C5C5C;
        }

        .footer_logo {
            width: 200px;
            height: 150px;
        }

        .footer_logo img {
            width: 200px;
            /* width: 100%; */
            height: 100%;
            object-fit: cover;
        }

        .details_logo {
            display: flex;
            justify-content: space-between;
        }

        .email_footer p {
            line-height: 1.4;
        }

        .managed_by_details {
            margin-right: 22em;
        }

        .managed_by_details,
        .mobile a,
        .mobile p {
            font-weight: 400;
            font-size: 18px;
            color: #5C5C5C;
            text-decoration: none;
            line-height: 1.4;
        }

        .managed_by_details .name {
            font-weight: 600;
            margin-top: 1em;
        }

        .mobile {
            margin: 2em 0;
        }

        .policy_letter_container footer {
            background: #F8F8F8;
            padding: 3em;
            margin-top: 1em;
        }

        .copyright {
            font-weight: 400;
            font-size: 18px;
            line-height: 38px;
            color: #5C5C5C;
            margin-bottom: 1em;
        }

        .company_info {
            margin-top: 1em;
            font-weight: 400;
            font-size: 18px;
            color: #5C5C5C;
        }

        .footer_content p,
        .company_info a {
            font-weight: 400;
            font-size: 18px;
            color: #5C5C5C;
        }

        .company_info a {
            margin-right: 0.5em;
        }

        .reserved_policy {
            margin-top: 1em;
        }

        .portal_link,
        .mail,
        .links {
            color: #3f86f0;
            text-decoration: none;
        }

        .content {
            display: flex;
        }

        .left_content {
            width: 70%;
        }

        .right_content {
            width: 30%;
        }

        .container_img {
            margin-bottom: 4em;
        }

        .container_img img {
            width: 200px;
            height: 200px;
            object-fit: cover;
        }
          .card_body:last-child {
            margin-right: 0;
        }

        @media (max-width:450px) {
            .right_content {
                padding-right: 1em;
                word-wrap: break-word;
            }
                    .managed_by_details {
                margin-right: 2em;
            }

            .intro_logo img {
                width: 50%;
                object-fit: cover;
            }

            .footer_logo img {
                width: 150px;
            }
            .managed_by_details {
                margin-right: 3em;
            }

            .container_img img {
                width: 150px;
                height: 150px;
                object-fit: cover;
            }

            .cards {
                display: block;
                margin-right: 0;
            }

            .card_body {
                width: 100%;
                margin-bottom: 1em;
            }

            .footer_logo {
                width: 100px;
                height: 100px;
                object-fit: cover;
            }

        }
    </style>

</head>

<body>

    <div class="main_container">
        <div class="content">
            <div class="left_content">
                <div class="container">
                    <div class="left_container">
                        <section class="intro_logo">
                            <img src="https://firebasestorage.googleapis.com/v0/b/mirats-fulcrum.appspot.com/o/SalesManagement%2FRough%2FImages%2Fmiratsinsights_logo%20(2).png?alt=media&token=e128e98f-2620-462c-9f1f-5f9bfdaf40fc"
                                alt="logo">
                        </section>
                        <section class="intro">
                            <h1>Hey """+ mail_obj['bid_contact_name'] +"""!</h1>
                            <h1>We've a new project for you!</h1>
                            <p>Please provide pricing, feasibility and field time for the following study. </p>
                        </section>
                    </div>

                </div>
                <div class="cards_order_container">

                    <div class="cards_container">
                    <section class="target_audience">
                            <p>Target Audience - """+ mail_obj['target_audience'] +"""</p>
                        </section>

                        """ + mail_obj["tableData"] + """
                        
                        <section class="details">
                            
                         
                            <p class="below_details"> Simplified Details (of what is given above) :</p>
                            <p>Target Audience : """+ mail_obj['target_audience'] +"""</p><br/>
                            """+ mail_obj['smallTableData'] +"""
                        </section>

                        <p class="portal_details">Please share your best quote. You can provide your quote directly from
                            our
                            <a href='https://supplier.miratsinsights.com/opportunity/"""+ mail_obj["opportunityID"] +"""' class="portal_link"> Supe (Supplier Portal)</a> — by clicking the button given
                            below you
                            can quote on this project or reply to this email.
                        </p>


                         <a href='https://supplier.miratsinsights.com/opportunity/"""+ mail_obj["opportunityID"] +"""' class="bid">
                              <p class="center">Bid Now</p>
                            </a>

                        <p class="note">Please Note - Always loop in
                            <a class="mail" href="mailto:vendors@miratsinsights.com">vendors@miratsinsights.com </a>
                            while
                            sending your quote.
                        </p>
                        <p class="managed_by">This project is managed by """+mail_obj["sales_manager"]["full_name"]+""" <a href='mailto:"""+mail_obj['sales_manager']['email'] +"""'>( """+ mail_obj['sales_manager']['email'] +""" )</a>
                            if you
                            have any questions you can reply to this email, or use our
                            <a class="links" href="https://supplier.miratsinsights.com"> Mirats Supe (our supplier portal — that’s
                                for you only)</a> to get quick response from our sales team and manage bids efficiently.
                        </p>
                    </div>

                </div>
            </div>

            <!-- right side -->
            <div class="right_content">
                <section class="container_img">
                    <img src="https://firebasestorage.googleapis.com/v0/b/mirats-fulcrum.appspot.com/o/SalesManagement%2FRough%2FImages%2Fnamaste_mail.png?alt=media&token=5062c9e3-87ad-4e8e-ae14-f669493cf90b"
                        alt="">
                </section>

                <div class="order">
                    <section class="order_details">
                        <span>Order ID</span>
                        <p>#"""+ mail_obj["opportunityID"] +"""</p>
                    </section>
                    <section class="order_details">
                        <span>Sales Manager</span>
                        <p>"""+ mail_obj["sales_manager"]["full_name"] +"""</p>
                    </section>
                    <section class="order_details">
                        <span>Study Type</span>
                        <p>"""+ mail_obj["study_type"] +"""</p>
                    </section>
                    <section class="order_details">
                        <span>Survey Type</span>
                        <p>"""+ mail_obj["survey_type"] +"""</p>
                    </section>
                    <section class="order_details">
                        <span>Device Allowed</span>
                        <p>"""+ mail_obj['devices'] +"""</p>
                    </section>
                </div>
            </div>
        </div>

        <footer class="email_footer">
            <p class="regards">Best Regards,</p>
            <div class="details_logo">
                <section class="managed_by_details">
                    <h3 class="name">""" + mail_obj["sales_manager"]["full_name"] + """</h3>
                    <p>"""+ mail_obj["sales_manager"]["position"] +""", """+ mail_obj["sales_manager"]["teamname"] +""",</p>
                    <p>"""+ mail_obj['sales_manager']['department'] +""" /"""+ mail_obj['sales_manager']["division"] +"""</p>
                    <p>Skype ID : """+ mail_obj['sales_manager']["skype_id"] +""" </p>
                </section>
                <section class="footer_logo">
                    <img src="https://firebasestorage.googleapis.com/v0/b/mirats-fulcrum.appspot.com/o/SalesManagement%2FRough%2FImages%2Fmiratsinsights_logo.png?alt=media&token=24c84374-91ca-4f39-b9c3-9fb39e611382"
                        alt="">
                </section>

            </div>
            <section class="mobile">
                <p>Mobile: """ + mail_obj['sales_manager']['mobile_no'] +  """</p>
                <p><a href='mailto:"""+mail_obj['sales_manager']['email'] +"""'>Email: """+ mail_obj['sales_manager']['email'] +"""</a></p>
                <p><a href="http://www.miratsinsights.com/"> Website: http://www.miratsinsights.com/</a></p>
            </section>
            <section class="footer_content">
                <h3 class="copyright">TM and © 2021 Mirats Insights, LLC. All rights reserved.</h3>
                <p>Mirats Insights Private Limited </p>
                <p>Office No 7022, 1Aerocity NIBR Corporate Park</p>
                <p>Nr Sakinaka Junction, Safed Pul, Mumbai,</p>
                <p>Maharashtra 400 072 India</p>
            </section>
            <section class="company_info">
                <p>CIN: U72900UP2021PTC153917.</p>
                <p>GSTIN: 27AAPCM0779A1ZD.</p>
                <p class="reserved_policy">All Rights Reserved <span>|</span> Privacy Policy</p>
            </section>
        </footer>
    </div>
</body>

</html>
    """
    mimeMessage.attach(MIMEText(email_msg,'html'))
    raw_string=base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message=service.users().messages().send(userId='me',body={'raw':raw_string}).execute()
    print(message)
    return HttpResponse(json.dumps({"success":True}))