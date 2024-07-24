import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import smtplib

def send_email(new_content):
    retry = 3
    from_email = "florianparker2704@gmail.com"
    from_password = "Vt5&Rw9*Ym4#Zp2!"
    to_email = "grownupcharlie2312@gmail.com"

    msg = MIMEText(new_content)
    msg['Subject'] = "send mail"
    msg['From'] = from_email
    msg['To'] = to_email


    for attempt in range(retry):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print("Email sent successfully!")
            break
        except smtplib.SMTPException as e:
            print(f"SMTPException: {e}")
            if attempt < retry - 1:
                print("Retrying...")
            else:
                print("Failed to send email after several attempts.")
                raise
            
def send_slack_notification(new_content):
    webhook_url = "https://app.slack.com/client/T07BUNWH8TH/C07C96VAGTD"  # Replace with your Slack webhook URL
    payload = {
        "text": f"Webpage Update Notification: {new_content}"
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code != 200:
            raise ValueError(f"Request returned with an unexpected status: {response.status_code}")
        
        print("Notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
def fetch_and_parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    
    return None

def scrape_and_extract(url):
    
    soup = fetch_and_parse(url)
    result = []
    if soup is not None:
        sms_cards = soup.find_all(class_='sms-card')
        if len(sms_cards) >= 1:
            card = sms_cards[0]
            country = card.find(class_="sms-card__header")
            number = card.find(class_="sms-card__number")
            info_elements = card.find(class_="sms-card__info")
            card_data = {}
            if country: 
              card_data['country'] = country.get_text(strip=True)
            if number:
                a_tag = number.find('a')
                if a_tag:
                    card_data['number'] = a_tag.get_text(strip=True)
            if info_elements:
                items = info_elements.find_all(class_="sms-card__item")
                if len(items) >= 3:
                  date_items = items[2].find_all("p")
                  if len(date_items) >= 2:
                      card_data['added_date'] = date_items[1].get_text(strip=True)
            result.append(card_data)
    else:
        print("Failed to retrieve or parse the webpage")
    return result
def load_last_result(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None
def save_current_result(filepath, content):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
def main():
    url = "https://anonymsms.com/"  # Replace with the URL you want to scrape
    result_filepath = "last_result.txt"
    # while True:
    current_result = scrape_and_extract(url)
    current_result_str = str(current_result)
    last_result = load_last_result(result_filepath)
    if current_result_str != last_result:
        print("Change detected")
        # send_slack_notification(current_result_str)
        # send_email(current_result_str)
        save_current_result(result_filepath, current_result_str)
        print(current_result_str)
    else:
        print("No change detected.")
if __name__ == "__main__":
    main()