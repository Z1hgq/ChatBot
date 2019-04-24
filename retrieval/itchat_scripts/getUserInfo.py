import itchat, time
from itchat.content import *
import json
from weather import getWeather

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT)
def text_rreply(msg):
    # print(json.dumps(msg, sort_keys=True, indent=4, separators=(',', ':')))
    print(msg['User']['City'])
    msg.user.send(getWeather(msg['User']['City']))
    # if msg.isAt:
    #     msg.user.send(u'@%s\u2005I received: %s' % (
    #         msg.actualNickName, msg.text))

itchat.auto_login(hotReload=True,enableCmdQR=2)
itchat.run(True)