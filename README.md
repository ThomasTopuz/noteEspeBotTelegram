<h1>Progetto bot telegram noteEspe in python</h1>
  L'idea del progetto è di creare un bot telegram per automatizzare l'invio degli espe fatti e delle note ricevute al datore di lavoro.
  Ogni settimana in un file docx bisogna mettere gli espe fatti e quelli ricevuti.
  Prevedo di espandere il progetto a più utenti, identificando l'utente tramite l'username di telegram 

<h3>Demo del progetto</h3>
<img src="https://github.com/ThomasTopuz/noteEspeBot/blob/master/media/Capture.PNG?raw=true">


<h3>Database</h3>
Come database userò il realtime database di firebase e lo organizzo nel seguente modo:
<img src = "https://github.com/ThomasTopuz/noteEspeBot/blob/master/media/Capsture.PNG?raw=true">
I dati che non ha ancora inserito l'utente verrano messi a -1.
Quando l'utente vorra inserire la nota di un espe che ha ricevuto, su telegram appariranno tutti gli espe che non hanno ancora la nota,
e con un click si può aggiungere la nota.

<h3>Hosting e Deploy</h3>
Per hostare il mio bot uso una vm di contabo, come ssh client uso termius.
Per il deploy ho pacchetizzato il bot in una immagine di docker, ho fatto il push su docker hub e ho fatto il pull dalla mia virtual machine, per finire ho eseguito la mia immagine.

<h3>Librerie</h3>
- "python-telegram-bot" è una wrapper dell'api di telegram --> https://github.com/python-telegram-bot/python-telegram-bot
- "python-docx" il file docx da inviare al datore di lavoro --> https://github.com/python-openxml/python-docx
- "smtplib" per inviare la email al datore, allegando il docx --> https://docs.python.org/3/library/smtplib.html
- "Pyrebase4" mi permette di interfacciarmi con il mio realtime database di firebase --> https://github.com/thisbejim/Pyrebase


