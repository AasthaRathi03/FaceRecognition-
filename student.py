from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")

        # =========variables=========

        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()

        # first image
        img = Image.open(r"C:\Users\Aastha Rathi\Downloads\face.jpg")
        img = img.resize((455, 180), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=455, height=180)

        # second image

        img1 = Image.open(r"C:\Users\Aastha Rathi\Downloads\main.jpg")
        img1 = img1.resize((455, 180), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=455, y=0, width=455, height=180)

        # third image

        img2 = Image.open(r"C:\Users\Aastha Rathi\Downloads\next.jpg")
        img2 = img2.resize((455, 180), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=910, y=0, width=455, height=180)

        # bg image

        img3 = Image.open(r"C:\Users\Aastha Rathi\Downloads\bg.jpg")
        img3 = img3.resize((1366, 768), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=150, width=1366, height=618)

        title_lbl = Label(
            bg_img,
            text="STUDENT MANAGEMENT SYSTEM SOFTWARE",
            font=("times new roman", 24, "bold"),
            bg="white",
            fg="dark green",
        )
        title_lbl.place(x=0, y=0, width=1355, height=40)

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=5, y=35, width=1355, height=560)

        # left label frame

        Left_frame = LabelFrame(
            main_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Student Details",
            font=("times new roman", 12, "bold"),
        )
        Left_frame.place(x=5, y=1, width=710, height=565)

        img_left = Image.open(r"C:\Users\Aastha Rathi\Downloads\next.jpg")
        img_left = img_left.resize((660, 100), Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl = Label(Left_frame, image=self.photoimg_left)
        f_lbl.place(x=3, y=2, width=660, height=100)

        # current course

        current_course_frame = LabelFrame(
            Left_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="current course information",
            font=("times new roman", 12, "bold"),
        )
        current_course_frame.place(x=3, y=105, width=700, height=100)

        # Department

        dep_label = Label(
            current_course_frame,
            text="Department",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        dep_label.grid(row=0, column=0, padx=10, sticky=W)

        dep_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_dep,
            font=("times new roman", 12, "bold"),
            width=17,
            state="readonly",
        )
        dep_combo["values"] = (
            "Select Department",
            "Computer Science",
            "IT",
            "Maths",
            "Physics",
        )
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Course

        course_label = Label(
            current_course_frame,
            text="Course",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        course_label.grid(row=0, column=2, padx=10, sticky=W)

        course_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_course,
            font=("times new roman", 12, "bold"),
            width=17,
            state="readonly",
        )
        course_combo["values"] = ("Select Course", "MCA", "BTech", "Maths", "Physics")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # year

        year_label = Label(
            current_course_frame,
            text="Year",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        year_label.grid(row=1, column=0, padx=10, sticky=W)

        year_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_year,
            font=("times new roman", 12, "bold"),
            width=17,
            state="readonly",
        )
        year_combo["values"] = (
            "Select Year",
            "2022-23",
            "2023-24",
            "2024-25",
            "2025-26",
        )
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester

        Semester_label = Label(
            current_course_frame,
            text="Semester",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        Semester_label.grid(row=1, column=2, padx=10, sticky=W)

        Semester_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_semester,
            font=("times new roman", 12, "bold"),
            width=17,
            state="readonly",
        )
        Semester_combo["values"] = (
            "Select Semester",
            "Semester 1",
            "Semester 2",
            "Semester 3",
            "Semester 4",
        )
        Semester_combo.current(0)
        Semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        # class student information

        class_Student_frame = LabelFrame(
            Left_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="class student information",
            font=("times new roman", 12, "bold"),
        )
        class_Student_frame.place(x=3, y=210, width=700, height=285)

        # student ID
        StudentId_label = Label(
            class_Student_frame,
            text="StudentID:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        StudentId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        studentID_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_std_id,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        studentID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # student name

        StudentName_label = Label(
            class_Student_frame,
            text="Student Name:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        StudentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        studentName_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_std_name,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        #

        # Class Division
        div_label = Label(
            class_Student_frame,
            text="Class division:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        div_combo = ttk.Combobox(
            class_Student_frame,
            textvariable=self.var_div,
            font=("times new roman", 12, "bold"),
            width=18,
            state="readonly",
        )

        div_combo["values"] = ("Select Division", "A", "B", "C")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Roll number

        roll_no_label = Label(
            class_Student_frame,
            text="Roll number:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        roll_no_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        roll_no_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_roll,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        roll_no_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # gender

        # Gender
        gender_label = Label(
            class_Student_frame,
            text="Gender:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        gender_combo = ttk.Combobox(
            class_Student_frame,
            textvariable=self.var_gender,
            font=("times new roman", 12, "bold"),
            width=18,
            state="readonly",
        )

        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # dob

        dob_label = Label(
            class_Student_frame,
            text="DOB:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        dob_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        dob_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_dob,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        dob_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Email

        Email_label = Label(
            class_Student_frame,
            text="Email :",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        Email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        Email_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_email,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        Email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # phone number

        Phone_label = Label(
            class_Student_frame,
            text="Phone No:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        Phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)

        Phone_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_phone,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        Phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Address

        address_label = Label(
            class_Student_frame,
            text="Address:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        address_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_address,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        address_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # Teacher name

        teacher_label = Label(
            class_Student_frame,
            text="Teacher Name:",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        teacher_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)

        teacher_entry = ttk.Entry(
            class_Student_frame,
            textvariable=self.var_teacher,
            width=20,
            font=("times new roman", 12, "bold"),
        )
        teacher_entry.grid(row=4, column=3, padx=10, pady=5, sticky=W)

        # radio buttons

        # radio buttons
        self.var_radio1 = StringVar()

        radiobtn1 = Radiobutton(
            class_Student_frame,
            text="Take Photo Sample",
            variable=self.var_radio1,
            value="Yes",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        radiobtn1.grid(row=5, column=0, padx=10, pady=5, sticky=W)

        radiobtn2 = Radiobutton(
            class_Student_frame,
            text="No Photo Sample",
            variable=self.var_radio1,
            value="No",
            font=("times new roman", 12, "bold"),
            bg="white",
        )
        radiobtn2.grid(row=5, column=1, padx=10, pady=5, sticky=W)

        # button frame

        btn_frame = Frame(Left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=10, y=465, width=640, height=32)

        save_btn = Button(
            btn_frame,
            text="Save",
            command=self.add_data,
            width=15,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        save_btn.grid(row=0, column=0)

        update_btn = Button(
            btn_frame,
            text="Update",
            command=self.update_data,
            width=15,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        update_btn.grid(row=0, column=1)

        delete_btn = Button(
            btn_frame,
            text="Delete",
            command=self.delete_data,
            width=15,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(
            btn_frame,
            text="Reset",
            command=self.reset_data,
            width=15,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        reset_btn.grid(row=0, column=3)
        
        

        btn_frame1 = Frame(Left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=10, y=505, width=640, height=32)
        
        import threading

        take_photo_btn = Button(
            btn_frame1,
            text="Take Photo Sample",
            command=self.generate_dataset,
            width=31,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        take_photo_btn.grid(row=0, column=0)

        update_photo_btn = Button(
            btn_frame1,
            text="Update Photo Sample",
            command=self.generate_dataset,
            width=31,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        update_photo_btn.grid(row=0, column=1)

        # right label frame

        Right_frame = LabelFrame(
            main_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Student Details",
            font=("times new roman", 12, "bold"),
        )
        Right_frame.place(x=685, y=1, width=665, height=545)

        img_right = Image.open(r"C:\Users\Aastha Rathi\Downloads\next.jpg")
        img_right = img_right.resize((650, 100), Image.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        right_img_lbl = Label(Right_frame, image=self.photoimg_right, bd=0)
        right_img_lbl.place(x=3, y=2, width=650, height=100)

        search_frame = LabelFrame(
            Right_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Search System",
            font=("times new roman", 12, "bold"),
        )
        search_frame.place(x=5, y=110, width=650, height=60)

        search_label = Label(
            search_frame,
            text="Search By:",
            font=("times new roman", 15, "bold"),
            bg="red",
            fg="white",
        )
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        search_combo = ttk.Combobox(
            search_frame,
            font=("times new roman", 12, "bold"),
            width=15,
            state="readonly",
        )
        search_combo["values"] = ("Select", "Roll No", "Phone No")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=5, pady=10)

        search_entry = ttk.Entry(
            search_frame, width=15, font=("times new roman", 12, "bold")
        )
        search_entry.grid(row=0, column=2, padx=5, pady=10)

        search_btn = Button(
            search_frame,
            text="Search",
            width=12,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        search_btn.grid(row=0, column=3, padx=5)

        showAll_btn = Button(
            search_frame,
            text="Show All",
            width=12,
            font=("times new roman", 12, "bold"),
            bg="blue",
            fg="white",
        )
        showAll_btn.grid(row=0, column=4, padx=5)

        # table frame
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=180, width=650, height=340)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=(
                "dep",
                "course",
                "year",
                "sem",
                "id",
                "name",
                "roll",
                "gender",
                "div",
                "dob",
                "email",
                "phone",
                "address",
                "teacher",
                "photo",
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="StudentId")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("roll", text="Roll number")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("div", text="Division")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="PhotoSampleStatus")

        self.student_table["show"] = "headings"

        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("div", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photo", width=150)

        self.student_table.pack(fill=BOTH, expand=True)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

        # =========function declaration======

    def add_data(self):
        if (
            self.var_dep.get() == "Select Department"
            or self.var_std_name.get() == ""
            or self.var_std_id.get() == ""
        ):
            messagebox.showerror("error", "All Fields are required", parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="Aastha123@@",
                    database="face_recognizer",
                )

                my_cursor = conn.cursor()

                my_cursor.execute(
                    "insert into student(department,course,year,semester,student_id,name,division,roll,gender,dob,email,phone,address,teacher,photo_sample) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_std_id.get(),
                        self.var_std_name.get(),
                        self.var_div.get(),
                        self.var_roll.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_teacher.get(),
                        self.var_radio1.get(),
                    ),
                )

                conn.commit()
                self.fetch_data()
                conn.close()

                messagebox.showinfo(
                    "Success",
                    "Student details has been added successfully",
                    parent=self.root,
                )

            except Exception as es:
                messagebox.showerror("Error", f"Due to : {str(es)}", parent=self.root)

    # ==================fetch data==========
    def fetch_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="Aastha123@@",
            database="face_recognizer",
        )

        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())

            for row in data:
                self.student_table.insert("", END, values=row)

            conn.commit()

        conn.close()

    # ============get cursor===============

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)

        data = content["values"]

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_semester.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_div.set(data[6])
        self.var_roll.set(data[7])
        self.var_gender.set(data[8])
        self.var_dob.set(data[9])
        self.var_email.set(data[10])
        self.var_phone.set(data[11])
        self.var_address.set(data[12])
        self.var_teacher.set(data[13])
        self.var_radio1.set(data[14])

    # ============update function============================

    def update_data(self):
        print("update button clicked")
        if (
            self.var_dep.get() == "Select Department"
            or self.var_std_name.get() == ""
            or self.var_std_id.get() == ""
        ):
            messagebox.showerror("Error", "All fields are required", parent=self.root)

        else:
            try:
                update = messagebox.askyesno(
                    "Update",
                    "Do you want to update this student details?",
                    parent=self.root,
                )

                if update > 0:
                    conn = mysql.connector.connect(
                        host="localhost",
                        username="root",
                        password="Aastha123@@",
                        database="face_recognizer",
                    )

                    my_cursor = conn.cursor()

                    my_cursor.execute(
                        """
                    update student set
                    department=%s,
                    course=%s,
                    year=%s,
                    semester=%s,
                    name=%s,
                    division=%s,
                    roll=%s,
                    gender=%s,
                    dob=%s,
                    email=%s,
                    phone=%s,
                    address=%s,
                    teacher=%s,
                    photo_sample=%s
                    where student_id=%s
                    """,
                        (
                            self.var_dep.get(),
                            self.var_course.get(),
                            self.var_year.get(),
                            self.var_semester.get(),
                            self.var_std_name.get(),
                            self.var_div.get(),
                            self.var_roll.get(),
                            self.var_gender.get(),
                            self.var_dob.get(),
                            self.var_email.get(),
                            self.var_phone.get(),
                            self.var_address.get(),
                            self.var_teacher.get(),
                            self.var_radio1.get(),
                            self.var_std_id.get(),
                        ),
                    )

                conn.commit()
                self.fetch_data()
                conn.close()

                messagebox.showinfo(
                    "Success", "Student details successfully updated", parent=self.root
                )

            except Exception as es:
                messagebox.showerror("Error", f"Due to : {str(es)}", parent=self.root)

    # =============delete function==================

    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Student ID must be required", parent=self.root
            )

        else:
            try:
                delete = messagebox.askyesno(
                    "Student Delete Page",
                    "Do you want to delete this student details?",
                    parent=self.root,
                )

                if delete > 0:
                    conn = mysql.connector.connect(
                        host="localhost",
                        username="root",
                        password="Aastha123@@",
                        database="face_recognizer",
                    )

                    my_cursor = conn.cursor()

                    sql = "delete from student where student_id=%s"
                    val = (self.var_std_id.get(),)

                    my_cursor.execute(sql, val)

                    conn.commit()
                    self.fetch_data()
                    conn.close()

                    messagebox.showinfo(
                        "Delete",
                        "Successfully deleted student details",
                        parent=self.root,
                    )

            except Exception as es:
                messagebox.showerror("Error", f"Due to : {str(es)}", parent=self.root)

    # ==================Reset button=================
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")

        self.var_std_id.set("")
        self.var_std_name.set("")

        self.var_div.set("Select Division")
        self.var_roll.set("")

        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")

        self.var_radio1.set("")

    # =================generate dataset====================

    def generate_dataset(self):
        
        
        if (
            self.var_dep.get() == "Select Department"
            or self.var_std_name.get() == ""
            or self.var_std_id.get() == ""
    ):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
        # ===== database update =====
            conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="Aastha123@@",
            database="face_recognizer",
        )

            my_cursor = conn.cursor()

            my_cursor.execute(
            """
            update student set
            department=%s,
            course=%s,
            year=%s,
            semester=%s,
            name=%s,
            division=%s,
            roll=%s,
            gender=%s,
            dob=%s,
            email=%s,
            phone=%s,
            address=%s,
            teacher=%s,
            photo_sample=%s
            where student_id=%s
            """,
            (
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_std_name.get(),
                self.var_div.get(),
                self.var_roll.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_email.get(),
                self.var_phone.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                "Yes",
                self.var_std_id.get(),
            ),
        )

            conn.commit()
            self.fetch_data()
            conn.close()

        # ===== face detection =====
            face_classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                for x, y, w, h in faces:
                    return img[y:y+h, x:x+w]

                return None
            
           


            cap = cv2.VideoCapture(1)

            
            img_id =0
            while True:
        
                ret, my_frame = cap.read()

                

                if not ret:
                    print("Frame not received, skipping...")
                    break
                
                    

                cv2.imshow("Camera Test", my_frame)   # 👈 IMPORTANT (raw camera check)

                face = face_cropped(my_frame)

                if face is not None:
                    img_id += 1

                    face = cv2.resize(face, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                    file_name_path = f"data/user.{self.var_std_id.get()}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)

                    cv2.imshow("Cropped Face", face)

    # ESC press = exit
                if cv2.waitKey(1) == 27 or img_id == 50:
                    break

            cap.release()
            cv2.destroyAllWindows()

            messagebox.showinfo(
            "Result",
            "Generating dataset completed!",
            parent=self.root,
        )

        except Exception as es:
            messagebox.showerror(
            "Error",
            f"Due to : {str(es)}",
            parent=self.root,
        )

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
