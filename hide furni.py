import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction

extension_info = {
    "title": "Hide Furni",
    "description": "Hide a furni",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()

on = False
stock_packet = []
count = 0


def furni(message):
    if on:
        global stock_packet
        (idd, p1, x, y, p2, p3, p4, p5, p6, p7, p8, p9, p10) = message.packet.read("iiiiissiisiii")
        ext.send_to_client('{l}{h:3776}{i:'+str(idd)+'}{i:3311}{i:'+str(x)+'}{i:'+str(y)+'}{i:2}{s:"60.0"}{s:"1.0"}{i:1}{i:0}{s:"0"}{i:-1}{i:1}{i:1257657231}')
        ext.send_to_client('{l}{h:1446}{i:0}{s:"Furni with id: "'+str(idd)+'" hidden"}{i:0}{i:1}{i:0}{i:0}')
        stock_packet.insert(0, [idd, p1, x, y, p2, p3, p4, p5, p6, p7, p8, p9, p10])


def roll():
    pack = '{l}{h:3776}'
    for i in range(0, len(stock_packet[0])):
        if isinstance(stock_packet[0][i], str):
            pack += '{s:"' + stock_packet[0][i] + '"}'
        else:
            pack += '{i:' + str(stock_packet[0][i]) + '}'
    ext.send_to_client(pack)
    del stock_packet[0]


def speech(message):
    global on
    (text, color, index) = message.packet.read('sii')

    if text.startswith(":rollback "):
        message.is_blocked = True
        countt = 0
        try:
            arg = int(text[10:])
        except ValueError:
            return ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => Only number available ]"}{i:0}{i:1}{i:0}{i:0}')
        for i in range(arg):
            if stock_packet:
                roll()
                countt += 1
            else:
                break
        ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => Rollback '+str(countt)+' furni ]"}{i:0}{i:1}{i:0}{i:0}')

    if text == ":rollback":
        message.is_blocked = True
        if stock_packet:
            roll()
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => Rollback 1 furni ]"}{i:0}{i:1}{i:0}{i:0}')
        else:
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => No furni found ]"}{i:0}{i:1}{i:0}{i:0}')

    if text == ":hide on":
        message.is_blocked = True
        if on:
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => Already on ]"}{i:0}{i:1}{i:0}{i:0}')
        else:
            on = True
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => On ]"}{i:0}{i:1}{i:0}{i:0}')

    if text == ":hide off":
        message.is_blocked = True
        if not on:
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => Already off ]"}{i:0}{i:1}{i:0}{i:0}')
        else:
            on = False
            ext.send_to_client('{l}{h:1446}{i:0}{s:"[ Hide furni => Off ]"}{i:0}{i:1}{i:0}{i:0}')


ext.intercept(Direction.TO_CLIENT, furni, 3776)
ext.intercept(Direction.TO_SERVER, speech, 1314)
