<h1>Progetto NoteEspeBot <img width="75px" src="https://avatars.githubusercontent.com/u/16178365?s=400&v=4"></h1>
  L'idea del progetto è di creare un bot telegram per automatizzare l'invio degli espe fatti e delle note ricevute al datore di lavoro.
  Ogni settimana in un file docx bisogna mettere gli espe fatti e quelli ricevuti.
  Il bot è usabile da più utenti, identificando l'utente tramite l'username di telegram.

<h2>Demo del progetto</h2>
<img width="500px" src="https://user-images.githubusercontent.com/49570615/118365545-7c9ba480-b59d-11eb-9e89-e91620cdd34d.PNG">

<h2>Funzionalità <img width="75px" height="75px" src="https://cdn.pixabay.com/photo/2017/10/24/00/39/bot-icon-2883144_1280.png"></h2>
<ul>
  <li>Comando <b>"nuovo_espe"</b> : ritorna il markup per la scelta della materia (viene presa dal database di firebase, dalle informazioni dell'utente prende l'anno scolastico), in seguito si può inserire una osservazione</li>
  <li>Comando <b>"registra_nota"</b> : ritorna il markup per la scelta dell'espe di qui si vuole registrare la nota, in seguito si può inserire la nota ed una ulteriore osservazione</li>
    <li>Comando <b>"insights"</b> : restituisce una panoramica della settimana corrente degli espe fatti e quelli ricevuti, con le rispettive note</li>
    <li>Comando <b>"invia_email"</b> : genera il documento word e lo invia sia al datore di lavoro (email fissa)</li>
</ul>

<h2>Database <img width="75px" src = "https://4.bp.blogspot.com/-rtNRVM3aIvI/XJX_U07Z-II/AAAAAAAAJXY/YpdOo490FTgdKOxM4qDG-2-EzcNFAWkKACK4BGAYYCw/s1600/logo%2Bfirebase%2Bicon.png"></h2>
Come database userò il realtime database di firebase e lo organizzo nel seguente modo:
<img src = "https://user-images.githubusercontent.com/49570615/118365475-39413600-b59d-11eb-81ac-339cba93958a.PNG">

I dati che non ha ancora inserito l'utente verrano messi a -1.
Quando l'utente vorra inserire la nota di un espe che ha ricevuto, su telegram appariranno tutti gli espe che non hanno ancora la nota,
e con un click si può aggiungere la nota.

Per ricevere le materie di un utente ho strutturato una collection dove ad ogni anno scolastico corrispondono le materia che l'allievo ha.
<img src = "https://user-images.githubusercontent.com/49570615/118365769-870a6e00-b59e-11eb-952f-274c6e7c8206.PNG">

<h2>Librerie <img width="75px" src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png"></h2>
<ul>
<li>"python-telegram-bot" è una wrapper dell'api di telegram --> https://github.com/python-telegram-bot/python-telegram-bot</li>
<li>"python-docx" per generare il file docx da inviare al datore di lavoro --> https://github.com/python-openxml/python-docx</li>
<li>"smtplib" per inviare la email al datore, allegando il docx --> https://docs.python.org/3/library/smtplib.html</li>
<li>"Pyrebase4" mi permette di interfacciarmi con il mio realtime database di firebase --> https://github.com/thisbejim/Pyrebase</li>
<li>"Cryptography" mi permette di encriptare e decriptare informazioni sensibili --> https://pypi.org/project/cryptography/</li>
</ul>

<h2>Hosting e Deploy <img width="75px" src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/Moby-logo.png?itok=sYH_JEaJ"></h2>
Per hostare il mio bot uso una vm di DigitalOcean, come ssh client uso termius.
Per il deploy ho pacchetizzato il bot in una immagine di docker, ho fatto il push su docker hub e ho fatto il pull dalla mia virtual machine, per finire ho eseguito la mia immagine.

