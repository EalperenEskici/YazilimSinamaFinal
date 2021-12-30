#Client Bağlantisi
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import hashlib as hasher
import tkinter

şifreleyici = hasher.sha256()
def gelen_mesaj():
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            sifrelenmeyecekMsg = ""
            sifrelenecekMsg = ""
            sayac = 0
            for i in msg:
                if sayac == 1:
                    sifrelenecekMsg+=i
                else:
                    sifrelenmeyecekMsg+=i
                    if i == ":":
                        sayac +=1
            şifreleyici.update(sifrelenecekMsg.encode("utf-8"))
            hasher = şifreleyici.hexdigest()
            if hasher == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
                msg = sifrelenmeyecekMsg
            else:
                msg = sifrelenmeyecekMsg
                msg += hasher
            mesaj_listesi.insert(tkinter.END,msg)
        except:
            break

def gonder(event=None):
    msg = mesajim.get()
    mesajim.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{cikis}":
        client_socket.close()
        app.quit()

def cikis_durumu(event=None):
    mesajim.set("{cikis}")
    gonder()

# App arayüzü
app = tkinter.Tk()
app.title("yzmsnmaProje")


mesaj_alani = tkinter.Frame(app)
mesajim = tkinter.StringVar()
mesajim.set("Mesajı Giriniz...")
scrollbar = tkinter.Scrollbar(mesaj_alani)
mesaj_listesi = tkinter.Listbox(mesaj_alani, height=20, width=70, yscrollcommand=scrollbar.set)
mesaj_listesi.see("end")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
mesaj_listesi.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mesaj_alani.pack()
giris_alani = tkinter.Entry(app, textvariable=mesajim)
giris_alani.bind("<Return>", gonder)
giris_alani.pack()
gonder_buton = tkinter.Button(app, text="Gonder", command= gonder)
gonder_buton.pack()

app.protocol("WM_DELETE_WINDOW", cikis_durumu)

HOST = '127.0.0.1'
PORT = 23458
BUFFERSIZE = 1024
ADDR= (HOST,PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
if not PORT:
    PORT = 23458
else:
    PORT = int(PORT)

gelen_thread = Thread(target=gelen_mesaj)
gelen_thread.start()
tkinter.mainloop()