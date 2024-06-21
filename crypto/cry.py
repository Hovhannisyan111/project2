"""
This file is for desktop app: Crypto
Created by: Arman Hoavhannisyan
Date: 10 June
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import requests
import xlsxwriter

def create_widgets(root, state):
    """
    Function: create_widgets
    Brief: create the widgets for tkinter window
    Params: root: state: dictsto store widget states
    """
    state["upload_btn"] = tk.Button(root, text="Upload file", command=lambda: upload_file(state))
    state["upload_btn"].pack(pady=20)
    state["file_label"] = tk.Label(root, text="")
    state["file_label"].pack()

    state["name_label"] = tk.Label(root, text="Enter Excel file  name")
    state["name_label"].pack()

    state["name_entry"] = tk.Entry(root)
    state["name_entry"].pack()

    state["save_btn"] = tk.Button(root, text="Save Excel File", command=lambda: save_file(state, root))
    state["save_btn"].pack(pady=20)

def upload_file(state):
    """
    Function: upload_file
    Brief: handle file upload and make content
    Parms: state: dict to store widget states
    """
    state["file_path"] = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if state["file_path"]:
        state["file_label"].config(text=f"Uploaded:{os.path.basename(state['file_path'])}")
    else:
        state["file_label"].config(text="Nothing selected")

def save_file(state, root):
    """
    Function: save_file
    Brief: Save data to excel file
    Params: state: dict to store widget states
            root: tkinter root window
    """
    if "file_path" not in state or not state["file_path"]:
        messagebox.showerror("Error", "Please upload file first")
        return

    excel_name = state["name_entry"].get()
    if not excel_name:
        messagebox.showerror("Error", "Please enter a name of Excel file")
        return

    default_save_path = os.path.join(os.path.expanduser("~/Downloads"), f"{excel_name}.xlsx")
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_save_path, initialdir=os.path.expanduser("~/Downloads"), filetypes=[("Excel files", "*.xlsx")])
    if not save_path:
        return

    try:
        save_data(save_path, state)
        messagebox.showinfo("Done", f"Date saved to {save_path}")
    except Exception as error:
        messagebox.showerror("Error", "Faild to save data {error}")
    root.destroy()

def save_data(save_path, state):
    """
    Function: save_data
    Brief: get data for url and save to Excel file
    Params: save_path: the path to save Excel file
            state: dict of widget states
    """

    symbols = read_symbols(state)
    data = get_data()
    filtered_data = [i for i in data if i["symbol"].upper() in symbols]

    if not filtered_data:
        raise Exception("No data found")

    workbook = xlsxwriter.Workbook(save_path)
    worksheet = workbook.add_worksheet()
    headers = ["Name", "Symbol", "Current Price", "Market Cap", "Total Volume", "Price Cahnge for 24 hours"]
    bold = workbook.add_format({"bold": True})
    currency_format = workbook.add_format({'num_format': '$#,##0.00'})

    for col in range(len(headers)):
        worksheet.write(0, col, headers[col], bold)
        worksheet.set_column(col, col, 23)

    row = 1
    for item in filtered_data:
        worksheet.write(row, 0, item["name"])
        worksheet.write(row, 1, item["symbol"])
        worksheet.write_number(row, 2, float(item["priceUsd"]), currency_format)
        worksheet.write_number(row, 3, float(item["marketCapUsd"]), currency_format)
        worksheet.write_number(row, 4, float(item["volumeUsd24Hr"]), currency_format)
        worksheet.write_number(row, 5, float(item["changePercent24Hr"]))

        row += 1
    workbook.close()

def read_symbols(state):
    """
    Function: read_symbols
    Brief: reading symbols from upladed file
    Params: state: dict to store wisget states
    Return: list of symbols
    """
    with open(state["file_path"]) as file:
        symbols = file.read().split()
    return [symbol.upper() for symbol in  symbols]

def get_data():
    """
    Function:: get_data
    Brief: getting data from api
    Return: list of crypto data
    """
    url = "https://api.coincap.io/v2/assets"
    params = {"limit": 20}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data from API: {e}")

    data = response.json()
    return data["data"]

def main():
    """
    Function: main
    Brief: Entery point
    """
    root = tk.Tk()
    root.title("Crypto")
    root.geometry("500x250")

    state = {}
    create_widgets(root, state)
    root.mainloop()

if __name__ == "__main__":
    main()
