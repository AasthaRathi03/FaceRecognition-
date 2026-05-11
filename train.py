from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np




class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Photo Sample Training")
        
         # ===== TITLE =====
        title_lbl = Label(
            self.root,
            text="TRAIN DATA SET",
            font=("times new roman", 30, "bold"),
            bg="white",
            fg="red"
        )
        title_lbl.place(x=0, y=250, width=1530, height=45)

        # ===== TOP IMAGE 1 =====
        img1 = Image.open(r"C:\Users\Aastha Rathi\Downloads\train1.jpg")
        img1 = img1.resize((500, 250), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=0, y=0, width=500, height=250)

        # ===== TOP IMAGE 2 =====
        img2 = Image.open(r"C:\Users\Aastha Rathi\Downloads\train2.jpg")
        img2 = img2.resize((500, 250), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=500, y=0, width=500, height=250)

        # ===== TOP IMAGE 3 =====
        img3 = Image.open(r"C:\Users\Aastha Rathi\Downloads\train3.jpg")
        img3 = img3.resize((530, 250), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        f_lbl = Label(self.root, image=self.photoimg3)
        f_lbl.place(x=1000, y=0, width=530, height=250)

       

       
        # ===== TRAIN BUTTON =====
        train_btn = Button(
            self.root,
            text="TRAIN DATA",
            command=self.train_classifier,
            font=("times new roman", 25, "bold"),
            bg="dark blue",
            fg="white",
            cursor="hand2"
        )
        train_btn.place(x=0, y=725, width=1530, height=60)
        
        
         # ===== BOTTOM IMAGE =====
        img4 = Image.open(r"C:\Users\Aastha Rathi\Downloads\train4.jpg")
        img4 = img4.resize((1530, 430), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        f_lbl = Label(self.root, image=self.photoimg4)
        f_lbl.place(x=0, y=295, width=1530, height=430)

        
        
    def train_classifier(self):
        if not os.path.exists("data") or len(os.listdir("data")) == 0:
            messagebox.showerror("Error", "No images found in data folder")
            return
        data_dir=("data")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)
        if file.endswith(".jpg")]
        faces=[]
        ids=[]
        
        for image in path:
            print(image)
            img=Image.open(image).convert('L')  
            #gray scale image
            img = img.resize((450, 450))
            imageNp = np.array(img , 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])
            
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)
            
        ids=np.array(ids)
        
        #===========train the classifier and save ==========
        
        
        
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result" ,"Training datasets completed!!")
        
             
           


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()