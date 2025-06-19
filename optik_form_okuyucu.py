import cv2
import numpy as np
import csv
import pandas as pd

#--------------------------------------------------------------
def bul_ogrenci_numarasi_konumlarini(hane_sayisi):
    """
    Öğrenci numarası kutusundaki işaretleme dairelerinin merkez koordinatlarını hesaplar.

    Her hane için 0-9 arası 10 daire yatay ve dikey olarak sıralanır. Daire merkezleri,
    başlangıç koordinatına göre 25 birim aralıklarla konumlandırılır.

    Parametre:
        hane_sayisi (int): Öğrenci numarasındaki hane sayısı.

    Return:
        list[tuple[int, int]]: Her dairenin (x, y) merkez koordinatları listesi.
    """

    konumlar = []
    x1 = 120 
    y1 = 150
    cap = 20
    for sutun in range(hane_sayisi):
        for satir in range(10):
            konumlar.append((x1 + cap// 2, y1 + cap // 2))
            y1 = y1 + 25
        x1 = x1 + 25    
        y1 = 150
    return konumlar



#-------------------------------------------------------------------------- 
def oku_ogrenci_numaralarini(thresh, konumlar):
    """
    Öğrenci numarası kutularındaki işaretli rakamları analiz ederek numarayı döndürür.

    Her hanedeki 10 daireyi kontrol eder. Dairenin içindeki siyah piksel oranı %15'ten fazlaysa
    işaretlenmiş kabul edilir. Bir hanede birden fazla daire işaretliyse 'X', hiçbiri işaretli
    değilse '?' karakteri eklenir. Her haneden yalnızca bir rakam alınması beklenir.

    Parametre:
        thresh (ndarray): Eşiklenmiş (siyah-beyaz, ters çevrilmiş) optik form görüntüsü.
        konumlar (list[tuple[int, int]]): Daire merkez koordinatları.

    Return:
        str: Okunan öğrenci numarası (örnek: '20315X8?').
    """

    cap = 20
    sonuc = ""
    hane_sayisi = len(konumlar) // 10  
    for hane in range(hane_sayisi):
        secilen = None 
        for rakam in range(10):
            index_numarasi = hane * 10 + rakam    
            x, y = konumlar[index_numarasi]
            alan = thresh[y - cap//2: y + cap//2, x - cap//2: x + cap//2] 
            if alan.shape != (cap, cap): 
                continue
            oran = cv2.countNonZero(alan) / alan.size 
            if oran > 0.15:
                if secilen is not None:
                    secilen = "X"
                    break
                secilen = str(rakam)
        if secilen is None:
            secilen = "?"
        sonuc = sonuc + secilen
    return sonuc

#----------------------------------------------------------------
def bul_soru_konumlarini(soru_sayisi, secenek_sayisi):
    """
    Her sorunun işaretleme dairelerinin merkez koordinatlarını hesaplar.

    Sorular iki sütuna bölünerek yerleştirilir. Her soruya ait şıklar (A, B, C, ...) yatayda,
    sorular ise dikeyde 25 birim aralıkla yerleştirilir. Tek sayıdaki sorular için
    ilk sütun bir soru fazla olacak şekilde ayarlanır. Her daire merkezi çap/2 kadar
    kaydırılarak belirlenir.

    Parametre:
        soru_sayisi (int): Formdaki toplam soru sayısı.
        secenek_sayisi (int): Her soruda bulunan şık sayısı.

    Return:
        list[tuple[int, int]]: Her şık için (x, y) merkez koordinatları listesi.
    """
    x_bas=120
    y_bas=420
    cap=20
    konumlar = []
    bolum = soru_sayisi // 2 
    for blok in range(2):
        y_bas=420 
        if soru_sayisi % 2 == 1:
            if blok == 0:
                 bolum = bolum + 1 
            else:
                 bolum = bolum - 1       
        for i in range(bolum):
            if blok == 0:
                 x_bas = 120
            else :
                x_bas = 280   
            for j in range(secenek_sayisi):
                konumlar.append((x_bas + cap // 2, y_bas + cap // 2))
                x_bas = x_bas + 25
            y_bas=y_bas + 25   
            
    return konumlar

#----------------------------------------------------------------
def oku_sorulari(thresh, konumlar, secenek_sayisi=5):
    cap=20
    cevaplar = []
    soru_sayisi = len(konumlar) // secenek_sayisi
    for soru in range(soru_sayisi):
        secilen = None
        for secenek in range(secenek_sayisi):
            index = soru * secenek_sayisi + secenek
            x, y = konumlar[index]
            alan = thresh[y - cap//2:y + cap//2, x - cap//2:x + cap//2]
            if alan.shape != (cap, cap):
                continue
            oran = cv2.countNonZero(alan) / alan.size
            if oran > 0.40:
                if secilen is not None:
                    secilen = "X"
                    break
                secilen = chr(65 + secenek)
        if secilen is None:
            secilen = "?"
        cevaplar.append(secilen)
    return cevaplar

#----------------------------------------------------------------
def duzenle_goruntuyu(path, soru_sayisi):
    """
    Optik form görüntüsünü işleyip hizalayarak düzgün bir şekilde kırpılmış form çıktısı döndürür.

    Bu fonksiyon, verilen optik form resmini okur ve:
    1. Görüntüyü gri tonlamaya çevirir.
    2. Eşikleme (thresholding) ile siyah-beyaz hale getirip tersine çevirir.
    3. Dış konturları tespit ederek köşe kareleri bulur.
    4. Bu dört köşe noktasına göre perspektif dönüşüm uygular.
    5. Sonuç olarak yamuk veya açılı çekilmiş görüntüyü düzeltilmiş olarak döndürür.

    Köşe kareler `cv2.findContours` ve `cv2.approxPolyDP` ile tespit edilir.
    `cv2.getPerspectiveTransform` fonksiyonu ile dönüşüm matrisi oluşturulur.
    `cv2.warpPerspective` ile bu matris görüntüye uygulanarak hizalama yapılır.

    Parametre:
        path (str): Okunacak optik form görüntüsünün dosya yolu.
        soru_sayisi (int): Formda yer alan toplam soru sayısı. (Görüntü yüksekliği hesaplamak için kullanılır.)

    Return:
        ndarray: Perspektif dönüşümü uygulanmış, hizalanmış ve kırpılmış optik form görüntüsü.
    """ 
    img = cv2.imread(path) 
    if img is None:
        raise FileNotFoundError(f"Resim bulunamadı: {path}") 

    gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    _, thresh = cv2.threshold(gri, 100, 255, cv2.THRESH_BINARY_INV) 
    kontur, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    konturlar = sorted(kontur, key=cv2.contourArea, reverse=True) 
    
    kose_noktalar = []
    for kontur_elemanlari in konturlar:
        yaklasik_kose_noktalar= cv2.approxPolyDP(kontur_elemanlari, 0.02*cv2.arcLength(kontur_elemanlari, True), True)
        if len(yaklasik_kose_noktalar) == 4:
            kose_noktalar.append(yaklasik_kose_noktalar.reshape(4, 2)) 
        if len(kose_noktalar) == 4:
            break
    if len(kose_noktalar) < 4:
        raise Exception("Dört köşe noktası bulunamadı")

    
    tum_noktalar = np.concatenate(kose_noktalar, axis=0) 

    def sirala_noktalari(pts):
        """
    Verilen dört köşe noktasını sol-üst, sağ-üst, sağ-alt, sol-alt sırasına göre sıralar.

    Noktalar, x+y toplamı ve y-x farkına göre analiz edilir.
    Bu sıralama, perspektif dönüşümün düzgün uygulanabilmesi için gereklidir.

    Parametre:
        pts (ndarray): Dört adet (x, y) köşe noktası içeren NumPy dizisi.

    Return:
        ndarray: Sıralanmış dört köşe noktası (float32 formatında).
    """
        toplam = pts.sum(axis=1) 
        fark = np.diff(pts, axis=1) # y-x farkı 
        return np.array([
            pts[np.argmin(toplam)],      # sol-üst: x+y toplamı en küçük olan nokta
            pts[np.argmin(fark)],       # sağ-üst: y-x farkı en küçük olan nokta
            pts[np.argmax(toplam)],      # sağ-alt: x+y toplamı en büyük olan nokta
            pts[np.argmax(fark)]        # sol-alt: y-x farkı en büyük olan nokta
        ], dtype="float32")
    kose_noktalar = sirala_noktalari(tum_noktalar)



    GENISLIK = 550
    YUKSEKLIK = int(450 + ((soru_sayisi * 25) / 2))
    hedef = np.array([
        [20, 20],
        [GENISLIK-20, 20],
        [GENISLIK-20, YUKSEKLIK-20],
        [20, YUKSEKLIK-20]
    ], dtype="float32")
    
    matris = cv2.getPerspectiveTransform(kose_noktalar, hedef) 
    img_duz = cv2.warpPerspective(img, matris, (GENISLIK, YUKSEKLIK))  

    return img_duz

#---------------------------------------------------------------- 
def olustur_csv(dosya_adi, ogrenci_no, cevaplar, soru_sayisi):
    """
    Verilen öğrenci numarası ve cevapları içeren bir CSV dosyası oluşturur.

    Parametre:
    dosya_adi : Oluşturulacak CSV dosyasının adı (örneğin 'cikti.csv').
    ogrenci_no : Öğrencinin numarası.
    cevaplar : Öğrencinin verdiği cevapları içeren liste (örn. ['A', 'C', 'B', ...]).
    soru_sayisi : Formda yer alan toplam soru sayısı.

    """
    with open(dosya_adi, "w", newline="") as f:
        yazdir = csv.writer(f)
        yazdir.writerow(["Ogrenci Numarasi"] + [f"{i+1}.Soru" for i in range(soru_sayisi)])
        yazdir.writerow([ogrenci_no] + cevaplar)

#----------------------------------------------------------------
def guncelle_csv(csv_dosyasi, cevap_anahtari):
    """
    Öğrenci cevaplarını cevap anahtarıyla karşılaştırarak doğru, yanlış, boş ve okunamayanları hesaplar
    ve bu bilgileri CSV dosyasına ekler.

    CSV dosyasındaki her satır bir öğrenciyi temsil eder. İlk sütun öğrenci numarasıdır,
    kalan sütunlar cevapladığı sorulardır. Bu fonksiyon her cevapla birlikte:

    - Cevap doğruysa 'Doğru' sayısını artırır.
    - Cevap '?' ise 'Boş' olarak sayar.
    - Cevap 'X' ise birden fazla işaretlenmiş olarak 'Okunmadı' sayar.
    - Diğer tüm hatalı cevaplar 'Yanlış' sayılır.

    Sonuçlar ["Dogru", "Yanlis", "Bos", "Okunmadi"] başlıklarıyla DataFrame'e eklenir
    ve dosya üzerine yazılarak güncellenir.

    Parametre:
        csv_dosyasi (str): Okunacak ve üzerine yazılacak CSV dosyasının adı.
        cevap_anahtari (list[str]): Her sorunun doğru cevabını içeren liste (örn. ["A", "B", "C", ...]).

    Return:
        None
    """
    df = pd.read_csv(csv_dosyasi)
    yeni_kolonlar = ["Dogru", "Yanlis", "Bos", "Okunmadi"]
    sonuclar = []

    for idx, satir in df.iterrows():
        cevaplar = satir.iloc[1:].tolist()  
        dogru = 0
        yanlis = 0
        bos = 0
        okunmadi = 0

        for ogrenci_cevabi, dogru_cevap in zip(cevaplar, cevap_anahtari):
            
            if ogrenci_cevabi == dogru_cevap:
                dogru =dogru + 1
            elif ogrenci_cevabi == "?":
                bos = bos + 1
            elif ogrenci_cevabi == "X":
                okunmadi = okunmadi + 1
            else:
                yanlis = yanlis + 1

        sonuclar.append([dogru, yanlis, bos, okunmadi])

    
    for i, kolon in enumerate(yeni_kolonlar):
        df[kolon] = [sonuc[i] for sonuc in sonuclar]

    
    df.to_csv(csv_dosyasi, index=False)
    print(f"Sonuçlar {csv_dosyasi} dosyasına eklendi.")


#----------------------------------------------------------------
cevap_anahtari = [
    "A", "B", "A", "A", "B", "A", "D", "B", "B", "C", "A", "A", "B", "A", "C", "D",
    "D", "C", "C", "A", "C", "D", "B", "A", "A", "B", "B", "B", "C", "A", "A", "B",
    "D", "C", "B", "A", "A"
]  

#---------------------------------------------------------------
# optik ayarları
soru_sayisi = int(input("Okunacak optiğin soru sayısını girin: "))
secenek_sayisi = int(input("Okunacak optiğin seçenek sayısını girin: "))
hane_sayisi = int(input("Okuncak optiğin öğrenci hane sayısını girin: "))

#---------------------------------------------------------------
img_path="okutulmus_form4.jpg"
#----------------------------------------------------------------
#Fonksiyonları çağırma 
img = duzenle_goruntuyu(img_path,soru_sayisi)  
gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gri, 100, 255, cv2.THRESH_BINARY_INV)

ogrenci_numara_konumlari = bul_ogrenci_numarasi_konumlarini(hane_sayisi)
soru_konumlar = bul_soru_konumlarini(soru_sayisi, secenek_sayisi)
ogrenci_numarasi = oku_ogrenci_numaralarini(thresh, ogrenci_numara_konumlari)
soru_cevaplari = oku_sorulari(thresh, soru_konumlar, secenek_sayisi=secenek_sayisi)
olustur_csv("cikti.csv", ogrenci_numarasi, soru_cevaplari, soru_sayisi)
guncelle_csv("cikti.csv", cevap_anahtari)

print("csv dosyasına yazıldı: cikti.csv")

