
import xlwings as xw
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import pandas as pd
import configparser

class unlockSApp:
    def __init__(self, root):
        self.root = root  # root를 인스턴스 변수로 저장
        self.config = configparser.ConfigParser()
        self.config_file = 'settings.ini'
        # self.load_settings()

        root.title("보안 해제 프로그램")
        root.geometry("400x500")  # 높이 조정

        # 화면 가운데 위치
        window_width = 400
        window_height = 500  # 높이 조정
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.build_ui(root)

    def build_ui(self, root):
        self.label_frame = ttk.LabelFrame(root, text="설정")
        self.label_frame.pack(padx=10, pady=10, fill="x", expand=True)

        self.folder_path = tk.StringVar(value=self.config['DEFAULT'].get('folder_path', ''))
        ttk.Label(self.label_frame, text="보안 해제할 파일").pack(anchor='w')
        self.folder_entry = ttk.Entry(self.label_frame, textvariable=self.folder_path)
        self.folder_entry.pack(fill="x")
        ttk.Button(self.label_frame, text="선택...", command=self.select_folder).pack(pady=5)

        self.output_path = tk.StringVar(value=self.config['DEFAULT'].get('output_path', ''))
        ttk.Label(self.label_frame, text="출력 경로").pack(anchor='w')
        self.output_entry = ttk.Entry(self.label_frame, textvariable=self.output_path)
        self.output_entry.pack(fill="x")
        ttk.Button(self.label_frame, text="선택...", command=self.select_output_folder).pack(pady=5)

        self.file_name = tk.StringVar(value=self.config['DEFAULT'].get('file_name', ''))
        ttk.Label(self.label_frame, text="파일 이름").pack(anchor='w')
        self.file_name_entry = ttk.Entry(self.label_frame, textvariable=self.file_name)
        self.file_name_entry.pack(fill="x")

        ttk.Button(root, text="보안 해제 시작", command=self.start_unlockS).pack(pady=20)

    def select_folder(self):
        folder_path = filedialog.askopenfilename(title="보안 해제할 파일 선택", initialdir=self.folder_path.get(), filetypes=[("Excel files", "*.xlsx;*.xls")])
        if folder_path:
            self.folder_path.set(folder_path)

    def select_output_folder(self):
        output_path = filedialog.askdirectory(title="출력 경로 선택", initialdir=self.output_path.get())
        if output_path:
            self.output_path.set(output_path)

    def reset_ui(self):
        # Reset UI elements to be editable after compression is complete
        self.folder_entry.config(state='normal')
        self.output_entry.config(state='normal')
        # self.max_size_entry.config(state='normal')
        self.file_name_entry.config(state='normal')
        messagebox.showinfo("보안 해제 완료", "파일 보안 해제가 완료되었습니다.")

    
    def start_unlockS(self):
        # 입력 필드 수정 불가능하게 설정
        self.folder_entry.config(state='disabled')
        self.output_entry.config(state='disabled')
        # self.max_size_entry.config(state='disabled')
        self.file_name_entry.config(state='disabled')

        # 작업 시작
        folder_path = self.folder_path.get()
        output_path = self.output_path.get()
        file_name = self.file_name.get()

        # 엑셀을 숨김모드로
        app = xw.App(visible=False)
        data = xw.Book(folder_path)
        df = data.sheets(1).used_range.options(pd.DataFrame).value
        df.to_excel(output_path+'/'+file_name)
        data.close()
        app.quit()

        self.root.after(0, self.reset_ui)  # Ensure UI reset is called in the main thread


root = tk.Tk()
app = unlockSApp(root)
root.mainloop()