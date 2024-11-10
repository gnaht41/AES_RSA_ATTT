import numpy as np
from .sbox import Sbox, InvSbox, Rcon
# Import các ma trận M được tính toán sẵn (a(x) và nghịch đảo)
from .sbox import M1, M2, M3, M9, M11, M13, M14
# Import các hàm mã hóa và giải mã base64
from base64 import urlsafe_b64encode as b64encode
from base64 import urlsafe_b64decode as b64decode

# Định nghĩa phạm vi cho trạng thái
# -1 Tự động điều chỉnh kích thước của mảng theo các chiều còn lại
# 4,4 là số chiều mỗi cột và hàng trong ma trận 4x4
StateSlice = [-1, 4, 4]

# Hàm chuyển đổi văn bản đầu vào thành các trạng thái AES (ma trận 4x4)


def textToStates(text):
    # Mã hóa văn bản đầu vào nếu nó là một chuỗi
    if isinstance(text, str):
        text = text.encode()
    # Nếu văn bản đầu vào là bytes hoặc mảng numpy, không làm gì cả
    elif isinstance(text, (bytes, np.ndarray)):
        pass
    else:
        # Nếu loại dữ liệu đầu vào không được hỗ trợ, raise một lỗi
        raise TypeError("Loại dữ liệu đầu vào",
                        type(text), "không được hỗ trợ.")

    # Chuyển đổi văn bản thành trạng thái AES (ma trận 4x4)
    s0 = np.array(list(text))
    rest = (16 - (len(s0) % 16)) % 16
    s1 = np.r_[s0, np.zeros(rest)]
    s2 = s1.reshape(StateSlice)
    return s2.astype(np.int8)

# Hàm chuyển các trạng thái AES thành văn bản


def statesToText(state):
    s0 = state.ravel()
    s1 = s0.tostring()
    return s1.rstrip(b"\0")

# Biến đổi SubBytes


def subBytes(state):
    return np.take(Sbox, state)

# Biến đổi Inverse SubBytes


def invSubBytes(state):
    return np.take(InvSbox, state)

# Biến đổi ShiftRows


def lShiftRows(state):
    for i in range(4):
        state[:, i, :] = np.roll(state[:, i, :], -i)
    return state

# Biến đổi Inverse ShiftRows


def rShiftRows(state):
    for i in range(4):
        state[:, i, :] = np.roll(state[:, i, :], i)
    return state

# Biến đổi MixColumns sử dụng phương pháp tra bảng được tính sẵn )


def mixColumnByTable(a):
    b0, b1, b2, b3 = a
    d = np.zeros(4, dtype=np.int8)
    d[0] = M2[b0] ^ M3[b1] ^ M1[b2] ^ M1[b3]
    d[1] = M1[b0] ^ M2[b1] ^ M3[b2] ^ M1[b3]
    d[2] = M1[b0] ^ M1[b1] ^ M2[b2] ^ M3[b3]
    d[3] = M3[b0] ^ M1[b1] ^ M1[b2] ^ M2[b3]
    return d

# Biến đổi Inverse MixColumns sử dụng phương pháp tra bảng


def invMixColumnByTable(a):
    b0, b1, b2, b3 = a
    d = np.zeros(4, dtype=np.int8)
    d[0] = M14[b0] ^ M11[b1] ^ M13[b2] ^ M9[b3]
    d[1] = M9[b0] ^ M14[b1] ^ M11[b2] ^ M13[b3]
    d[2] = M13[b0] ^ M9[b1] ^ M14[b2] ^ M11[b3]
    d[3] = M11[b0] ^ M13[b1] ^ M9[b2] ^ M14[b3]
    return d

# Biến đổi MixColumns cho toàn bộ trạng thái


def mixColumn(state):
    s0 = state.transpose([0, 2, 1]).reshape((-1, 4))
    s1 = np.apply_along_axis(mixColumnByTable, 1, s0)
    s2 = s1.reshape([-1, 4, 4]).transpose([0, 2, 1])
    return s2

# Biến đổi Inverse MixColumns cho toàn bộ trạng thái


def invMixColumn(state):
    s0 = state.transpose([0, 2, 1]).reshape((-1, 4))
    s1 = np.apply_along_axis(invMixColumnByTable, 1, s0)
    s2 = s1.reshape([-1, 4, 4]).transpose([0, 2, 1])
    return s2

# Mở rộng khóa KeyExpansion


def keySchedule(key):
    if len(key) != 16:
        raise ValueError("Chỉ hỗ trợ khóa có độ dài 16 byte!")

    r0 = textToStates(key).reshape((4, 4)).tolist()
    for i in range(4, 4 * 11):
        r0.append([])   

        if i % 4 == 0:
            byte = r0[i - 4][0] ^ Sbox[r0[i - 1][1]] ^ Rcon[i // 4]
            r0[i].append(byte)

            for j in range(1, 4):
                byte = r0[i - 4][j] ^ Sbox[r0[i - 1][(j + 1) % 4]]
                r0[i].append(byte)
        else:
            for j in range(4):
                byte = r0[i - 4][j] ^ r0[i - 1][j]
                r0[i].append(byte)
    return np.array(r0).reshape((-1, 4, 4))

# Biến đổi AddRoundKey


def addRoundKey(state, key):
    return np.bitwise_xor(state, key)

# Hàm mã hóa AES


def aes_encrypt(data, key):
    # Tạo các khóa vòng
    roundKey = keySchedule(key)
    # Chuyển đổi dữ liệu đầu vào thành trạng thái AES
    state = textToStates(data)
    # Thêm khóa vòng ở vòng ban đầu
    s0 = addRoundKey(state, roundKey[0])
    # Các vòng từ 1 đến 10
    for i in range(1, 11):
        s1 = subBytes(s0)
        s2 = lShiftRows(s1)
        s3 = mixColumn(s2) if i != 10 else s2
        s0 = addRoundKey(s3, roundKey[i])
    # Chuyển trạng thái cuối cùng thành bytes và sau đó mã hóa base64
    s4 = s0.ravel().astype(np.int8)
    b0 = s4.tobytes()
    b1 = b64encode(b0)

    return b1

# Hàm giải mã AES


def aes_decrypt(b1, key):
    # Tạo các khóa vòng
    roundKey = keySchedule(key)
    # Giải mã dữ liệu đã được mã hóa base64 và chuyển đổi nó trở lại trạng thái AES
    b0 = b64decode(b1)
    s4 = np.frombuffer(b0, dtype=np.int8)
    s0 = s4.reshape([-1, 4, 4])
    # Các vòng từ 10 đến 1
    for i in reversed(range(1, 11)):
        s3 = addRoundKey(s0, roundKey[i])
        s2 = invMixColumn(s3) if i != 10 else s3
        s1 = rShiftRows(s2)
        s0 = invSubBytes(s1)
    # Vòng cuối cùng
    state = addRoundKey(s0, roundKey[0])
    # Chuyển trạng thái cuối cùng thành văn bản
    text = statesToText(state.astype(np.int8))

    return text
