import email
from email.header import decode_header
import re
import string
import os
# from pylibpff import container # pip install pylibpff, for .pst files, figure out how to install
# from pylibpff import errors
# from pylibpff import file
# from win32com import client # pip install pywin32, for .msg files, figure out how to install

# read .eml files and separate header (subject, sender, links), text, and attachments
def read_eml(input):
    with open(input, "r", encoding="utf-8", errors="ignore") as file:
        email_text = file.read()

    # Parse the email
    msg = email.message_from_string(email_text)

    # Initialize variables to store decoded subject and sender
    subject, sender = "", ""

    has_attachments = False

    # Decode subject if available
    if msg["subject"]:
        subject, encoding = decode_header(msg["subject"])[0]
        if encoding:
            subject = subject.decode(encoding)

    # Decode sender if available
    if msg["from"]:
        sender, encoding = decode_header(msg["from"])[0]
        if encoding:
            sender = sender.decode(encoding)

    if msg["X-MS-Has-Attach"]:
        if msg["X-MS-Has-Attach"] == "yes":
            has_attachments = True

    # Extract email content (plain text and HTML)
    email_content = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset()
            if charset:
                email_content += payload.decode(charset)
            else:
                # If charset is not available, use UTF-8 as a fallback
                email_content += payload.decode("utf-8", errors="ignore")

    # Extract links from email_content using a comprehensive regex pattern
    links = re.findall(r'https?://\S+|www\.\S+|ftp://\S+|ftps?://\S+|mailto:\S+|\b(?:[a-z]+://\S+)', email_content)


    # Clean the email content to remove non-printable characters
    email_content = "".join(filter(lambda x: x in string.printable, email_content))

    return subject, sender, links, email_content, has_attachments

# Function to read .pst files and separate header (subject, sender, links) and text
def read_pst(input):
    subjects, senders, links, email_contents = [], [], [], []

    try:
        pst_file = file()
        pst_file.open(input)

        # Iterate over all folders in the PST file
        for folder in pst_file.get_root_folder().get_folders():
            for email_object in folder.get_sub_messages():
                subject = email_object.get_subject()
                sender = email_object.get_sender_name()
                email_content = email_object.get_plain_text_body()

                # Extract links from email_content using a comprehensive regex pattern
                links = re.findall(r'https?://\S+|www\.\S+|ftp://\S+|ftps?://\S+|mailto:\S+|\b(?:[a-z]+://\S+)', email_content)

                # Clean the email content to remove non-printable characters
                email_content = "".join(filter(lambda x: x in string.printable, email_content))

                subjects.append(subject)
                senders.append(sender)
                links.append(links)
                email_contents.append(email_content)

        return subjects, senders, links, email_contents

    except errors.PFFError as e:
        print(f"Error reading PST file: {e}")
    finally:
        if pst_file:
            pst_file.close()

# Function to read .msg files and separate header (subject, sender, links) and text
def read_msg(input):
    
    outlook = client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    msg = namespace.OpenSharedItem(input)

    subjects, senders, links, email_contents = [], [], [], []

    # If the item is a collection (e.g., multiple emails in one .msg file)
    if msg.Class == 43:
        for item in msg.Items:
            subject, sender, links, email_content, _ = read_eml(item)
            subjects.append(subject)
            senders.append(sender)
            links.append(links)
            email_contents.append(email_content)
    else:
        subject, sender, links, email_content, _ = read_eml(input)
        subjects.append(subject)
        senders.append(sender)
        links.append(links)
        email_contents.append(email_content)

    return subjects, senders, links, email_contents

# Function to read .mbox files and separate header (subject, sender, links) and text
def read_mbox(input):
    subjects, senders, links, email_contents = [], [], [], []

    with open(input, "r", encoding="utf-8", errors="ignore") as mbox_file:
        email_text = mbox_file.read()

    email_text = email_text.split("From ")
    email_text = [x for x in email_text if x]

    for email_str in email_text:
        msg = email.message_from_string("From " + email_str)

        subject, sender, links, email_content, _ = read_eml(email_str)
        subjects.append(subject)
        senders.append(sender)
        links.append(links)
        email_contents.append(email_content)

    return subjects, senders, links, email_contents

def read_email(input):
    file_extension = os.path.splitext(input)[1].lower()
    if file_extension == ".eml":
        return read_eml(input)
    elif file_extension == ".msg":
        return read_msg(input)
    elif file_extension == ".pst":
        return read_pst(input)
    elif file_extension == ".mbox":
        return read_mbox(input)
    else:
        raise ValueError("Unsupported file format: {}".format(file_extension))
    

# TODO: handle attachments, other metadata from emails, link in text same as actual link
# TODO: add some other features to the model (e.g., sender, links, attachments, etc.)