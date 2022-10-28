import os
from tkinter import Tk, Canvas
from PIL import Image, ImageTk
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 14:39:15 2022"""
"""
la base de la création d'un plateau de jeu (échecs, jeu de go, dames etc.)
certaine fonctions ne sont pas encore au point, ou à jour... c'est en cours'
"""
"""Ps: essayer de généraliser les fonctions"""


class Application:
    """squelette de la base pour la création de plateau de jeu avec
    des pieces, mouvante ou non"""

    def __init__(self):
        self.id_piece = {}
        self.id_grille = {}
        self.id_photo = []
        self.nombre_piece = -1

    def fenetre(self, **kwargs):
        """création de la fenetre Tkinter"""
        self.roof = Tk()
        self.roof.resizable(width=False, height=False)
        if kwargs.get("title", False) != False:
            self.roof.title(kwargs["title"])

        if kwargs.get("icon", False) != False:
            kwargs["icon"] = ImageTk.PhotoImage(
                master=self.roof, file=kwargs["icon"])
            self.roof.iconphoto(False, kwargs["icon"])

        if "image" in kwargs and os.path.isfile(kwargs["image"]):
            self.image_p = Image.open(str(kwargs["image"]))
            self.photo_p = ImageTk.PhotoImage(
                master=self.roof, file=kwargs["image"])
        else:
            raise FileNotFoundError("La photo n'existe pas")

        if kwargs.get("width", False) is False:
            kwargs["width"] = self.image_p.size[0]

        if kwargs.get("height", False) is False:
            kwargs["height"] = self.image_p.size[1]

        self.canvas = Canvas(
            self.roof, width=kwargs["width"], height=kwargs["height"])
        self.plateau = self.canvas.create_image(
            0, 0, anchor="nw", image=self.photo_p)

    def test_error(fonction):

        def test_error_fonction(self, *args, **kwargs):
            if (("x" not in kwargs or "y" not in kwargs) and
                    ("ligne" not in kwargs or "colonne" not in kwargs)):
                raise TypeError("valeurs manquantes")

            if len(self.id_grille) == 0:
                raise TypeError("grille non implémentée")

            if "ligne" not in kwargs or "colonne" not in kwargs:
                ligne, colonne = self.conv_mesure(x=kwargs["x"], y=kwargs["y"])
            else:
                kwargs["x"], kwargs["y"] = self.conv_mesure(
                    ligne=kwargs["ligne"], colonne=kwargs["colonne"])
                ligne, colonne = kwargs["ligne"], kwargs["colonne"]

            if kwargs.get("type_put", "square") == "square":
                kwargs["ligne"] = ligne
                kwargs["colonne"] = colonne

            if self.verify_sortie(ligne, colonne):
                raise IndexError("la piece sort de la grille")

            if "image" in kwargs and not os.path.isfile(kwargs["image"]):
                raise FileNotFoundError(
                    f"La photo '{kwargs['image']}' n'existe pas")
            
            
            retour = fonction(self, *args, **kwargs)
            return retour

        return test_error_fonction

    def test_set_piece_error(fonction):

        def test_set_piece_error_fonction(self, *args, **kwargs):
            if "check_position" not in kwargs:
                kwargs.update({"check_position": True})

            if kwargs.get("groupe_piece", False) is False:
                kwargs.update({"groupe_piece": "main"})

            if kwargs.get("type_verify_position", False) is False:
                kwargs.update({"type_verify_position": "main"})

            if kwargs.get("autres", False) is False:
                kwargs.update({"autres": {}})

            if kwargs["check_position"] and self.verify_position(
                    kwargs["ligne"], kwargs["colonne"],
                    groupe_piece=kwargs["type_verify_position"]):
                position = f"[{str(kwargs['ligne'])},{str(kwargs['colonne'])}]"
                raise ValueError(f"la position {position} est déjà occupée")

            retour = fonction(self, *args, **kwargs)
            return retour

        return test_set_piece_error_fonction

    def test_move_piece_error(fonction):

        def test_move_piece_error_fonction(self, *args, **kwargs):
            if kwargs.get("type_move", "square") == "square":
                kwargs["type_move"] = "square"
                kwargs["x"], kwargs["y"] = self.conv_mesure(
                    ligne=kwargs["ligne"], colonne=kwargs["colonne"])

            elif kwargs["type_move"] != "free":
                raise ValueError("put the right type of move")

            if "slide" not in kwargs:
                kwargs["slide"] = False

            if kwargs.get("tour", False) is False:
                kwargs["tour"] = 100

            if kwargs.get("vitesse", False) is False:
                kwargs["vitesse"] = 1
            retour = fonction(self, *args, **kwargs)
            return retour

        return test_move_piece_error_fonction

    def start(self):
        """affichage de la fenetre"""
        self.canvas.pack()
        self.roof.mainloop()

    def delete(self, piece):
        """supprier l'objet défini de la fenetre"""
        if piece == "all":
            self.id_piece.clear()
            self.numero = -1
        else:
            sauv = self.id_piece[piece]
            self.canvas.tag_lower(self.id_piece[piece]["tk_image"])
            self.id_piece.pop(piece)
            sauv.pop("id_photo")
            sauv.pop("tk_image")
            return sauv

    def set_grille(self, **kwargs):
        """instance de la grille du plateau"""
        if kwargs.get("bord", False) is False:
            kwargs["bord"] = 0

        if kwargs.get("x", False) is False:
            kwargs["x"] = int((self.image_p.width-2*kwargs["bord"])
                              / (kwargs["ligne"])-1)
        if kwargs.get("y", False) is False:
            kwargs["y"] = int((self.image_p.height-2*kwargs["bord"])
                              / (kwargs["colonne"])-1)
        self.id_grille.update({"x": kwargs["x"],
                               "y": kwargs["y"],
                               "ligne": kwargs["ligne"],
                               "colonne": kwargs["colonne"],
                               "bord": kwargs["bord"]})

    @test_set_piece_error
    @test_error
    def set_piece(self, **kwargs):
        """ajouter une ou plusieurs pieces sur le plateau.
        ex: ligne,colonne,image.exe,**options..."""
        self.nombre_piece += 1
        nom_piece = f"piece{self.nombre_piece}"
        self.id_piece.update({nom_piece: kwargs})
        photo = ImageTk.PhotoImage(master=self.roof, file=kwargs["image"])
        tk_image = self.canvas.create_image(
            kwargs["x"], kwargs["y"], image=photo, anchor="nw")
        self.id_piece[nom_piece].update(
            {"id_photo": photo, "tk_image": tk_image})
        return nom_piece

    @test_move_piece_error
    @test_error
    def move_piece(self, piece, **kwargs):
        """permet de faire bouger une piece"""
        if kwargs["slide"]:
            full_vect_x = kwargs["x"]-self.id_piece[piece]["x"]
            full_vect_y = kwargs["y"]-self.id_piece[piece]["y"]
            vect_x, vect_y = full_vect_x / \
                kwargs["tour"], full_vect_y/kwargs["tour"]
            self.__deplace_piece(piece, vect_x, vect_y,
                                 kwargs["tour"], kwargs["vitesse"])

        else:
            self.canvas.coords(
                self.id_piece[piece]["tk_image"], kwargs["x"], kwargs["y"])
        self.id_piece[piece].update(
            {"x": kwargs["x"],
             "y": kwargs["y"],
             "ligne": kwargs["ligne"],
             "colonne": kwargs["colonne"]})

    def __deplace_piece(self, piece, vect_x, vect_y, tour, vitesse):
        """fonction pour faire deplacer la piece de facon "slide"
        (la fonction ne peut pas etre relie a la fonction principale
         pour des problemes de boucles)"""
        tour -= 1
        self.canvas.move(self.id_piece[piece]["tk_image"], vect_x, vect_y)
        if tour > 0:
            self.roof.after(vitesse, lambda i=1: self.__deplace_piece(
                piece, vect_x, vect_y, tour, vitesse))

    def change_setting(self, piece, **kwargs):
        """permet de changer les options de chaque piece"""
        tk_piece = self.id_piece[piece]["tk_image"]
        if kwargs.get("is_photo", False) is True:
            del kwargs["is_photo"]
            tk_kwargs = kwargs.copy()
            for keys in kwargs:
                kwargs[keys] = ImageTk.PhotoImage(
                    master=self.roof, file=kwargs[keys])
                tk_kwargs[f"tk_photo_{keys}"] = kwargs[keys]
            self.canvas.itemconfigure(tk_piece, **kwargs)
            self.id_piece[piece].update(tk_kwargs)

        else:
            self.canvas.itemconfigure(tk_piece, **kwargs)
            self.id_piece[piece].update(kwargs)

    def conv_mesure(self, x=None, y=None, ligne=None, colonne=None):
        """convertir les position en pixel vers des lignes et colonnes
        résultant de la fonction self.put_grille"""
        if x is not None and y is not None:
            ligne = int((x-self.id_grille["bord"])/self.id_grille["x"])
            colonne = int((y-self.id_grille["bord"])/self.id_grille["y"])
            return ligne, colonne

        elif ligne is not None and colonne is not None:
            x = int(ligne*self.id_grille["x"]+self.id_grille["bord"])
            y = int(colonne*self.id_grille["y"]+self.id_grille["bord"])
            return x, y

        else:
            raise ValueError("veuillez mettre de bonne valeurs")

    def verify_sortie(self, ligne, colonne):
        if not ((ligne >= 0 and ligne < self.id_grille["ligne"]) and (
                colonne >= 0 and colonne < self.id_grille["colonne"])):
            return True
        else:
            return False

    def verify_position(self, ligne, colonne, groupe_piece="main"):
        """vérifier si une pièce ne prend pas la même position qu'une autre"""
        if groupe_piece == "all":
            for keys, valeurs in self.id_piece.items():
                if ligne == valeurs["ligne"] and colonne == valeurs["colonne"]:
                    return keys
        else:
            for keys, valeurs in self.id_piece.items():
                if (valeurs["groupe_piece"] == groupe_piece and
                        ligne == valeurs["ligne"] and
                        colonne == valeurs["colonne"]):
                    return keys
        return False
