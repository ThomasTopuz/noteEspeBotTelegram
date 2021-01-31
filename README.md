<h1>Progetto bot telegram noteEspe in python</h1>
  L'idea del progetto è di creare un bot telegram per automatizzare l'invio degli espe fatti e delle note ricevute al datore di lavoro.
  Ogni settimana in un file docx bisogna mettere gli espe fatti e quelli ricevuti.
  Prevedo di espandere il progetto a più utenti, identificando l'utente tramite l'username di telegram
  
<h3>Hosting</h3>
Per hostare il mio bot uso una vm di gcloud, come ssh client uso termius
Usando una sessione tmux posso continuare a runnare il mio script anche con terminale chiuso

<h3>Database</h3>
Come database userò il realtime database di firebase e lo organizzo nel seguente modo:
<img src="https://github.com/ThomasTopuz/noteEspeBot/blob/master/Capture.PNG?raw=true">
I dati che non ha ancora inserito l'utente verrano messi a -1.
Quando l'utente vorra inserire la nota di un espe che ha ricevuto, su telegram appariranno tutti gli espe che non hanno ancora la nota,
e con un click si può aggiungere la nota.


<h3>Librerie</h3>
- python-telegram-bot --> https://github.com/python-telegram-bot/python-telegram-bot
- python-docx per generare ogni venerdi il file docx da inviare al datore di lavoro --> https://github.com/python-openxml/python-docx
- prevedo anche di usare yagmail per inviare la email al datore, allegando il docx --> https://github.com/kootenpv/yagmail
- pyrebase che mi permette di interfacciarmi con il mio realtime db --> https://github.com/thisbejim/Pyrebase
