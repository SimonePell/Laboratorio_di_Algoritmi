import time
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Nodo:
    def __init__(self, chiave, valore):#costruttore nodo
        self.chiave = chiave
        self.valore = valore
        self.prossimo = None

class TabellaHash:
    def __init__(self, dimensione):#inizializzazione della tabella hash
        self.dimensione = dimensione
        self.tabella = [None] * dimensione

    def hash(self, chiave):#funzione hash
        return hash(chiave) % self.dimensione

    def aggiungi(self, chiave, valore):
        indice = self.hash(chiave)
        nodo = self.tabella[indice]

        if nodo is None:
            self.tabella[indice] = Nodo(chiave, valore)#caso in cui il nodo non esiste ancora
            return

        while nodo is not None:
            if nodo.chiave == chiave:
                nodo.valore = valore
                return
            if nodo.prossimo is None:
                nodo.prossimo = Nodo(chiave, valore)#scorre fino alla fine della lista
                return
            nodo = nodo.prossimo

    def recupera(self, chiave):
        indice = self.hash(chiave)
        nodo = self.tabella[indice]

        while nodo is not None:
            if nodo.chiave == chiave:
                return nodo.valore
            nodo = nodo.prossimo

        return None

    def elimina(self, chiave):
        indice = self.hash(chiave)#stesso principio delle liste concatenate 
        nodo = self.tabella[indice]
        precedente = None

        while nodo is not None:
            if nodo.chiave == chiave:
                if precedente is None:
                    self.tabella[indice] = nodo.prossimo
                else:
                    precedente.prossimo = nodo.prossimo
                return True
            precedente = nodo
            nodo = nodo.prossimo

        return False

def misura_tempo_aggiungi(Hash, chiavi):
    tempi = []
    for chiave in chiavi:
        inizio = time.perf_counter()
        Hash.aggiungi(chiave, chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def misura_tempo_recupera(Hash, chiavi):
    tempi = []
    for chiave in chiavi:
        inizio = time.perf_counter()
        Hash.recupera(chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def misura_tempo_elimina(Hash, chiavi):
    tempi = []
    chiavi = list(reversed(chiavi))
    for chiave in chiavi:
        inizio = time.perf_counter()
        Hash.elimina(chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def media_mobile(dati, finestra):
    kernel = np.ones(finestra) / finestra
    dati_smussati = np.convolve(dati, kernel, mode='same')
    return dati_smussati

def test_con_grafico_e_tabella_Hash(dimensione, rand, finestra):
    Hash = TabellaHash(1)
    chiavi = list(range(1, dimensione + 1))
    if rand == True:
        random.shuffle(chiavi)  # Shuffle per simulare un caso d'uso realistico

    # Misura il tempo per l'aggiunta
    tempi_aggiungi = misura_tempo_aggiungi(Hash, chiavi)
    tempi_aggiungi = media_mobile(tempi_aggiungi, finestra)

    # Misura il tempo per il recupero
    tempi_recupera = misura_tempo_recupera(Hash, chiavi)
    tempi_recupera = media_mobile(tempi_aggiungi, finestra)

    # Misura il tempo per l'eliminazione
    tempi_elimina = misura_tempo_elimina(Hash, chiavi)
    tempi_elimina = media_mobile(tempi_aggiungi, finestra)

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
    plt.plot(df['Nodi'], df['Tempo Aggiungi (s)'], label="Tempo di aggiunta (Hash)", color="blue")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione (secondi)")
    plt.grid(False)

    # Grafico per il recupero
    plt.subplot(3, 1, 2)
    plt.plot(df['Nodi'], df['Tempo Recupera (s)'], label="Tempo di recupero (Hash)", color="green")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione (secondi)")
    plt.grid(False)

    # Grafico per l'eliminazione
    plt.subplot(3, 1, 3)
    plt.plot(df['Nodi'], df['Tempo Elimina (s)'], label="Tempo di eliminazione (Hash)", color="red")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione (secondi)")
    plt.grid(False)

    if rand == False:
        plt.savefig("Hash_WC")
    else:
        plt.savefig("Hash_AC")

    # Mostra il grafico
    plt.tight_layout()
    #plt.show()


#test_con_grafico_e_tabella_Hash(2001, True, 75)