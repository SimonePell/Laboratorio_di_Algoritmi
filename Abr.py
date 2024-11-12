import time
import matplotlib.pyplot as plt
import random
import pandas as pd 
import numpy as np
import sys
sys.setrecursionlimit(10000000)

class Nodo:
    def __init__(self, chiave, valore):
        self.chiave = chiave
        self.valore = valore
        self.destra = None
        self.sinistra = None

class AlberoBinariodiRicerca:
    def __init__(self):
        self.radice = None

    def aggiungi(self, chiave, valore):
        if self.radice is None:                 #caso in cui l'albero p vuoto
            self.radice = Nodo(chiave, valore)
        else:
            self.aggiungi_ric(self.radice, chiave, valore) #caso in cui l'albero NON è vuoto

    def aggiungi_ric(self, nodo, chiave, valore):
        if chiave < nodo.chiave:                            #si sposta sul figlio sinistro
            if nodo.sinistra is None:                       #se non esiste il figlio sinistro crea un nodo
                nodo.sinistra = Nodo(chiave, valore)
            else:                                           #ricorsione figlio sinistro
                self.aggiungi_ric(nodo.sinistra, chiave, valore)
        elif chiave > nodo.chiave:                          #si sposta sul figlio destro
            if nodo.destra is None:                         #se non esiste il figlio destro crea un nodo
                nodo.destra = Nodo(chiave, valore)
            else:                                           #ricorsione figlio destro
                self.aggiungi_ric(nodo.destra, chiave, valore)

    def recupera(self, chiave):
        return self.recupera_ric(self.radice, chiave)

    def recupera_ric(self, nodo, chiave):
        if nodo is None:                                    #caso in cui NON esiste la chiave e ritorna None
            return None
        if chiave == nodo.chiave:                           #caso in cui esiste la chiave e ritorna il valore
            return nodo.valore
        elif chiave < nodo.chiave:
            return self.recupera_ric(nodo.sinistra, chiave)
        else:
            return self.recupera_ric(nodo.destra, chiave)

    def elimina(self, chiave):
        self.radice = self.elimina_ric(self.radice, chiave)

    def elimina_ric(self, nodo, chiave):
        if nodo is None:                                    #caso in cui NON esiste la chiave
            return nodo
        if chiave < nodo.chiave:
            nodo.sinistra = self.elimina_ric(nodo.sinistra, chiave)
        elif chiave > nodo.chiave:
            nodo.destra = self.elimina_ric(nodo.destra, chiave)
        else:
            if nodo.sinistra is None:                       #caso in cui il figlio sinistro non esiste, quindi possiamo semplicemente sostituire
                return nodo.destra                          #il nodo con il figlio destro
            if nodo.destra is None:                         #caso in cui il figlio destro non esiste, quindi possiamo semplicemente sostituire
                return nodo.sinistra                        #il nodo con il figlio sinistro
            temp = self._minimo(nodo.destra)                #caso in cui i figli esistono, quinid devo andare a prendere il minimo del sottoalbero
            nodo.chiave = temp.chiave                       #destro e metterlo al nodo eliminandolo dalla vecchia posizione
            nodo.valore = temp.valore
            nodo.destra = self.elimina_ric(nodo.destra, temp.chiave)
        return nodo

    def _minimo(self, nodo):                                #trova il nodo con chiave minore di un albero
        corrente = nodo
        while corrente.sinistra is not None:
            corrente = corrente.sinistra
        return corrente

def misura_tempo_aggiungi(Abr, chiavi):
    tempi = []
    for chiave in chiavi:
        inizio = time.perf_counter()
        Abr.aggiungi(chiave, chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def misura_tempo_recupera(Abr, chiavi):
    tempi = []
    for chiave in chiavi:
        inizio = time.perf_counter()
        Abr.recupera(chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def misura_tempo_elimina(Abr, chiavi):
    tempi = []
    chiavi = list(reversed(chiavi))
    for chiave in chiavi:
        inizio = time.perf_counter()
        Abr.elimina(chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def media_mobile(dati, finestra):
    kernel = np.ones(finestra) / finestra
    dati_smussati = np.convolve(dati, kernel, mode='same')
    return dati_smussati

def test_con_grafico_e_tabella_Abr(dimensione, rand, finestra):
    Abr = AlberoBinariodiRicerca()
    chiavi = list(range(1, dimensione + 1))
    if rand == True:
        random.shuffle(chiavi)  # Shuffle per simulare un caso d'uso realistico
    
    # Misura il tempo per l'aggiunta
    tempi_aggiungi = misura_tempo_aggiungi(Abr, chiavi)
    tempi_aggiungi = media_mobile(tempi_aggiungi, finestra)

    # Misura il tempo per il recupero
    tempi_recupera = misura_tempo_recupera(Abr, chiavi)
    tempi_recupera = media_mobile(tempi_recupera, finestra)

    # Misura il tempo per l'eliminazione
    tempi_elimina = misura_tempo_elimina(Abr, chiavi)
    tempi_elimina = media_mobile(tempi_elimina, finestra)

    # Crea la tabella dei tempi
    dati_tabella = {
        'Nodi': list(range(1, dimensione + 1)),
        'Tempo Aggiungi (s)': tempi_aggiungi,
        'Tempo Recupera (s)': tempi_recupera,
        'Tempo Elimina (s)': tempi_elimina
    }
    
    df = pd.DataFrame(dati_tabella)
    print("Tabella dei Tempi di Esecuzione Completa:")
    print(df)

    # Seleziona i nodi specifici
    nodi_interesse = [1, 2, 3, 4, 5, 2499, 2500, 2501, 4999, 5000, 5001, 9999, 10000, 10001, 19999, 20000, 20001]
    df_selezionato = df[df['Nodi'].isin(nodi_interesse)]
    print("\nDati dei nodi specifici selezionati:")
    print(df_selezionato)

    # Creazione dei grafici
    plt.figure(figsize=(12, 8))

    # Grafico per l'aggiunta
    plt.subplot(3, 1, 1)
    plt.plot(df['Nodi'], df['Tempo Aggiungi (s)'], label="Tempo di aggiunta (ABR)", color="blue")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione (secondi)")
    if rand == True:
        plt.yscale("log")
    plt.grid(False)

    # Grafico per il recupero
    plt.subplot(3, 1, 2)
    plt.plot(df['Nodi'], df['Tempo Recupera (s)'], label="Tempo di recupero (ABR)", color="green")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione (secondi)")
    if rand == True:
        plt.yscale("log")
    plt.grid(False)

    # Grafico per l'eliminazione
    plt.subplot(3, 1, 3)
    plt.plot(df['Nodi'], df['Tempo Elimina (s)'], label="Tempo di eliminazione (ABR)", color="red")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione (secondi)")
    if rand == True:
        plt.yscale("log")
    plt.grid(False)
    
    if rand == False:
        plt.savefig("Abr_WC")
    else:
        plt.savefig("Abr_AC")

    # Mostra il grafico
    plt.tight_layout()
    #plt.show()


#test_con_grafico_e_tabella_Abr(2001, False, 75)