from PIL import Image, ImageDraw, ImageFont
DOSYA_ADI = "olusan_bos_optik.jpg"
SAYI_FONTU = ImageFont.truetype("arial.ttf", 10)
YAZI_FONTU = ImageFont.truetype("arial.ttf", 20)
HARF_FONTU = ImageFont.truetype("arial.ttf", 12)

soru_sayisi = int(input("Soru sayisini girin(MAX 99):")) 
secenek_sayisi = int(input("Seçenek sayısını girin(MAX 5):")) 

GENISLIK = 550
YUKSEKLIK=int(450 + ((soru_sayisi*25) / 2))
    
img=Image.new("RGB", (GENISLIK, YUKSEKLIK), color="white")
cizim=ImageDraw.Draw(img)

#---------------------------------------------------
def ciz_siyah_kose_kare():
    """
    Optik formun dört köşesine hizalama amacıyla siyah kareler çizer.
    Sol üst  (x1,y1) sağ alt  (x2,y2) köşelere sabit koordinatlarla 
    50x50 boyutlarında dört adet siyah kutu çizilir.
    Bu kutular, formun kamera veya tarayıcıyla hizalanması için referans olarak kullanılır.
    """
    x1 = 20
    x2 = 70
    y1 = 20
    y2 = 70  
    cizim.rectangle((x1 , y1 , x2 , y2) , fill="black")
    cizim.rectangle((x1,(YUKSEKLIK - 70), x2, (YUKSEKLIK - 20)), fill="black")
    cizim.rectangle(((GENISLIK - 70), y1, (GENISLIK - 20), y2), fill="black")
    cizim.rectangle(((GENISLIK - 70), (YUKSEKLIK - 70), (GENISLIK - 20), (YUKSEKLIK - 20)),fill="black")

#---------------------------------------------------
def yaz_ogrenci_bilgileri():
    """
    Optik formun üst kısmına öğrencinin Ad, Soyad ve İmza etiketlerini yazar.

    Bu fonksiyon, y ekseni boyunca aralıklı(30 birim) şekilde üç metni (Ad, Soyad, İmza)
    sabit x koordinatına yazarak formun üst bölümünde bilgi alanlarını oluşturur.
    """
    
    y_ekseni=0
    bilgi=["Ad","Soyad","İmza"]
    for i in bilgi:
        cizim.text((120 , y_ekseni), f"{i}:", fill="black", font=YAZI_FONTU)
        y_ekseni = y_ekseni + 30
    
#---------------------------------------------------
def ciz_ogrenci_numarasi_daireleri():
    """
    Öğrenci numarasını yazmak için kutucuklar ve altına 0-9 arası işaretleme daireleri çizer.

    Parametre olarak gelen hane sayısına göre üstte dikdörtgen kutucuklar çizilir.
    Her kutucuğun altında 0'dan 9'a kadar rakamlar ve işaretleme için daireler yerleştirilir.
    Bu yapı, optik formlarda öğrenci numarasının doldurulması için kullanılır.

    Parametre:
        hane_sayisi (int): Öğrenci numarasının kaç haneden oluştuğu bilgisi.

    Return:
        None
    """
    cizim.text((120,100), text="NUMARA", fill="black", font=SAYI_FONTU)
    x1 = 120
    y1 = 120
    x2 = 140
    y2 = 140
    hane_sayisi=int(input("Öğrenci numarasını girin:")) 

    for i in range(hane_sayisi):       
        cizim.rectangle((x1, y1, x2, y2), outline="black")
        x1 = x1 + 25
        y1 = 120
        x2 = x2 + 25    
        y2 = y1 + 20
    daire_x1 = 120
    daire_y1 = 150
    daire_x2 = 140
    daire_y2 = 170
    for j in range(10):
        cizim.text(((daire_x1 - 10), (daire_y1 + 5)), f"{j}", fill="black", font=SAYI_FONTU)
        for i in range(hane_sayisi):
            cizim.ellipse((daire_x1, daire_y1, daire_x2, daire_y2),outline="black")
            # y degerleri sabit olup x degerleri artırılıyor 
            daire_x1 = daire_x1 + 25
            daire_x2= daire_x2 + 25    
         # x leri eski konumuna getirip y degerini artırıyoruz    
        daire_x1 = 120
        daire_x2 = 140
        daire_y1 = daire_y1 + 25
        daire_y2 = daire_y2 + 25
    
#---------------------------------------------------
def yaz_secenek_harfleri():
    """
    Soru baloncuklarının üzerine seçenek harflerini (A, B, C, D,E ) yazar.

    Seçenek sayısına göre A'dan başlayarak harfler, yatay olarak hizalanır.
    Bu işlem, formun iki sütununda yapılır. Harfler genellikle her sorunun üstüne denk gelecek şekilde konumlandırılır.Konumlar sabit değerlerdir sayfa boyutuna göre ayarlanmıştır.
    
    Return:
        None
    """
    harfler=["A","B","C","D","E","F"]
    harf_konum_x = 125
    harf_konum_y = 403
    for j in range(2):
        for i in range(secenek_sayisi):
            cizim.text((harf_konum_x, harf_konum_y), harfler[i], fill="black", font=HARF_FONTU)
            harf_konum_x = harf_konum_x + 25
        harf_konum_x = 285

#---------------------------------------------------
def ciz_soru_daireleri():
    """
    Form üzerine, her soru için seçenek baloncuklarını iki sütun halinde çizer.

    Bu fonksiyon, soruları optik forma yerleştirmek için kullanılır.
    Soru sayısı ikiye bölünerek iki sütuna dağıtılır.
    Her soru satırına, soru numarası ve altında seçilen 'secenek_sayisi' kadar boş daire çizilir.
    Daireler üst üste hizalanmış şekilde konumlandırılır.

    Tek sayıdaki sorular için ilk sütun 1 fazla olacak şekilde denge sağlanır.

    Yatayda her şık arasında 5 px boşluk bırakılır.
    Dikeyde her soru satırı 5 px aşağıya kayar.
    1. for yapısı soruları iki sütuna ayırır.
    2. for yapısı her bir sorunun altına seçenek dairelerini çizer y ekseni artırılır.
    3. for yapısı ise her bir seçeneğin dairesini çizer ve x eksenini artırır.
    1. for yapısı ilk dögüsünde 120 px den başlarken ikinci döngüde 280 px den başlar ikinici sütun için.

    Return:
        None
    """
    soru_bolum=int(soru_sayisi/2)
    secenek_x1 = 120
    secenek_y1 = 420
    secenek_x2 = 140
    secenek_y2 = 440

    sayac = 0 
    for a in range(2):
        if  soru_sayisi%2 == 1 :
            if a % 2 == 0:
                soru_bolum = soru_bolum + 1
            else:
                soru_bolum = soru_bolum - 1

        for i in range(soru_bolum):
            sayac = sayac + 1 # text ile soru numarsını yazdırmak için kullanılır
            cizim.text(((secenek_x1 - 15), (secenek_y1 + 5)), f"{sayac}", fill="black",  font=SAYI_FONTU)

            for j in range(secenek_sayisi): # ellipse ile daire çizimi için kullanılır
                cizim.ellipse((secenek_x1, secenek_y1, secenek_x2, secenek_y2), outline="black")
                secenek_x1 = secenek_x1 + 25
                secenek_x2 = secenek_x2 + 25
            if a == 0:
                secenek_x1 = 120
                secenek_x2 = 140
            elif a == 1 :
                i = soru_bolum
                secenek_x1 = 280
                secenek_x2 = 300
     
            secenek_y1 = secenek_y1 + 25
            secenek_y2 = secenek_y2 + 25

        secenek_x1 = 280
        secenek_y1 = 420
        secenek_x2 = 300
        secenek_y2 = 440
        
# Fonkisyonları çağırma
ciz_siyah_kose_kare()
yaz_ogrenci_bilgileri()
ciz_ogrenci_numarasi_daireleri()
yaz_secenek_harfleri()
ciz_soru_daireleri()

img.save(DOSYA_ADI)

