import hashlib as hasher
şifreleyici = hasher.sha256()
metin ="abc1234"
metin2 ="abc1234"
şifreleyici.update(metin.encode("utf8"))
şifreleyici.update(metin2.encode("utf8"))
hashlenmişŞifre = şifreleyici.hexdigest()



