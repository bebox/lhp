import operator

spriteFont = [
    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
    " ", "!", "\"", "#", "$", "%", "", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
    "", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_",
    "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", ""
    ]

loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque posuere, est eu finibus posuere, velit nunc faucibus orci, eget congue ligula erat eu nisi. Mauris sed accumsan risus. Nulla pretium urna eu ante consequat lobortis. Suspendisse non arcu porta, aliquam ante eu, ornare tellus. Ut vestibulum vel ex quis consequat. Phasellus auctor fringilla orci, ac viverra metus pulvinar at. Suspendisse non lectus eget justo dapibus scelerisque. Nullam nec venenatis lorem, in elementum sem. Cras sollicitudin ligula vitae nibh dignissim sagittis. Duis vitae finibus nibh. Maecenas ut orci a elit tristique porta quis in massa. Suspendisse id mattis mi, eu dapibus enim. Praesent sodales ante eget ligula euismod, vel pulvinar nibh tempor."

color_white = (255,255,255)
color_git = (77,78,80)

roundSnap = {
    4 : 1/4,
    2 : 1/2,
    1 : 1,
    1/2 : 2,
    1/4 : 4,
    1/8 : 8,
    1/16 : 16
}

listMusic2Float = [64, 32, 16, 8, 4, 2, 1]
hashMusic2Float = {
    1 : 4,
    2 : 2,
    4 : 1,
    8 : 1/2,
    16 : 1/4,
    32 : 1/8,
    64 : 1/16,
}

def listIndexStep(obj, lista, step):
    return(lista[lista.index(obj)+step])

class dodaj_notu(object):
  def __init__(self, pozicija, ton, trajanje, predikat):
    self.pozicija=pozicija
    self.ton=ton
    self.trajanje=trajanje
    self.predikat=predikat
    self.ligatura=False

class cursor(object):
  def __init__(self, pozicija, ton, trajanje, snap):
    self.pozicija = pozicija
    self.ton = ton
    self.trajanje = trajanje
    self.sprite = 0
    self.snap = snap
    #self.bg_scroll_x = 0
    #self.bg_scroll_y = 0
    #self.bg_scroll_x_offset = 0 #used for cursor follow efect
    #self.bg_scroll_y_offset = 0 #used for cursor follow efect
    #self.apsolute_x = 0 #used for cursor follow efect
    #self.apsolute_y = 0 #used for cursor follow efect

def findNote(nota, cursorLeft, trajanje):
  if ( nota.pozicija == cursorLeft):
    print("na pocetku note s CL")
    return(1)
  elif ( cursorLeft > nota.pozicija ) & ( cursorLeft < ( nota.pozicija + nota.trajanje )):
    print("na sredini note s CL")
    return(2)
  elif ( cursorLeft == ( nota.pozicija + nota.trajanje )):
    print("na kraju note s CL")
    return(3)
  elif ( nota.pozicija == ( cursorLeft + trajanje)):
    print("na pocetku note s CR")
    return(4)
  elif ( ( cursorLeft + trajanje ) > nota.pozicija ) & ( ( cursorLeft + trajanje ) < ( nota.pozicija + nota.trajanje )):
    print("na sredini note sa CR")
    return(5)
  elif ( ( cursorLeft + trajanje ) == ( nota.pozicija + nota.trajanje )):
    print("na kraju note s CR")
    return(6)
  elif ( ( cursorLeft < nota.pozicija ) & ( ( cursorLeft + trajanje ) > (nota.pozicija + nota.trajanje ))):
    print("note unutar Cursora")
    return(7)
  else:
    return(False)

def get_git_revision_short_hash():
    import subprocess
    return(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8"))
