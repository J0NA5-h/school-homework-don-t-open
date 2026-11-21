import pyxel
import math

# merci à la chaine inboundshovel pour l'idée de mettre tout en variable pour la lisibilitée.
LARGEUR_MONDE = 640
HAUTEUR_MONDE = 480
ACCEL_SOL = 0.005
ACCEL_AIR = 0.003
FROTT_APPUI = 0.995  # frottement au sol, touche enfoncée
FROTT_LACHE = 0.99  # frottement au sol, touche lâchée (C pour l'arret)
FROTT_AIR = 0.987
VMIN = 0.06  # vitesse du début pour ne pas accéléré car c bizard sinon
SEUIL_DEPART = 0.03  # en dessous, on donne le coup de départ ,doit être < VMIN
SEUIL_ARRET = 0.01  # en dessous, sans touche, on s'arrête net
GRAVITE = 0.0025
VITESSE_SAUT = -0.5  #c la vitesse verticale au moment du saut (négatif = vers le haut)
VCHUTE_MAX = 0.8
FPS = 600  # j'ai mis à 600 car sinon ça rend mal (c'est sacadé,ect)


# on utilise une classe car tout le monde sur internet en utilisait, et car le père de jonas lui a expliqué.
class App:
    def __init__(self):
        pyxel.init(320, 240, title="hello world", fps=FPS, display_scale=2)
        pyxel.load("mon_jeu.pyxres")
        # position de la caméra
        self.datacam = [0, 0]
        # stockage pour de la data. l'indice 0 indiquant quel
        # perso est choisi (ça sert pour la caméra et le mouvement pour l'instant)
        self.data = [0]
        # l'indice 0 indique quel perso c'est, le 1er indique son état, vivant ou mort.
        # les 2e et 3e indiquent son emplacement, le 4e et 5e indiquent sa vitesse, le 6e indique s il est sur le sol ou non.
        # le 7e indique sa taille, le 8e indique si il est présent.
        self.dataperso0 = [0, True, 160, 120, 0, 0, True, 32, True]
        self.dataperso1 = [1, True, 160, 120, 0, 0, True, 8, False]
        self.dataperso2 = [2, True, 0, 0, 0, 0, True, 8, False]
        self.dataperso3 = [3, True, 0, 0, 0, 0, True, 8, False]
        self.perso = (
            self.dataperso0,
            self.dataperso1,
            self.dataperso2,
            self.dataperso3,
        )
        self.persoutilise()
        pyxel.run(self.update, self.draw)

    def persoutilise(self):
        self.persou = 0

    def calculacceleration(self):
        pass

    def isgrounded(self):
        pass
        # servira à modifier l'indice 6 de dataperso

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        p = self.perso[self.persou]
        # btn revois True ou false, donc soit 1, soit 0. ce qui permet de conaitre la direction(merci YT)
        direction = pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)

        #  AXE X
        if p[6]: # si le perso est au sol
            accel = ACCEL_SOL
            if direction != 0:
                self.frott = FROTT_APPUI
            else:
                self.frott = FROTT_LACHE
        else:
            self.accel = ACCEL_AIR
            self.frott = FROTT_AIR

        p[4] *= self.frott
        if direction != 0:
            if p[6] and abs(p[4]) < SEUIL_DEPART:  #abs pour valeure absolue
                # si c'est au sol et si abs(sa vitesse) est inférieur au truc, on lui met un boost(l'accel rend mieu avec)
                p[4] = direction * VMIN
            else:
                p[4] += direction * self.accel
        elif p[6] and abs(p[4]) < SEUIL_ARRET: #même chose que l 78 sauf que direction = 0
            p[4] = 0 # on arrête le perso

        # AXE Y
        if p[6] and (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_SPACE)): # si au sol+ touche appuyée. j'ai mis espace au cas où.
            p[5] = VITESSE_SAUT # p5 est la vitesse verticale
            p[6] = False # le perso deviens en l'air.

        if not p[6]:
            p[5] = min(p[5] + GRAVITE, VCHUTE_MAX)
            #On ne prend que le résultat le plus petit entre p[5] + GRAVITE et VCHUTE_MAX pour éviter que la vitesse de chute soit infinie

        #position
        p[2] += p[4]
        p[3] += p[5]


        # sol temporaire (sera remplacé par la tilemap)
        sol = HAUTEUR_MONDE - p[7]
        if p[3] >= sol and p[5] >= 0:
            p[3] = sol
            p[5] = 0
            p[6] = True
        else:
            p[6] = False

        self.datacam[0] = p[2] - 160
        self.datacam[1] = p[3] - 120

    def draw(self):
        pyxel.cls(0)

        # Cette ligne ne déplace aucun objet et ne change aucune variable.
        # Elle règle un décalage que Pyxel retranche à toutes les commandes de dessin écrites après elle,
        # jusqu’au prochain pyxel.camera(...).
        # Avec self.datacam[0] = 50, un sprite à self.x = 70 serait dessiné à l’écran en 70 − 50 = 20, et un trait du quadrillage à gx = 64 en 14. Tout glisse de 50 pixels vers la gauche.
        pyxel.camera(self.datacam[0], self.datacam[1])

        for gx in range(0, LARGEUR_MONDE, 16):
            pyxel.line(gx, 0, gx, HAUTEUR_MONDE, 1)
        # mettre scale=var pour changer la taille
        pyxel.blt(self.perso[self.persou][2], self.perso[self.persou][3], 0, 32, 0, 32, 32)
        pyxel.camera()


App()
