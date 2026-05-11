from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import mysql.connector


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # ===== TOP IMAGE 1 =====
        img = Image.open(r"C:\Users\Aastha Rathi\Downloads\face.jpg")
        img = img.resize((500, 250), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=500, height=250)

        # ===== TOP IMAGE 2 =====
        img1 = Image.open(r"C:\Users\Aastha Rathi\Downloads\main.jpg")
        img1 = img1.resize((500, 250), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=500, y=0, width=500, height=250)

        # ===== TOP IMAGE 3 =====
        img2 = Image.open(r"C:\Users\Aastha Rathi\Downloads\next.jpg")
        img2 = img2.resize((530, 250), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=1000, y=0, width=530, height=250)

        # ===== TITLE =====
        title_lbl = Label(
            self.root,
            text="FACE RECOGNITION",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="dark green"
        )
        title_lbl.place(x=0, y=250, width=1530, height=45)

        # ===== BOTTOM IMAGE =====
        img3 = Image.open(r"C:\Users\Aastha Rathi\Downloads\bg.jpg")
        img3 = img3.resize((1530, 430), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        f_lbl = Label(self.root, image=self.photoimg3)
        f_lbl.place(x=0, y=295, width=1530, height=430)

        # ===== BUTTON =====
        detect_btn = Button(
            self.root,
            text="FACE DETECTOR",
            font=("times new roman", 25, "bold"),
            bg="dark blue",
            fg="white",
            cursor="hand2"
        )
        detect_btn.place(x=0, y=725, width=1530, height=60)

    def face_recog(self):

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            features = classifier.detectMultiScale(
                gray_image,
                scaleFactor,
                minNeighbors
            )

            for (x, y, w, h) in features:
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])

                confidence = int(100 * (1 - predict / 300))
                print("Confidence:", confidence)

                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="Aastha123@@",
                    database="face_recognizer"
                )

                my_cursor = conn.cursor()

                my_cursor.execute(
                    "select name from student where student_id=%s",
                    (id,)
                )
                n = my_cursor.fetchone()

                my_cursor.execute(
                    "select roll from student where student_id=%s",
                    (id,)
                )
                r = my_cursor.fetchone()

                my_cursor.execute(
                    "select student_id from student where student_id=%s",
                    (id,)
                )
                i = my_cursor.fetchone()

                conn.close()

                i = str(i[0]) if i else "Unknown"
                n = str(n[0]) if n else "Unknown"
                r = str(r[0]) if r else "Unknown"

                if confidence > 75:
                    cv2.rectangle(
                        img,
                        (x, y),
                        (x+w, y+h),
                        (0, 255, 0),
                        3
                    )

                    cv2.putText(
                        img,
                        f"ID: {i}",
                        (x, y-60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        img,
                        f"Name: {n}",
                        (x, y-35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        img,
                        f"Roll: {r}",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2
                    )

                else:
                    cv2.rectangle(
                        img,
                        (x, y),
                        (x+w, y+h),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        img,
                        "Unknown Face",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2
                    )

            return img

        faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()

            if not ret:
                break

            img = draw_boundary(
                img,
                faceCascade,
                1.1,
                10,
                clf
            )

            cv2.putText(
                img,
                "Press Q to Exit",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.imshow("Live Face Recognition", img)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27 or key == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()
        
    


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()