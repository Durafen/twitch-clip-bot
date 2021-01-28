# Twitch Clip Bot
Twitch Bot capable of clipping last 25 sec of twitch stream.<br/>
Showing all chat in  channels with color-coded twitch users.

## Requirements:
```
pip3 install -r requirements.txt
```
## Config:
All the configs can be found in `config.py`.<br/>
Check out guides below for detailed information about filling it.

## Usage:
Run in terminal `./twitch-clip-bot.py` or `python3 twitch-clip-bot.py`<br/>

## Files:
`config.py` - All the config needed to run the bot.<br/>
`cliplog.txt` - All clipping done by the bot.<br/>
`twitch-clip-bot.log` - Debug log (only if `DEBUG = 1` in `config.py`).<br/>

## Based on:<br />
- https://blog.christoffer.online/2019-06-05-twitch-clip-aws-lambda-function-command/ <br />
- https://pimylifeup.com/raspberry-pi-twitch-bot/ <br />

