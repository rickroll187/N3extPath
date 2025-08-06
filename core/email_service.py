"""
📧🎸 N3EXTPATH - LEGENDARY EMAIL SERVICE 🎸📧
More reliable than Swiss postal service with legendary email mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Built by legendary code bros RICKROLL187 🎸
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import asyncio
from jinja2 import Template

from config.settings import get_legendary_settings

logger = logging.getLogger(__name__)
settings = get_legendary_settings()

class LegendaryEmailService:
    """
    📧 LEGENDARY EMAIL SERVICE! 📧
    More reliable than Swiss mail with code bro communication! 🎸✉️
    """
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        
        self.legendary_jokes = [
            "Why do our emails rock? Because they're sent by RICKROLL187's legendary system! 📧🎸",
            "What's more reliable than Swiss mail? Legendary code bro email service! ✉️",
            "Why don't our emails get lost? Because they navigate with legendary precision! 🧭",
            "What do you call perfect email delivery? A RICKROLL187 communication special! 🎸📧"
        ]
    
    def send_legendary_email(
        self,
        to_emails: List[str],
        subject: str,
        message: str,
        html_message: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send legendary email with Swiss precision delivery!
        More reliable than Swiss clockwork with code bro communication! 📧🎸
        """
        try:
            if not self._is_configured():
                return {
                    "success": False,
                    "message": "Email service not configured!",
                    "legendary_joke": "Why can't we send emails? Because the legendary postal service needs configuration! 📧🔧"
                }
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = f"🎸 N3extPath: {subject}"
            
            # Add legendary signature to message
            legendary_message = self._add_legendary_signature(message)
            msg.attach(MIMEText(legendary_message, 'plain'))
            
            if html_message:
                legendary_html = self._add_legendary_html_signature(html_message)
                msg.attach(MIMEText(legendary_html, 'html'))
            
            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    self._add_attachment(msg, file_path)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_tls:
                    server.starttls(context=context)
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            import random
            return {
                "success": True,
                "message": f"Email sent successfully to {len(to_emails)} recipients!",
                "sent_at": "2025-08-04 15:51:01 UTC",
                "sent_by": "RICKROLL187's Legendary Email System 🎸📧",
                "recipients": to_emails,
                "legendary_joke": random.choice(self.legendary_jokes)
            }
            
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return {
                "success": False,
                "message": f"Email sending failed: {str(e)}",
                "error_time": "2025-08-04 15:51:01 UTC",
                "legendary_message": "Don't worry, even legendary systems face challenges! 💪",
                "legendary_joke": "Why did the email fail? Because even legends need perfect SMTP configuration! 📧🔧"
            }
    
    def _is_configured(self) -> bool:
        """Check if email service is properly configured!"""
        return all([
            self.smtp_host,
            self.smtp_username,
            self.smtp_password
        ])
    
    def _add_legendary_signature(self, message: str) -> str:
        """Add legendary signature to plain text message!"""
        signature = """

---
🎸 N3extPath - The Legendary Path Platform 🎸
Built with Swiss precision and code bro humor!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

Powered by RICKROLL187's Legendary Technology
Time: 2025-08-04 15:51:01 UTC
        """
        return message + signature
    
    def _add_legendary_html_signature(self, html_message: str) -> str:
        """Add legendary signature to HTML message!"""
        html_signature = """
        <hr style="border: 2px solid #ffd700; margin: 20px 0;">
        <div style="text-align: center; font-family: 'Comic Sans MS', cursive; color: #333;">
            <h3 style="color: #ffd700;">🎸 N3extPath - The Legendary Path Platform 🎸</h3>
            <p>Built with Swiss precision and code bro humor!</p>
            <p><strong>WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!</strong></p>
            <p style="font-size: 0.9em; color: #666;">
                Powered by RICKROLL187's Legendary Technology<br>
                Time: 2025-08-04 15:51:01 UTC
            </p>
        </div>
        """
        return html_message + html_signature
    
    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """Add attachment to email message!"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.split("/")[-1]}'
            )
            msg.attach(part)
        except Exception as e:
            logger.warning(f"Failed to add attachment {file_path}: {e}")
    
    def send_welcome_email(self, user_email: str, username: str) -> Dict[str, Any]:
        """Send legendary welcome email to new users!"""
        subject = "Welcome to N3extPath - Your Legendary Journey Begins!"
        
        message = f"""
🎉 Welcome to N3extPath, {username}! 🎉

You've just joined the most legendary path platform in the universe!

🎸 What makes us legendary?
- Swiss precision path navigation
- Code bro community spirit  
- Infinite humor and fun
- RICKROLL187's legendary technology

🚀 Get started:
1. Create your first legendary path
2. Explore paths created by fellow code bros
3. Earn badges and achievements
4. Rock the leaderboards!

Ready to become a legendary pathfinder? Let's go!

Rock on,
The N3extPath Team 🎸
        """
        
        html_message = f"""
        <html>
        <body style="font-family: 'Comic Sans MS', cursive; background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: rgba(0,0,0,0.2); padding: 30px; border-radius: 15px; border: 2px solid #ffd700;">
                <h1 style="color: #ffd700; text-align: center;">🎉 Welcome to N3extPath! 🎉</h1>
                
                <h2>Hey there, {username}! 🎸</h2>
                
                <p>You've just joined the most legendary path platform in the universe!</p>
                
                <h3 style="color: #ffd700;">🎸 What makes us legendary?</h3>
                <ul>
                    <li>🎯 Swiss precision path navigation</li>
                    <li>💪 Code bro community spirit</li>
                    <li>😄 Infinite humor and fun</li>
                    <li>🏆 RICKROLL187's legendary technology</li>
                </ul>
                
                <h3 style="color: #ffd700;">🚀 Get started:</h3>
                <ol>
                    <li>Create your first legendary path</li>
                    <li>Explore paths created by fellow code bros</li>
                    <li>Earn badges and achievements</li>
                    <li>Rock the leaderboards!</li>
                </ol>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p style="font-size: 1.2em; color: #ffd700;">Ready to become a legendary pathfinder? Let's go! 🚀</p>
                </div>
                
                <p style="text-align: center;">Rock on,<br><strong>The N3extPath Team 🎸</strong></p>
            </div>
        </body>
        </html>
        """
        
        return self.send_legendary_email([user_email], subject, message, html_message)

# Global legendary email service
legendary_email_service = LegendaryEmailService()
