import os
import csv
import asyncio
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from async_tkinter_loop import async_mainloop, async_handler

class CsvViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CSV Viewer")
        self.geometry("500x500")
        self.minsize(width=500, height=500)

        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        self.selectedItem = tk.StringVar(self, value="To get started, load CSV file please.")

        actionsPanel = tk.Menu()
        actionsPanel.add_radiobutton(label="select CSV file", command=self.read_csv)
        actionsPanel.add_radiobutton(label="exit", command=self.exit_app)

        self.config(menu=actionsPanel)

        self.csvDataView = ttk.Treeview()
        self.csvDataView.grid(row=0, column=0, sticky="nsew")
        csvDataViewVerticalScrollBar = ttk.Scrollbar(orient="vertical", command=self.csvDataView.yview)
        csvDataViewVerticalScrollBar.grid(row=0, column=1, sticky="ns")

        self.csvItemView = ttk.Label(self, textvariable=self.selectedItem)
        self.csvItemView.grid(row=1, column=0, sticky="ew")
      
        csvDataViewHorizontalScrollBar = ttk.Scrollbar(orient="horizontal", command=self.csvDataView.xview)
        csvDataViewHorizontalScrollBar.grid(row=2, column=0, sticky="ew")
        self.csvDataView.config(xscrollcommand=csvDataViewHorizontalScrollBar.set)
        self.csvDataView.config(yscrollcommand=csvDataViewVerticalScrollBar.set)

        self.csvDataView.tag_configure("style", foreground="white", background="black")
        self.csvDataView.bind("<<TreeviewSelect>>", self.on_element_click)

    def exit_app(self): self.destroy()

    def on_element_click(self, event):
        selected_items = self.csvDataView.selection()

        for item in selected_items:
            data = self.csvDataView.item(item)["values"]
            strResultData = ' | '.join(map(str, data))

            self.selectedItem.set(f"-> {strResultData}")

    @async_handler
    async def read_csv(self):
        path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV file", "*.csv"), ("All files", "*.")])
        data = []

        if os.path.exists(path):
            with open(path, newline="") as csvFile:
                csvReader = csv.reader(csvFile)

                for row in csvReader:
                    data.append(row)

            await asyncio.sleep(0.1)
            
            if len(data) > 0:
                elements = self.csvDataView.get_children()

                if (len(elements) > 0):
                    for element in elements:
                        self.csvDataView.delete(element)

                columnsTuple = (data[0])

                self.csvDataView.config(columns=columnsTuple, show="headings")

                for column in data[0]:
                    self.csvDataView.heading(column=column, text=column)

                await asyncio.sleep(0.1)

                for dataGroup in data[1:len(data)]:
                    self.csvDataView.insert("", "end", values=dataGroup, tags=("style"))
            else:
                messagebox.showerror("Error", "CSV file is empty!")
        else:
            messagebox.showerror("Error", "Incorrect path!")

if __name__ == "__main__":
    csvViewerApp = CsvViewerApp()
    async_mainloop(csvViewerApp)
