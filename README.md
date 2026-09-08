# Nepal Electrical Jobs AI Agent — V1

Free-first automated vacancy monitor for Electrical / Electronics / Power / Renewable Energy jobs in Nepal.

## Included
- Nepal Electricity Authority (NEA) open recruitment collector
- Nepal Impact public API collector
- Optional JobsNepal and Kumari Job adapters (disabled by default)
- Rule-based relevance scoring
- Persistent duplicate detection
- Telegram notifications
- GitHub Actions scheduler
- Optional AI adapter kept separate so the core system does not require a paid AI API

## Cost target
₹0/month. GitHub Actions, Telegram Bot API, NEA public pages and Nepal Impact's public API are used without a paid server/database.

## Setup
1. Create a Telegram bot with @BotFather.
2. Put `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` into `.env` for local use, or GitHub repository Secrets for Actions.
3. Install:
   `pip install -r requirements.txt`
4. Test:
   `python -m app.main --dry-run`
5. Real run:
   `python -m app.main`

For GitHub Actions, upload the project to a repository, add the two Telegram secrets, enable Actions, and run the workflow manually once.

## Important
JobsNepal and Kumari Job are opt-in adapters. Review their current terms/access policies before enabling them and keep request frequency low. Do not bypass authentication, CAPTCHA, rate limits, or technical restrictions.

MeroJob is intentionally not implemented as a direct scraper because its current terms restrict automated scraping/data mining.

Edit `config/profile.json` to change the candidate profile and notification threshold.
