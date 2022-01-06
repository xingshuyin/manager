import binascii
from pyDes import des, CBC, PAD_PKCS5


def pages_divider(page, page_range, perpage=5):
    page = int(page)
    if len(page_range) < perpage:
        return page_range
    if perpage / 2 - int(perpage / 2) == 0.5:
        start = page - int(perpage / 2)
        end = page + int(perpage / 2)
        if start < 1:
            start = 1
            end = perpage
        if end > page_range[-1]:
            end = page_range[-1]
            start = end - perpage
        return range(start, end + 1)
    else:
        start = page - int(perpage / 2) + 1
        end = page + int(perpage / 2)
        if start < 1:
            start = 1
            end = perpage
        if end > page_range[-1]:
            end = page_range[-1]
            start = end - perpage + 1
        return range(start, end + 1)


def secret(key, s):
    # key加密密钥 CBC加密模式  padmode自动补全缺失长度 pad补充字符
    d = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)  # 创建加密器
    r = d.encrypt(s)  # 加密
    return binascii.b2a_hex(r).decode()  # 二进制转换字符串返回


def desecret(key, s):
    d = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
    r = d.decrypt(binascii.a2b_hex(s))
    return r.decode()
