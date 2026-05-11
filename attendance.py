from tkinter import *
from tkinter import ttk, filedialog, messagebox
import csv
import os


class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600+200+100")
        self.root.title("Attendance Management System")

        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_attendance = StringVar()
        

        # ===== LEFT FRAME =====
        left_frame = Frame(self.root, bd=2, relief=RIDGE)
        left_frame.place(x=10, y=10, width=450, height=580)

        Label(left_frame, text="Student Information",
              font=("times new roman", 15, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # fields
        Label(left_frame, text="Student ID").grid(row=1, column=0, padx=10, pady=5)
        Entry(left_frame, textvariable=self.var_id).grid(row=1, column=1)

        Label(left_frame, text="Name").grid(row=2, column=0, padx=10, pady=5)
        Entry(left_frame, textvariable=self.var_name).grid(row=2, column=1)

        Label(left_frame, text="Roll").grid(row=3, column=0, padx=10, pady=5)
        Entry(left_frame, textvariable=self.var_roll).grid(row=3, column=1)

        Label(left_frame, text="Time").grid(row=4, column=0, padx=10, pady=5)
        Entry(left_frame, textvariable=self.var_time).grid(row=4, column=1)

        Label(left_frame, text="Date").grid(row=5, column=0, padx=10, pady=5)
        Entry(left_frame, textvariable=self.var_date).grid(row=5, column=1)

        Label(left_frame, text="Status").grid(row=6, column=0, padx=10, pady=5)
        combo = ttk.Combobox(left_frame, textvariable=self.var_attendance, state="readonly")
        combo["values"] = ("Present", "Absent")
        combo.grid(row=6, column=1)

        # ===== BUTTONS =====
        btn_frame = Frame(left_frame, bd=2, relief=RIDGE)
        btn_frame.place(x=10, y=250, width=420, height=50)

        Button(btn_frame, text="Import CSV", command=self.import_csv, bg="blue", fg="white").grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Export CSV", command=self.export_csv, bg="blue", fg="white").grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Update", command=self.update_data, bg="blue", fg="white").grid(row=0, column=2, padx=5)
        Button(btn_frame, text="Reset", command=self.reset_data, bg="blue", fg="white").grid(row=0, column=3, padx=5)

        # ===== RIGHT FRAME (TABLE) =====
        right_frame = Frame(self.root, bd=2, relief=RIDGE)
        right_frame.place(x=480, y=10, width=500, height=580)

        scroll_x = ttk.Scrollbar(right_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(right_frame, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(
            right_frame,
            columns=("id", "name", "roll", "time", "date", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        for col in ("id", "name", "roll", "time", "date", "status"):
            self.attendance_table.heading(col, text=col.upper())
            self.attendance_table.column(col, width=100)

        self.attendance_table["show"] = "headings"
        self.attendance_table.pack(fill=BOTH, expand=1)

        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)
        self.load_default_data()

    # ===== FUNCTIONS =====

    def fetch_data(self, rows):
        self.attendance_table.delete(*self.attendance_table.get_children())
        for row in rows:
            self.attendance_table.insert("", END, values=row)

    def import_csv(self):
        fln = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Open CSV",
        filetypes=(("CSV File", "*.csv"),),
        parent=self.root
    )

        if fln == "":
            return

        try:
            with open(fln, newline="", encoding="utf-8") as myfile:
                csvread = csv.reader(myfile)
            
                data = []
                for row in csvread:
                    if len(row) > 0:   # skip empty lines
                        data.append(row)

                self.fetch_data(data)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {str(e)}")

    def export_csv(self):
        try:
            if len(self.attendance_table.get_children()) == 0:
                messagebox.showerror("Error", "No data found")
                return

            fln = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=(("CSV file", "*.csv"),),
                parent=self.root   
        )

            if fln == "":
                return

            with open(fln, mode="w", newline="") as myfile:
                exp_write = csv.writer(myfile)
                for row_id in self.attendance_table.get_children():
                    row = self.attendance_table.item(row_id)["values"]
                    exp_write.writerow(row)

            messagebox.showinfo("Success", "Data Exported Successfully")

        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}")

    def get_cursor(self, event=""):
        cursor_row = self.attendance_table.focus()
        content = self.attendance_table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_id.set(row[0])
            self.var_name.set(row[1])
            self.var_roll.set(row[2])
            self.var_time.set(row[3])
            self.var_date.set(row[4])
            self.var_attendance.set(row[5])

    def update_data(self):
        selected = self.attendance_table.focus()
        self.attendance_table.item(selected, values=(
            self.var_id.get(),
            self.var_name.get(),
            self.var_roll.get(),
            self.var_time.get(),
            self.var_date.get(),
            self.var_attendance.get()
        ))

    def reset_data(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_roll.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attendance.set("")
        
        
    def load_default_data(self):
        if os.path.exists("attendance.csv"):
            with open("attendance.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                data = list(reader)
                self.fetch_data(data)
                
if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()