#  Optik Form Oluşturucu ve Okuyucu Sistemi

Bu proje, eğitim ortamlarında yaygın olarak kullanılan optik formların dijital ortamda hem oluşturulmasını hem de görüntüler üzerinden otomatik okunmasını sağlamak amacıyla geliştirilmiştir.

##  Proje Amacı

- Kullanıcının belirlediği soru ve seçenek sayısına göre **optik form oluşturmak**.
- Öğrenciler tarafından doldurulan bu formların fotoğrafları üzerinden **otomatik olarak değerlendirme yapmak**.
- **Öğrenci numarası**, **adı soyadı**, **imza alanı**, **cevaplar** ve **hizalama kutuları** gibi alanları forma ekleyerek gerçek sınav formatına uygunluk sağlamak.

##  Kullanılan Teknolojiler ve Kütüphaneler

- Python
- Pillow (görsel oluşturma)
- OpenCV (görüntü işleme)
- NumPy (sayısal işlemler)
- pandas (veri analizi)
- csv (veri kaydı)

##  Özellikler

-  Dinamik optik form oluşturma (soru/satır/sütun sayısı kullanıcı tarafından ayarlanabilir)
-  Görüntüden optik form okuma
-  Cevap anahtarı ile karşılaştırma yaparak puan hesaplama
-  Sonuçları CSV formatında dışa aktarma

##  Nasıl Kullanılır?

1- Gerekli kütüphaneleri yükleyin ve kodu çalıştırın 
2- Optik form oluşturmada soru sayısını, öğrenci numarsını,seçenek sayısını uygun bir şekilde doldurun.
3- Oluşan optiği doldurun.
4- Doldurduğunuz optik formu fotoğrafını çekerek sisteme yükleyin.
5- Çıkan sonuçlar csv dosyasına yazılır.
