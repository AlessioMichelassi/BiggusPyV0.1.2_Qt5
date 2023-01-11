BiggusPy è un editor di nodi che ti consente di programmare in modo visuale utilizzando una interfaccia 
grafica intuitiva. Ciascun nodo rappresenta un'istruzione python, come una variabile, una stringa o un 
comando print, che può essere collegato ad altri nodi per creare un flusso di dati e una serie di operazioni. 
Collegando ad esempio una stringa al nodo print posso stampare sullo schermo la celebre frase "Hello World".

Il programma è ancora in fase embrionale ma è già possibile effettuare alcune operazioni base come collegare, 
scollegare, cancellare, salvare un progetto e aprire un progetto.

Per inserire nodi nella scena basta premere tab, scrivere il nome del nodo, oppure si può selezionare 
il nodo dal menù contestuale che si apre cliccando con il tasto destro un qualsiasi punto della canvas.


PER GLI SVILUPPATORI:

I nodi sono stati programmati, mettendo insieme tre classi, una classe per la parte dati che varia in funzione 
del tipo di nodo, una classe graphica che si occupa di disegnare il nodo nella canvas e una classe interfaccia 
che è quella che viene richiamata al momento della creazione del nodo e che si occupa di scambiare i dati fra 
la parte dati e la parte grafica.

la parte dati è chiamata "AbstractNodeData" e definisce le caratteristiche comuni dei nodi e dei dei plug. 
Ci sono poi varie classi figlie, come "NumberNode", "SumNode", "ProductNode", che estendono la classe base 
per implementare funzionalità specifiche. I plug sono le connessioni al nodi. Ogni nodo può avere uno o più ingressi 
e una o più uscite,

Inoltre, ci sono classi per la creazione di interfacce grafiche, come "graphicViewOverride" e "graphicSceneOverride", 
che estendono le classi di base di Qt per creare un'interfaccia grafica per visualizzare e interagire con il grafico.

Il programma utilizza anche un sistema di "Observer" per notificare i nodi interessati quando un valore cambia, 
in modo che possano aggiornare il loro stato di conseguenza.

In sintesi, questo programma fornisce un sistema di creazione e gestione di nodi e plug per la creazione 
di grafici di calcolo, utilizzando classi e interfacce grafiche e un sistema di notifica degli observer 
per la gestione del flusso dei dati.

to do:
quando si cancella il nodo collegato rimane il riferimento al vecchio nodo