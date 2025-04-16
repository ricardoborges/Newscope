import requests
from typing import Optional, Dict, Any

class Telegram:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{token}'

    def send_message(
        self,
        message: str,
        chat_id: Optional[str] = None,
        parse_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        if not chat_id and not self.default_chat_id:
            raise ValueError("No chat_id provided or configured")
            
        url = f'{self.base_url}/sendMessage'
        
        params = {
            'chat_id': chat_id or self.default_chat_id,
            'text': message
        }
        
        if parse_mode:
            params['parse_mode'] = parse_mode
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error sending message: {str(e)}')
            raise

    def get_updates(self) -> Dict[str, Any]:
        url = f'{self.base_url}/getUpdates'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error getting updates: {str(e)}')
            raise

if __name__ == '__main__':
    # Constants
    TOKEN = '7220989732:AAF0c94aY_TQEUjxRgdt_nyQNrRvFL_nxbw'
    CHAT_ID = '1278487117'

    # Create bot instance
    bot = Telegram(token=TOKEN, default_chat_id=CHAT_ID)

    try:
        # Example usage
        # Basic message
        bot.send_message("Olá! Isso é um teste do bot!")

        # Message with markdown
        bot.send_message(
            "*Texto em negrito*\n_Texto em itálico_",
            parse_mode="Markdown"
        )

        # Message with HTML
        bot.send_message(
            "<b>Texto em negrito</b>\n<i>Texto em itálico</i>",
            parse_mode="HTML"
        )
      
        # Get updates
        updates = bot.get_updates()
        print("Updates:", updates)

    except requests.RequestException as e:
        print(f'Error occurred: {str(e)}')
    except ValueError as e:
        print(f'Configuration error: {str(e)}')
