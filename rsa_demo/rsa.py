import random

# Kiểm tra số nguyên tố


def isprime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Viết n dưới dạng 2^r * d + 1
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Tìm ước số chung lớn nhất


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# Sinh số nguyên tố lớn


def generateLargePrime(keysize):
    # Hàm này tạo một số nguyên tố lớn với số bit cho trước.
    while True:
        # Sinh một số ngẫu nhiên trong khoảng đã cho.
        num = random.randrange(2 ** (keysize - 1), 2 ** (keysize + 1))
        # Kiểm tra xem số vừa sinh có phải là số nguyên tố hay không.
        if isprime(num):
            return num


# Tính GCD mở rộng


def gcdExtended(a, m):
    # Hàm tính gcd (ước số chung lớn nhất) mở rộng giữa hai số a và m.
    if a == 0:  # Nếu a bằng 0, trả về m và hai giá trị 0, 1.
        return m, 0, 1
    gcd, x1, y1 = gcdExtended(m % a, a)  # Gọi đệ quy để tính gcd, x1, y1.
    x = y1 - (m // a) * x1  # Tính giá trị mới của x.
    return gcd, x, x1

# Tính nghịch đảo modulo


def moduloInverse(a, m):
    # Hàm tính nghịch đảo modulo của a mod m.
    gcd, x, y = gcdExtended(a, m)  # Tính gcd và hai giá trị mở rộng.
    if gcd != 1:  # Nếu gcd không bằng 1, không có nghịch đảo modulo.
        return -1
    return x % m  # Trả về nghịch đảo modulo.

# Khởi tạo các thông số RSA


def initialize(keysize):
    # Hàm khởi tạo các thông số cần thiết cho thuật toán RSA.
    p = generateLargePrime(keysize)  # Tạo số nguyên tố lớn p.
    q = generateLargePrime(keysize)  # Tạo số nguyên tố lớn q.
    while p == q:  # Đảm bảo p và q không bằng nhau.
        q = generateLargePrime(keysize)
    n = p * q  # Tính n = p * q.
    phiN = (p - 1) * (q - 1)  # Tính số Euler của n.

    while True:  # Lặp cho đến khi chọn được e thỏa mãn điều kiện.
        # Chọn một số e ngẫu nhiên.
        e = random.randrange(2 ** (keysize - 1), 2 ** (keysize + 1))
        # Kiểm tra xem e có là số nguyên tố cùng nhau với phiN hay không (e.d===1(mod)).
        if gcd(e, phiN) == 1:
            break
    d = moduloInverse(e, phiN)  # Tính nghịch đảo modulo của e mod phiN.
    return p, q, n, e, d  # Trả về các thông số đã tạo.


class RSA(object):
    def __init__(self, keysize):
        # Khởi tạo đối tượng RSA với kích thước khóa cho trước.
        self.keysize = keysize
        # Khởi tạo p, q, n, e, d cho thuật toán RSA.
        self.p, self.q, self.n, self.e, self.d = initialize(self.keysize)

    def encrypt(self, msg):
        cipher = ""  # Chuỗi để lưu trữ mã hóa.
        for c in msg:  # Duyệt qua từng ký tự trong tin nhắn.
            m = ord(c)  # Chuyển đổi ký tự thành mã ASCII.
            # Mã hóa và thêm vào chuỗi mã hóa (m mũ e mod n)
            cipher += str(pow(m, self.e, self.n)) + " "
        return cipher

    def decrypt(self, cipher):
        msg = ""  # Chuỗi để lưu trữ tin nhắn giải mã.
        parts = cipher.split()  # Tách chuỗi mã hóa thành các phần.
        for part in parts:  # Duyệt qua từng phần.
            c = int(part)  # Chuyển đổi phần đã mã hóa thành số nguyên.
            # Mã hóa và thêm vào chuỗi mã hóa (c mũ d mod n)
            # Chuyển đổi số nguyên (giá trị ASCII) thành ký tự
            msg += chr(pow(c, self.d, self.n))
        return msg
