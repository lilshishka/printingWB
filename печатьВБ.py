import requests
import base64
import subprocess
import os
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import threading
import time

def get_supplies():
    url = 'https://suppliers-api.wildberries.ru/api/v3/supplies'

    params = {
        'limit': 1000,
        'next': 70886137
    }


    headers = {
        'Cookie': '_wbauid=5002380581688475209; ___wbu=972de8e6-7d02-4670-967c-e1664224c9c0.1688475209; x-supplier-id-external=f5c3e5bb-e000-4f39-8b5f-ad558f5bb7da; WBToken=Aof21TGi3KDKDKKqqugMOtaOAXHQug_wfgXEPBiPpjcEIOJBY3DrlaOYo0iLpC280C0sv7rzqVwHpKS2egwdK6t5YUWEoCxTGLg; external-locale=ru; cfidsw-wb=fs0qAFq0En8e9/FJ+GDRuhf9hthOKIdZYOnZZ5m46A2R9nM7qm06UXd7UXk2omlxk75LkXMeClcTn0E01NrgwEfrKyFRbcAcqIMcEJwG6u2aQilgNinAnwJCJ68MQLzzNv0mggx6/KeVOSyGGSWts3xhJjjIM8NCxv1NJLE=; __zzatw-wb=MDA0dBA=Fz2+aQ==;',
        'Authorization': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNTk5MjI5OSwiaWQiOiI3ZjYzMDQxNi0yMDY0LTQ4YjItYTQwOC1mMDJkMTUzNzFkZjciLCJpaWQiOjczMTQwNTEwLCJvaWQiOjY0NDE2NCwicyI6MTYsInNpZCI6ImY1YzNlNWJiLWUwMDAtNGYzOS04YjVmLWFkNTU4ZjViYjdkYSIsInQiOmZhbHNlLCJ1aWQiOjczMTQwNTEwfQ.Sk0WYDcupx35budpVGen1i21QhdL23ia_u7JC3W1OWwowzx0X4oHkW2tbfW7JXzR8r1QRRWwvYwhpTtMqiITUg',
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()
    qrs = []
    for supply in response_json['supplies']:
        qrs.append(supply['id'])
    return qrs



def get_tasks(qr):
    url = f'https://suppliers-api.wildberries.ru/api/v3/supplies/{qr}/orders'

    payload = {
        "supplyId": qr
    }

    headers = {
        'Cookie': '_wbauid=5002380581688475209; ___wbu=972de8e6-7d02-4670-967c-e1664224c9c0.1688475209; x-supplier-id-external=f5c3e5bb-e000-4f39-8b5f-ad558f5bb7da; WBToken=Aof21TGi3KDKDKKqqugMOtaOAXHQug_wfgXEPBiPpjcEIOJBY3DrlaOYo0iLpC280C0sv7rzqVwHpKS2egwdK6t5YUWEoCxTGLg; external-locale=ru; cfidsw-wb=fs0qAFq0En8e9/FJ+GDRuhf9hthOKIdZYOnZZ5m46A2R9nM7qm06UXd7UXk2omlxk75LkXMeClcTn0E01NrgwEfrKyFRbcAcqIMcEJwG6u2aQilgNinAnwJCJ68MQLzzNv0mggx6/KeVOSyGGSWts3xhJjjIM8NCxv1NJLE=; __zzatw-wb=MDA0dBA=Fz2+aQ==;',
        'Authorization': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNTk5MjI5OSwiaWQiOiI3ZjYzMDQxNi0yMDY0LTQ4YjItYTQwOC1mMDJkMTUzNzFkZjciLCJpaWQiOjczMTQwNTEwLCJvaWQiOjY0NDE2NCwicyI6MTYsInNpZCI6ImY1YzNlNWJiLWUwMDAtNGYzOS04YjVmLWFkNTU4ZjViYjdkYSIsInQiOmZhbHNlLCJ1aWQiOjczMTQwNTEwfQ.Sk0WYDcupx35budpVGen1i21QhdL23ia_u7JC3W1OWwowzx0X4oHkW2tbfW7JXzR8r1QRRWwvYwhpTtMqiITUg',
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    data =response.json()

    first_article = data['orders'][0]['article']
    total_orders = len(data['orders'])
    output_data = {
        "qr" : qr,
        "first_article": first_article,
        "total_orders": total_orders
    }
    return output_data


def get_ids(qr):
    url = f'https://suppliers-api.wildberries.ru/api/v3/supplies/{qr}/orders'

    payload = {
        "supplyId": qr
    }

    headers = {
        'Cookie': '_wbauid=5002380581688475209; ___wbu=972de8e6-7d02-4670-967c-e1664224c9c0.1688475209; x-supplier-id-external=f5c3e5bb-e000-4f39-8b5f-ad558f5bb7da; WBToken=Aof21TGi3KDKDKKqqugMOtaOAXHQug_wfgXEPBiPpjcEIOJBY3DrlaOYo0iLpC280C0sv7rzqVwHpKS2egwdK6t5YUWEoCxTGLg; external-locale=ru; cfidsw-wb=fs0qAFq0En8e9/FJ+GDRuhf9hthOKIdZYOnZZ5m46A2R9nM7qm06UXd7UXk2omlxk75LkXMeClcTn0E01NrgwEfrKyFRbcAcqIMcEJwG6u2aQilgNinAnwJCJ68MQLzzNv0mggx6/KeVOSyGGSWts3xhJjjIM8NCxv1NJLE=; __zzatw-wb=MDA0dBA=Fz2+aQ==;',
        'Authorization': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNTk5MjI5OSwiaWQiOiI3ZjYzMDQxNi0yMDY0LTQ4YjItYTQwOC1mMDJkMTUzNzFkZjciLCJpaWQiOjczMTQwNTEwLCJvaWQiOjY0NDE2NCwicyI6MTYsInNpZCI6ImY1YzNlNWJiLWUwMDAtNGYzOS04YjVmLWFkNTU4ZjViYjdkYSIsInQiOmZhbHNlLCJ1aWQiOjczMTQwNTEwfQ.Sk0WYDcupx35budpVGen1i21QhdL23ia_u7JC3W1OWwowzx0X4oHkW2tbfW7JXzR8r1QRRWwvYwhpTtMqiITUg',
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    ids = []
    for supply in data['orders']:
        ids.append(supply['id'])
    return ids


def convert_png_to_pdf(png_files, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    for png_file in png_files:
        img = Image.open(png_file)
        width, height = img.size
        c.setPageSize((width, height))
        c.drawImage(png_file, 0, 0, width, height)
        c.showPage()

    c.save()



def printfunc():
    subprocess.run(["C:\\Program Files (x86)\\Adobe\\Reader 9.0\\Reader\\AcroRd32.exe", "/t", "toprint.pdf"])
    subprocess.run(["taskkill", "/f", "/im", "C:\\Program Files (x86)\\Adobe\\Reader 9.0\\Reader\\AcroRd32.exe"])

def print_stickers(ids):
    png_files = []
    url = 'https://suppliers-api.wildberries.ru/api/v3/orders/stickers'

    params = {
        'type' : 'png',
        'width': 58,
        'height': 40
    }
    payload = {
        'orders': ids
    }

    headers = {
        'Cookie': '_wbauid=5002380581688475209; ___wbu=972de8e6-7d02-4670-967c-e1664224c9c0.1688475209; x-supplier-id-external=f5c3e5bb-e000-4f39-8b5f-ad558f5bb7da; WBToken=Aof21TGi3KDKDKKqqugMOtaOAXHQug_wfgXEPBiPpjcEIOJBY3DrlaOYo0iLpC280C0sv7rzqVwHpKS2egwdK6t5YUWEoCxTGLg; external-locale=ru; cfidsw-wb=fs0qAFq0En8e9/FJ+GDRuhf9hthOKIdZYOnZZ5m46A2R9nM7qm06UXd7UXk2omlxk75LkXMeClcTn0E01NrgwEfrKyFRbcAcqIMcEJwG6u2aQilgNinAnwJCJ68MQLzzNv0mggx6/KeVOSyGGSWts3xhJjjIM8NCxv1NJLE=; __zzatw-wb=MDA0dBA=Fz2+aQ==;',
        'Authorization': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNTk5MjI5OSwiaWQiOiI3ZjYzMDQxNi0yMDY0LTQ4YjItYTQwOC1mMDJkMTUzNzFkZjciLCJpaWQiOjczMTQwNTEwLCJvaWQiOjY0NDE2NCwicyI6MTYsInNpZCI6ImY1YzNlNWJiLWUwMDAtNGYzOS04YjVmLWFkNTU4ZjViYjdkYSIsInQiOmZhbHNlLCJ1aWQiOjczMTQwNTEwfQ.Sk0WYDcupx35budpVGen1i21QhdL23ia_u7JC3W1OWwowzx0X4oHkW2tbfW7JXzR8r1QRRWwvYwhpTtMqiITUg',
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = requests.request("POST", url, headers=headers, params=params, json=payload)

    data = response.json()
    for sticker in data["stickers"]:
        file_data = sticker["file"]
        file_data = base64.b64decode(file_data)

        # Сохранение содержимого в файл
        file_path = f"sticker_{sticker['orderId']}.png"
        with open(file_path, "wb") as png_file:
            png_file.write(file_data)
            png_files.append(file_path)
    convert_png_to_pdf(png_files, 'toprint.pdf')
    thread = threading.Thread(target=printfunc)
    thread.start()
    time.sleep(6)
    thread.join(timeout=0)

    for file in png_files:
        os.remove(file)



def create_supplies_dict():
    supplies_dict = {}
    qr_list = get_supplies()
    for qr in qr_list:
        tasks_info = get_tasks(qr)
        first_article = tasks_info['first_article']
        total_orders = tasks_info['total_orders']
        supplies_dict[first_article] = {'qr': qr, 'total_orders': total_orders}
    return supplies_dict


# Создание главного окна приложения
root = tk.Tk()
root.title("Печать")

# Получение словаря supplies
supplies = create_supplies_dict()

# Создание фрейма для списка поставок
supplies_frame = tk.Frame(root)
supplies_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Создание фрейма для информации о задачах
tasks_frame = tk.Frame(root)
tasks_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Создание кнопки "Печать" и привязка к ней функции
print_button = tk.Button(tasks_frame, text="Печать", command=lambda: print_selected())
print_button.pack()

# Функция для печати выбранного артикула и вызова функции print_stickers
def print_selected():
    # Получаем выбранный артикул из списка поставок
    selected_article = supplies_listbox.get(supplies_listbox.curselection())
    # Меняем цвет выбранного артикула на зеленый
    selected_index = supplies_listbox.curselection()
    supplies_listbox.itemconfig(selected_index, {'bg': 'green'})
    # Вызываем функцию print_stickers с соответствующим QR-номером
    qr = supplies[selected_article]['qr']
    print_stickers(get_ids(qr))

# Создание метки для отображения информации о задачах
tasks_label = tk.Label(tasks_frame, text="")
tasks_label.pack()

# Создание списка поставок и привязка к нему функции
supplies_listbox = tk.Listbox(supplies_frame)
supplies_listbox.pack()

# Заполнение списка поставок данными
for article in supplies:
    supplies_listbox.insert(tk.END, article)

# Функция для отображения информации о задачах
def display_info(event):
    # Получаем выбранный артикул из списка поставок
    selected_article = supplies_listbox.get(supplies_listbox.curselection())
    # Получаем информацию о поставке по выбранному артикулу
    supply_info = supplies[selected_article]
    # Очищаем информацию о задачах
    tasks_label.config(text="")
    # Отображаем информацию о поставке в метке
    info_label.config(text=f"QR: {supply_info['qr']}\nКоличество: {supply_info['total_orders']}")

# Создание метки для отображения информации о задачах
info_label = tk.Label(tasks_frame, text="")
info_label.pack()

# Привязка обработчика события к списку поставок для отображения информации о поставке при выборе артикула
supplies_listbox.bind('<<ListboxSelect>>', display_info)

# Запуск основного цикла обработки событий
root.mainloop()
