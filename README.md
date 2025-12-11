Powerful telegram bot that scrape Posters from multiple OTT platforms & Bypass direct download links from cloud sites.

## Supported Platforms

<details>
<summary><strong>DDL Bypass Sites</strong></summary>

- Gdflix
- Hubdrive
- Hubcloud
- Transfer.it

</details>

<details>
<summary><strong>OTT & Streaming Platforms</strong></summary>

- Prime Video
- Netflix
- ZEE5
- Apple TV+
- Airtel Xstream
- Sun NXT
- Aha Video
- iQIYI
- WeTV
- ShemarooMe
- BookMyShow
- Plex
- Addatimes
- Stage

</details>

<details>
<summary><strong>Social Media Platforms</strong></summary>

- YouTube
- Instagram
- Facebook
- TikTok

</details>

## Commands
<details>
<summary><strong>Click Here </strong></summary>

  ```
/poster - Scrape any movie/show poster
/imdb - Search movie/series on IMDb
/anime - Search Anime on Anilist
/gdflix - Bypass GDFlix links to direct links
/hubcloud - Bypass HubCloud links to direct links
/hubdrive - Bypass Hubdrive links to direct links
/transfer_it - Bypass Transfer.it links to direct links
/overlap - Overlay a logo on a poster
/prime - Prime Video poster
/netflix - Netflix poster
/zee5 - ZEE5 poster
/appletv - Apple TV+ poster
/airtel - Airtel Xstream poster
/sunnxt - Sun NXT poster
/aha - Aha Video poster
/iqiyi - iQIYI poster
/wetv - WeTV poster
/shemaroo - ShemarooMe poster
/bms - BookMyShow poster
/plex - Plex TV poster
/adda - Addatimes poster
/stage - Stage poster
/youtube - YouTube thumbnail
/instagram - Instagram thumbnail
/facebook - Facebook thumbnail
/tiktok - TikTok thumbnail
/start - Start the bot
/ping - Check Bot Ping
/authorize - Authorize a user or chat[Admins Only]
/unauthorize - Unauthorize a user or chat[Admins Only]
/log - Get bot logs[Admins Only]
/restart - Restart the bot[Admins Only]
/broadcast - Broadcast message to users[Admins Only]
```
</details>

## Variables 
<details>
<summary><strong>Click Here</strong></summary>

### Required Variables

- **`API_ID`** - Get this from [my.telegram.org](https://my.telegram.org)
- **`API_HASH`** - Get this from [my.telegram.org](https://my.telegram.org)
- **`BOT_TOKEN`** - Get this from [@BotFather](https://t.me/BotFather)
- **`DATABASE_URL`** - MongoDB database URL
- **`OWNER_ID`** - Your Telegram user ID

### Optional Variables

- **`DATABASE_NAME`** - MongoDB database name 
- **`SUDO_USERS`** - Space-separated list of user IDs with sudo access
- **`AUTH_CHATS`** - Space-separated list of authorized chat IDs
- **`PUBLIC_MODE`** - Set to `True` for public access, `False` for private use only
- **`TIMEZONE`** - Timezone for the bot 
- **`TMDB_ACCESS_TOKEN`** - TMDB API token (optional, uses proxy if not set)
- **`UPSTREAM_REPO`** - Your forked repository URL for autu update
- **`UPSTREAM_BRANCH`** - Repository branch name 
- **`OTT_TEMPLATE`** - Format for OTT platform poster results
- **`IMDB_TEMPLATE`** - Format for IMDb search results
- **`BYPASS_TEMPLATE`** - Format for bypass link results
- **`POSER_TEMPLATE`** - Format for TMDB poster results

</details>

## Deployment

<details>
  <summary><strong>Heroku (One-Click Deploy)</strong></summary>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/XalFH/Poster-Scraper-Bot)

</details>

<details>
  <summary><strong>Render (One-Click Deploy)</strong></summary>
  
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/XalFH/Poster-Scraper-Bot)

</details>

<details>
  <summary><strong>VPS/Locally</strong></summary>

### Prerequisites
Before starting, ensure you have:
- Docker installed ([Installation Guide](https://docs.docker.com/engine/install/))
- Docker Compose installed ([Installation Guide](https://docs.docker.com/compose/install/))
- Git installed

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/XalFH/Poster-Scraper-Bot
   cd Poster-Scraper-Bot
   ```

2. **Setup Configuration File**
   
   Create `config.env` file:
   ```bash
   nano config.env
   ```
   
   Add the required variables (replace with your actual values):
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   DATABASE_URL=your_mongodb_url
   OWNER_ID=your_telegram_user_id
   ```
   
   Save and exit (`Ctrl + X`, then `Y`, then `Enter`)

3. **Start the Bot**
   ```bash
   docker-compose up -d
   ```
   
   The bot will start in detached mode (background).

4. **Verify Bot is Running**
   ```bash
   docker-compose ps
   ```
   
   You should see `poster-bot` with status "Up".

### Xtras

**View Live Logs:**
```bash
docker-compose logs -f
```
Press `Ctrl + C` to exit logs

**Stop the Bot:**
```bash
docker-compose down
```

**Restart the Bot:**
```bash
docker-compose restart
```

**Update and Restart:**
```bash
git pull
docker-compose up -d --build
```

**Stop and Remove Everything:**
```bash
docker-compose down -v
```
</details>

<details>
  <summary><strong>Heroku CLI</strong></summary>

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Clone Repository & switch to deploy branch**
   ```bash
   git clone https://github.com/XalFH/Poster-Scraper-Bot && cd Poster-Scraper-Bot && git checkout deploy
   ```

3. **Create config.env file**
   ```bash
   nano config.env
   ```
   Add required variables:
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   DATABASE_URL=your_database_url
   OWNER_ID=your_owner_id
   ```

4. **Commit Changes**
   ```bash
   git add . -f
   git commit -m "echo"
   ```

5. **Create Heroku App**
   ```bash
   heroku create YOUR-APP-NAME
   ```

6. **Add Remote**
   ```bash
   heroku git:remote -a YOUR-APP-NAME
   ```

7. **Create Container**
   ```bash
   heroku stack:set container
   ```

8. **Deploy**
   ```bash
   git push heroku deploy:main -f
   ```

9. **Check Logs**
   ```bash
   heroku logs --tail
   ```

</details>

## Admin Side

<details>
<summary><strong>Authorization Management</strong></summary>

### Authorize Users/Chats

Grant access to users or groups to use the bot.

Authorizes the current chat.
```
/authorize
```
**Authorize Specific User/Chat:**
```
/authorize CHAT_ID or USER_ID
```
**Authorize Topic in Group:**
```
/authorize CHAT_ID|TOPIC_ID
```

---

### Unauthorize Users/Chats

Remove access from authorized users or groups.

Unauthorizes the current chat.
```
/unauthorize
```

**Unauthorize Specific User/Chat:**
```
/unauthorize CHAT_ID
```

**Unauthorize Topic:**
```
/unauthorize CHAT_ID|TOPIC_ID
```

</details>

<details>
<summary><strong>Broadcast System</strong></summary>

**Forward with Tag:**
Broadcast with original sender tag.
```
/broadcast -f
```

**Silent Broadcast:**
Broadcast without notification sound.
```
/broadcast -q
```

**Combined Options:**
```
/broadcast -f -q
```

---

### Edit Broadcasts

Edit previously sent broadcast messages.
```
/broadcast BROADCAST_ID -e
```

---

### Delete Broadcasts

Delete broadcast messages from all users.

```
/broadcast BROADCAST_ID -d
```

---

### Broadcast Options

| Flag | Description |
|------|-------------|
| `-f` or `-forward` | Forward message with tag |
| `-q` or `-quiet` | Send without notification |
| `-e` or `-edit` | Edit existing broadcast |
| `-d` or `-delete` | Delete broadcast |

**Important Notes:**
- Broadcast IDs are valid only until bot restart
- After restart, you cannot edit/delete old broadcasts
- Forwarded messages can only be deleted, not edited
- Stats show: Total, Success, Blocked, Deleted, Failed

</details>

## Extras

Live bot can be found here

**Bot:** [@PostersDLBot](https://t.me/PostersDLBot)

U can test all features and commands to see how it works!

<details>
  <summary><strong>Disclaimer</strong></summary>

This bot is developed strictly for **educational and research purposes only**.

</details>

---

[![License](https://img.shields.io/github/license/XalFH/Poster-Scraper-Bot)](https://github.com/XalFH/Poster-Scraper-Bot/blob/main/LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?logo=telegram&logoColor=white)](https://t.me/NxMirror)

If you like this project, don't forget to give it a Star !

**Developer:** [@TheZake](https://t.me/TheZake)
