import os

config = {
    "api": {
        "odds_api_key": os.getenv('ODDS_API_KEY'),
        "telegram_bot_token": os.getenv('TELEGRAM_BOT_TOKEN'),
        "telegram_chat_id": os.getenv('TELEGRAM_CHAT_ID')
    },
    "betting": {
        "min_odds": 2.5, "max_odds": 5.0, "value_threshold": 0.05,
        "max_bets_per_day": 5, "min_confidence": 0.65
    }
}