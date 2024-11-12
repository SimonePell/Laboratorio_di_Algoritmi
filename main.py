import time
import random
import Abr 
import Tab
import Lc
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import sys
sys.setrecursionlimit(10000000)

def media_mobile(dati, finestra):
    kernel = np.ones(finestra) / finestra
    dati_smussati = np.convolve(dati, kernel, mode='same')
    return dati_smussati

def test(dim, rand, finestra):

    Albero = Abr.AlberoBinariodiRicerca()
    TabHash = Tab.TabellaHash(1)
    lista = Lc.ListaC()
    chiavi = list(range(1, dim + 1))
    if rand:
        random.shuffle(chiavi)

    tempi_aggiungi_A = media_mobile(Abr.misura_tempo_aggiungi(Albero, chiavi), finestra)
    tempi_recupera_A = media_mobile(Abr.misura_tempo_recupera(Albero, chiavi), finestra)
    tempi_elimina_A = media_mobile(Abr.misura_tempo_elimina(Albero, chiavi), finestra)

    tempi_aggiungi_H = media_mobile(Tab.misura_tempo_aggiungi(TabHash, chiavi), finestra)
    tempi_recupera_H = media_mobile(Tab.misura_tempo_recupera(TabHash, chiavi), finestra)
    tempi_elimina_H = media_mobile(Tab.misura_tempo_elimina(TabHash, chiavi), finestra)

    tempi_aggiungi_L = media_mobile(Lc.misura_tempo_aggiungi(lista, chiavi), finestra)
    tempi_recupera_L = media_mobile(Lc.misura_tempo_recupera(lista, chiavi), finestra)
    tempi_elimina_L = media_mobile(Lc.misura_tempo_elimina(lista, chiavi), finestra)
    
    dati_tabella_A = {'Nodi': list(range(1, dim + 1)), 'Tempo Aggiungi (s)': tempi_aggiungi_A,
                  'Tempo Recupera (s)': tempi_recupera_A, 'Tempo Elimina (s)': tempi_elimina_A}
    dati_tabella_H = {'Nodi': list(range(1, dim + 1)), 'Tempo Aggiungi (s)': tempi_aggiungi_H,
                    'Tempo Recupera (s)': tempi_recupera_H, 'Tempo Elimina (s)': tempi_elimina_H}
    dati_tabella_L = {'Nodi': list(range(1, dim + 1)), 'Tempo Aggiungi (s)': tempi_aggiungi_L,
                    'Tempo Recupera (s)': tempi_recupera_L, 'Tempo Elimina (s)': tempi_elimina_L}

    # Creazione dei DataFrame
    dfa = pd.DataFrame(dati_tabella_A)
    dfh = pd.DataFrame(dati_tabella_H)
    dfl = pd.DataFrame(dati_tabella_L)

    # Stampa delle tabelle complete
    print("Tabella dei Tempi di Esecuzione dell'albero:")
    print(dfa)
    print("\nTabella dei Tempi di Esecuzione dell'hash:")
    print(dfh)
    print("\nTabella dei Tempi di Esecuzione della lista:")
    print(dfl)

    # Seleziona i nodi specifici
    nodi_interesse = [1, 2, 3, 4, 5, 2499, 2500, 2501, 4999, 5000, 5001, 9999, 10000, 10001, 19999, 20000, 20001]

    # Filtraggio dei nodi di interesse per ciascuna tabella
    dfa_selezionato = dfa[dfa['Nodi'].isin(nodi_interesse)]
    dfh_selezionato = dfh[dfh['Nodi'].isin(nodi_interesse)]
    dfl_selezionato = dfl[dfl['Nodi'].isin(nodi_interesse)]

    # Stampa dei dati filtrati
    print("\nDati dei nodi specifici selezionati nell'albero:")
    print(dfa_selezionato)
    print("\nDati dei nodi specifici selezionati nell'hash:")
    print(dfh_selezionato)
    print("\nDati dei nodi specifici selezionati nella lista:")
    print(dfl_selezionato)

    # Creazione dei grafici
    plt.figure(figsize=(12, 8))

    legende = [
        Line2D([0], [0], color="red", lw=4, label="Hash"),
        Line2D([0], [0], color="blue", lw=4, label="ABR"),
        Line2D([0], [0], color="green", lw=4, label="Lista")
    ]

    # Grafico per l'aggiunta
    plt.subplot(3, 1, 1)
    ax1 = plt.gca()
    ax1.plot(dfh['Nodi'], dfh['Tempo Aggiungi (s)'], label="Tabella Hash", color="red")
    ax1.plot(dfl['Nodi'], dfl['Tempo Aggiungi (s)'], label="Lista Collegata", color="green")
    ax1.set_xlabel("Numero di nodi")
    ax1.set_ylabel("Tempo di esecuzione (secondi)")
    #ax1.legend(loc="upper left")
    ax1.grid(False)

    # Aggiunge un secondo asse per l'albero binario con scala logaritmica
    ax2 = ax1.twinx()
    ax2.plot(dfa['Nodi'], dfa['Tempo Aggiungi (s)'], label="Albero Binario", color="blue")
    if rand:
        ax2.set_yscale("log")
    #ax2.legend(loc="upper right")
    plt.legend(handles=legende, loc="upper left", fontsize=12, title="Colori")
    
    # Grafico per il recupero
    plt.subplot(3, 1, 2)
    ax1 = plt.gca()
    ax1.plot(dfh['Nodi'], dfh['Tempo Recupera (s)'], label="Tabella Hash", color="red")
    ax1.plot(dfl['Nodi'], dfl['Tempo Recupera (s)'], label="Lista Collegata", color="green")
    ax1.set_xlabel("Numero di nodi")
    ax1.set_ylabel("Tempo di esecuzione (secondi)")
    #ax1.legend(loc="upper left")
    ax1.grid(False)

    ax2 = ax1.twinx()
    ax2.plot(dfa['Nodi'], dfa['Tempo Recupera (s)'], label="Albero Binario", color="blue")
    if rand:
        ax2.set_yscale("log")
    #ax2.legend(loc="upper right")
    plt.legend(handles=legende, loc="upper left", fontsize=12, title="Colori")

    # Grafico per l'eliminazione
    plt.subplot(3, 1, 3)
    ax1 = plt.gca()
    ax1.plot(dfh['Nodi'], dfh['Tempo Elimina (s)'], label="Tabella Hash", color="red")
    ax1.plot(dfl['Nodi'], dfl['Tempo Elimina (s)'], label="Lista Collegata", color="green")
    ax1.set_xlabel("Numero di nodi")
    ax1.set_ylabel("Tempo di esecuzione (secondi)")
    ax1.grid(False)
    #plt.legend(loc="upper left", bbox_to_anchor=(1, 1), ncol=1, title="Tipi di funzione")

    ax2 = ax1.twinx()
    ax2.plot(dfa['Nodi'], dfa['Tempo Elimina (s)'], label="Albero Binario", color="blue")
    if rand:
        ax2.set_yscale("log")
    
    # Aggiungi la legenda personalizzata
    plt.legend(handles=legende, loc="upper right", fontsize=12, title="Colori")

    if rand == False:
        plt.savefig("Tutti_WC")
    else:
        plt.savefig("Tutti_AC")
    
    plt.tight_layout()
    plt.show()  # Chiamata singola a plt.show() alla fine

# Esecuzione della funzione di test
plt.close('all')  # Chiude tutte le finestre grafiche aperte
test(2001, False, 250)
