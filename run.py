from DingTalkBot import *

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)
    bot = BotServer(config['client_id'], config['client_secret'])
    bot.run()