"""Программа конвертер валют (с) Самсоненко Станислав, 2022"""
from datetime import datetime, timedelta
import urllib.request
import xml.dom.minidom
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker
from tkinter import *
from tkinter.ttk import Combobox, Label, Radiobutton
import tkinter.ttk as ttk




window = Tk()
window.title("Конвертер валют")
window.geometry("1500x750")
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")
tab_control.add(tab2, text="Динамика курса")

CURRENT_DATETIME = datetime.now()
DAY = CURRENT_DATETIME.day
if DAY < 10:
    DAY = "0" + str(DAY)
MONTH = CURRENT_DATETIME.month
if MONTH < 10:
    MONTH = "0" + str(MONTH)
YEAR = str(CURRENT_DATETIME.year)
url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={DAY}/{MONTH}/{YEAR}"
responce = urllib.request.urlopen(url)
dom = xml.dom.minidom.parse(responce)
dom.normalize()
valutes = ["Российский рубль"]
prices = [1]
nominals = [1]
nodeArray = dom.getElementsByTagName("Valute")
for node in nodeArray:
    childList = node.childNodes
    for child in childList:
        if child.nodeName == "Name":
            valutes.append(child.childNodes[0].nodeValue)
        if child.nodeName == "Nominal":
            nominals.append(
                float(child.childNodes[0].nodeValue.replace(",", ".")))
        if child.nodeName == "Value":
            prices.append(float(child.childNodes[0].nodeValue.replace(",", ".")))
input_cur = Combobox(tab1)
input_cur["values"] = valutes
input_cur.current()
input_cur.grid(row=0, column=0)
output_cur = Combobox(tab1)
output_cur["values"] = valutes
output_cur.grid(row=1, column=0, padx=20, pady=10)
entry_sum = Entry(tab1)
entry_sum.grid(row=0, column=1, padx=20, pady=10)


def calc():
    answer = ""
    for i in range(len(valutes)):
        if str(valutes[i]) == str(input_cur.get()):
            in_index = i
        if str(valutes[i]) == str(output_cur.get()):
            out_index = i
    answer = str(
        float(entry_sum.get())
        * nominals[out_index]
        * prices[in_index]
        / (nominals[in_index] * prices[out_index])
    )
    out_answer = Label(tab1, text=answer)
    out_answer.grid(row=1, column=1)


btn_conv = Button(tab1, text="Конвертировать", command=calc)
btn_conv.grid(row=0, column=3, padx=20, pady=10)
label1 = Label(tab2, text="Валюта")
label1.grid(row=0, column=0, padx=20, pady=0)
graf_cur = Combobox(tab2)
graf_cur["values"] = valutes
graf_cur.current()
graf_cur.grid(row=1, column=0, padx=20, pady=0)
label1 = Label(tab2, text="Период")
label1.grid(row=0, column=1, padx=20, pady=0)
per_1 = Combobox(tab2)
per_2 = Combobox(tab2)
per_3 = Combobox(tab2)
per_4 = Combobox(tab2)
months = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]
weeks = []
days_1 = []
days_2 = []
d = datetime.now().weekday()
day_1 = datetime.now() - timedelta(days=d)
while day_1.year > 1993:
    day_2 = day_1 + timedelta(days=6)
    days_1.append(day_1)
    days_2.append(day_2)
    d_1 = str(day_1.day)
    d_2 = str(day_2.day)
    month_1 = str(day_1.month)
    month_2 = str(day_2.month)
    if len(d_1) == 1:
        d_1 = "0" + d_1
    if len(d_2) == 1:
        d_2 = "0" + d_2
    if len(month_1) == 1:
        month_1 = "0" + month_1
    if len(month_2) == 1:
        month_2 = "0" + month_2
    week = "{}.{}.{} - {}.{}.{}".format(
        d_1, month_1, day_1.year, d_2, month_2, day_2.year
    )
    weeks.append(week)
    day_1 -= timedelta(days=7)
per_1["values"] = weeks
cur_months = []
cur_years = []
per_months = []
y1 = int(datetime.now().year)
cur_month = int(datetime.now().month)
while y1 > 1993:
    if cur_month < 0:
        cur_month += 12
        y1 -= 1
    cur_months.append(cur_month)
    cur_years.append(y1)
    cur_my = "{} {}".format(months[cur_month - 1], y1)
    per_months.append(cur_my)
    cur_month -= 1
per_2["values"] = per_months
num_month_1 = int(datetime.now().month) - int(datetime.now().month) % 3 + 1
y1 = int(datetime.now().year)
cur_months_1 = []
cur_years_1 = []
cur_months_2 = []
cur_years_2 = []
kvartals = []
while y1 > 1993:
    if num_month_1 < 1:
        y1 = y1 - 1
        num_month_1 += 12
        num_month_1 = num_month_1 - num_month_1 % 3 + 1
    num_month_2 = num_month_1 + 2
    y2 = y1
    if num_month_2 > 12:
        y2 = y1 + 1
        num_month_2 -= 12
        num_month_2 = num_month_2 - num_month_2 % 3 + 1
    cur_months_1.append(int(num_month_1))
    cur_years_1.append(y1)
    cur_months_2.append(int(num_month_2))
    cur_years_2.append(y2)
    cur_kvartal = "{} {}-{} {}".format(
        months[num_month_1 - 2], y1, months[num_month_2 - 2], y2
    )
    kvartals.append(cur_kvartal)
    num_month_1 -= 3
per_3["values"] = kvartals
y1 = int(datetime.now().year)
years = []
while y1 > 1993:
    years.append(y1)
    y1 -= 1
per_4["values"] = years


def choose():
    """
    Функция для выбора функции приложения.
    """
    if var.get() == 0:
        per_1.current()
        per_1.grid(row=1, column=2, padx=20, pady=5)
        per_2.grid_remove()
        per_3.grid_remove()
        per_4.grid_remove()
    elif var.get() == 1:
        per_2.current()
        per_2.grid(row=2, column=2, padx=20, pady=5)
        per_1.grid_remove()
        per_3.grid_remove()
        per_4.grid_remove()
    elif var.get() == 2:
        per_3.current()
        per_3.grid(row=3, column=2, padx=20, pady=5)
        per_1.grid_remove()
        per_2.grid_remove()
        per_4.grid_remove()
    elif var.get() == 3:
        per_4.current()
        per_4.grid(row=4, column=2, padx=20, pady=5)
        per_1.grid_remove()
        per_2.grid_remove()
        per_3.grid_remove()


var = IntVar()
radiobutton1 = Radiobutton(
    tab2, text="Неделя", variable=var, value=0, command=choose)
radiobutton1.grid(row=1, column=1, padx=20, pady=0)
radiobutton2 = Radiobutton(
    tab2, text="Месяц", variable=var, value=1, command=choose
)
radiobutton2.grid(row=2, column=1, padx=20, pady=0)
radiobutton3 = Radiobutton(
    tab2, text="Квартал", variable=var, value=2, command=choose
)
radiobutton3.grid(row=3, column=1, padx=20, pady=0)
radiobutton4 = Radiobutton(
    tab2, text="Год", variable=var, value=3, command=choose
)
radiobutton4.grid(row=4, column=1, padx=20, pady=0)
label1 = Label(tab2, text="Выбор периода")
label1.grid(row=0, column=2, padx=20, pady=0)


def graf():
    """Функция для построения графиков."""
    matplotlib.use("TkAgg")
    fig = plt.figure()
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(
        fig, master=tab2
    )
    plot_widget = canvas.get_tk_widget()
    ax = fig.add_subplot()
    fig.clear()
    сy = datetime.now()
    x = []
    y = []
    if var.get() == 0:
        index = 0
        for i in range(len(weeks)):
            if str(weeks[i]) == str(per_1.get()):
                сy = days_1[i]
                index = i
        if datetime.now() < days_2[index]:
            n = int(datetime.now().isoweekday()) + 1
        else:
            n = 7
        for i in range(n):
            c_day = str(сy.day)
            if len(c_day) == 1:
                c_day = "0" + c_day
            c_month = str(сy.month)
            if len(c_month) == 1:
                c_month = "0" + c_month
            c_year = str(сy.year)
            url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req= \
            {c_day}/{c_month}/{c_year}"
            responce = urllib.request.urlopen(url)
            dom = xml.dom.minidom.parse(responce)
            dom.normalize()
            print(url)
            x.append("{}-{}-{}".format(c_day, c_month, c_year))
            nodeArray = dom.getElementsByTagName("Valute")
            valutes = ["Российский рубль"]
            prices = [1]
            for node in nodeArray:
                childList = node.childNodes
                for child in childList:
                    if child.nodeName == "Name":
                        valutes.append(child.childNodes[0].nodeValue)
                    if child.nodeName == "Value":
                        prices.append(
                            float(
                                child.childNodes[0].nodeValue.replace(",", ".")
                            )
                        )
            pr_index = 0
            for i in range(len(valutes)):
                if str(valutes[i]) == str(graf_cur.get()):
                    pr_index = i
            y.append(float(prices[pr_index]))
            сy += timedelta(days=1)
    if var.get() == 1:
        for i in range(len(per_months)):
            print(per_months[i], per_2.get())
            if str(per_months[i]) == str(per_2.get()):
                cm = int(cur_months[i])
                index = i
        if (
            cur_years[index] % 4 == 0
            and cur_years[index] % 100 != 0
            or cur_years[index] % 400 == 0
        ) and cm == 2:
            n = 29
        elif cm == 2:
            n = 28
        elif (cm == 4) or (cm == 6) or (cm == 9) or (cm == 11):
            n = 30
        else:
            n = 31
        if int(datetime.now().month) == cm:
            n = int(datetime.now().day) + 1
        if cm < 10:
            cm_1 = "0" + str(cm)
        else:
            cm_1 = cm
        for i in range(1, n + 1):
            if i < 10:
                i = "0" + str(i)
            url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req= \
            {i}/{cm_1}/{cur_years[index]}"
            responce = urllib.request.urlopen(url)
            dom = xml.dom.minidom.parse(responce)
            dom.normalize()
            print(url)
            x.append(i)
            nodeArray = dom.getElementsByTagName("Valute")
            valutes = ["Российский рубль"]
            prices = [1]
            for node in nodeArray:
                childList = node.childNodes
                for child in childList:
                    if child.nodeName == "Name":
                        valutes.append(child.childNodes[0].nodeValue)
                    if child.nodeName == "Value":
                        prices.append(
                            float(
                                child.childNodes[0].nodeValue.replace(",", ".")
                            )
                        )
            pr_index = 0
            for i in range(len(valutes)):
                if str(valutes[i]) == str(graf_cur.get()):
                    pr_index = i
            y.append(float(prices[pr_index]))
    if var.get() == 2:
        for i in range(len(kvartals)):
            if str(kvartals[i]) == str(per_3.get()):
                m = int(cur_months_1[i])
                y1 = int(cur_years_1[i])
                for k in range(3):
                    m1 = ""
                    for j in range(1, 30, 10):
                        if m < 10:
                            m1 = "0" + str(m)
                        else:
                            m1 = m
                        if j < 10:
                            d1 = "0" + str(j)
                        else:
                            d1 = j
                        if m > int(datetime.now().month):
                            break
                        if (
                            m == int(datetime.now().month)
                            and j > int(datetime.now().day) + 1
                        ):
                            break
                        url = f"http://www.cbr.ru/scripts/XML_daily.asp \
                        ?date_req= {d1}/{m1}/{y1}"
                        responce = urllib.request.urlopen(url)
                        dom = xml.dom.minidom.parse(responce)
                        dom.normalize()
                        print(url)
                        x.append("{}.{}.{} ".format(d1, m1, y1 % 100))
                        nodeArray = dom.getElementsByTagName("Valute")
                        valutes = ["Российский рубль"]
                        prices = [1]
                        for node in nodeArray:
                            childList = node.childNodes
                            for child in childList:
                                if child.nodeName == "Name":
                                    valutes.append(
                                        child.childNodes[0].nodeValue
                                    )
                                if child.nodeName == "Value":
                                    prices.append(
                                        float(
                                            child.childNodes[0]
                                            .nodeValue.replace(
                                                ",", "."
                                            )
                                        )
                                    )
                        pr_index = 0
                        for i in range(len(valutes)):
                            if str(valutes[i]) == str(graf_cur.get()):
                                pr_index = i
                        y.append(float(prices[pr_index]))
                    m += 1
    if var.get() == 3:
        for i in range(len(years)):
            if str(years[i]) == str(per_4.get()):
                y1 = int(years[i])
                for m in range(1, 13):
                    for d in range(1, 16, 14):
                        if m < 10:
                            m1 = "0" + str(m)
                        else:
                            m1 = m
                        if d < 10:
                            d1 = "0" + str(d)
                        else:
                            d1 = d
                        if y1 == datetime.now().year:
                            if m > int(datetime.now().month):
                                break
                            if (
                                m == int(datetime.now().month)
                                and d > int(datetime.now().day) + 1
                            ):
                                break
                        url = f"http://www.cbr.ru/scripts/XML_daily.asp \
                        ?date_req={d1}/{m1}/{y1}"
                        responce = urllib.request.urlopen(url)
                        dom = xml.dom.minidom.parse(responce)
                        dom.normalize()
                        print(url)
                        if d1 == "01":
                            x.append(months[m - 1])
                        else:
                            x.append(m * " ")
                        nodeArray = dom.getElementsByTagName("Valute")
                        valutes = ["Российский рубль"]
                        prices = [1]
                        for node in nodeArray:
                            childList = node.childNodes
                            for child in childList:
                                if child.nodeName == "Name":
                                    valutes.append(
                                        child.childNodes[0].nodeValue
                                    )
                                if child.nodeName == "Value":
                                    prices.append(
                                        float(
                                            child.
                                            childNodes[0].nodeValue.replace(
                                                ",", "."
                                            )
                                        )
                                    )
                        pr_index = 0
                        for i in range(len(valutes)):
                            if str(valutes[i]) == str(graf_cur.get()):
                                pr_index = i
                        y.append(float(prices[pr_index]))
    btn_graf = Button(tab2, text="Построить график", command=graf)
    btn_graf.place(height=25, width=150, x=15, y=80)
    print("x=", x)
    print("y=", y)

    def funcForFormatter(x, pos):
        if pos % 2 == 1:
            return u"{}".formate(x="")
        else:
            return u"{x}".format(x=x)

    formatter = matplotlib.ticker.FuncFormatter(funcForFormatter)
    ax.xaxis.set_major_formatter(formatter)
    plt.plot(x, y)
    plt.grid()
    plot_widget.place(height=500, width=1000, x=450, y=150)


graf(valutes)
tab_control.pack(expand=1, fill="both")
window.mainloop()