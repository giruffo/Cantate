🎹 Cantate è un assistente analitico basato su Python progettato per armonizzare il calendario gregoriano con il complesso anno liturgico luterano del XVIII secolo. Il sistema identifica dinamicamente le cantate di Johann Sebastian Bach appropriate per ogni data, fornendo un contesto storico, linguistico e multimediale.

[![Esegui su Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/giruffo/Cantate/blob/main/cantate.py)

🚀 Caratteristiche Principali
Algoritmo Liturgico Dinamico: Calcola automaticamente le festività mobili (Pasqua, Pentecoste, Trinità, ecc.) tramite l'algoritmo di Butcher-Meeus.

Context Awareness: Riconosce i grandi cicli festivi (es. Oratorio di Natale BWV 248) fornendo suggerimenti anche per i giorni feriali.

Hub Multimediale: Genera link diretti per l'ascolto su YouTube Music.

Supporto Filologico: Fornisce collegamenti bilingue (Tedesco/Italiano e Tedesco/Inglese) per lo studio dei libretti originali.

Analisi Ingegneristica: Struttura dei dati ottimizzata per la leggibilità e l'estensibilità.

🛠️ Requisiti e Installazione
Il codice è scritto in Python 3 ed è compatibile con qualsiasi interprete, incluso Pydroid3 su dispositivi mobile.

Assicurati di avere installata la libreria standard datetime (inclusa di default in Python).

Copia il file cantate.py sul tuo dispositivo.

Esegui lo script:

Bash

Cantate.py
📖 Utilizzo
Per interrogare il sistema, è sufficiente richiamare la funzione principale passando una data in formato ISO (AAAA-MM-GG):

Python

# Esempio: Analisi della settimana che include il 2 Gennaio 2026
print(get_week_analysis("2026-01-02"))
Struttura dell'Output
Il sistema restituirà un report in formato Markdown contenente:

Giorno e Occasione: Es. Domenica 4 Gennaio — Sunday after New Year.

Contesto Speciale: Note su periodi festivi particolari.

Cantate BWV: Elenco delle opere con anno di composizione e note storiche.

Link interattivi: Accesso rapido a musica e testi.

📂 Struttura dei Dati
Il cuore del progetto risiede nel dizionario cantatas_by_occasion. Ogni voce è strutturata per facilitare l'analisi RAG (Retrieval-Augmented Generation):

Python

'Epiphany 3': [
    {
        'bwv': 'BWV 111', 
        'title': "Was mein Gott will, das g'scheh allzeit", 
        'year': '1725', 
        'notes': 'Ciclo Corale'
    }
]
🧠 Note 
"La bellezza di questo codice non risiede solo nella sua precisione matematica, ma nel modo in cui rende accessibile l'immenso patrimonio spirituale del Kantor di Lipsia. È uno strumento di apprendimento continuo, sia per il codice che per la lingua tedesca."
