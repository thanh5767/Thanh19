"cau 1"

d = (input("Nhap van ban can tim xac suat xuat hien: ")) + " "
temp = ""
count_d = []
for i in d:
    if i != " ":
        temp += i.upper()
    else:
        count_d.append(temp)
        temp = ""
text = {}
for i in count_d:
    if i not in text:    
        text[i] = 1
    elif i in text:
        text[i] += 1
for i in text:
    text[i] = (text[i]/len(count_d))*100
for i in text:
    print(f"p({i}): {text[i]}%")
    
        
"Cau 3"

class congnhan:
    def _intf__(self, mcn, ht, b, snlv, nkhd):
        self.mcn + mcn
        self.ht + ht
        self.b + b
        self.snlv + snlv
        self.nkhd + nkhd 
        self.tl
    def In(self):
        self.nkhd = ("day" + "/" + "month" + "/" "year")
        print("Nhap ma cong nhan: {self.mcn}")
        print("Nhap ho ten cong nhan: {self.ht}")
        print("Nhap bac cong nhan (1 den 3): {self.b}")
        print("Nhap so ngay cua cong nhan: {self.snlv}")
        print("Nhap ngay ki cua cong nhan: {self.nkhd}")
    def Out(self):
        print("Ma cong nhan: ", self.mcn)
        print("Ho ten cong nhan: ", self.ht)
        print("Bac cong nhan: ", self.b)
        print("So ngay cua cong nhan: ", self.snlv)
        print("Ngay ki hop dong cua cong nhan: ", self.nkhd)
        tl = 0
        if self.b == 1:
            tl = self.snlv * 300000
            print("Tien luong tong: {tl}")
        if self.b == 2:
            tl = self.snlv * 350000
            print("Tien luong tong: {tl}")
        if self.b == 3:
            tl = self.snlv * 400000
            print("Tien luong tong: {tl}")
congnhan = "22t102", "Ho Trong Giap", "1", "50", "20/5/2020"
print(congnhan)


    
        

