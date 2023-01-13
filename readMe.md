BiggusPy è un editor di nodi che ti consente di programmare in modo visuale utilizzando una interfaccia 
grafica intuitiva. Ciascun nodo rappresenta un'istruzione python, come una variabile, una stringa o un 
comando print, che può essere collegato ad altri nodi per creare un flusso di dati e una serie di operazioni. 
Collegando ad esempio una stringa al nodo print posso stampare sullo schermo la celebre frase "Hello World".

    https://imgur.com/JFpHwsY

Il programma è ancora in fase embrionale ma è già possibile effettuare alcune operazioni base come collegare, 
scollegare, cancellare o salvare un progetto e aprire un progetto. BiggusPy è in grado d'interpretare il codice 
python scritto in modo tradizionale e creare una struttura di nodi corrispondente, rendendo la transizione 
dalla programmazione testuale alla programmazione visiva più semplice e l'obbiettivo è quello di poter esportare 
il progetto sviluppato in BiggusPy in un codice python tradizionale per la condivisione o la distribuzione.

E' sicuramente un modo diverso di visualizzare il codice e ha il vantaggio di far guardare il proprio progetto 
da un punto di vista diverso e questo in molte occasioni, si traduce in un debugging più avanzato anche perchè 
il nuo modo di visualizzare il codice permette di vedere eventuali errori che potrebbero essere difficili 
da individuare con i sistemi di programmazione tradizionali. Ad esempio, la connessione tra i nodi rende 
immediatamente evidente se si stanno passando parametri sbagliati in una funzione o se si sta utilizzando 
un oggetto invece di un altro. Questo rende BiggusPy uno strumento potente per la risoluzione degli errori 
e per la creazione di codice pulito e ben strutturato.

Alcuni nodi sono presenti nel menù contestuale quindi, per poterli inserire basta premere il tasto destro e 
selezionare il nodo da inserire dal menu. Non sono presenti ancora tutti i comandi di Python, però ce ne sono già 
alcuni che permettono di creare un'ampia gamma di esempi. Un altro modo Per inserire nodi nella scena è usando
il tasto tab, scrivere il nome del nodo, premere invio e boom, il nodo sarà pronto li ad essere collegato. 


PER GLI SVILUPPATORI:

Il programma è stato sviluppato in collaborazione con Chat Bot Ai e mi ha dato un boost di conoscenze incredibili; E'
stato scritto in python utilizzando la versione dalla 3.7 alla 3.11 e utilizza alcune librerie come ast per lavorare 
il codice, jSon per la serializzazione delle classi e PyQt5 per la creazione dell'interfaccia. Dovrebbe erre compatibile 
con la nuova versione di PyQt6, purtroppo da alcuni test soprattutto con la parte multimediale ho visto che per alcune
cose la versione precedente ha una marcia in più. Alcune chiamate non sono più compatibili nella versione successiva, 
ma più in là farò probabilmente un upgrade.

E' un programma scritto a oggetti, ma non è molto hardcore, anzi ho tentato di mantenere il codice il più pulito 
possibile per mantenere alta la leggibilità. Il codice quindi è suddiviso in varie cartelle diviso per argomenti,
nella graphicElements quindi ci sono gli oggetti che possono essere inseriti nella scena, nella graphicEngine, 
gli oggetti per l'overrides dei motori grafici, in widgets, il canvas per creare l'editor vero e proprio ed 
esternamente alle cartelle sono presenti solo due file main.py che fa partire il programma e mainWin che in qt 
si occupa di creare la finestra principale con il menu, la status bar, il menu e via discorrendo.

La struttura dei nodi è stata programmata, mettendo insieme tre classi, una per la parte dati, una per la 
parte grafica che si occupa di disegnare il nodo nella canvas e una classe interfaccia che è quella che si prefigge
di fare fra ponte fra i dati e la grafica, ha funzioni per la modifica dei nodi in modo da farlo adattare alle 
varie esigenze e in più è quella che viene richiamata al momento della creazione. 

I nodi veri e propri vengono poi creati in base alla libreria di rifermimento che al momento è python. Per creare ad
esempio un NumberNode basta creare un file Python che fa l'override della classe data e inserendo alcune proprietà,
metodi e variabili amplia la classe astratta in modo da mimare una istruzione di int, come funzione per il casting, ma 
anche come variabile che può quindi essere collegata a un SumNode che ha due ingressi e che fornisce in uscita 
una semplice somma.

La funzione più complessa è la function nella quale si può inserire una funzione qualsiasi e il nodo si ridimensiona 
in modo da avere tanti ingressi, quante uscite sono necessarie per poter calcolare il risultato:

La funzione:
'''
def add_and_multiply(a, b, c):
    d = a + b
    e = d * c
    return e
'''
può essere trasformata in un nodo. Grazie alla libreria ast si può calcolare che ha tre ingressi (a, b, c) e una 
uscita e. 



Problemi nodi:
quando si cancella il nodo collegato rimane il riferimento al vecchio nodo - bisogna migliarare il sistema di rimozione 
dei plug in-plug out e questo è una bug anche nel caso in cui si usi new per creare una nuova scena.

Quando si prova a incollare un codice completo le connessioni anchora non sono perfette.

bisogna implementare anche altri nodi di python e costruire alcuni file di esempio in modo che chi è interessato 
abbia una linea guida di partenza. 
