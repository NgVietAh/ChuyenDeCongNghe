class FourDigitYearConverter:
    # regex này cho phép chỉ nhận đúng 4 chữ số
    regex = "[0-9]{4}"

    # Hàm này chuyển chuỗi (string) từ URL thành kiểu dữ liệu Python
    def to_python(self, value):
        return int(value)

    # Hàm này chuyển ngược từ Python thành string để đưa vào URL
    def to_url(self, value):
        return "%04d" % value
