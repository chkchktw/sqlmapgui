import tkinter as tk
from tkinter import ttk
import subprocess
import threading

# 建立主窗口
root = tk.Tk()
root.title("SQLMap GUI")

# 設定字型大小
font_size = 14
font = ("TkDefaultFont", font_size)

# 布局
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# URL 輸入
url_label = ttk.Label(frame, text="URL:")
url_label.grid(row=0, column=0, sticky=tk.W)
url_entry = ttk.Entry(frame, width=50)
url_entry.grid(row=0, column=1)

# Checkbox選項
random_agent_var = tk.BooleanVar()
random_agent_var.set(True)  # 設定為預設勾選
random_agent_check = ttk.Checkbutton(frame, text="Random Agent", variable=random_agent_var)
random_agent_check.grid(row=1, column=0, sticky=tk.W)

tamper_var = tk.BooleanVar()
tamper_var.set(True)  # 設定為預設勾選
tamper_check = ttk.Checkbutton(frame, text="Tamper=space2comment", variable=tamper_var)
tamper_check.grid(row=2, column=0, sticky=tk.W)

batch_var = tk.BooleanVar()
batch_var.set(True)  # 設定為預設勾選
batch_check = ttk.Checkbutton(frame, text="Batch", variable=batch_var)
batch_check.grid(row=3, column=0, sticky=tk.W)

skip_waf_var = tk.BooleanVar()
skip_waf_var.set(True)  # 設定為預設勾選
skip_waf_check = ttk.Checkbutton(frame, text="Skip WAF", variable=skip_waf_var)
skip_waf_check.grid(row=4, column=0, sticky=tk.W)

dbms_var = tk.StringVar()
dbms_combo = ttk.Combobox(frame, textvariable=dbms_var, values=[
    "", "MySQL", "Oracle", "PostgreSQL", "\'Microsoft SQL Server\'",
    "\"Microsoft Access\"", "SQLite", "Firebird", "Sybase", "Informix", "MariaDB"])
dbms_combo.grid(row=5, column=1, sticky=tk.W)

# 下拉式選單
level_label = ttk.Label(frame, text="Level:")
level_label.grid(row=6, column=0, sticky=tk.W)
level_var = tk.StringVar()
level_var.set("1")  # 設定為預設選1
level_combo = ttk.Combobox(frame, textvariable=level_var, values=["1", "2", "3", "4", "5"])
level_combo.grid(row=6, column=1, sticky=tk.W)

risk_label = ttk.Label(frame, text="Risk:")
risk_label.grid(row=7, column=0, sticky=tk.W)
risk_var = tk.StringVar()
risk_var.set("1")  # 設定為預設選1
risk_combo = ttk.Combobox(frame, textvariable=risk_var, values=["1", "2", "3"])
risk_combo.grid(row=7, column=1, sticky=tk.W)

# 新增forms參數選項
forms_var = tk.BooleanVar()
forms_check = ttk.Checkbutton(frame, text="Forms", variable=forms_var)
forms_check.grid(row=8, column=0, sticky=tk.W)

# 命令輸出框
output_text = tk.Text(frame, height=10, width=80, font=font)  # 設定字型大小
output_text.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E))

# 顯示命令的框
command_text = tk.Text(frame, height=10, width=80, font=font)  # 設定字型大小
command_text.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E))

# 組成語法
def compose_sqlmap_command():
    cmd = ["python", "sqlmap.py", "-u", url_entry.get()]
    if random_agent_var.get():
        cmd.append("--random-agent")
    if tamper_var.get():
        cmd.append("--tamper=space2comment")
    if batch_var.get():
        cmd.append("--batch")
    if skip_waf_var.get():
        cmd.append("--skip-waf")
    if level_var.get():
        cmd.append(f"--level={level_var.get()}")
    if risk_var.get():
        cmd.append(f"--risk={risk_var.get()}")
    if dbms_var.get():  # 只有在勾选了DBMS时才将其添加到命令中
        cmd.append(f"--dbms={dbms_var.get()}")
    if forms_var.get():  # 只有在勾选了Forms时才将其添加到命令中
        cmd.append("--forms")

    # 顯示命令
    command_text.delete(1.0, tk.END)
    command_text.insert(tk.END, " ".join(cmd))

# 執行命令
def execute_sqlmap_command():
    cmd = command_text.get("1.0", tk.END).strip().split()
    if cmd:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
            root.update()

# 在新線程中運行命令，防止GUI凍結
def execute_sqlmap_thread():
    threading.Thread(target=execute_sqlmap_command).start()

# 設定元件隨著調整大小
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# 按鈕
compose_button = ttk.Button(frame, text="組成語法", command=compose_sqlmap_command)
compose_button.grid(row=11, column=0, sticky=tk.W)

execute_button = ttk.Button(frame, text="執行", command=execute_sqlmap_thread)
execute_button.grid(row=11, column=1, sticky=tk.W)

# 運行主迴圈
root.mainloop()
