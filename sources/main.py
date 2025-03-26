from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

from ui.interface_enigma import Ui_MainWindow
from ui.dialogue_config import Ui_Dialog
from enigma.classe_enigma import Enigma

import sys 

style_lampe = "QLabel{border-radius: 30px;border: 3px solid #32353A;color: #32353A;}"
style_lampe_active = "QLabel{border-radius: 30px;color:#8BB7B3;border: 5px solid #8BB7B3;font-weight: bold;}"
style_lettre = "QPushButton { border-radius: 30px; border: 3px solid #BFBFC1; color: #BFBFC1; background: qradialgradient(spread:pad, cx:0.65, cy:0.65, radius:0.60, stop:0 #393B3F, stop:0.65 #393B3F, stop:0.66 #2D3033, stop:1 #2D3033); }QPushButton:Hover{background: qradialgradient(spread:pad, cx:0.66, cy:0.77, radius:0.70, stop:0 #242629, stop:0.65 #242629, stop:0.66 #242629, stop:1 #242629);}\n"
style_lettre_active = "QPushButton{border-radius: 30px;border: 3px solid #BFBFC1;color: #BFBFC1;background: #242629}"

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.machine = Enigma(1,2,3,1)
        self.machine.Set_cablage_depart("")
        self.machine.Set_Configuration_depart("A","A","A")


    def reinitialiser_machine(self):
        # Reinitialisation des variables
        self.machine = Enigma(1,2,3,1)
        self.machine.Set_Configuration_depart("A","A","A")
        self.machine.Set_cablage_depart("")
        self.dico_cablage = {}

        self.lettre_init_g = "A"
        self.lettre_init_c = "A"
        self.lettre_init_d = "A"

        # Reinitialisation visuelle
        self.entry_non_crypte.clear()
        self.entry_crypte.clear()

        for cle, valeur in self.dico_associations_lettres.items():
            valeur[3].clear()
            valeur[3].setReadOnly(False)

        self.position_rg.setText("Z\nA\nB\n")
        self.position_rc.setText("Z\nA\nB\n")
        self.position_rd.setText("Z\nA\nB\n")

        self.s_bouton.play()

    def verifier_touche(self, lettre):
        if self.entry_non_crypte.toPlainText() == "":
            self.machine.Set_Configuration_depart(self.lettre_init_g, self.lettre_init_c, self.lettre_init_d)
        self.activer_touche(lettre)

    def activer_touche(self, lettre):
        lettre_crypte = self.machine.Decodagelettre(lettre)

        self.remplir_champ(self.entry_non_crypte, lettre)
        self.remplir_champ(self.entry_crypte, lettre_crypte)
        
        lampe = self.dico_associations_lettres[lettre_crypte][1]
        touche = self.dico_associations_lettres[lettre][0] # lettre = l'objet bouton qui represente les touches

        lampe.setStyleSheet(style_lampe_active)
        touche.setStyleSheet(style_lettre_active)
        
        self.s_clavier.play()
        QTimer.singleShot(230, lambda:(lampe.setStyleSheet(style_lampe), touche.setStyleSheet(style_lettre)))

    def remplir_champ(self, champ, lettre):
        texte = champ.toPlainText()
        if len(texte.replace(" ", "")) % 5 == 0 and len(texte) > 0:
            champ.insertPlainText(" ")
        champ.insertPlainText(lettre)
        
    def dialogue_config(self):
        self.s_bouton.play()
        
        dialogue = QtWidgets.QDialog()
        dialogue.ui = Ui_Dialog()
        dialogue.ui.setupUi(dialogue)

        #Inserer les valeurs au demarrage
        if self.machine.GetNumReflecteur() == 1:
            dialogue.ui.combo_box_reflecteur.setCurrentText("UKW-B")
        else:
            dialogue.ui.combo_box_reflecteur.setCurrentText("UKW-C")

        dialogue.ui.combo_box_rg.setCurrentText(self.convertir_arabe_en_romain(self.machine.GetNumRotorGauche()))
        dialogue.ui.combo_box_rc.setCurrentText(self.convertir_arabe_en_romain(self.machine.GetNumRotorCentre()))
        dialogue.ui.combo_box_rd.setCurrentText(self.convertir_arabe_en_romain(self.machine.GetNumRotorDroite()))

        #Mettre a jour les valeurs a la fermeture
        if dialogue.exec_() == QtWidgets.QDialog.Accepted:
            if dialogue.ui.combo_box_reflecteur.currentText() == "UKW-B":
                refl = 1
            else:
                refl = 2
                
            rotor_g = self.convertir_romain_en_arabe(dialogue.ui.combo_box_rg.currentText())
            rotor_c = self.convertir_romain_en_arabe(dialogue.ui.combo_box_rc.currentText())
            rotor_d = self.convertir_romain_en_arabe(dialogue.ui.combo_box_rd.currentText())
            
            if rotor_g == rotor_c or rotor_g == rotor_d or rotor_c == rotor_d:
                print("ERREUR - Il ne peut pas y avoir deux mêmes rotors dans des emplacements différents.")
            else:
                self.machine.Set_Configuration_depart("A","A","A")

                self.lettre_init_g = "A"
                self.lettre_init_c = "A"
                self.lettre_init_d = "A"
                
                self.position_rg.setText("Z\nA\nB\n")
                self.position_rc.setText("Z\nA\nB\n")
                self.position_rd.setText("Z\nA\nB\n")
                self.machine = Enigma(rotor_g, rotor_c, rotor_d, refl)
        self.s_bouton.play()

    def convertir_romain_en_arabe(self, c_romain):
        """
        Fonction qui convertit les chiffres romains (c_romain) en chiffres arabes
        """
        if c_romain == "I":
            c_arabe = 1
        elif c_romain == "II":
            c_arabe = 2
        elif c_romain == "III":
            c_arabe = 3
        elif c_romain == "IV":
            c_arabe = 4
        elif c_romain == "V":
            c_arabe = 5
        return c_arabe

    def convertir_arabe_en_romain(self, c_arabe):
        """
        Fonction qui convertit les chiffres arabes (c_arabes) en chiffres romains
        """
        if c_arabe == 1:
            c_romain = "I"
        elif c_arabe == 2:
            c_romain = "II"
        elif c_arabe == 3:
            c_romain = "III"
        elif c_arabe == 4:
            c_romain = "IV"
        elif c_arabe == 5:
            c_romain = "V"
        return c_romain

    def afficher_trois_lettres(self, i):
        """
        Fonction qui renvoie une chaîne de caractères avec trois lettres qui se suivent
        dans l'alphabet, autour de la lettre à l'index "i"
        """
        lettre_precedente = self.alphabet[(i - 1) % 26]
        lettre_actuelle = self.alphabet[i % 26]
        lettre_suivante = self.alphabet[(i + 1) % 26]
        return f"{lettre_precedente}\n{lettre_actuelle}\n{lettre_suivante}"
    
    def changer_lettre_initiale(self, label, direction, emplacement):
        lettre_actuelle = label.text().split("\n")[1]
        lettre_actuelle_indice = self.alphabet.index(lettre_actuelle)

        if direction == "precedent":
            nouvelle_lettre_indice = (lettre_actuelle_indice - 1) % 26
        else:
            nouvelle_lettre_indice = (lettre_actuelle_indice + 1) % 26

        nouvelle_lettre = self.alphabet[nouvelle_lettre_indice]

        label.setText(self.afficher_trois_lettres(nouvelle_lettre_indice))

        if emplacement == "gauche":
            self.lettre_init_g = nouvelle_lettre
        elif emplacement == "centre":
            self.lettre_init_c = nouvelle_lettre
        else:
            self.lettre_init_d = nouvelle_lettre

        self.s_rotor.play()
        
    def gerer_changement_cablage(self, lettre_emplacement):
        entry = self.dico_associations_lettres[lettre_emplacement][3]
        lettre_entree = entry.text().upper()

        #Ignore si lettre_entree est vide
        if not lettre_entree:
            return

        #Empeche les lettres de se lier a elles meme
        if lettre_entree not in self.alphabet and lettre_entree != "-":
            entry.blockSignals(True)
            entry.setText("")
            entry.blockSignals(False)
            return
        
        if lettre_entree == lettre_emplacement:
            entry.blockSignals(True)
            entry.setText("")
            entry.blockSignals(False)
            return

        if lettre_entree in self.dico_cablage or lettre_entree in self.dico_cablage.values():
            entry.blockSignals(True)
            entry.setText("")
            entry.blockSignals(False)
            return

        #Met en majuscules
        if entry.text().islower():
            entry.blockSignals(True)
            entry.setText(lettre_entree)
            entry.blockSignals(False)
            entry.setReadOnly(True)

        #Met a jour le dictionnaire
        if lettre_entree != "-":
            self.dico_cablage[lettre_emplacement] = lettre_entree
        else:
            if lettre_emplacement in self.dico_cablage:
                ancienne_lettre = self.dico_cablage.pop(lettre_emplacement)
            elif lettre_emplacement in self.dico_cablage.values():
                ancienne_lettre = [cle for cle, valeur in self.dico_cablage.items() if valeur == lettre_emplacement][0]  
                self.dico_cablage.pop(ancienne_lettre)
            
            if ancienne_lettre in self.dico_associations_lettres:
                entry_enr = self.dico_associations_lettres[ancienne_lettre][3]
                entry_enr.blockSignals(True)
                entry_enr.setText("")
                entry_enr.blockSignals(False)
                entry_enr.setReadOnly(False)

            entry.blockSignals(True)
            entry.setText("")
            entry.blockSignals(False)

        #Verifie si la lettre existe dans le dico
        if lettre_entree not in self.dico_associations_lettres and lettre_entree != "-":
            return

        if lettre_entree != "-":
            entry2 = self.dico_associations_lettres[lettre_entree][3]

            entry2.blockSignals(True)
            entry2.setText(lettre_emplacement)
            entry2.blockSignals(False)
            entry2.setReadOnly(True)

            entry2.textChanged.disconnect()
            entry2.textChanged.connect(lambda: self.gerer_changement_cablage(lettre_entree))
        else:
            entry2 = entry_enr
            entry2.blockSignals(True)
            entry2.setText("")
            entry2.blockSignals(False)
            entry2.setReadOnly(False)

        entry.clearFocus()
        self.s_bouton.play()
        self.machine.Set_cablage_depart(self.generer_chaine_cablage(self.dico_cablage))

    def generer_chaine_cablage(self, dico):
        """
        Fonction qui renvoie une chaine de caracteres qui represente le cablage a partir
        d'un dictionnaire.
        """
        ch = ""
        for cle, valeur in dico.items():
            ch += cle + valeur
        return ch
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
