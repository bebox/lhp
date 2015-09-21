import operator

def pozicijaSprite(broj, x_velicina):
  #vraca pixel na kojem se sprite nalazi
  pixel = broj * (x_velicina + 1) #1 je prazan red izmedu spritova
  return(pixel)

#spriteSlova = ["A", "B", "C", "D", "E", "F", "G", "H", "i", "s", "e"]
spriteSlova = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "s", ",", "'", "1", "2", "4", "8", "6", "3", ".", "5", "7", "9", "0", "M", "B"]

def pixel2Ton(pixel):
  rezolucija = 90
  indent = -12 #extra pixeli
  height = 3
  broj = ( rezolucija - pixel - indent ) / height
  return(int(broj))
  
kljucevi = {
        0 : ("d", ",,"),
        1 : ("e", ",,"),
        2 : ("f", ",,"),
        3 : ("g", ",,"),
        4 : ("a", ",,"),
        5 : ("h", ",,"),
        6 : ("c", ","),
        7 : ("d", ","),
        8 : ("e", ","),
        9 : ("f", ","),
        10 : ("g", ","),
        11 : ("a", ","),
        12 : ("h", ","),
        13 : ("c", ""),
        14 : ("d", ""),
        15 : ("e", ""),
        16 : ("f", ""),
        17 : ("g", ""),
        18 : ("a", ""),
        19 : ("h", ""),
        20 : ("c", "'"),
        21 : ("d", "'"),
        22 : ("e", "'"),
        23 : ("f", "'"),
        24 : ("g", "'"),
        25 : ("a", "'"),
        26 : ("h", "'"),
        27 : ("c", "''"),
        28 : ("d", "''"),
        29 : ("e", "''"),
        30 : ("f", "''"),
        31 : ("g", "''"),
        32 : ("a", "''"),
        33 : ("h", "''"),
        34 : ("c", "'''"),
        35 : ("d", "'''"),
        36 : ("e", "'''"),
        37 : ("f", "'''"),
        38 : ("g", "'''"),
        39 : ("a", "'''"),
        40 : ("h", "'''")
}

def removeLily(slovo):
  return(slovo.replace(',', '').replace('\'', '').upper())

def slovoPozicija(slovo):
  for i in [i for i,x in enumerate(spriteSlova) if x == slovo]:
    return(i)

rijecnikNotnihVrijednosti = {
  0 : "16",
  1 : "8",
  2 : "8.",
  3 : "4",
  4 : "416",
  5 : "4.",
  6 : "4.16",
  7 : "2",
  8 : "216",
  9 : "28",
  10 : "28.",
  11 : "2.",
  12 : "2.16",
  13 : "2.8",
  14 : "2.8.",
  15 : "1"
}

def pixel2Pozicija(pixel):
  rezolucija = 90
  indent = 19 #extra pixeli
  width = 6
  broj = ( pixel - indent ) / width
  return(int(broj))

def pixel2Trajanje(pixel):
  indent = 4
  width = 6
  broj = ( pixel - indent ) / width
  return(int(broj))

def ton2Pixel(ton):
  rezolucija = 90
  indent = -12
  height = 3
  pixel = rezolucija - indent - ( ton * height )
  return(pixel)

def pozicija2Pixel(pozicija):
  rezolucija = 90
  indent = 19 #extra pixeli
  width = 6
  pixel = pozicija * width + indent 
  return(pixel)

def trajanje2Pixel(trajanje):
  indent = 4
  width = 6
  pixel = trajanje * width + indent
  return(pixel)

class dodaj_notu(object):
  def __init__(self, pozicija, ton, trajanje, predikat):
    self.pozicija=pozicija
    self.ton=ton
    self.trajanje=trajanje
    self.predikat=predikat

class cursor(object):
  def __init__(self, pozicija, ton, trajanje):
    self.pozicija = pozicija
    self.ton = ton
    self.trajanje = trajanje
    self.sprite = 0
    self.bg_scroll_x = 0
    self.bg_scroll_y = 0
    self.bg_scroll_x_offset = 0 #used for cursor follow efect
    self.bg_scroll_y_offset = 0 #used for cursor follow efect
    self.apsolute_x = 0 #used for cursor follow efect
    self.apsolute_y = 0 #used for cursor follow efect

def checkXColision(nota, cursorLeft, trajanje):
  if ( nota.pozicija == cursorLeft):
    print("kolizija na pocetku note s CL")
    return(True)
  elif ( cursorLeft > nota.pozicija ) & ( cursorLeft < ( nota.pozicija + nota.trajanje )):
    print("kolizija na sredini note s CL")
    return(True)
  elif ( cursorLeft == ( nota.pozicija + nota.trajanje )):
    print("kolizija na kraju note s CL")
    return(True)
  elif ( nota.pozicija == ( cursorLeft + trajanje)):
    print("kolizija na pocetku note s CR")
    return(True)
  elif ( ( cursorLeft + trajanje ) > nota.pozicija ) & ( ( cursorLeft + trajanje ) < ( nota.pozicija + nota.trajanje )):
    print("kolizija na sredini note sa CR")
    return(True)
  elif ( ( cursorLeft + trajanje ) == ( nota.pozicija + nota.trajanje )):
    print("kolizija na kraju note s CR")
    return(True)
  elif ( ( cursorLeft < nota.pozicija ) & ( ( cursorLeft + trajanje ) > (nota.pozicija + nota.trajanje ))):
    print("kolizija note unutar Cursora")
    return(True)
  else:
    return(False)

#sortiraj listu klasa
#lista.sort(key=operator.attrgetter('broj'))

def brisiNotu(nota, cursorLeft, trajanje):
  if ( nota.pozicija == cursorLeft):
    print("brisanje na pocetku note s CL")
    return(True)
  elif ( cursorLeft > nota.pozicija ) & ( cursorLeft < ( nota.pozicija + nota.trajanje )):
    print("brisanje na sredini note s CL")
    return(True)
  elif ( cursorLeft == ( nota.pozicija + nota.trajanje )):
    print("brisanje na kraju note s CL")
    return(True)
  elif ( nota.pozicija == ( cursorLeft + trajanje)):
    print("brisanje na pocetku note s CR")
    return(True)
  elif ( ( cursorLeft + trajanje ) > nota.pozicija ) & ( ( cursorLeft + trajanje ) < ( nota.pozicija + nota.trajanje )):
    print("brisanje na sredini note sa CR")
    return(True)
  elif ( ( cursorLeft + trajanje ) == ( nota.pozicija + nota.trajanje )):
    print("brisanje na kraju note s CR")
    return(True)
  elif ( ( cursorLeft < nota.pozicija ) & ( ( cursorLeft + trajanje ) > (nota.pozicija + nota.trajanje ))):
    print("brisanje note unutar Cursora")
    return(True)
  else:
    return(False)
