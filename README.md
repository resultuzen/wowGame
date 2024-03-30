# wowGame

![](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTkzeTE1YTdlYnBqZHc4d3Nib3p1YjBvemZ5b2hnb2l3cHU2ODk4NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xThuWtNFKZWG6fUFe8/giphy.gif)


#USB Ses Kartı Ayarları

İlk başta onboarddaki ses çıkışını pasifize etmemiz gerekiyor.

"sudo nano /etc/modprobe.d/raspi-blacklist.conf" dosyasına girip içerisine "blacklist snd_bcm2835" yazıyoruz.
 
Daha sonra USB ses kartının default indisini kaldırıyoruz. Satır başına # işareti koyuyoruz ve kaydediyoruz.

"sudo nano /lib/modprobe.d/aliases.conf dizinine giriyoruz" ve "options snd-usb-audio index=-2" satırını buluyoruz. Bu satırın başına # işareti koyuyoruz.

Hepsi bu kadar!

Bu sayede en başa USB ses kartının gelmesini sağlıyoruz. Onboard jackı da iptal etmiş oluyoruz.
