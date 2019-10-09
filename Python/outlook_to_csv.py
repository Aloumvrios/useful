import win32com.client
import csv
import datetime


def main():

    # const=win32com.client.constants
    # olMailItem = 0x0
    # obj = win32com.client.Dispatch("Outlook.Application")
    # newMail = obj.CreateItem(olMailItem)
    # newMail.Subject = "I AM SUBJECT!!"
    # newMail.Body = "I AM\nTHE BODY MESSAGE!"
    # newMail.BodyFormat = 2 # olFormatHTML https://msdn.microsoft.com/en-us/library/office/aa219371(v=office.11).aspx
    # newMail.HTMLBody = "<HTML><BODY>Enter the <span style='color:red'>message</span> text here.</BODY></HTML>"
    # newMail.To = "nikolaos.nikolaou@something.com"
    # attachment1 = r"C:\Temp\example.pdf"
    # newMail.Attachments.Add(Source=attachment1)
    # newMail.display()
    # newMail.send()

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    inbox = outlook.GetDefaultFolder(6)
    # "6" refers to the index of a folder - in this case,
    # the inbox. You can change that number to reference
    # any other folder
    
    # create csv
    with open('attrition.csv', 'w') as my_csv:
        # define columns
        writer = csv.DictWriter(my_csv, fieldnames=["Date", "Surname", "Name", "Sex"])
        writer.writeheader()
        # iterate folder
        for message in inbox.Folders['attrition'].Items:
            # define format for date
            fmt = '%Y-%m-%d'  # ex. 20110104172008 -> Jan. 04, 2011 5:20:08pm
            date = message.ReceivedTime.date().strftime(fmt)
            # reformat mailItem format
            sender = str(message.SenderName)
            # split name from surname
            s_list = sender.split(",")
            # print(message)
            # print(message.ReceivedTime.date)
            # print(date)
            # print(sender)
            # write in rows
            mydict = {"Date": date, "Surname": s_list[0], "Name": s_list[1], "Sex": "yespliz"}
            writer.writerow(mydict)


if __name__ == "__main__":
    main()
