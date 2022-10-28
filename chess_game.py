import board
from tkinter.messagebox import showinfo, askquestion

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 19:58:22 2022
"""
"""
un jeu d'echecs... c tout
"""

class Jeu:

    def __init__(self, *, instance=True):
        self.pattern = {}
        self.release = True
        self.piece_coords = {}
        self.roi_echec = False
        self.histo_partie = []
        self.piece_attaquante = []
        self.ligne_attaque = []
        self.piece_clouee = []
        self.piece_cloueuse = {}
        self.ligne_clouage = {}
        self.piece_suivi = True
        self.follow_piece = False
        self.couleur = "blanc"
        self.first_tour_motion = False
        self.first_tour_release = True
        self.piece_clicked = False
        self.piece_sortie = False
        self.has_moved = True
        self.occupe_case = {"blanc": [], "noir": []}
        self.list_piece = ["tour", "cavalier", "fou",
                           "dame", "roi", "fou", "cavalier", "tour"]
        self.fonction_piece()

        if instance:
            self.instance()
            self.put_pion()
            self.put_occupe_case()
            self.echecs.start()
            self.echecs.delete("all")

        else:
            self.echecs.delete("all")
            self.put_pion()
            self.put_occupe_case()

    def fonction_piece(self):
        self.pattern.update({"tour": {
            "coords": [[0, 1], [0, -1], [1, 0], [-1, 0]],
            "longueur": 8}})

        self.pattern.update({"cavalier": {
            "coords": [
                [1, 2], [-1, 2],
                [2, 1], [2, -1],
                [1, -2], [-1, -2],
                [-2, -1], [-2, 1]
            ],
            "longueur": 1}})

        self.pattern.update({"fou": {
            "coords": [[1, 1], [-1, 1], [-1, -1], [1, -1]],
            "longueur": 8}})

        self.pattern.update({"dame": {
            "coords":
                self.pattern["fou"]["coords"]
                + self.pattern["tour"]["coords"],
            "longueur": 8}})

        self.pattern.update({"roi": {
            "coords":
                self.pattern["fou"]["coords"]
                + self.pattern["tour"]["coords"],
            "longueur": 1}})

        self.pattern.update({"pion_blanc": {
            "coords": [[-1, -1], [1, -1]],
            "longueur": 1}})

        self.pattern.update({"pion_noir": {
            "coords": [[-1, 1], [1, 1]],
            "longueur": 1}})

    def instance(self):
        """faire une instance de la fenetre"""
        self.echecs = board.Application()
        self.echecs.fenetre(image="Images/Echecs/plateau_echecs.png")
        self.echecs.set_grille(x=68, y=68, ligne=8, colonne=8)
        self.echecs.canvas.bind("<Button-1>", self.event_select_piece)
        self.echecs.canvas.bind("<Motion>", self.event_motion_piece)
        self.echecs.canvas.bind("<ButtonRelease>", self.event_release_piece)

    def put_pion(self):
        """placer les pieces par défaut sur le plateau"""
        ligne = 0
        colonne = 0
        couleur = "noir"
        for i in range(2):
            for piece in self.list_piece:
                image = f"Images/Echecs/{piece}_{couleur}.png"
                if piece in ["tour", "roi"]:
                    roque = True
                else:
                    roque = False

                self.echecs.set_piece(ligne=ligne,
                                      colonne=colonne,
                                      image=image,
                                      autres={"roque": roque,
                                              "couleur": couleur,
                                              "type": piece})
                ligne += 1
            ligne = 0
            if couleur == "noir":
                colonne += 1
            elif couleur == "blanc":
                colonne -= 1
            for i in self.list_piece:
                image = f"Images/Echecs/pion_{couleur}.png"
                self.echecs.set_piece(ligne=ligne,
                                      colonne=colonne,
                                      image=image,
                                      autres={
                                          "roque": False,
                                          "couleur": couleur,
                                          "type": "pion"})
                ligne += 1
            ligne = 0
            colonne = 7
            couleur = "blanc"

    def event_select_piece(self, event, slide=True):
        """fonction gerant le clic gauche de la souris"""
        self.release = False
        ligne, colonne = self.echecs.conv_mesure(event.x, event.y)
        test_piece = self.echecs.verify_position(ligne, colonne, "abstract")
        touche_piece = self.echecs.verify_position(ligne, colonne)
        move_piece = self.echecs.verify_position(ligne, colonne, "position")
        prise_piece = self.echecs.verify_position(ligne, colonne, "prise")
        roque_piece = self.echecs.verify_position(ligne, colonne, "roque")

        if touche_piece:
            couleur = self.echecs.id_piece[touche_piece]["autres"]["couleur"]
            if not prise_piece and couleur == self.couleur:
                self.first_tour_motion = True

        if test_piece:
            self.piece_clicked = True
            self.piece_suivi = touche_piece
            return

        if roque_piece:
            lien_piece = self.echecs.id_piece[roque_piece]["autres"][
                "lien_piece"]
            lien_tour = self.echecs.id_piece[roque_piece]["autres"][
                "lien_tour"]
            couleur = self.echecs.id_piece[lien_piece]["autres"]["couleur"]
            if (self.echecs.id_piece[lien_piece]["ligne"] <
                    self.echecs.id_piece[lien_tour]["ligne"]):
                cote = -1
            if (self.echecs.id_piece[lien_piece]["ligne"] >
                    self.echecs.id_piece[lien_tour]["ligne"]):
                cote = 2
            ligne += cote
            touche_piece = False
            move_piece = lien_piece

        if prise_piece:
            piece_capture = self.echecs.id_piece[
                self.echecs.verify_position(ligne, colonne)]["autres"]["type"]
            if self.echecs.id_piece[prise_piece][
                    "autres"].get("prise_en_passant", False) is True:
                prise_en_passant = True
                lien_piece = self.echecs.id_piece[prise_piece]["autres"][
                    "lien_piece"]
                couleur = self.echecs.id_piece[lien_piece]["autres"]["couleur"]
            else:
                prise_en_passant = False

        self.piece_clicked = False
        piece = self.clear_abstract()

        if move_piece or prise_piece:
            if self.echecs.id_piece[piece]["autres"]["roque"]:
                self.echecs.id_piece[piece]["autres"].update({"roque": False})
            self.has_moved = True
            self.roi_echec = False
            self.piece_attaquante = []
            self.ligne_attaque = []
            self.piece_clouee = []
            self.piece_cloueuse = {}
            self.ligne_clouage = {}
            self.clear_abstract(type_abstract=["trajectoire", "echec"])
            self.echecs.set_piece(
                ligne=self.echecs.id_piece[piece]["ligne"],
                colonne=self.echecs.id_piece[piece]["colonne"],
                image="Images/Echecs/vert_trajectoire.png",
                check_position=False, groupe_piece="trajectoire",
                autres={"lien_piece": piece})
            self.echecs.set_piece(
                ligne=ligne,
                colonne=colonne,
                image="Images/Echecs/vert_trajectoire.png",
                check_position=False,
                groupe_piece="trajectoire",
                autres={"lien_piece": piece})

            promotion = False
            if self.echecs.id_piece[piece]["autres"]["type"] == "pion":
                if self.promotion_pion(piece, ligne, colonne):
                    promotion = piece

            self.echecs.canvas.tag_raise(
                self.echecs.id_piece[piece]["tk_image"])

        if (touche_piece and not prise_piece and couleur == self.couleur):
            self.piece_suivi = touche_piece
            self.echecs.set_piece(ligne=ligne,
                                  colonne=colonne,
                                  check_position=False,
                                  groupe_piece="abstract",
                                  image="Images/Echecs/fond_vert.png",
                                  autres={"lien_piece": touche_piece})
            self.echecs.canvas.tag_raise(
                self.echecs.id_piece[touche_piece]["tk_image"])

            if self.echecs.id_piece[touche_piece]["autres"]["type"] == "pion":
                self.put_position_point_pion(touche_piece, ligne, colonne)
            else:
                self.put_position_point(touche_piece, ligne, colonne)

        elif move_piece:
            roque = self.event_move_piece(piece, ligne, colonne, slide=slide)
            self.put_occupe_case()
            self.put_histo_partie(roque=roque, promotion=promotion)
            self.test_nulle()
            self.test_echec_et_mat()

        elif prise_piece:
            if prise_en_passant:
                if couleur == "blanc":
                    i = 1
                elif couleur == "noir":
                    i = -1
                delete_piece = self.echecs.verify_position(ligne, colonne+i)
                self.echecs.delete(delete_piece)
            else:
                self.echecs.delete(touche_piece)
            roque = self.event_move_piece(piece, ligne, colonne, slide=slide)
            self.put_occupe_case()
            self.put_histo_partie(type_prise=piece_capture,
                                  roque=roque,
                                  promotion=promotion)
            self.test_nulle()
            self.test_echec_et_mat()

    def event_motion_piece(self, event):
        """fonction gerant la molette de la souris"""
        if self.first_tour_motion:
            self.echecs.change_setting(self.piece_suivi, state="hidden")
            self.follow_piece = self.echecs.set_piece(
                x=event.x,
                y=event.y,
                image=self.echecs.id_piece[self.piece_suivi]["image"],
                check_position=False,
                groupe_piece="follow",
                type_put="free")
            self.echecs.change_setting(self.follow_piece, anchor="c")
            self.first_tour_motion = False

        if not self.release and self.follow_piece:
            if not self.piece_sortie:
                ligne, colonne = self.echecs.conv_mesure(event.x, event.y)
                touche_piece = self.echecs.verify_position(ligne, colonne)
                if touche_piece != self.piece_suivi:
                    self.piece_sortie = True

            try:
                self.echecs.move_piece(
                    self.follow_piece,
                    x=event.x,
                    y=event.y,
                    type_move="free",
                    slide=False)
            except IndexError:
                pass

    def event_release_piece(self, event):
        """fonction gerant le relachement du clic gauche de la souris"""
        self.release = True
        self.first_tour_motion = False

        if self.first_tour_release:
            self.first_tour_release = False
            ligne, colonne = self.echecs.conv_mesure(event.x, event.y)
            move_piece = self.echecs.verify_position(
                ligne, colonne, "position")
            prise_piece = self.echecs.verify_position(ligne, colonne, "prise")
            roque_piece = self.echecs.verify_position(ligne, colonne, "roque")

            if move_piece or prise_piece or roque_piece:
                self.clear_abstract(type_abstract=["trajectoire", "echec"])
                self.event_select_piece(event, slide=False)
                self.event_release_piece(event)
                self.piece_sortie = False

            elif self.piece_sortie:
                self.clear_abstract()
                self.same_piece = False
                self.piece_sortie = False

            else:
                if self.piece_clicked:
                    self.clear_abstract()

            self.first_tour_release = True

            if self.piece_suivi and self.follow_piece:
                self.echecs.delete(self.follow_piece)
                self.echecs.change_setting(self.piece_suivi, state="normal")
                self.follow_piece = False
                self.piece_suivi = False

    def event_move_piece(self, piece, ligne, colonne, slide=True):
        """fonction permettant de bouger une piece"""
        if self.couleur == "blanc":
            self.couleur = "noir"
        elif self.couleur == "noir":
            self.couleur = "blanc"
        else:
            raise AssertionError
        pose_tour = self.test_roque(piece, ligne, colonne)
        if pose_tour:
            self.clear_abstract(type_abstract="trajectoire")
            self.echecs.set_piece(
                ligne=self.echecs.id_piece[piece]["ligne"],
                colonne=self.echecs.id_piece[piece]["colonne"],
                image="Images/Echecs/vert_trajectoire.png",
                check_position=False,
                groupe_piece="trajectoire",
                autres={"lien_piece": piece})

            self.echecs.set_piece(
                ligne=self.echecs.id_piece[pose_tour["piece"]]["ligne"],
                colonne=self.echecs.id_piece[pose_tour["piece"]]["colonne"],
                image="Images/Echecs/vert_trajectoire.png",
                check_position=False, groupe_piece="trajectoire",
                autres={"lien_piece": pose_tour["piece"]})
            
            self.echecs.move_piece(pose_tour["piece"],
                                   ligne=pose_tour["ligne"],
                                   colonne=pose_tour["colonne"],
                                   groupe_piece="trajectoire")
        self.echecs.move_piece(piece,
                               ligne=ligne,
                               colonne=colonne,
                               slide=slide)
        
        return pose_tour

    def clear_abstract(self, type_abstract=["abstract", "position",
                                            "prise", "roque"]):
        """fonction pour enlever tout les elements d'un certain type,
        ici 'abstract' """
        test = True
        for keys, values in self.echecs.id_piece.copy().items():
            if values["groupe_piece"] in type_abstract:
                if test:
                    piece = self.echecs.id_piece[keys]["autres"]["lien_piece"]
                    test = False
                self.echecs.delete(keys)
        if not test:
            return piece

    def test_roque(self, piece, ligne, colonne):
        """rappel: ligne et colonne sont la position du roi
        à L'ARRIVÉE du roi au roque
        retourne l'id de la tour et son arivee apres le roque"""
        if (self.echecs.id_piece[piece]["autres"]["type"] == "roi" and
                self.echecs.id_piece[piece]["colonne"] == colonne):
            move_roi = self.echecs.id_piece[piece]["ligne"]-ligne
            if move_roi == 2:
                move_tour = 3
            elif move_roi == -2:
                move_tour = -2
            else:
                return False

            if self.echecs.id_piece[piece]["autres"]["couleur"] == "blanc":
                couleur = "blanc"
            elif self.echecs.id_piece[piece]["autres"]["couleur"] == "noir":
                couleur = "noir"
            else:
                raise AssertionError

            for keys, values in self.echecs.id_piece.items():
                if (values["autres"]["type"] == "tour" and
                        values["autres"]["couleur"] == couleur and
                        ((ligne < values["ligne"] and
                          ligne > values["ligne"]+move_tour) or
                         (ligne > values["ligne"] and
                          ligne < values["ligne"]+move_tour))):
                    return {"piece": keys,
                            "ligne": values["ligne"]+move_tour,
                            "colonne": values["colonne"],
                            "move_tour": move_tour}

        return False

    def put_position_point(self, piece, ligne, colonne):
        """mettre les points de deplacements"""
        copy_ligne = ligne
        copy_colonne = colonne
        type_piece = self.echecs.id_piece[piece]["autres"]["type"]
        couleur = self.echecs.id_piece[piece]["autres"]["couleur"]
        test_changement = False
        direction = 0
        test_longueur = 0
        self.test_position_point_roque(
            piece, type_piece, copy_ligne, copy_colonne)

        while (direction != len(self.pattern[type_piece]["coords"]) and
                self.pattern[type_piece]["longueur"] != test_longueur):
            test_longueur += 1
            ligne += self.pattern[type_piece]["coords"][direction][0]
            colonne += self.pattern[type_piece]["coords"][direction][1]
            if couleur == "blanc":
                couleur_adverse = "noir"
            elif couleur == "noir":
                couleur_adverse = "blanc"
            else:
                raise AssertionError

            try:
                if (type_piece != "roi" or
                    [ligne, colonne] not in
                        self.occupe_case[couleur_adverse]):

                    if ((not self.roi_echec or
                         type_piece == "roi" or
                         (len(self.piece_attaquante) == 1 and
                            (type_piece == "roi" or
                             [ligne, colonne] in self.ligne_attaque))) and
                            (piece not in self.piece_clouee or
                             [ligne, colonne] in self.ligne_clouage[piece])):
                        point = self.echecs.set_piece(
                            ligne=ligne,
                            colonne=colonne,
                            groupe_piece="position",
                            image="Images/Echecs/point_vert.png",
                            autres={"lien_piece": piece})
                        self.echecs.change_setting(
                            point,
                            activeimage="Images/Echecs/fond_vert_survol.png",
                            is_photo=True)
                    else:
                        if self.echecs.verify_position(ligne, colonne):
                            raise ValueError
                        elif self.echecs.verify_sortie(ligne, colonne):
                            raise IndexError

            except ValueError:
                self.deplacement_error(piece, ligne, colonne)
                test_changement = True

            except IndexError:
                test_changement = True

            if self.pattern[type_piece]["longueur"] == test_longueur:
                test_changement = True

            if test_changement:
                direction += 1
                ligne = copy_ligne
                colonne = copy_colonne
                test_longueur = 0
                test_changement = False

    def deplacement_error(self, piece, ligne, colonne):
        """verifier quelle piece se trouve sur la ligne et la colonne et si
        la couleur de la piece correspond,elle est marquée de prise_vert.png"""
        """ps: essayer un jour de descendre le tag du fond_vert_survol"""
        for keys, values in self.echecs.id_piece.items():
            if (values["groupe_piece"] == "main" and
                ligne == values["ligne"] and
                colonne == values["colonne"] and
                values["autres"]["couleur"] !=
                self.echecs.id_piece[piece]["autres"]["couleur"] and
                (piece == self.roi_echec or
                ((not self.roi_echec or
                 (len(self.piece_attaquante) == 1 and
                  keys in self.piece_attaquante)) and
                 (piece not in self.piece_clouee or
                  keys in self.piece_cloueuse[piece])))):

                prise = self.echecs.set_piece(
                    ligne=ligne,
                    colonne=colonne,
                    check_position=False,
                    groupe_piece="prise",
                    image="Images/Echecs/prise_vert.png",
                    autres={"lien_piece": piece})
                self.echecs.change_setting(
                    prise,
                    activeimage="Images/Echecs/fond_vert_survol.png",
                    is_photo=True)

                return True
        return False

    def test_position_point_roque(self, piece, type_piece, ligne, colonne):
        """fonction pour mettre les points destine au roque"""
        if type_piece == "roi" and not self.roi_echec:
            for keys, values in self.echecs.id_piece.copy().items():
                if (values["groupe_piece"] == "main" and
                    values["autres"]["type"] == "tour" and
                    values["autres"]["couleur"] == self.echecs.id_piece[piece]
                    ["autres"]["couleur"] and
                    self.echecs.id_piece[piece]["autres"]["roque"] and
                        values["autres"]["roque"]):
                    if self.echecs.id_piece[keys]["ligne"] < ligne:
                        cote = -2
                    elif self.echecs.id_piece[keys]["ligne"] > ligne:
                        cote = 1
                    else:
                        raise AssertionError
                    ligne = self.echecs.id_piece[piece]["ligne"]

                    if values["autres"]["couleur"] == "blanc":
                        couleur_adverse = "noir"
                    elif values["autres"]["couleur"] == "noir":
                        couleur_adverse = "blanc"
                    else:
                        raise AssertionError

                    while ligne != values["ligne"]-cote:
                        ligne += cote
                        if (self.echecs.verify_position(ligne, colonne) or
                                [ligne, colonne] in
                                self.occupe_case[couleur_adverse]):
                            break
                    else:
                        point = self.echecs.set_piece(
                            ligne=ligne,
                            colonne=colonne,
                            groupe_piece="position",
                            image="Images/Echecs/point_vert.png",
                            autres={"lien_piece": piece})
                        prise = self.echecs.set_piece(
                            ligne=values["ligne"],
                            colonne=values["colonne"],
                            groupe_piece="roque",
                            image="Images/Echecs/prise_vert.png",
                            check_position=False,
                            autres={"lien_piece": piece,
                                    "lien_tour": keys})
                        self.echecs.change_setting(
                            point,
                            activeimage="Images/Echecs/fond_vert_survol.png",
                            is_photo=True)
                        self.echecs.change_setting(
                            prise,
                            activeimage="Images/Echecs/fond_vert_survol.png",
                            is_photo=True)

    def put_occupe_case(self):
        """fonction permettant de mettre les cases occupés par les pieces
        de sorte que le roi ne puisse pas aller dessus"""
        if not self.has_moved:
            return
        else:
            self.has_moved = False
        self.occupe_case["blanc"] = []
        self.occupe_case["noir"] = []
        for keys, values in self.echecs.id_piece.copy().items():
            if self.echecs.id_piece[keys]["groupe_piece"] != "main":
                continue

            ligne = values["ligne"]
            colonne = values["colonne"]
            copy_ligne = ligne
            copy_colonne = colonne
            type_piece = self.echecs.id_piece[keys]["autres"]["type"]
            direction = 0
            test_longueur = 0
            couleur = self.echecs.id_piece[keys]["autres"]["couleur"]

            if type_piece == "pion":
                type_piece = f"pion_{couleur}"

            while (direction != len(self.pattern[type_piece]["coords"])
                    and self.pattern[type_piece]["longueur"] != test_longueur):
                test_longueur += 1
                ligne += self.pattern[type_piece]["coords"][direction][0]
                colonne += self.pattern[type_piece]["coords"][direction][1]
                touche_piece = self.echecs.verify_position(ligne, colonne)
                piece_sortie = self.echecs.verify_sortie(ligne, colonne)
                if not piece_sortie:
                    self.occupe_case[couleur].append([ligne, colonne])

                else:
                    direction += 1
                    ligne = copy_ligne
                    colonne = copy_colonne
                    test_longueur = 0

                if touche_piece:
                    longueur_attaque = test_longueur

                    while (direction != len(self.pattern[type_piece]["coords"])
                           and self.pattern[type_piece]["longueur"]
                           != test_longueur):
                        test_longueur += 1
                        ligne += (self.pattern[type_piece]
                                  ["coords"][direction][0])
                        colonne += (self.pattern[type_piece]
                                    ["coords"][direction][1])
                        piece_derriere = self.echecs.verify_position(
                            ligne, colonne)

                        if piece_derriere:
                            if (self.echecs.id_piece[piece_derriere]
                                ["autres"]["type"] == "roi" and
                                self.echecs.id_piece[touche_piece]
                                ["autres"]["type"] != "roi" and
                                self.echecs.id_piece[keys]
                                ["autres"]["couleur"] !=
                                self.echecs.id_piece[touche_piece]
                                ["autres"]["couleur"] ==
                                self.echecs.id_piece[piece_derriere]
                                    ["autres"]["couleur"]):
                                self.piece_clouee.append(touche_piece)
                                self.piece_cloueuse.update(
                                    {touche_piece: keys})
                                self.ligne_clouage.update({touche_piece: []})
                                ligne = copy_ligne
                                colonne = copy_colonne
                                for i in range(
                                        self.pattern[type_piece]["longueur"]):
                                    ligne += (self.pattern[type_piece]
                                              ["coords"][direction][0])
                                    colonne += (self.pattern[type_piece]
                                                ["coords"][direction][1])
                                    piece_clouee_derriere = (
                                        self.echecs.verify_position(
                                            ligne, colonne))

                                    if (piece_clouee_derriere and
                                            piece_clouee_derriere not in
                                            self.piece_clouee):
                                        break

                                    self.ligne_clouage[touche_piece].append(
                                        [ligne, colonne])

                            else:
                                break

                        elif (self.echecs.id_piece[touche_piece]
                                ["autres"]["type"] == "roi"):
                            self.occupe_case[couleur].append([ligne, colonne])

                    if (self.echecs.id_piece[touche_piece]
                            ["autres"]["type"] == "roi" and
                        self.echecs.id_piece[keys]["autres"]["couleur"] !=
                            self.echecs.id_piece[touche_piece]
                            ["autres"]["couleur"]):
                        self.roi_echec = touche_piece
                        self.piece_attaquante.append(keys)

                        ligne = copy_ligne
                        colonne = copy_colonne
                        for i in range(longueur_attaque-1):
                            ligne += (self.pattern[type_piece]["coords"]
                                      [direction][0])
                            colonne += (self.pattern[type_piece]["coords"]
                                        [direction][1])
                            self.ligne_attaque.append([ligne, colonne])
                        try:
                            self.echecs.set_piece(
                                ligne=self.echecs.id_piece[touche_piece]
                                ["ligne"],
                                colonne=self.echecs.id_piece[touche_piece]
                                ["colonne"],
                                groupe_piece="echec",
                                type_verify_position="echec",
                                image="Images/Echecs/tache_rouge.png",
                                autres={"lien_piece": touche_piece})
                            self.echecs.canvas.tag_raise(
                                self.echecs.id_piece[touche_piece]["tk_image"])

                        except ValueError or IndexError:
                            pass

                    direction += 1
                    ligne = copy_ligne
                    colonne = copy_colonne
                    test_longueur = 0

                elif self.pattern[type_piece]["longueur"] == test_longueur:
                    direction += 1
                    ligne = copy_ligne
                    colonne = copy_colonne
                    test_longueur = 0

    def put_histo_partie(self, **kwargs):
        """mettre la notation des coups de la partie"""
        if kwargs.get("roque"):
            if abs(kwargs["roque"]["move_tour"]) == 2:
                self.histo_partie.append("O-O")
            elif abs(kwargs["roque"]["move_tour"]) == 3:
                self.histo_partie.append("O-O-O")
            else:
                raise AssertionError
            return

        prise = ""
        type_prise = ""
        if kwargs.get("type_prise"):
            prise = "x"
            type_prise = kwargs['type_prise'][0].upper()

        echec = ""
        if self.roi_echec:
            if kwargs.get("echec_et_mat") is True:
                echec = "#"
            else:
                echec = "+"

        coords_trajectoire = []
        for keys, values in self.echecs.id_piece.copy().items():
            if values["groupe_piece"] == "trajectoire":
                lettre_ligne = chr(values["ligne"]+97)
                if self.echecs.verify_position(values["ligne"],
                                               values["colonne"]):
                    type_piece = (self.echecs.id_piece[values["autres"][
                        "lien_piece"]]["autres"]["type"][0].upper())
                    coords_trajectoire.append(
                        f"{lettre_ligne}{abs(8-values['colonne'])}")
                else:
                    coords_trajectoire.insert(
                        0,
                        f"{lettre_ligne}{abs(8-values['colonne'])}")

        promotion = ""
        if kwargs.get("promotion"):
            type_piece = "P"
            promotion = f"""={self.echecs.id_piece[kwargs["promotion"]][
                "autres"]["type"][0].upper()}"""

        self.histo_partie.append(
f"""{type_piece}{coords_trajectoire[0]}{prise}{type_prise}{
coords_trajectoire[1]}{promotion}{echec}""")
        print(self.histo_partie[-1])

    def put_position_point_pion(self, piece, ligne, colonne):
        """fonction spéciale pour mettre les points des pions"""
        if self.echecs.id_piece[piece]["autres"]["couleur"] == "blanc":
            sens = -1
            test_pion_position = 6
        elif self.echecs.id_piece[piece]["autres"]["couleur"] == "noir":
            sens = 1
            test_pion_position = 1
        else:
            raise ValueError("la couleur n'existe pas")

        """déplacement"""
        for cote in [1, 2]:
            if ((not self.roi_echec or
                 (len(self.piece_attaquante) == 1 and
                  [ligne, colonne+cote*sens] in self.ligne_attaque)) and
                (piece not in self.piece_clouee or
                 [ligne, colonne+cote*sens] in self.ligne_clouage[piece]) and
                    (cote != 2 or colonne == test_pion_position)):
                try:
                    point = self.echecs.set_piece(
                                    ligne=ligne,
                                    colonne=colonne+cote*sens,
                                    groupe_piece="position",
                                    image="Images/Echecs/point_vert.png",
                                    autres={"lien_piece": piece})
                    self.echecs.change_setting(
                        point,
                        activeimage="Images/Echecs/fond_vert_survol.png",
                        is_photo=True)
                except ValueError:
                    break

        for cote in [1, -1]:
            """prise"""
            touche_piece = self.echecs.verify_position(
                ligne+cote, colonne+sens)
            if (touche_piece and
                self.echecs.id_piece[touche_piece]["autres"]["couleur"]
                != self.couleur and
                (not self.roi_echec or (len(self.piece_attaquante) == 1 and
                 touche_piece in self.piece_attaquante)) and
                (piece not in self.piece_clouee or
                 touche_piece == self.piece_cloueuse[piece])):

                try:
                    point = self.echecs.set_piece(
                        ligne=ligne+cote,
                        colonne=colonne+sens,
                        check_position=False,
                        groupe_piece="prise",
                        image="Images/Echecs/prise_vert.png",
                        autres={"lien_piece": piece})
                    self.echecs.change_setting(
                        point,
                        activeimage="Images/Echecs/fond_vert_survol.png",
                        is_photo=True)
                except IndexError:
                    pass

            """prise en pasant"""
            touche_depart = self.echecs.verify_position(
                ligne+cote, colonne+sens*2, groupe_piece="trajectoire")
            touche_arrive = self.echecs.verify_position(
                ligne+cote, colonne, groupe_piece="trajectoire")

            if (touche_depart and
                touche_arrive and
                self.echecs.id_piece[self.echecs.id_piece[touche_arrive]
                                     ["autres"]["lien_piece"]]
                ["autres"]["type"] == "pion" and
                (not self.roi_echec or self.piece_attaquante == 1 or
                 self.echecs.id_piece[touche_arrive]["autres"]["lien_piece"]
                 in self.piece_attaquante or
                 [ligne, colonne+sens] in self.ligne_attaque) and
                (piece not in self.piece_clouee or
                 [ligne+cote, colonne+sens] in self.ligne_clouage[piece])):

                point = self.echecs.set_piece(
                    ligne=ligne+cote,
                    colonne=colonne+sens,
                    check_position=False,
                    groupe_piece="prise",
                    image="Images/Echecs/point_vert.png",
                    autres={"lien_piece": piece, "prise_en_passant": True})
                self.echecs.change_setting(
                    point,
                    activeimage="Images/Echecs/fond_vert_survol.png",
                    is_photo=True)

    def promotion_pion(self, piece, ligne, colonne):
        """permettre la promotion d'un pion"""
        if (self.echecs.id_piece[piece]["autres"]["couleur"] == "noir" and
                self.echecs.id_piece[piece]["colonne"] == 6):
            self.echecs.change_setting(
                piece, image="Images/Echecs/dame_noir.png", is_photo=True)
            self.echecs.id_piece[piece]["autres"].update({"type": "dame"})

        elif (self.echecs.id_piece[piece]["autres"]["couleur"] == "blanc" and
                self.echecs.id_piece[piece]["colonne"] == 1):
            self.echecs.change_setting(
                piece, image="Images/Echecs/dame_blanc.png", is_photo=True)
            self.echecs.id_piece[piece]["autres"].update({"type": "dame"})
        else:
            return False
        return True

    def test_nulle(self):
        """fonction pour tester si la partie est nulle"""
        if not self.roi_echec:

            """test_pat"""
            is_break = False
            for keys, values in self.echecs.id_piece.copy().items():
                if (values["groupe_piece"] == "main" and
                        values["autres"]["couleur"] == self.couleur):

                    if values["autres"]["type"] != "pion":
                        self.put_position_point(keys,
                                                values["ligne"],
                                                values["colonne"])
                    else:
                        self.put_position_point_pion(keys,
                                                     values["ligne"],
                                                     values["colonne"])

                    for keys1, values1 in self.echecs.id_piece.copy().items():
                        if values1["groupe_piece"] in ["position", "prise"]:
                            is_break = True
                            break
                if is_break:
                    break
            else:
                self.clear_abstract()
                self.couleur = None
                self.echecs.canvas.after(200, lambda i=1: self.text_finish(
                    text="""1/2 1/2 la partie est nulle
                         pat"""))
                return
            self.clear_abstract()

            """test_nombre_piece"""
            list_piece = []
            type_piece = {}
            coords_fou = []
            for keys, values in self.echecs.id_piece.copy().items():
                if values["groupe_piece"] == "main":
                    list_piece.append(keys)
                    type_piece.update(
                        {keys: self.echecs.id_piece[keys]["autres"]["type"]})

            if len(list_piece) == 4:
                for keys in list_piece:
                    if type_piece[keys] not in ["roi", "fou"]:
                        break
                    elif type_piece[keys] == "fou":
                        coords_fou.append([
                            self.echecs.id_piece[keys]["ligne"],
                            self.echecs.id_piece[keys]["colonne"]])

                else:
                    if ((coords_fou[0][0] + coords_fou[0][1]) % 2 ==
                            (coords_fou[1][0] + coords_fou[1][1]) % 2):
                        self.couleur = None
                        self.echecs.canvas.after(200, lambda i=1:
                                                 self.text_finish(
                                                     text="""
1/2 1/2 la partie est nulle
nombre de pieces insuffisantes"""))
                        return True

            elif len(list_piece) < 4:
                for keys in list_piece:
                    if type_piece[keys] not in ["roi", "fou", "cavalier"]:
                        break
                else:
                    self.couleur = None
                    self.echecs.canvas.after(200, lambda i=1: self.text_finish(
                        text="""
1/2 1/2 la partie est nulle
nombre de pieces insuffisantes"""))
                    return True

            """test_triple_repetition"""
            if (len(self.histo_partie) >= 10 and
                    len(set(self.histo_partie[-10:])) == 4):
                self.echecs.canvas.after(200, lambda i=1: self.text_finish(
                    question="askquestion",
                    text="""
une triple répétition a eu lieu
voulez vous déclarer la nulle?""",
                    reponse="""
1/2 1/2 la partie est nulle
triple répétition"""))
                return True

            """test_regle_des_50_coups"""
            if len(self.histo_partie) >= 100:
                for coup in self.histo_partie[-100:]:
                    if "P" in coup or "x" in coup:
                        break
                else:
                    self.couleur = None
                    self.echecs.canvas.after(200, lambda i=1: self.text_finish(
                        text="""
1/2 1/2 la partie est nulle
règle des 50 coups"""))
                    return True

    def test_echec_et_mat(self):
        """fonction pour tester si un echec et mat a lieu"""
        if self.roi_echec:
            ligne = self.echecs.id_piece[self.roi_echec]["ligne"]
            colonne = self.echecs.id_piece[self.roi_echec]["colonne"]
            copy_ligne = ligne
            copy_colonne = colonne
            type_piece = self.echecs.id_piece[self.roi_echec]["autres"]["type"]

            if self.echecs.id_piece[
                    self.roi_echec]["autres"]["couleur"] == "blanc":
                couleur_adverse = "noir"
                score = [0, 1]
                sens = -1
                test_pion_position = 6

            elif self.echecs.id_piece[
                    self.roi_echec]["autres"]["couleur"] == "noir":
                couleur_adverse = "blanc"
                score = [1, 0]
                sens = 1
                test_pion_position = 1

            else:
                raise AssertionError

            for coords in self.pattern[type_piece]["coords"]:
                ligne = copy_ligne+coords[0]
                colonne = copy_colonne+coords[1]

                if (not self.echecs.verify_sortie(ligne, colonne) and
                    (not self.echecs.verify_position(ligne, colonne) or
                    self.echecs.verify_position(ligne, colonne)
                     == couleur_adverse) and
                        [ligne, colonne] not in
                        self.occupe_case[couleur_adverse]):
                    return

            if len(self.piece_attaquante) == 1:

                for keys, values in self.echecs.id_piece.copy().items():
                    if (self.echecs.id_piece[keys]["groupe_piece"]
                        == "main" and
                            self.echecs.id_piece[keys]["autres"]["couleur"]
                            == self.couleur):
                        ligne = values["ligne"]
                        colonne = values["colonne"]
                        copy_ligne = ligne
                        copy_colonne = colonne
                        type_piece = self.echecs.id_piece[keys]["autres"][
                                                                    "type"]
                        direction = 0
                        test_longueur = 0

                        if type_piece == "pion":
                            type_piece = f"pion_{self.couleur}"

                        while (direction
                               != len(self.pattern[type_piece]["coords"])
                               and self.pattern[type_piece]["longueur"]
                               != test_longueur):
                            test_longueur += 1
                            ligne += self.pattern[type_piece]["coords"][
                                direction][0]
                            colonne += self.pattern[type_piece]["coords"][
                                direction][1]

                            if [ligne, colonne] in self.ligne_attaque:
                                if ("roi" != type_piece and
                                        "pion" not in type_piece):
                                    return

                            elif ([ligne, colonne] ==
                                  [self.echecs.id_piece[
                                    self.piece_attaquante[0]]["ligne"],
                                      self.echecs.id_piece[
                                         self.piece_attaquante[0]][
                                             "colonne"]] and
                                    (type_piece != "roi" or
                                     [ligne, colonne] not in
                                     self.occupe_case[couleur_adverse])):
                                return

                            elif (
                                self.echecs.verify_position(ligne, colonne) or
                                self.echecs.verify_sortie(ligne, colonne) or
                                    self.pattern[type_piece]["longueur"]
                                    == test_longueur):
                                direction += 1
                                ligne = copy_ligne
                                colonne = copy_colonne
                                test_longueur = 0

                    for keys, values in self.echecs.id_piece.copy().items():
                        if (self.echecs.id_piece[keys]["groupe_piece"]
                            == "main" and
                            self.echecs.id_piece[keys]["autres"]["couleur"]
                            == self.couleur
                                and self.echecs.id_piece[keys]["autres"]
                                                              ["type"]
                                == "pion"):

                            ligne = self.echecs.id_piece[keys]["ligne"]
                            colonne = self.echecs.id_piece[keys]["colonne"]
                            for cote in [1, 2]:
                                if ([ligne, colonne+cote*sens]
                                    in self.ligne_attaque and
                                        (cote != 2 or
                                         colonne == test_pion_position)):
                                    return

            """echec et mat valide"""
            self.histo_partie[-1] = self.histo_partie[-1].replace("+", "#")
            self.echecs.canvas.after(200, lambda i=1: self.text_finish(
                text=f"{score[0]}/{score[1]} victoire des {couleur_adverse}s"))
            return True

    def text_finish(self, *, text, question="showinfo", reponse=None):
        """fonction permettant d'afficher le texte de fin"""
        if question == "showinfo":
            showinfo("résultat", text)
        elif question == "askquestion":
            if askquestion("question", text) == "yes":
                showinfo("résultat", reponse)
            else:
                return
        else:
            raise ValueError("put the right type of show")

        restart = askquestion("restart", "voulez-vous recommencer?")
        if restart == "yes":
            self.__init__(instance=False)


if __name__ == "__main__":
    jeu_echecs = Jeu()
