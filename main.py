import pyxel
import math


LARGEUR_MONDE = 640
HAUTEUR_MONDE = 480


# on utilise une classe car tout le monde sur internet en utilisait, et car le père de jonas lui a expliqué.
class App:
    def __init__(self):
        pyxel.init(320, 240, title="hello world", fps=600, display_scale=2)
        pyxel.load("mon_jeu.pyxres")
        # position de la caméra
        self.datacam = [0, 0]
        # stockage pour de la data. l'indice 0 indiquant quel
        # perso est choisi (ça sert pour la caméra et le mouvement pour l'instant)
        self.data = [0]
        # l'indice 0 indique quel perso c'est, le 1er indique son état, vivant ou mort.
        # les 2e et 3e indiquent son emplacement, le 4e et 5e indiquent sa vitesse, le 6e indique s il est sur le sol ou non.
        # le 7e indique sa taille, le 8e indique si il est présent.
        self.dataperso0 = [0, True, 160, 120, 0, 0, False, 32, True]
        self.dataperso1 = [1, True, 160, 120, 0, 0, True, 8, False]
        self.dataperso2 = [2, True, 0, 0, 0, 0, True, 8, False]
        self.dataperso3 = [3, True, 0, 0, 0, 0, True, 8, False]
        self.perso = (self.dataperso0,self.dataperso1,self.dataperso2,self.dataperso3)
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
            print(self.perso[self.persou][4], self.perso[self.persou][5])
            pyxel.quit()
        if not self.perso[self.persou][6]:
            if pyxel.btn(pyxel.KEY_LEFT):
                self.perso[self.persou][4] += -0.005
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.perso[self.persou][4] += 0.005
            if pyxel.btn(pyxel.KEY_DOWN):
                self.perso[self.persou][5] += 0.005
            if pyxel.btn(pyxel.KEY_UP):
                self.perso[self.persou][5] += -0.005

        self.perso[self.persou][4] *= 0.985
        self.perso[self.persou][5] *= 0.985
        self.perso[self.persou][2] += self.perso[self.persou][4]
        self.perso[self.persou][3] += self.perso[self.persou][5]
        self.datacam[0] = self.perso[self.persou][2] - 160
        self.datacam[1] = self.perso[self.persou][3] - 120

    def draw(self):
        pyxel.cls(0)

        # Cette ligne ne déplace aucun objet et ne change aucune variable.
        # Elle règle un décalage que Pyxel retranche à toutes les commandes de dessin écrites après elle,
        # jusqu’au prochain pyxel.camera(...).
        # Avec self.datacam[0] = 50, un sprite à self.x = 70 serait dessiné à l’écran en 70 − 50 = 20, et un trait du quadrillage à gx = 64 en 14. Tout glisse de 50 pixels vers la gauche.
        pyxel.camera(self.datacam[0], self.datacam[1])

        for gx in range(0, LARGEUR_MONDE, 16):
            pyxel.line(gx, 0, gx, HAUTEUR_MONDE, 1)
        #mettre scale=var pour changer la taille
        pyxel.blt(self.perso[self.persou][2], self.perso[self.persou][3], 0, 32, 0, 32, 32)
        pyxel.camera()


App()
