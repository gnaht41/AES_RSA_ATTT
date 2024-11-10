import tkinter as tk  # Import thư viện tkinter để tạo giao diện người dùng.
from rsa import RSA  # Import lớp RSA từ file rsa.py.


class RSAApplication(tk.Tk):
    def __init__(self, keysize):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha.
        self.keysize = keysize  # Thiết lập kích thước khóa cho ứng dụng.
        # Đặt tiêu đề cho cửa sổ ứng dụng.
        self.title("RSA Encryption and Decryption")
        self.geometry("500x400")  # Đặt kích thước của cửa sổ ứng dụng.

        # Tạo nhãn để nhập thông điệp.
        self.label = tk.Label(self, text="Enter message:")
        self.label.pack()

        # Tạo ô nhập thông điệp.
        self.input_entry = tk.Text(self, width=50, height=3)
        self.input_entry.pack()

        # Tạo nhãn hiển thị khóa công khai.
        self.public_key_label = tk.Label(self, text="Public Key:")
        self.public_key_label.pack()

        # Ô văn bản để hiển thị khóa công khai.
        self.public_key_text = tk.Text(self, height=2, width=50)
        self.public_key_text.pack()

        # Tạo nhãn hiển thị khóa riêng tư.
        self.private_key_label = tk.Label(self, text="Private Key:")
        self.private_key_label.pack()

        # Ô văn bản để hiển thị khóa riêng tư.
        self.private_key_text = tk.Text(self, height=2, width=50)
        self.private_key_text.pack()

        self.result_text_label = tk.Label(
            self, text="Encrypted/Decrypted message")
        self.result_text_label.pack()

        self.result_text = tk.Text(self, width=50, height=3)
        self.result_text.pack()

        # Tạo nút Encrypt để mã hóa thông điệp.
        self.encrypt_button = tk.Button(
            self, text="Encrypt", command=self.encrypt_message)
        self.encrypt_button.pack()

        # Tạo nút Decrypt để giải mã thông điệp.
        self.decrypt_button = tk.Button(
            self, text="Decrypt", command=self.decrypt_message)
        self.decrypt_button.pack()

        # Tạo nút Generate Keys để tạo khóa công khai và riêng tư.
        self.generate_keys_button = tk.Button(
            self, text="Generate Keys", command=self.generate_keys)
        self.generate_keys_button.pack()

    def encrypt_message(self):
        # Kiểm tra xem đã tạo khóa chưa.
        if self.rsa is None:
            self.public_key_text.delete("1.0", tk.END)
            self.public_key_text.insert(tk.END, "Please generate keys first!")
            return

        # Lấy thông điệp từ ô nhập và mã hóa.
        msg = self.input_entry.get("1.0", tk.END)
        encrypted_message = self.rsa.encrypt(msg)
        # Xóa nội dung cũ và hiển thị thông điệp đã mã hóa.
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, encrypted_message)

    def decrypt_message(self):
        # Lấy thông điệp đã mã hóa từ ô văn bản và giải mã.
        encrypted_message = self.input_entry.get("1.0", tk.END)
        decrypted_message = self.rsa.decrypt(encrypted_message)
        # Xóa nội dung cũ và hiển thị thông điệp đã giải mã.
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, decrypted_message)

    def generate_keys(self):
        # Tạo khóa công khai và riêng tư.
        self.rsa = RSA(self.keysize)
        # Hiển thị khóa công khai và riêng tư.
        public_key = f"{self.rsa.e}"
        private_key = f"{self.rsa.d}"
        self.public_key_text.delete("1.0", tk.END)
        self.public_key_text.insert(tk.END, public_key)
        self.private_key_text.delete("1.0", tk.END)
        self.private_key_text.insert(tk.END, private_key)


if __name__ == "__main__":
    # Tạo ứng dụng RSA với kích thước khóa là 1024 bit và chạy ứng dụng.
    app = RSAApplication(1024)
    app.mainloop()
