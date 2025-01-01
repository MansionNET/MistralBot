#!/usr/bin/env python3
"""
MansionNet MistralBot
An IRC bot that provides AI assistance using the Mistral AI API with rate limiting,
customizable prompt templates, and improved message handling.
"""

import socket
import ssl
import time
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, deque
import requests
from typing import Dict, List, Optional

class RateLimiter:
    def __init__(self, requests_per_minute: int, requests_per_day: int):
        self.requests_per_minute = requests_per_minute
        self.requests_per_day = requests_per_day
        self.minute_window = deque()
        self.day_window = deque()
    
    def can_make_request(self) -> bool:
        now = datetime.now()
        
        # Clean up old requests
        while self.minute_window and self.minute_window[0] < now - timedelta(minutes=1):
            self.minute_window.popleft()
        while self.day_window and self.day_window[0] < now - timedelta(days=1):
            self.day_window.popleft()
        
        return (len(self.minute_window) < self.requests_per_minute and 
                len(self.day_window) < self.requests_per_day)
    
    def add_request(self):
        now = datetime.now()
        self.minute_window.append(now)
        self.day_window.append(now)

class UserQuota:
    def __init__(self, daily_limit: int):
        self.daily_limit = daily_limit
        self.usage: Dict[str, List[datetime]] = defaultdict(list)
    
    def can_make_request(self, user: str) -> bool:
        now = datetime.now()
        user_requests = self.usage[user]
        
        # Clean up old requests
        while user_requests and user_requests[0] < now - timedelta(days=1):
            user_requests.pop(0)
        
        return len(user_requests) < self.daily_limit
    
    def add_request(self, user: str):
        self.usage[user].append(datetime.now())

class MistralBot:
    def load_api_key(self) -> Optional[str]:
        """Load API key from .env file"""
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('MISTRAL_API_KEY='):
                        return line.split('=')[1].strip().strip("'").strip('"')
        except Exception as e:
            print(f"Error loading API key: {str(e)}")
            return None

    def __init__(self):
        # Load API key
        api_key = self.load_api_key()
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("MISTRAL_API_KEY")
            
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in .env file or environment variables")
            
        # IRC Configuration
        self.server = "irc.example.com"
        self.port = 6697  # SSL port
        self.nickname = "MistralBot"
        self.channels = ["#help", "#welcome"]
        
        # Rate Limiting
        self.rate_limiter = RateLimiter(
            requests_per_minute=10,
            requests_per_day=1000
        )
        
        # User Quotas
        self.user_quota = UserQuota(daily_limit=50)
        
        # Prompt Templates
        self.prompt_templates = {
            "default": "You are a helpful assistant. Provide clear, direct responses without unnecessary detail. Question: {query}",
            "code": "You are a programming teacher. First give a ONE-SENTENCE explanation. Then after 'CODE:', show simple, practical code examples with minimal comments. Keep both explanation and code concise. Question: {query}",
            "explain": "Explain this concept in 2-3 short, clear sentences: {query}"
        }
        
        # SSL Configuration
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def connect(self) -> bool:
        """Establish connection to the IRC server"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.irc = self.ssl_context.wrap_socket(sock)
            
            print(f"Connecting to {self.server}:{self.port}...")
            self.irc.connect((self.server, self.port))
            
            self.send(f"NICK {self.nickname}")
            self.send(f"USER {self.nickname} 0 * :MansionNet AI Assistant Bot")
            
            buffer = ""
            while True:
                temp = self.irc.recv(2048).decode("UTF-8")
                buffer += temp
                
                if "PING" in buffer:
                    ping_token = buffer[buffer.find("PING"):].split()[1]
                    self.send(f"PONG {ping_token}")
                
                if "001" in buffer:  # RPL_WELCOME
                    for channel in self.channels:
                        self.send(f"JOIN {channel}")
                        time.sleep(1)
                    return True
                
                if "Closing Link" in buffer or "ERROR" in buffer:
                    return False
                
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def send(self, message: str):
        """Send a raw message to the IRC server"""
        try:
            self.irc.send(bytes(f"{message}\r\n", "UTF-8"))
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    def send_message(self, target: str, message: str, is_code: bool = False):
        """Send a message to a channel or user with proper line handling"""
        try:
            # Remove any markdown formatting
            message = message.replace("```python", "")
            message = message.replace("```", "")
            message = message.replace("`", "")

            # Prefix format - just use the bot's nickname
            prefix = f"{self.nickname}: "

            if is_code:
                # Split into explanation and code parts
                parts = message.split('CODE:', 1)
                
                # Send explanation
                explanation = parts[0].strip()
                if explanation:
                    self.send(f"PRIVMSG {target} :{prefix}{explanation}")
                    time.sleep(0.5)
                
                if len(parts) > 1:
                    # Process code part
                    code = parts[1].strip()
                    # Replace newlines with a separator for IRC
                    code_lines = [line.strip() for line in code.split('\n') if line.strip()]
                    
                    # Group code lines into reasonable chunks
                    chunk_size = 4  # Number of lines per message
                    for i in range(0, len(code_lines), chunk_size):
                        chunk = ' | '.join(code_lines[i:i + chunk_size])
                        if chunk:
                            self.send(f"PRIVMSG {target} :{prefix}Code: {chunk}")
                            time.sleep(0.5)
            else:
                # Handle regular text messages
                remaining = message
                max_length = 400 - len(prefix) - 10  # Extra safety margin
                
                while remaining:
                    if len(remaining) <= max_length:
                        self.send(f"PRIVMSG {target} :{prefix}{remaining}")
                        break
                    
                    # Find break point
                    split_point = max_length
                    for sep in ['. ', '? ', '! ', '; ', ', ', ' ']:
                        last_sep = remaining.rfind(sep, 0, max_length)
                        if last_sep > max_length // 2:
                            split_point = last_sep + 1
                            break
                    
                    current_chunk = remaining[:split_point].rstrip()
                    remaining = remaining[split_point:].lstrip()
                    
                    self.send(f"PRIVMSG {target} :{prefix}{current_chunk}")
                    if remaining:
                        prefix = f"{self.nickname}: ..."
                    time.sleep(0.5)
                    
        except Exception as e:
            print(f"Error sending message: {e}")
            self.send(f"PRIVMSG {target} :Error: Message delivery failed.")

    def get_mistral_response(self, prompt: str, template: str = "default") -> Optional[str]:
        """Get a response from Mistral AI API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "mistral-tiny",
                "messages": [
                    {"role": "user", "content": self.prompt_templates[template].format(query=prompt)}
                ],
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Mistral AI API: {str(e)}")
            return None

    def handle_command(self, sender: str, target_channel: str, message: str):
        """Handle bot commands"""
        try:
            if not self.rate_limiter.can_make_request():
                self.send_message(target_channel, "Rate limit exceeded. Please try again later.")
                return
                
            if not self.user_quota.can_make_request(sender):
                self.send_message(target_channel, f"{sender}: You have reached your daily query limit.")
                return
            
            if message.startswith("!ask "):
                query = message[5:].strip()
                response = self.get_mistral_response(query)
                
            elif message.startswith("!code "):
                query = message[6:].strip()
                response = self.get_mistral_response(query, template="code")
                
            else:
                return
            
            if response:
                self.rate_limiter.add_request()
                self.user_quota.add_request(sender)
                self.send_message(target_channel, response, is_code=message.startswith("!code "))
            else:
                self.send_message(target_channel, f"{sender}: Sorry, I couldn't generate a response.")
                
        except Exception as e:
            print(f"Error handling command: {str(e)}")
            self.send_message(target_channel, f"{sender}: An error occurred processing your request.")

    def run(self):
        """Main bot loop"""
        while True:
            try:
                if self.connect():
                    buffer = ""
                    
                    while True:
                        try:
                            buffer += self.irc.recv(2048).decode("UTF-8")
                            lines = buffer.split("\r\n")
                            buffer = lines.pop()
                            
                            for line in lines:
                                print(line)  # Debug output
                                
                                if line.startswith("PING"):
                                    ping_token = line.split()[1]
                                    self.send(f"PONG {ping_token}")
                                
                                # Improved PRIVMSG handling
                                if "PRIVMSG" in line:
                                    # Extract sender
                                    sender = line.split("!")[0][1:]
                                    
                                    # Extract channel and message using proper IRC message format
                                    # Format is typically: :sender!user@host PRIVMSG #channel :message
                                    try:
                                        # Split only on first PRIVMSG to handle messages containing "PRIVMSG"
                                        msg_parts = line.split("PRIVMSG ", 1)[1]
                                        # Split on first : to separate channel from message
                                        target_channel, message = msg_parts.split(":", 1)
                                        target_channel = target_channel.strip()
                                        message = message.strip()
                                        
                                        if target_channel in self.channels:
                                            if message.startswith(("!ask ", "!code ")):
                                                self.handle_command(sender, target_channel, message)
                                            elif message == "!help":
                                                help_msg = ("MistralBot Commands: "
                                                          "!ask <question> - Ask a general question | "
                                                          "!code <question> - Get programming help | "
                                                          "!help - Show this help message")
                                                self.send_message(target_channel, help_msg)
                                    except IndexError as e:
                                        print(f"Error parsing PRIVMSG: {e}")
                                        continue
                        
                        except UnicodeDecodeError:
                            buffer = ""
                            continue
                            
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                time.sleep(30)
                continue

if __name__ == "__main__":
    bot = MistralBot()
    bot.run()
