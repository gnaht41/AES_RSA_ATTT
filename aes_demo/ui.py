from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from aes import aes_encrypt, aes_decrypt
# tkinter.filedialog: Thư viện cung cấp hộp thoại chọn tệp để người dùng có thể chọn tệp văn bản cần mã hóa hoặc giải mã.
# aes_encrypt, aes_decrypt: Các hàm dùng để mã hóa và giải mã văn bản sử dụng thuật toán AES từ mô-đun aes.


def browsepage():
    # Tạo một cửa sổ Tkinter mới cho hộp thoại tập tin
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ gốc

    # Yêu cầu người dùng chọn một tập tin
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))

    # Nếu một tệp được chọn, hãy đọc nội dung của tệp đó và cập nhật tiện ích Văn bản
    if filename:
        with open(filename, 'r') as file:
            text = file.read()
            # Xóa bất kỳ văn bản hiện có nào trong tiện ích Văn bản
            e1.delete(1.0, END)
            # Chèn nội dung của tệp vào tiện ích Văn bản
            e1.insert(END, text)


# Giới hạn độ dài của khóa AES (trong trường hợp này là 16 ký tự).
# Nếu người dùng nhập khóa dài hơn 16 ký tự, hàm này sẽ cắt bớt khóa chỉ còn 16 ký tự.


def lim(*args):
    value = dayValue.get()
    if len(value) > 16:
        dayValue.set(value[:16])


# Đảm bảo khóa AES có độ dài chính xác là 16 ký tự (mặc định của AES-128).
# Nếu khóa ngắn hơn 16 ký tự, nó sẽ được thêm padding (bằng ký tự null \x00) cho đến khi đạt độ dài 16 ký tự.
def pad_key(key, desired_length):
    if len(key) >= desired_length:
        return key[:desired_length]  # Cắt bớt nếu dài hơn độ dài mong muốn
    padding_length = desired_length - len(key)
    padded_key = key + '\x00' * padding_length  # Pad với byte rỗng
    return padded_key

# Lấy văn bản từ widget e1, khóa từ widget e2, và sau đó mã hóa văn bản đó bằng thuật toán AES.
# Nếu khóa không đủ 16 ký tự, một hộp thoại thông báo lỗi sẽ xuất hiện. Kết quả mã hóa sẽ được hiển thị trong widget e3.


def show_entry_fields():
    text = e1.get(1.0, END).strip()
    key = e2.get()
    key = pad_key(key, 16)
    error = "Please insert 16 character Key"
    if len(key) < 16:
        tkinter.messagebox.showerror("Error", error)
    encrypted = aes_encrypt(text, key)
    # print("\n\tEncrypted message is:\n")
    # print(encrypted.decode())
    # tkinter.messagebox.showinfo("Encrypted Text",encrypted.decode())
    e3.delete(1.0, END)
    e3.insert(END, encrypted.decode())

# Lấy văn bản mã hóa từ widget e3 và giải mã nó bằng thuật toán AES. Nếu khóa không đủ 16 ký tự, sẽ có thông báo lỗi.
# Kết quả giải mã sẽ được hiển thị trong widget e4.


def show_decryption_fields():
    text = e3.get(1.0, END).strip()
    key = e2.get()
    key = pad_key(key, 16)
    error = "Please insert 16 character Key"
    if len(key) < 16:
        tkinter.messagebox.showerror("Error", error)
    decrypted = aes_decrypt(text, key)
    # print("\n\tDecrypted message is:\n")
    # print(decrypted.decode())
    # tkinter.messagebox.showinfo("Decrypted Text",decrypted.decode())
    e4.delete(1.0, END)
    e4.insert(END, decrypted.decode())


# Cửa sổ chính của ứng dụng (master) có kích thước 600x400 và tiêu đề "AES Encryption".
master = Tk()
master.geometry('600x400')
master.title("AES Encryption")


# Các Label dùng để hiển thị thông tin cho người dùng như: "Plaintext", "Key", "Encrypted message", và "Decrypted message".
Label(master, text="Plaintext").grid(row=0, column=1)
Label(master, text="Key").grid(row=10, column=1)
Label(master, text="Encrypted message").grid(row=12, column=1)
Label(master, text="Decrypted message").grid(row=14, column=1)

dayValue = StringVar()
encrypted_msg = StringVar()
decrypted_msg = StringVar()
dayValue.trace('w', lim)

e1 = Text(master, width=40, height=5)
e2 = Entry(master, width=20, textvariable=dayValue)
e3 = Text(master, width=50, height=3)
e4 = Text(master, width=50, height=3)

e1.grid(row=1, column=1)
e2.grid(row=11, column=1)
e3.grid(row=13, column=1)
e4.grid(row=15, column=1, rowspan=2)


# Các Button cho phép người dùng thực hiện các hành động như:
# "Import from File" để nhập dữ liệu từ tệp.
# "Encrypt" để mã hóa văn bản.
# "Decrypt" để giải mã văn bản.
Button(master, text='Import from File', command=browsepage).grid(
    row=80, column=1, sticky=W, pady=4)
Button(master, text='Encrypt', command=show_entry_fields).grid(
    row=80, column=2, sticky=W, pady=4)
Button(master, text='Decrypt', command=show_decryption_fields).grid(
    row=80, column=3, sticky=W, pady=4)

# Vòng lặp chính của ứng dụng Tkinter, giữ cho cửa sổ giao diện hoạt động và chờ người dùng tương tác.
mainloop()
