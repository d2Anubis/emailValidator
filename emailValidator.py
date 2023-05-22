import streamlit as st
import re
import smtplib
import dns.resolver

# Create an input box for text
default_email = "abcdefg@gmail.com"
user_input = st.text_input("Enter email_id", default_email)

def validate_email(email):    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    domain = email.split('@')[1]
    try:        
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange.to_text()
        with smtplib.SMTP() as server:
            server.set_debuglevel(0)
            server.connect(mx_record)
            server.helo(server.local_hostname)
            server.mail('test@example.com')
            code, _ = server.rcpt(email)
            return code == 250
    except (dns.resolver.NXDOMAIN, smtplib.SMTPConnectError):
        return False

# Display the output on the screen
st.write("Output: ", validate_email(user_input))