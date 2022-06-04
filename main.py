import random
import time
from statistics import median, mean

import pygame, sys, copy, math



def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL else False
    return False


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    GOL = '#'

    @classmethod
    def initializeaza(cls, display, NR_COLOANE=8, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.dim_img = 50
        cls.negru_img = pygame.image.load('negru.png')
        cls.negru_img = pygame.transform.scale(cls.negru_img, (
        cls.dim_img, math.floor(cls.dim_img * cls.negru_img.get_height() / cls.negru_img.get_width())))
        cls.alb_img = pygame.image.load('alb.png')
        cls.alb_img = pygame.transform.scale(cls.alb_img, (
        cls.dim_img, math.floor(cls.dim_img * cls.alb_img.get_height() / cls.alb_img.get_width())))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        cls.colturi = []
        for linie in range(NR_COLOANE):
            cls.celuleGrid.append([])
            cls.colturi.append([])
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * dim_celula + dim_celula / 2, linie * dim_celula + dim_celula / 2, dim_celula, dim_celula)
                colt = pygame.Rect(coloana * dim_celula, linie * dim_celula, dim_celula, dim_celula)
                print(colt)
                cls.colturi[linie].append(colt)
                cls.celuleGrid[linie].append(patr)


    def deseneaza_grid(self, marcaj=None):
        pygame.draw.rect(self.display, (255, 255, 255), (0, 0, 800, 800))
        for linie in range(Joc.NR_COLOANE):
            for coloana in range(Joc.NR_COLOANE):
                negru = (0, 0, 0)
                if marcaj == (linie, coloana):
                    # daca am o patratica selectata, o desenez cu rosu
                    culoare = (255, 0, 0)
                else:
                    # altfel o desenez cu alb
                    culoare = (255,255,255)

                if coloana != Joc.NR_COLOANE - 1 and linie != Joc.NR_COLOANE - 1:
                    pygame.draw.rect(self.display, negru,
                                     self.celuleGrid[linie][coloana], 1)

                if marcaj == (linie, coloana):
                    pygame.draw.rect(self.display, culoare,
                                        self.colturi[linie][coloana], 3, 50)

                if self.matr[linie][coloana] == 'n':
                    self.display.blit(self.negru_img, (coloana * self.dim_celula + self.dim_celula / 2 - self.dim_img / 2, linie * self.dim_celula + self.dim_celula / 2 - self.dim_img / 2))
                elif self.matr[linie][coloana] == 'a':
                    self.display.blit(self.alb_img, (coloana * self.dim_celula + self.dim_celula / 2 - self.dim_img / 2, linie * self.dim_celula + self.dim_celula / 2 - self.dim_img / 2))
        pygame.display.flip() # !!! obligatoriu pentru a actualiza interfata (desenul)
        pygame.display.update()

    def __init__(self, tabla=None):
        if tabla:
            self.matr = tabla
        else:
            self.matr = []
            for i in range(self.__class__.NR_COLOANE):
                self.matr.append([self.__class__.GOL] * self.__class__.NR_COLOANE)

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        if self.matr[0][7] == 'n':
            return 'n'
        elif self.matr[7][0] == 'a':
            return 'a'
        else:
            return False


    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        """
            Clasa care stabileste mutarile valide pentru calculator.
        """
        l_mutari = []
        for i in range(self.__class__.NR_COLOANE):
            for j in range(self.__class__.NR_COLOANE):
                if self.matr[i][j] == jucator:
                    l_mutari_valabile = []

                    for lin in range(i + 1, 8):                         # vad pana unde pot sa o mut in jos
                        if self.matr[lin][j] == '#':
                            l_mutari_valabile.append([lin, j])
                        else:                                           # daca am dat de alta piesa, ma opresc(nu pot sari peste ea)
                            break

                    for lin in range(i - 1, -1, -1):                    # vad pana unde pot sa o mut in sus
                        if self.matr[lin][j] == '#':
                            l_mutari_valabile.append([lin, j])
                        else:
                            break

                    for col in range(j + 1, 8):                         # vad pana unde pot sa o mut spre dreapta
                        if self.matr[i][col] == '#':
                            l_mutari_valabile.append([i, col])
                        else:
                            break

                    for col in range(j - 1, -1, -1):                    # vad pana unde pot sa o mut spre stanga
                        if self.matr[i][col] == '#':
                            l_mutari_valabile.append([i, col])
                        else:
                            break

                    lin = i - 1
                    col = j - 1
                    while lin >= 0 and col >= 0:                    # vad pana unde pot sa o mut pe diagonala stanga sus
                        if self.matr[lin][col] == '#':
                            l_mutari_valabile.append([lin, col])
                        else:
                            break
                        lin -= 1
                        col -= 1

                    lin = i - 1
                    col = j + 1
                    while lin >= 0 and col <= 7:                    # vad pana unde pot sa o mut pe diagonala dreapta sus
                        if self.matr[lin][col] == '#':
                            l_mutari_valabile.append([lin, col])
                        else:
                            break
                        lin -= 1
                        col += 1

                    lin = i + 1
                    col = j - 1
                    while lin <= 7 and col >= 0:                    # vad pana unde pot sa o mut pe diagonala stanga jos
                        if self.matr[lin][col] == '#':
                            l_mutari_valabile.append([lin, col])
                        else:
                            break
                        lin += 1
                        col -= 1

                    lin = i + 1
                    col = j + 1
                    while lin <= 7 and col <= 7:                    # vad pana unde pot sa o mut pe diagonala dreapta jos
                        if self.matr[lin][col] == '#':
                            l_mutari_valabile.append([lin, col])
                        else:
                            break
                        lin += 1
                        col += 1

                    k = 0
                    L = len(l_mutari_valabile)
                    while k < L:                                # pentru fiecare spatiu in care pot muta piesa, verific daca
                        lin = l_mutari_valabile[k][0]           # gasesc macar 3 piese ale adversarului opus, pe aceeasi
                        col = l_mutari_valabile[k][1]           # linie, coloana sau diagonala cu spatiul curent
                        tot_piese_adversar = 0

                        for x in range(lin + 1, 8):             # ma uit pe aceeasi coloana in jos
                            if self.matr[x][col] == jucator:    # am deja o piesa aliat care ma protejeaza, deci nu mai caut
                                break                           # in continuare
                            elif self.matr[x][col] != '#':
                                tot_piese_adversar += 1         # daca gasesc o piesa inamica, incrementez si ies
                                break

                        for x in range(lin - 1, -1, -1):        # ma uit pe aceeasi coloana in sus
                            if self.matr[x][col] == jucator:
                                break
                            elif self.matr[x][col] != '#':
                                tot_piese_adversar += 1
                                break

                        for y in range(col + 1, 8):             # ma uit pe linie spre dreapta
                            if self.matr[lin][y] == jucator:
                                break
                            elif self.matr[lin][y] != '#':
                                tot_piese_adversar += 1
                                break

                        if tot_piese_adversar == 3:
                            k -= 1
                            L -= 1
                                                                # de acum dupa fiecare for pot sa am conditia
                            l_mutari_valabile.remove([lin, col])  # si verific mereu ca sa nu mai parcurg degeaba

                        else:
                            for y in range(col - 1, -1, -1):     # ma uit pe linie spre stanga
                                if self.matr[lin][y] == jucator:
                                    break
                                elif self.matr[lin][y] != '#':
                                    tot_piese_adversar += 1
                                    break
                                                                 # print("Linie spre stanga" + str(tot_piese_adversar))
                            if tot_piese_adversar == 3:
                                k -= 1
                                L -= 1
                                l_mutari_valabile.remove([lin, col])

                            else:
                                x = lin - 1
                                y = col - 1
                                while x >= 0 and y >= 0:        # ma uit pe diagonala stanga sus
                                    if self.matr[x][y] == jucator:
                                        break
                                    elif self.matr[x][y] != '#':
                                        tot_piese_adversar += 1
                                        break
                                    x -= 1
                                    y -= 1

                                if tot_piese_adversar == 3:
                                    k -= 1
                                    L -= 1
                                    l_mutari_valabile.remove([lin, col])

                                else:
                                    x = lin - 1
                                    y = col + 1
                                    while x >= 0 and y <= 7:            # ma uit pe diagonala dreapta sus
                                        if self.matr[x][y] == jucator:
                                            break
                                        elif self.matr[x][y] != '#':
                                            tot_piese_adversar += 1
                                            break
                                        x -= 1
                                        y += 1

                                    if tot_piese_adversar == 3:
                                        # print(lin, col)
                                        k -= 1
                                        L -= 1
                                        l_mutari_valabile.remove([lin, col])
                                                                        # print("Termin dupa diagonala dreapta sus")
                                    else:
                                        x = lin + 1
                                        y = col - 1
                                        while x <= 7 and y >= 0:        # ma uit pe diagonala stanga jos
                                            if self.matr[x][y] == jucator:
                                                break
                                            elif self.matr[x][y] != '#':
                                                tot_piese_adversar += 1
                                                break
                                            x += 1
                                            y -= 1

                                        if tot_piese_adversar == 3:
                                            k -= 1
                                            L -= 1
                                            l_mutari_valabile.remove([lin, col])

                                        else:
                                            x = lin + 1
                                            y = col + 1
                                            while x <= 7 and y <= 7:                    # ma uit pe diagonala dreapta jos
                                                if self.matr[x][y] == jucator:
                                                    break
                                                elif self.matr[x][y] != '#':
                                                    tot_piese_adversar += 1
                                                    break
                                                x += 1
                                                y += 1

                                            if tot_piese_adversar == 3:
                                                k -= 1
                                                L -= 1
                                                l_mutari_valabile.remove([lin, col])
                                                # print("Termin dupa diagonala stanga jos")
                        k += 1


                    if jucator == 'n':                      # nu pot muta in propriul port
                        if [7, 0] in l_mutari_valabile:
                            l_mutari_valabile.remove([7, 0])
                    else:
                        if [0, 7] in l_mutari_valabile:
                            l_mutari_valabile.remove([0, 7])


                    if jucator == 'n':
                        jucatorOpus = 'a'
                    else:
                        jucatorOpus = 'n'
                    pieseEliminate = eliminaPiese(self.matr, jucatorOpus)

                    L = len(pieseEliminate)
                    if L > 0:
                        for piesaEliminata in pieseEliminate:
                            self.matr[piesaEliminata[0]][piesaEliminata[1]] = Joc.GOL
                    for pereche in l_mutari_valabile:
                        copie_matr = copy.deepcopy(self.matr)
                        copie_matr[i][j] = Joc.GOL
                        copie_matr[pereche[0]][pereche[1]] = jucator
                        l_mutari.append(Joc(copie_matr))

        return l_mutari

    def estimeaza_scor(self, adancime):
        return random.randint(1, 100)

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_COLOANE):  # itereaza prin linii
            sir += str(i) + " |" + " ".join([str(x) for x in self.matr[i]]) + "\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]
        return l_stari_mutari

    def posibilitateMutare(self, linie, coloana, matr, display):
        """
            Clasa folosita pentru a verifica daca mutarea jucatorului este valida.
        """
        l_mutari_valabile = []

        for lin in range(linie+1, 8):                               #vad pana unde pot sa o mut in jos
                if matr[lin][coloana] == '#':
                    l_mutari_valabile.append([lin, coloana])
                else:                                               #daca am dat de alta piesa, ma opresc(nu pot sari peste ea)
                    break

        for lin in range(linie-1, -1, -1):                          #vad pana unde pot sa o mut in sus
            if matr[lin][coloana] == '#':
                l_mutari_valabile.append([lin, coloana])
            else:
                break

        for col in range(coloana+1, 8):                            #vad pana unde pot sa o mut spre dreapta
            if matr[linie][col] == '#':
                l_mutari_valabile.append([linie, col])
            else:
                break

        for col in range(coloana-1, -1, -1):                      #vad pana unde pot sa o mut spre stanga
            if matr[linie][col] == '#':
                l_mutari_valabile.append([linie, col])
            else:
                break

        lin = linie - 1
        col = coloana - 1
        while lin >= 0 and col >= 0:                            #vad pana unde pot sa o mut pe diagonala stanga sus
            if matr[lin][col] == '#':
                l_mutari_valabile.append([lin, col])
            else:
                break
            lin -= 1
            col -= 1

        lin = linie - 1
        col = coloana + 1
        while lin >= 0 and col <= 7:                             #vad pana unde pot sa o mut pe diagonala dreapta sus
            if matr[lin][col] == '#':
                l_mutari_valabile.append([lin, col])
            else:
                break
            lin -= 1
            col += 1

        lin = linie + 1
        col = coloana - 1
        while lin <= 7 and col >= 0:                        #vad pana unde pot sa o mut pe diagonala stanga jos
            if matr[lin][col] == '#':
                l_mutari_valabile.append([lin, col])
            else:
                break
            lin += 1
            col -= 1

        lin = linie + 1
        col = coloana + 1
        while lin <= 7 and col <= 7:                       #vad pana unde pot sa o mut pe diagonala dreapta jos
            if matr[lin][col] == '#':
                l_mutari_valabile.append([lin, col])
            else:
                break
            lin += 1
            col += 1

        if Joc.JMIN == 'n':                                 #nu pot muta in propriul port
            if [7, 0] in l_mutari_valabile:
                l_mutari_valabile.remove([7, 0])
        else:
            if [0, 7] in l_mutari_valabile:
                l_mutari_valabile.remove([0, 7])

        k = 0
        L = len(l_mutari_valabile)
        while k < L:                                            #pentru fiecare spatiu in care pot muta piesa, verific daca
            lin = l_mutari_valabile[k][0]                       #gasesc macar 3 piese ale adversarului opus, pe aceeasi
            col = l_mutari_valabile[k][1]                       #linie, coloana sau diagonala cu spatiul curent
            tot_piese_adversar = 0

            for i in range(lin + 1, 8):                             # ma uit pe aceeasi coloana in jos
                if matr[i][col] == Joc.JMIN:                        # am deja o piesa aliat care ma protejeaza, deci nu mai caut
                    break                                           # in continuare
                elif matr[i][col] == Joc.JMAX:
                    tot_piese_adversar += 1                         # daca gasesc o piesa inamica, incrementez si ies
                    break

            for i in range(lin - 1, -1, -1):                        # ma uit pe aceeasi coloana in sus
                if matr[i][col] == Joc.JMIN:
                    break
                elif matr[i][col] == Joc.JMAX:
                    tot_piese_adversar += 1
                    break

            for j in range(col + 1, 8):                             # ma uit pe linie spre dreapta
                if matr[lin][j] == Joc.JMIN:
                    break
                elif matr[lin][j] == Joc.JMAX:
                    tot_piese_adversar += 1
                    break

            if tot_piese_adversar == 3:
                k -= 1
                L -= 1
                                                                    # de acum dupa fiecare for pot sa am conditia
                l_mutari_valabile.remove([lin, col])                # si verific mereu ca sa nu mai parcurg degeaba

            else:
                for j in range(col - 1, -1, -1):                    # ma uit pe linie spre stanga
                    if matr[lin][j] == Joc.JMIN:
                        break
                    elif matr[lin][j] == Joc.JMAX:
                        tot_piese_adversar += 1
                        break

                if tot_piese_adversar == 3:
                    k -= 1
                    L -= 1
                    l_mutari_valabile.remove([lin, col])

                else:
                    i = lin - 1
                    j = col - 1
                    while i >= 0 and j >= 0:                        # ma uit pe diagonala stanga sus
                        if matr[i][j] == Joc.JMIN:
                            break
                        elif matr[i][j] == Joc.JMAX:
                            tot_piese_adversar += 1
                            break
                        i -= 1
                        j -= 1

                    if tot_piese_adversar == 3:
                        k -= 1
                        L -= 1
                        l_mutari_valabile.remove([lin, col])

                    else:
                        i = lin - 1
                        j = col + 1
                        while i >= 0 and j <= 7:                    # ma uit pe diagonala dreapta sus
                            if matr[i][j] == Joc.JMIN:
                                break
                            elif matr[i][j] == Joc.JMAX:
                                tot_piese_adversar += 1
                                break
                            i -= 1
                            j += 1

                        if tot_piese_adversar == 3:
                            #print(lin, col)
                            k -= 1
                            L -= 1
                            l_mutari_valabile.remove([lin, col])

                        else:
                            i = lin + 1
                            j = col - 1
                            while i <= 7 and j >= 0:                # ma uit pe diagonala stanga jos
                                if matr[i][j] == Joc.JMIN:
                                    break
                                elif matr[i][j] == Joc.JMAX:
                                    tot_piese_adversar += 1
                                    break
                                i += 1
                                j -= 1

                            if tot_piese_adversar == 3:
                                k -= 1
                                L -= 1
                                l_mutari_valabile.remove([lin, col])

                            else:
                                i = lin + 1
                                j = col + 1
                                while i <= 7 and j <= 7:            # ma uit pe diagonala dreapta jos
                                    if matr[i][j] == Joc.JMIN:
                                        break
                                    elif matr[i][j] == Joc.JMAX:
                                        tot_piese_adversar += 1
                                        break
                                    i += 1
                                    j += 1

                                if tot_piese_adversar == 3:
                                    k -= 1
                                    L -= 1
                                    l_mutari_valabile.remove([lin, col])

            k+=1



        for elem in l_mutari_valabile:
            pygame.draw.rect(display, (0, 255, 0),
                             (elem[1]*100, elem[0]*100, 100, 100), 3, 50)
            pygame.display.flip()  # !!! obligatoriu pentru a actualiza interfata (desenul)
            pygame.display.update()
        return l_mutari_valabile

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir

def eliminaPiese(matr, jucator):
    """
                Clasa care verifica daca am piese ce trebuiesc eliminate.
    """
    pieseDeEliminat = []
    if jucator == 'n':
        jucatorOpus = 'a'
    else:
        jucatorOpus = 'n'
    for i in range(8):
        for j in range(8):
            if matr[i][j] == jucatorOpus:
                lin = i                 # gasesc macar 3 piese ale adversarului opus, pe aceeasi
                col = j                 # linie, coloana sau diagonala cu spatiul curent
                tot_piese_adversar = 0

                for x in range(lin + 1, 8):             # ma uit pe aceeasi coloana in jos
                    if matr[x][col] == jucatorOpus:      # am deja o piesa aliat care ma protejeaza, deci nu mai caut
                        break                           # in continuare
                    elif matr[x][col] == jucator:
                        tot_piese_adversar += 1         # daca gasesc o piesa inamica, incrementez si ies
                        break

                for x in range(lin - 1, -1, -1):        # ma uit pe aceeasi coloana in sus
                    if matr[x][col] == jucatorOpus:
                        break
                    elif matr[x][col] == jucator:
                        tot_piese_adversar += 1
                        break

                for y in range(col + 1, 8):             # ma uit pe linie spre dreapta
                    if matr[lin][y] == jucatorOpus:
                        break
                    elif matr[lin][y] == jucator:
                        tot_piese_adversar += 1
                        break

                if tot_piese_adversar == 3:
                    pieseDeEliminat.append([i, j])
                    break

                else:
                    for y in range(col - 1, -1, -1):    # ma uit pe linie spre stanga
                        if matr[lin][y] == jucatorOpus:
                            break
                        elif matr[lin][y] == jucator:
                            tot_piese_adversar += 1
                            break

                    if tot_piese_adversar == 3:
                        pieseDeEliminat.append([i, j])
                        break

                    else:
                        x = lin - 1
                        y = col - 1
                        while x >= 0 and y >= 0:
                            if matr[x][y] == jucatorOpus:
                                break
                            elif matr[x][y] == jucator:
                                tot_piese_adversar += 1
                                break
                            x -= 1
                            y -= 1

                        if tot_piese_adversar == 3:
                            pieseDeEliminat.append([i, j])
                            break

                        else:
                            x = lin - 1
                            y = col + 1
                            while x >= 0 and y <= 7:            # ma uit pe diagonala dreapta sus
                                if matr[x][y] == jucatorOpus:
                                    break
                                elif matr[x][y] == jucator:
                                    tot_piese_adversar += 1
                                    break
                                x -= 1
                                y += 1

                            if tot_piese_adversar == 3:
                                pieseDeEliminat.append([i, j])
                                break

                            else:
                                x = lin + 1
                                y = col - 1
                                while x <= 7 and y >= 0:            # ma uit pe diagonala stanga jos
                                    if matr[x][y] == jucatorOpus:
                                        break
                                    elif matr[x][y] == jucator:
                                        tot_piese_adversar += 1
                                        break
                                    x += 1
                                    y -= 1

                                if tot_piese_adversar == 3:
                                    pieseDeEliminat.append([i, j])
                                    break

                                else:
                                    x = lin + 1
                                    y = col + 1
                                    while x <= 7 and y <= 7:        # ma uit pe diagonala dreapta jos
                                        if matr[x][y] == jucatorOpus:
                                            break
                                        elif matr[x][y] == jucator:
                                            tot_piese_adversar += 1
                                            break
                                        x += 1
                                        y += 1

                                    if tot_piese_adversar == 3:
                                        pieseDeEliminat.append([i, j])
                                        break




    return pieseDeEliminat

total_noduri_generate = 0
def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    global total_noduri_generate
    total_noduri_generate += len(stare.mutari_posibile)

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    global total_noduri_generate
    total_noduri_generate += len(stare.mutari_posibile)
    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final == 'n':
        print("A castigat negru!")
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0),
                         (700, 0, 100, 100), 3)
        pygame.display.update()
        return True
    elif final == 'a':
        print("A castigat alb!")
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0),
                         (0, 700, 100, 100), 3)
        pygame.display.update()
        return True

    return False

def main():
    # initializare algoritm
    t_start = int(round(time.time()))
    while True:
        dificultate = input("Alegeti dificultatea(easy/medium/hard): ")
        if dificultate == "easy":
            ADANCIME_MAX = 2
            break
        elif dificultate == "medium":
            ADANCIME_MAX = 3
            break
        elif dificultate == "hard":
            ADANCIME_MAX = 4
            break
        else:
            print("Inputul poate fi doar 'easy', 'medium' sau 'hard'! Alegeti din nou.")

    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu alb sau cu negru?(n/a) ").lower()
        if (Joc.JMIN in ['a', 'n']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie alb sau negru (a sau n).")
    Joc.JMAX = 'a' if Joc.JMIN == 'n' else 'n'

    # initializare tabla
    tabla_start = [['#', '#', '#', '#', 'a', 'a', 'a', '#'],
                   ['#', '#', '#', '#', 'a', 'a', 'a', 'a'],
                   ['#', '#', '#', '#', '#', 'a', 'a', 'a'],
                   ['#', '#', '#', '#', '#', '#', 'a', 'a'],
                   ['n', 'n', '#', '#', '#', '#', '#', '#'],
                   ['n', 'n', 'n', '#', '#', '#', '#', '#'],
                   ['n', 'n', 'n', 'n', '#', '#', '#', '#'],
                   ['#', 'n', 'n', 'n', '#', '#', '#', '#']]
    tabla_curenta = Joc(tabla_start)
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'n', ADANCIME_MAX)

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('Nacu_Andrei_Emilian - Archimedes')
    # dimensiunea ferestrei in pixeli
    # dim_celula=..
    ecran = pygame.display.set_mode(
        size=(800, 800))  # N *100+ (N-1)*dimensiune_linie_despartitoare (dimensiune_linie_despartitoare=1)
    Joc.initializeaza(ecran)
    de_mutat = False
    tabla_curenta.deseneaza_grid()

    timpi_gandire_calculator = []
    lista_numar_noduri = []
    nr_mutari_jucator = 0
    nr_mutari_calculator = 0

    lista_matrice_calculator = []
    copie_start = copy.deepcopy(tabla_start)
    lista_matrice_calculator.append(copie_start)
    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            t1 = int(round(time.time() * 1000))
            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.quit()
                        main()
                    elif event.key == pygame.K_u:
                        Lg = len(lista_matrice_calculator)
                        if Lg > 1:
                            stare_curenta.tabla_joc.matr = copy.deepcopy(lista_matrice_calculator[-2])
                            stare_curenta.tabla_joc.deseneaza_grid()
                            lista_matrice_calculator.pop()
                            lista_matrice_calculator.pop()
                        else:
                            stare_curenta.tabla_joc.matr = copy.deepcopy(copie_start)
                            stare_curenta.tabla_joc.deseneaza_grid()

                if event.type == pygame.QUIT:
                    pygame.quit()  # inchide fereastra
                    print("Total mutari jucator: " + str(nr_mutari_jucator))
                    print("Total mutari calculator: " + str(nr_mutari_calculator))
                    print("------------------------------------")
                    print("Timpul minim de gandire al calculatorului: " + str(
                        min(timpi_gandire_calculator)) + " milisecunde.")
                    print("Timpul maxim de gandire al calculatorului: " + str(
                        max(timpi_gandire_calculator)) + " milisecunde.")
                    print("Timpul mediu de gandire al calculatorului: " + str(
                        int(mean(timpi_gandire_calculator))) + " milisecunde.")
                    print("Mediana timpilor medii: " + str(int(median(timpi_gandire_calculator))) + " milisecunde.")
                    print("------------------------------------")
                    print("Numarul minim de noduri generate: " + str(min(lista_numar_noduri)))
                    print("Numarul maxim de noduri generate: " + str(max(lista_numar_noduri)))
                    print("Numarul mediu de noduri generate: " + str(int(mean(lista_numar_noduri))))
                    print("Mediana numerelor de noduri generate: " + str(int(median(lista_numar_noduri))))

                    t_finish = int(round(time.time()))
                    print("Timpul final de executie al programului este: " + str((t_finish - t_start)) + " secunde.")
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click

                    pos = pygame.mouse.get_pos()  # coordonatele clickului

                    for linie in range(Joc.NR_COLOANE):
                        for coloana in range(Joc.NR_COLOANE):
                            if Joc.colturi[linie][coloana].collidepoint(pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMIN:
                                    if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
                                        # daca am facut click chiar pe patratica selectata, o deselectez
                                        de_mutat = False
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                    else:
                                        de_mutat = (linie, coloana)
                                        # desenez gridul cu patratelul marcat
                                        stare_curenta.tabla_joc.deseneaza_grid(de_mutat)
                                        l_mutari_posibile = stare_curenta.posibilitateMutare(de_mutat[0], de_mutat[1],
                                                                                         stare_curenta.tabla_joc.matr,
                                                                                         Joc.display)
                                        #print(de_mutat[0], de_mutat[1], l_mutari_posibile)
                                elif stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                                    if de_mutat:
                                        #### eventuale teste legate de mutarea simbolului

                                        if [linie, coloana] in l_mutari_posibile:
                                            stare_curenta.tabla_joc.matr[de_mutat[0]][de_mutat[1]] = Joc.GOL
                                            de_mutat = False
                                            # plasez simbolul pe "tabla de joc"
                                            stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                            pieseEliminate = eliminaPiese(stare_curenta.tabla_joc.matr, Joc.JMIN)
                                            L = len(pieseEliminate)
                                            if L > 0:
                                                for piesaEliminata in pieseEliminate:
                                                    stare_curenta.tabla_joc.matr[piesaEliminata[0]][piesaEliminata[1]] = Joc.GOL
                                            stare_curenta.tabla_joc.deseneaza_grid()

                                            t2 = int(round(time.time() * 1000))
                                            print("Jucatorul a \"gandit\" timp de " + str(t2 - t1) + " milisecunde.")

                                            nr_mutari_jucator += 1
                                            # afisarea starii jocului in urma mutarii utilizatorului
                                            print("\nTabla dupa mutarea jucatorului")
                                            print(str(stare_curenta))

                                            # testez daca jocul a ajuns intr-o stare finala
                                            # si afisez un mesaj corespunzator in caz ca da
                                            if (afis_daca_final(stare_curenta)):

                                                print("Total mutari jucator: " + str(nr_mutari_jucator))
                                                print("Total mutari calculator: " + str(nr_mutari_calculator))
                                                print("------------------------------------")
                                                print("Timpul minim de gandire al calculatorului: " + str(
                                                    min(timpi_gandire_calculator)) + " milisecunde.")
                                                print("Timpul maxim de gandire al calculatorului: " + str(
                                                    max(timpi_gandire_calculator)) + " milisecunde.")
                                                print("Timpul mediu de gandire al calculatorului: " + str(
                                                    int(mean(timpi_gandire_calculator))) + " milisecunde.")
                                                print("Mediana timpilor medii: " + str(
                                                    int(median(timpi_gandire_calculator))) + " milisecunde.")
                                                print("------------------------------------")
                                                print(
                                                    "Numarul minim de noduri generate: " + str(min(lista_numar_noduri)))
                                                print(
                                                    "Numarul maxim de noduri generate: " + str(max(lista_numar_noduri)))
                                                print("Numarul mediu de noduri generate: " + str(
                                                    int(mean(lista_numar_noduri))))
                                                print("Mediana numerelor de noduri generate: " + str(
                                                    int(median(lista_numar_noduri))))

                                                t_finish = int(round(time.time()))
                                                print("Timpul final de executie al programului este: " + str(
                                                    (t_finish - t_start)) + " secunde.")

                                                break

                                            # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)

            print("Estimare: " + str(stare_actualizata.estimare))
            global total_noduri_generate
            print("Numar noduri generate: " + str(total_noduri_generate))

            lista_numar_noduri.append(total_noduri_generate)
            total_noduri_generate = 0
            nr_mutari_calculator += 1
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            copie = copy.deepcopy(stare_curenta.tabla_joc.matr)
            lista_matrice_calculator.append(copie)
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            stare_curenta.tabla_joc.deseneaza_grid()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            timpi_gandire_calculator.append(int(t_dupa - t_inainte))
            if (afis_daca_final(stare_curenta)):
                print("Total mutari jucator: " + str(nr_mutari_jucator))
                print("Total mutari calculator: " + str(nr_mutari_calculator))
                print("------------------------------------")
                print("Timpul minim de gandire al calculatorului: " + str(
                    min(timpi_gandire_calculator)) + " milisecunde.")
                print("Timpul maxim de gandire al calculatorului: " + str(
                    max(timpi_gandire_calculator)) + " milisecunde.")
                print("Timpul mediu de gandire al calculatorului: " + str(
                    int(mean(timpi_gandire_calculator))) + " milisecunde.")
                print("Mediana timpilor medii: " + str(int(median(timpi_gandire_calculator))) + " milisecunde.")
                print("------------------------------------")
                print("Numarul minim de noduri generate: " + str(min(lista_numar_noduri)))
                print("Numarul maxim de noduri generate: " + str(max(lista_numar_noduri)))
                print("Numarul mediu de noduri generate: " + str(int(mean(lista_numar_noduri))))
                print("Mediana numerelor de noduri generate: " + str(median(lista_numar_noduri)))

                t_finish = int(round(time.time()))
                print("Timpul final de executie al programului este: " + str((t_finish - t_start)) + " secunde.")
                break

            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
