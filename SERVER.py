from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 23458
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def gelen_mesaj():
    """Gelen Mesajların Kontrolünü Sağlayan Fonksiyon."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s baglandı. " % client_address)
        client.send(bytes("Chat Uygulamasına Hoşgeldiniz! \n " +
                          "Lütfen Adinizi Giriniz:", "utf8"))
        addresses[client] = client_address
        Thread(target=baglan_client, args=(client,)).start()


def baglan_client(client):
    """Client Bağlantısını Sağlar"""
    isim = client.recv(BUFFERSIZE).decode("utf8")
    hosgeldin = "Hosgeldin %s! Cikmak için {cikis} yaziniz!" % isim
    try:
        client.send(bytes(hosgeldin, "utf8"))
    except ConnectionResetError:
        print("Çıkış başarıyla gerçekleşti")
    msg = "%s Chat Kanalina Baglandi!" % isim
    yayin(bytes(msg, "utf8"))
    clients[client] = isim
    while True:
        try:
           msg = client.recv(BUFFERSIZE)
        except ConnectionResetError:
            pass
        if msg != bytes("{cikis}", "utf8"):
            yayin(msg, isim + ":")
        else:
            client.send(bytes("{cikis}", "utf8"))
            client.close()
            del clients[client]
            yayin(bytes("%s Kanaldan Cikis Yapti." % isim, "utf8"))
            break


def yayin(msg, kisi=""):
    for yayim in clients:
        try:
            yayim.send(bytes(kisi, "utf8") + msg)
        except TypeError:
            pass

# Program Başlangıc
if __name__ == "__main__":
        SERVER.listen(10)  # MAX 10 BAĞLANTIYA İZİN VERİR!
        print("Baglanti Bekleniyor...")
        ACCEPT_THREAD = Thread(target=gelen_mesaj)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()