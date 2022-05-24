import sqlite3
from datetime import datetime
import re
import PySimpleGUI as sg
# Create table
#create window
layout =[[sg.Text('qty')],[sg.InputText(key='qty')],
         [sg.Text('price')],[sg.InputText(key='price')],
         [sg.Text('article')],[sg.InputText(key='article')],
         [sg.Button('push'),sg.Button('show'),sg.Button('del')],
         [sg.Button('edit')]
]
window=sg.Window('sql', layout)
con = sqlite3.connect('new2.db')
cur = con.cursor()
def clea():
    window['qty'].update('')
    window['price'].update('')
    window['article'].update('')
try:
    cur.execute('''CREATE TABLE stocks
           (date text, trans text, article text, qty real, price real, edited)''')
except:
    pass
# Insert a row of data
while True:
    event, values =window.read()
    qty = values['qty']
    price = values['price']
    article = values['article']
    curdate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    edited='Null'
    if event == 'push':
        cur.execute(f"INSERT INTO stocks VALUES ('{curdate}','BUY','{article}','{qty}','{price}','{edited}' )")
        clea()
    if event == 'show':
        for row in cur.execute(f'SELECT * FROM stocks WHERE article = "{article}"'):
            window['qty'].update(row[3])
            window['price'].update(row[4])
            #window['article'].update(row[2])
        #     #print(type(cur.execute(f'SELECT * FROM stocks WHERE article = "{article}"')))
        # for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
        #     print(row)
        
    if event == 'del':
        cur.execute(f'DELETE FROM stocks WHERE article="{article}";')
        clea()
    if event =='edit':
        edited=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(f'UPDATE stocks SET qty ="{qty}" , price = "{price}" , edited = "{edited}" where article="{article}"')
        clea()
    if event == sg.WIN_CLOSED:
        break
    con.commit()
# Save (commit) the changes
con.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
window.close()