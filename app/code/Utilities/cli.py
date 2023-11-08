import argparse
from app.code.Utilities.classify import classify_email, classify_url
from email_modeling.read_email import read_email

def cli():
    parser = argparse.ArgumentParser(description="Phishing Detector")
    parser.add_argument("-f", "--file", help="Check a file for phishing.")
    parser.add_argument("-u", "--url", help="Check a URL for phishing.")
    args = parser.parse_args()

    if args.file:
        # check if file exists

        subject, sender, links, email_content, has_attachments = read_email(args.file)
        # print(subject)
        # print(sender)
        # print(len(email_content))
        # print(len(links))
        # print(has_attachments)
        is_phishing = classify_email(email_content)
        if is_phishing:
            print("This file may be a phishing attempt!")
        else:
            print("This file is safe.")
    elif args.url:
        is_phishing = classify_url(args.url)
        if is_phishing:
            print("This URL may be a phishing attempt!")
        else:
            print("This URL is safe.")
    else:
        print("Please specify a file or URL to check for phishing.")

if __name__ == "__main__":
    cli()
