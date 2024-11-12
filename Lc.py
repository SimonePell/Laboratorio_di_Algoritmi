import time
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Nodo:
    def __init__(self, chiave, valore):#costruttore nodo
        self.chiave = chiave
        self.valore = valore
        self.next = None

class ListaC:
    def __init__(self):#costruttore
        self.testa = None

    def aggiungi(self, chiave, valore):#aggiunge un valore alla lista o alla testa
        nodo = Nodo(chiave, valore)
        if self.testa is None:
            self.testa = nodo
            return
        indice = self.testa
        while indice.next is not None:
            indice = indice.next
        indice.next = nodo

    def recupera(self, chiave):#ciclia e cerca la chiave data, se non ha successo ritorno None
        indice = self.testa
        while indice.next is not None and indice.chiave is not chiave:
            indice = indice.next
        if indice.next is None:
            return None
        else:
            return indice.valore
        
    def elimina(self, chiave):#controlla se esiste la lista e se è composta da un solo elemento,
        indice = self.testa   # dopo cicla fino a trovare ed eliminare il nodo che ha la chiave data
        nodo = None
        if indice is None:
            return False
        if indice.next is None:
            self.testa = None
            return True
        nodo = indice.next
        while nodo.next is not None and nodo.chiave is not chiave:
            indice = indice.next
            nodo = nodo.next
        indice.next = nodo.next
        return True

def misura_tempo_aggiungi(lista, chiavi):
    tempi = []
    for chiave in chiavi:
        inizio = time.perf_counter()
        lista.aggiungi(chiave, chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def misura_tempo_recupera(lista, chiavi):
    tempi = []
    for chiave in chiavi:
        inizio = time.perf_counter()
        lista.recupera(chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def misura_tempo_elimina(lista, chiavi):
    tempi = []
    chiavi = list(reversed(chiavi))
    for chiave in chiavi:
        inizio = time.perf_counter()
        lista.elimina(chiave)
        fine = time.perf_counter()
        tempi.append(fine - inizio)
    return tempi

def media_mobile(dati, finestra):
    kernel = np.ones(finestra) / finestra
    dati_smussati = np.convolve(dati, kernel, mode='same')
    return dati_smussati

def test_con_grafico_e_tabella_lista_concatenata(dimensione, rand, finestra):
    lista = ListaC()
    chiavi = list(range(1, dimensione + 1))
    if rand == True:
        random.shuffle(chiavi)  # Shuffle per simulare un caso d'uso realistico

    # Misura il tempo per l'aggiunta
    tempi_aggiungi = misura_tempo_aggiungi(lista, chiavi)
    tempi_aggiungi = media_mobile(tempi_aggiungi, finestra)

    # Misura il tempo per il recupero
    tempi_recupera = misura_tempo_recupera(lista, chiavi)
    tempi_recupera = media_mobile(tempi_recupera, finestra)

    # Misura il tempo per l'eliminazione
    tempi_elimina = misura_tempo_elimina(lista, chiavi)
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
    plt.plot(df['Nodi'], df['Tempo Aggiungi (s)'], label="Tempo di aggiunta (LC)", color="blue")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione aggiunta")
    plt.grid(False)

    # Grafico per il recupero
    plt.subplot(3, 1, 2)
    plt.plot(df['Nodi'], df['Tempo Recupera (s)'], label="Tempo di recupero (LC)", color="green")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione recupero")
    plt.grid(False)

    # Grafico per l'eliminazione
    plt.subplot(3, 1, 3)
    plt.plot(df['Nodi'], df['Tempo Elimina (s)'], label="Tempo di eliminazione (LC)", color="red")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo di esecuzione eliminazione")
    plt.grid(False)
    
    if rand == False:
        plt.savefig("Lc_WC")
    else:
        plt.savefig("Lc_AC")

    plt.subplots_adjust(hspace=1.5)

    # Mostra il grafico
    plt.tight_layout()
    #plt.show()


#test_con_grafico_e_tabella_lista_concatenata(2001, False, 75)