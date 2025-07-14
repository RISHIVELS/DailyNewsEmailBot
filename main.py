import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()

# load credentials from dotenv files
sender_email_name = os.getenv('EMAIL_USER')
sender_password = os.getenv("EMAIL_PASS")
api_key = os.getenv("NEWS_API_KEY")
receiver_email_name = os.getenv('RECEIVER_EMAIL')
# Gather news using api

def gather_news():
    url = f'''https://gnews.io/api/v4/search?q=technology&lang=en&country=in&max=10&apikey={api_key}'''
    with requests.get(url) as response:
        news = []
        data = json.loads(response.text)
        articles = data["articles"]

        for i in range(len(articles)):
            title = articles[i]['title']
            description = articles[i]['description']
            url = articles[i]['url']
            news.append({'title':title,'description':description,'url':url})

    return news

# create a html template

def generate_html():
    articles = gather_news()
    html = """
    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9;">
        <h2 style="color: #2c3e50;">🗞️ Morning News Digest</h2>
    """
    for article in articles:
        html += f"""
        <div style="margin-bottom: 20px; padding: 15px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h3 style="margin-bottom: 10px; font-size: 18px; color: #2980b9;">
                <a href="{article['url']}" target="_blank" style="text-decoration: none; color: #2980b9;">
                    {article['title']}
                </a>
            </h3>
            <p style="margin: 0; font-size: 14px; color: #555;">{article['description']}</p>
        </div>
        """
    html += "</div>"
    return html


# send an email

def send_news_email():
    sender_email = sender_email_name
    receiver_email = receiver_email_name
    password = sender_password
    subject = "📰 Daily News"
    html_content = generate_html()

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)


send_news_email()