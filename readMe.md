BiggusPy è un editor di nodi per la creazione di un grafico di calcolo. 

Viene utilizzato una gerarchia di classi, con una classe base chiamata "AbstractNodeData", 
che definisce le caratteristiche comuni dei nodi e delle interfacce dei plug. Ci sono poi varie classi figlie, 
come "NumberNode", "SumNode", "ProductNode", che estendono la classe base per implementare funzionalità specifiche.

Inoltre, ci sono classi per la creazione di interfacce grafiche, come "graphicViewOverride" e "graphicSceneOverride", 
che estendono le classi di base di Qt per creare un'interfaccia grafica per visualizzare e interagire con il grafico.

Il programma utilizza anche un sistema di "Observer" per notificare i nodi interessati quando un valore cambia, 
in modo che possano aggiornare il loro stato di conseguenza.

In sintesi, questo programma fornisce un sistema di creazione e gestione di nodi e plug per la creazione 
di grafici di calcolo, utilizzando classi e interfacce grafiche e un sistema di notifica degli observer 
per la gestione del flusso dei dati.

to do:
quando si cancella il nodo collegato rimane il riferimento al vecchio nodo