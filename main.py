#!/usr/bin/python
# -*- coding: utf8 -*-

import urwid
import tushare as ts
import requests
import json

tickers = ['300059','600518','000063','601288','688188']

# 0：”大秦铁路”，股票名字；
# 1：”27.55″，今日开盘价；
# 2：”27.25″，昨日收盘价；
# 3：”26.91″，当前价格；
def getprice(ticker):
    tickerurl = "http://hq.sinajs.cn/list="
    if str(ticker).startswith('30') or str(ticker).startswith('00'):
        url = tickerurl + 'sz' + str(ticker)
    elif str(ticker).startswith('6'):
        url = tickerurl + 'sh' + str(ticker)
    else:
        url = tickerurl + 'sh000001'
    res = requests.get(url).text
    test = res.split(',')
    test[0] = test[0][-4:]
    return test[0:4]


# Set up color scheme
palette = [
    ('titlebar', 'dark red,bold', ''),
    ('refresh button', 'dark green,bold', ''),
    ('quit button', 'dark red', ''),
    ('getting quote', 'dark blue', ''),
    ('headers', 'white,bold', ''),
    ('change ', 'dark red', ''),
    ('change negative', 'dark green', '')]

header_text = urwid.Text(u' Stock Quotes')
header = urwid.AttrMap(header_text, 'titlebar')

# Create the menu
menu = urwid.Text([
    u'Press (', ('refresh button', u'R'), u') to manually refresh. ',
    u'Press (', ('quit button', u'Q'), u') to quit.'
])

# Create the quotes box
quote_text = urwid.Text(u'Press (R) to get your first quote!')
quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
v_padding = urwid.Padding(quote_filler, left=1, right=1)
quote_box = urwid.LineBox(v_padding)

# Assemble the widgets
layout = urwid.Frame(header=header, body=quote_box, footer=menu)


def pos_neg_change(change):
    if not change:
        return "0"
    else:
        return ("+{}".format(change) if change >= 0 else str(change))


def get_color(change):
    color = 'change '
    if change < 0:
        color += 'negative'
    return color

def append_text(l, s, tabsize=10, color='white'):
    l.append((color, s.expandtabs(tabsize)))

def calculate_gain(price_in, current_price, shares):
    gain_per_share = float(current_price) - float(price_in)
    gain_percent = round(gain_per_share / float(price_in) * 100, 3)
    return gain_per_share * int(shares), gain_percent


def get_update():
    updates = [
        ('titlebar', u'Stock \t '.expandtabs(10)),
        ('titlebar', u'Cur_Price \t '.expandtabs(4)),
        ('titlebar', u'Pre_Close \t '.expandtabs(3)),
        ('titlebar', u'Change \t '.expandtabs(3)),
        ('titlebar', u'Change% '.expandtabs(10))
    ]
    updates.append('\n')
    
    for t in tickers:
        append_text(updates, '{} \t '.format(getprice(t)[0]), tabsize=10)
        append_text(updates, '{} \t '.format(getprice(t)[3]), tabsize=12)
        append_text(updates, '{} \t '.format(getprice(t)[2]), tabsize=6)
        append_text(updates, '{} \t '.format(round(float(getprice(t)[3])-float(getprice(t)[2]),2)), tabsize=10) 
        data = round((float(getprice(t)[3]) - float(getprice(t)[2])) / float(getprice(t)[2]),2) * 100
        append_text(updates, '{} \t '.format(str(data) + '%'), tabsize=6)
        updates.append('\n')
    
    return updates


# Handle key presses
def handle_input(key):
    if key == 'R' or key == 'r':
        refresh(main_loop, '')

    if key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()


def refresh(_loop, _data):
    main_loop.draw_screen()
    quote_box.base_widget.set_text(get_update())
    main_loop.set_alarm_in(60, refresh)


main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)


def cli():
    main_loop.set_alarm_in(0, refresh)
    main_loop.run()


cli()
