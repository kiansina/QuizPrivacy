#CREATE TABLE qst
# (Username TEXT PRIMARY KEY, Nome TEXT, Cognome TEXT,
#  Livello_sodisfazione integer, q1 varchar(1),  time1 varchar(6), q2 varchar(1), time2 varchar(6),
#  q3 varchar(1), time3 varchar(6), q4 varchar(1), time4 varchar(6), q5 varchar(1), time5 varchar(6), q6 varchar(1), time6 varchar(6),
#  q7 varchar(1), time7 varchar(6), q8 varchar(1), time8 varchar(6), q9 varchar(1), time9 varchar(6), q10 varchar(1), time10 varchar(6),time varchar(10));

#CREATE TABLE signin
# (User_In TEXT PRIMARY KEY);

#INSERT INTO qst2 (Username, Nome, Cognome,Livello_sodisfazione, q1, q2,q3 ,q4 ,q5 , time) VALUES('ssin','sin','sin','100','sin','sin','sin','sin','sin','120');




import streamlit as st
import pandas as pd
import psycopg2
import time
import random
from PIL import Image

img=Image.open('lo.jfif')
st.set_page_config(page_title="Questionnaire", page_icon=img)

hide_menu_style= """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """
col1, col2, col3 = st.columns(3)


st.markdown(hide_menu_style, unsafe_allow_html=True)
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

conn.autocommit = True

sql = """select * from qst"""
cursor = conn.cursor()
cursor.execute(sql)
df=pd.DataFrame(cursor.fetchall(),columns=['Username',	'Nome',	'Cognome',	'Livello_sodisfazione',	'q1', 't1',	'q2', 't2',	'q3', 't3',	'q4', 't4',	'q5', 't5',	'q6', 't6', 'q7', 't7', 'q8', 't8', 'q9', 't9', 'q10', 't10', 'time'])

sql = """select * from signin"""
cursor = conn.cursor()
cursor.execute(sql)
ds=pd.DataFrame(cursor.fetchall(),columns=['User_In'])

sql = """select * from quiz_user"""
cursor = conn.cursor()
cursor.execute(sql)
df_user=pd.DataFrame(cursor.fetchall(),columns=['ID','User', 'nome',	'Dipartimento',	'Qualifica', 'Tariffa'])

questions = {
  "1": "Per dato personale si intende:",
  "2": "Quali dati posso acquisire ai sensi del GDPR per eseguire il mio lavoro?",
  "3": "Con riferimento al Trattamento dei dati personali, cosa si intende con il termine “limitare”?",
  "4": "Quale dei seguenti è l’uso corretto che posso fare dei dati personali di un individuo?",
  "5": "I Trattamenti di dati personali implicano tutti lo stesso livello di rischio?",
  "6": "Quale delle seguenti azioni può essere utilizzata per mitigare i rischi legati al Trattamento di dati personali?",
  "7": "Durante una trasferta di lavoro, o in una qualunque altra situazione,  mi rubano lo zaino (o la borsa) contenente uno o più strumenti di lavoro (es.: PC, telefono “aziendale”, documenti, etc.) contenenti informazioni riguardanti persone fisiche: a chi devo rivolgermi per comunicare l’incidente?",
  "8": "Titolare o Responsabile del Trattamento: quale ruolo assume i-law quando esegue un incarico professionale ricevuto da un cliente?",
  "9": "Devo inviare una email ad un elevato numero di destinatari: quale tra le seguenti azioni costituisce una best practice per la spedizione di comunicazioni massive?",
  "10": "Nell’ambito degli incarichi professionali, devo fornire ai rappresentanti e referenti (persone fisiche) del cliente l’Informativa sul Trattamento dei dati personali?",
  "11": "Quando un dato può dirsi effettivamente “anonimo” o “anonimizzato”?",
  "12": "Il GDPR si applica al Trattamento dei dati personali:",
  "13": "Ai sensi del GDPR, cosa si intende per «Titolare del Trattamento» e quali attività ha diritto di svolgere tale soggetto?",
  "14": "Ai sensi del GDPR quando due o più soggetti possono essere “contitolari del Trattamento”?",
  "15": "Ai sensi del GDPR il Responsabile del Trattamento dei dati, deve attenersi alle istruzioni impartite:",
  "16": "Ai sensi del GDPR, si intende per «Responsabile del Trattamento»:",
  "17": "Ai sensi del GDPR quale soggetto ha l'obbligo di tenere un Registro delle attività di Trattamento?",
  "18": "Qual è la sanzione massima prevista dal GDPR in caso di violazione delle disposizioni relative ai diritti degli interessati?",
  "19": "Una violazione di dati personali consiste:",
  "20": "Secondo quanto disposto dal GDPR, da chi possono essere effettuate le operazioni di Trattamento dei dati personali?",
  "21": "Qual è il comportamento da tenere nel caso in cui un cliente/fornitore/altro soggetto terzo metta a disposizione del professionista di i-law dati personali non necessari per l’esecuzione dell’incarico/altra attività di propria competenza, senza effettuare alcuna selezione?",
  "22": "Quando termina l’incarico in cui I-law ha agito quale Titolare del Trattamento, con quali modalità devo conservare i dati personali che ho utilizzato per lo svolgimento del lavoro?",
  "23": "Ai sensi della normativa in materia di protezione dei dati personali, per «Persona autorizzata al Trattamento» si intende:",
  "24": "Che differenza c’è tra confidenzialità, data protection e information security?",
  "25": "Come mi devo comportare se smarrisco un documento (elettronico o cartaceo) contenente un elenco di debitori indicati come “debitore 1”, “debitore 2”, “debitore 3” di una società cliente di cui non è riportata la denominazione?",
  "26": "Quale, tra quelli di seguito indicati, è un dato personale: (i) sesso femminile, (ii) 35 anni di età (iii) qualifica aziendale “manager”?",
  "27": "Per trattare i dati personali devo avere sempre acquisito preventivamente il consenso dell’Interessato?",
  "28": "Se il cliente ha necessità di fornire al team di lavoro un’ingente quantità di documenti ai fini dell’esecuzione dell’incarico:",
  "29": "In cosa consiste il principio di “clean-desk” previsto dalle procedure di i-law per tutelare i dati personali, oltre alle informazioni riservate di natura non personale?",
  "30": "Quali di questi dati non sono considerati categorie particolari di dati personali?",
  "31": "Il registro dei trattamenti è…",
  "32": "Il rapporto tra titolare e responsabile del trattamento…",
  "33": "L’informativa all’interessato…",
  "34": "L’interessato può chiedere che i suoi dati personali vengano rettificati…",
  "35": "Il diritto alla portabilità è…",
  "36": "Il principio di privacy by design impone al titolare di…",
  "37": "Cosa è un data breach?",
}

choices = {
"1": [("Ogni tipo di dato o informazione che identifica o rende identificabile univocamente una persona fisica","T"),
      ("Qualsiasi tipo di informazione riguardante una persona fisica","F"),
      ("Ogni tipo di dato o informazione che identifica o rende identificabile univocamente una persona fisica, un ente, un’associazione o una società","F")],
"2": [("Soltanto i dati personali strettamente necessari, se possibile resi anonimi o utilizzando pseudonimi","T"),
      ("Tutti i dati personali raccolti e forniti dal cliente senza necessità di effettuare alcuna selezione","F"),
      ("Soltanto i dati personali strettamente necessari e previa autorizzazione del cliente","F")],
"3": [("Acquisire il minor numero possibile di dati personali, consentire l’accesso ai dati solo alle persone che hanno una effettiva necessità di utilizzarli, al termine del lavoro conservare adeguatamente solo i dati necessari","T"),
      ("Non acquisire in alcun caso dati personali quando devo effettuare un lavoro","F"),
      ("Acquisire tutti i dati necessari per il mio lavoro, ma distruggerli tutti indistintamente al temine del lavoro","F")],
"4": [("Posso utilizzare i dati unicamente per gli scopi precedentemente concordati con i soggetti da cui sono stati ricevuti, ad esempio un cliente o un fornitore, verificando, in caso di dubbi, gli accordi contrattuali sottoscritti da i-law a questo proposito","T"),
      ("Posso utilizzare i dati per tutti gli scopi utili per i-law o per il raggiungimento dei suoi obiettivi, senza dover chiedere alcuna autorizzazione alla persona a cui i dati si riferiscono","F"),
      ("Posso utilizzare i dati per tutti gli scopi utili per i soggetti a cui i dati si riferiscono e/o per i soggetti che li hanno trasmessi a  i-law, ma solo se è stato ricevuto il previo consenso dell’Interessato","F")],
"5": [("No, alcuni Trattamenti sono più rischiosi di altri, in funzione del tipo di dati trattati, dell’ambito di diffusione, degli strumenti utilizzati e del quantitativo di dati raccolti o comunque disponibili","T"),
      ("Sì perché trattare i dati personali è sempre un’attività che espone i-law ad alto rischio","F"),
      ("No, i Trattamenti di dati acquisiti dai clienti sono più rischiosi dei trattamenti di dati riguardanti il personale di i-law in quanto soltanto i primi possono comportare l’avvio di un ricorso dinanzi all’Autorità Garante per la protezione dei dati personali","F")],
"6": [("Tutti i comportamenti indicati nelle altre risposte sono corretti ai sensi del GDPR e sono idonei a mitigare il rischio","T"),
      ("Raccogliere il minor quantitativo possibile di dati e, ove possibile, renderli anonimi o utilizzare degli pseudonimi","F"),
      ("Limitare l’accesso ai dati solo alle persone che hanno necessità di utilizzarli e cancellare, al termine del lavoro, tutti i dati non necessari","F")],
"7": [("Al Team Privacy il  quale, se ravvisa la consumazione di un Data Breach (effettivo o potenziale), provvede a coinvolgere il DPO e i soggetti incaricati della sicurezza dei sistemi informatici","T"),
      ("Al legale rappresentante di i-law che provvede, se ravvisa la consumazione di un Data Breach (effettivo o potenziale), a coinvolgere il Team Privacy e il DPO","F"),
      ("A uno qualunque dei soci di i-law il quale, se ravvisa la consumazione di un Data Breach (effettivo o potenziale), provvede a coinvolgere il Team Privacy e il DPO","F")],
"8": [("a seconda degli accordi negoziali conclusi con il cliente  e del tipo di mandato conferito, i-law può assumere la veste di Titolare del Trattamento oppure  il ruolo di Responsabile. Questa circostanza è solitamente indicata nel contratto con il cliente e di essa va tenuto conto nel trattamento dei dati personali ricevuti","T"),
      ("i-law è sempre Titolare del Trattamento in quanto, proponendo servizi professionali ai propri clienti tramite le proprie lettere di incarico, definisce in ogni caso lo scopo e la finalità del Trattamento dei dati personali ricevuti","F"),
      ("i-law tratta sempre i dati personali in qualità di Responsabile su nomina del cliente in quanto, in relazione a ciascun incarico conferito, quest’ultimo consegna a i-law i dati di cui è Titolare, che lo Studio deve trattare secondo le modalità indicate dal cliente stesso","F")],
"9": [("Tutti i destinatari della email devono essere inseriti in modalità “copia conoscenza nascosta” (“CCN” o “BCC”) in modo tale che il singolo destinatario non sia in grado di avere visibilità degli altri soggetti a cui la email è stata inviata","T"),
      ("L’invio della email può avvenire con visibilità di tutti i destinatari in quanto l’indirizzo email non è un dato personale","F"),
      ("L’invio della email, con modalità massive, è consentita solamente previa consultazione con il Team Privacy","F")],
"10": [("Sì, sempre","T"),
       ("Solo quando anche il cliente fornisce la propria Informativa sul Trattamento dei dati personali","F"),
       ("Devo valutare attentamente, caso per caso, ogni singola posizione","F")],
"11": [("Un dato è anonimo o anonimizzato quando non è possibile risalire all’identità della persona cui si riferisce","T"),
       ("Un dato è anonimo o anonimizzato quando non si conosce il Titolare o il Responsabile del Trattamento","F"),
       ("Un dato è anonimo o anonimizzato quando non può più essere attribuito a un Interessato specifico, se non utilizzando informazioni aggiuntive in possesso dell’utilizzatore del dato","F")],
"12": [("Riferito a soggetti Interessati che si trovano nell’Unione Europea, effettuato da un Titolare o da un Responsabile del Trattamento anche non stabilito nell'Unione Europea","T"),
       ("Effettuato nell’ambito delle attività svolte da un’organizzazione con sedi in diversi Paesi anche non appartenenti allo Spazio Economico Europeo","F"),
       ("Effettuato da un Responsabile del Trattamento che non è stabilito nell'Unione Europea ma tratta dati personali relativi a condanne penali e reati di interessati residenti nello Spazio Economico Europeo","F")],
"13": [("La persona fisica o giuridica, l'autorità pubblica, il servizio o altro organismo che ha diritto di determinare le finalità e i mezzi del Trattamento di dati personali, sempre in presenza delle condizioni, previste dal GDPR, che rendono legittimo il Trattamento dei dati","T"),
       ("La persona fisica cui i dati personali si riferiscono, la quale può liberamente consentire qualsiasi uso dei propri dati personali","F"),
       ("La persona fisica o giuridica avente il diritto di determinare i mezzi con cui effettuare un Trattamento di dati personali, per le sole finalità previste da normative vigenti","F")],
"14": [("Quando due o più Titolari del Trattamento determinano congiuntamente le finalità e i mezzi del Trattamento, stabilendo in modo trasparente, mediante un accordo interno, le rispettive responsabilità in merito all'osservanza degli obblighi derivanti dal GDPR","T"),
       ("Si configura la contitolarità del Trattamento quando un Titolare ed un Responsabile utilizzano gli stessi dati e a condizione che il Titolare abbia fornito precise istruzioni al Responsabile","F"),
       ("Il GDPR non prevede tale possibilità. Il Titolare del Trattamento è sempre un solo soggetto","F")],
"15": [("Dal Titolare","T"),
       ("Dal Garante per la protezione dei dati personali","F"),
       ("Dall’Interessato","F")],
"16": [("La persona fisica o giuridica, l'autorità pubblica, il servizio o altro organismo che tratta dati personali per conto del Titolare del Trattamento","T"),
       ("La persona fisica o giuridica che vigila sulla corretta applicazione del GDPR secondo le istruzioni impartite dal Titolare","F"),
       ("La persona fisica o giuridica, ente o associazione, cui si riferiscono i dati","F")],
"17": [("Sia il Titolare che il Responsabile hanno l’obbligo di tenere un Registro delle attività di Trattamento","T"),
       ("Il Titolare ha l'obbligo di tenere un Registro delle attività di Trattamento","F"),
       ("Il Responsabile ha l'obbligo di tenere un Registro delle attività di Trattamento effettuate per conto del Titolare","F")],
"18": [("Sanzioni amministrative pecuniarie fino a 20.000.000 di euro, o per le imprese, fino al 4 % del fatturato mondiale totale annuo dell'esercizio precedente","T"),
       ("Da 50.000 a 50.000.000 euro a seconda del tipo di violazione","F"),
       ("Sanzioni amministrative pecuniarie fino a 10.000.000 di euro, o per le imprese, fino al 2 % del fatturato mondiale totale annuo dell'esercizio precedente","F")],
"19": [("Entrambe l'altre risposte","T"),
       ("In una violazione di sicurezza che comporta - accidentalmente o in modo illecito - la distruzione, la perdita, la modifica, la divulgazione non autorizzata o l’accesso ai dati personali trasmessi, conservati o comunque trattati","F"),
       ("In una divulgazione di dati riservati o confidenziali all’interno di un ambiente privo di misure di sicurezza (ad esempio, sul web) in maniera involontaria o volontaria. Tale divulgazione può avvenire in seguito a: perdita accidentale, furto, accesso abusivo","F")],
"20": [("Solo da persone fisiche autorizzate che operano seguendo le istruzioni impartite dal Titolare o del Responsabile del Trattamento","T"),
       ("Esclusivamente da persone qualificate che risultano iscritte in appositi Albi Professionali","F"),
       ("Tanto da persone fisiche quanto da persone giuridiche che operano seguendo le istruzioni impartite dal Titolare o dal Responsabile del Trattamento","F")],
"21": [("Devo chiedere al cliente di fornire (se possibile anonimizzati o pseudonimizzati) solo i dati personali necessari ai fini dello svolgimento dell’incarico/attività di mia competenza e rifiutare la consegna di grandi quantitativi di dati non selezionati e non necessari","T"),
       ("Se ritengo che possa essere utile all’esecuzione dell’incarico posso accettare dal cliente/fornitore/altro soggetto terzo la banca dati senza effettuare alcun intervento","F"),
       ("Devo selezionare e anonimizzare in autonomia i dati che mi occorrono cancellando quelli non necessari e darne atto al cliente/fornitore/altro soggetto terzo","F")],
"22": [("Devo conservare i dati personali unicamente su server e cartelle di rete messe a disposizione da I-law, con divieto di creare cartelle di backup o copie personali dei dati trattati","T"),
       ("Devo conservare le banche dati sul pc personale o su chiavetta USB, previa autorizzazione del Team Privacy","F"),
       ("Devo conservare i dati personali su server e cartelle di rete messe a disposizione da I-law, ma per sicurezza è buona norma creare anche cartelle di backup o copie personali dei dati trattati","F")],
"23": [("La persona fisica autorizzata a compiere operazioni di Trattamento dal Titolare o dal Responsabile","T"),
       ("La persona fisica o giuridica, l'autorità pubblica, il servizio o altro organismo che, singolarmente o insieme ad altri, determina le finalità e i mezzi del Trattamento di dati personali","F"),
       ("La persona fisica o giuridica, l'autorità pubblica, il servizio o altro organismo che tratta dati personali per conto del Titolare del Trattamento","F")],
"24": [("La confidenzialità ha ad oggetto la tutela di dati e informazioni considerate “riservate”, riguardanti indifferentemente un soggetto giuridico oppure una persona fisica; la data protection tutela i dati personali riguardanti esclusivamente persone fisiche; mentre l’information security è l’insieme di processi aziendali e attività finalizzate a prevenire e contrastare le minacce a tutte le informazioni contenute su supporti digitali e non digitali","T"),
       ("Pressoché nessuna, tutte e tre le materie fanno parte della disciplina sulla privacy","F"),
       ("La confidenzialità e la data protection disciplinano il Trattamento dei dati personali: in particolare, la confidenzialità riguarda le informazioni relative a persone giuridiche, mentre la data protection tutela le informazioni delle persone fisiche. L’information security ha invece ad oggetto la protezione del patrimonio informativo aziendale","F")],
"25": [("Devo segnalare che ho smarrito il documento al Team Privacy, il quale, se ravvisa la consumazione di un Data Breach (effettivo o potenziale), provvede a coinvolgere il DPO per valutare congiuntamente  il da farsi","T"),
       ("Non devo fare nulla posto che il documento non contiene dati personali “in chiaro” che consentono l’identificazione diretta dei debitori del cliente (non compaiono, ad esempio, Mario Rossi, Carla Bianchi, ecc.)","F"),
       ("i-law deve notificare lo smarrimento del documento elettronico al Garante entro 72 ore dall’evento. Se il documento è cartaceo, invece, non occorre procedere ad alcuna comunicazione all’Autorità","F")],
"26": [("I dati indicati possono assumere natura di dato personale se, eventualmente integrati da ulteriori informazioni disponibili, consentono di identificare univocamente una persona fisica","T"),
       ("Tutti i dati indicati hanno natura personale in quanto possono consentire di identificare una persona fisica","F"),
       ("Nessuno dei dati indicati nel quesito può essere considerato un dato personale, a meno che non sia associato al nome e cognome (o altro dato identificativo “in chiaro”) di un individuo","F")],
"27": [("No, il consenso dell’Interessato non è l’unica condizione che consente di trattare legittimamente i dati personali in quanto la normativa prevede ulteriori e differenti basi giuridiche","T"),
       ("Sì, devo in ogni caso avere preventivamente ottenuto il consenso dell’Interessato in quanto solo questo presupposto rende lecito il Trattamento, fatta eccezione per i dati pubblicamente disponibili, che posso utilizzare per qualsiasi finalità","F"),
       ("Sì, la normativa vieta qualsiasi uso di dati personali a meno che il soggetto che intende trattarli non abbia ricevuto un esplicito consenso da parte dell’Interessato","F")],
"28": [("Posso utilizzare esclusivamente unità esterne fornite da i-law","T"),
       ("Posso utilizzare hard disk esterni del cliente purché siano dotati di password aventi almeno 8 caratteri e mi consentono di trasferire in sicurezza i dati sul mio PC  e/o sulla rete aziendale","F"),
       ("Posso utilizzare una  chiavetta USB per trasferire dati sul mio PC aziendale solo se ritengo che sia uno strumento idoneo a rispettare i più adeguati standard di sicurezza","F")],
"29": [("L’obbligo di archiviare in luogo protetto i documenti di lavoro riservati e di custodire adeguatamente gli strumenti di lavoro, in particolare al termine della giornata e in caso di assenze prolungate dalla postazione di lavoro","T"),
       ("L’obbligo di consegnare al proprio referente i documenti di lavoro riservati in caso di assenza dalla propria postazione per oltre 3 ore","F"),
       ("L’obbligo di conservare e archiviare adeguatamente in formato elettronico le carte di lavoro, per limitare il più possibile l’uso di supporti documentali cartacei","F")],
"30": [("Immagini e video che ritraggono l’interessato","T"),
       ("Informazioni relative agli orientamenti sessuali, politici o religiosi dell’interessato","F"),
       ("Informazioni relative alla salute dell’interessato","F")],
"31": [("Un documento contenente una mappatura delle principali informazioni relative alle operazioni di trattamento svolte dal titolare (e dal responsabile) del trattamento","T"),
       ("Un documento in cui vengono raccolte informazioni sul personale del titolare del trattamento","F"),
       ("Un documento in cui vengono raccolte informazioni sugli incidenti di sicurezza informatica occorsi","F")],
"32": [("Deve essere regolato mediante apposito accordo scritto contenente i requisiti previsti dall’articolo 28, GDPR","T"),
       ("Non necessita di alcuna regolamentazione in quanto trattasi di due entità autonome ed indipendenti","F"),
       ("È regolato da apposito accordo scritto che deve essere inoltrato all’Autorità Garante per la protezione dei dati","F")],
"33": [("Deve essere preferibilmente fornita in via preventiva rispetto all’inizio delle attività di trattamento o contestualmente allo stesso","T"),
       ("Non può mai essere fornita all’interessato successivamente al trattamento posto in essere","F"),
       ("È necessario fornirla solo nel caso in cui i trattamenti svolti siano particolarmente complessi","F")],
"34": [("Sempre e comunque in modo semplice e potendo contare su una rapida esecuzione da parte del titolare del trattamento","T"),
       ("Solo a valle di una richiesta dell’Autorità giudiziaria","F"),
       ("Solo se fa domanda all'Autorità Garante per la protezione dei dati","F")],
"35": [("Il diritto dell’interessato a ricevere in un formato strutturato, di uso comune e leggibile da dispositivo automatico i dati personali che lo riguardano forniti a un titolare del trattamento","T"),
       ("Il diritto del titolare del trattamento a conoscere le attività di trattamento di dati personali poste in essere da un altro titolare","F"),
       ("Il diritto dell’interessato ad opporsi in qualsiasi momento, per motivi connessi alla sua situazione particolare, al trattamento dei dati personali che lo riguardano","F")],
"36": [("Osservare le previsioni dettate dal GDPR sin dal momento della progettazione dei sistemi mediante cui il trattamento verrà posto in essere","T"),
       ("Dimostrare di aver adempiuto alle prescrizioni di cui al GDPR","F"),
       ("Sviluppare degli automatismi per l’aggiornamento dei propri database","F")],
"37": [("Un incidente/evento (che attiene alla sicurezza informatica o a qualunque altra circostanza) che comporti una compromissione delle caratteristiche dei dati personali trattati in formato digitale o cartaceo","T"),
       ("Un trasferimento dei dati personali al di fuori dello Spazio Economico Europeo","F"),
       ("Qualsiasi attacco informatico all’infrastruttura IT di una certa azienda/organizzazione","F")],
}


explan = {
  "1": "Per poter essere definita “dato personale” un’informazione deve riferirsi a una persona fisica e consentire di risalire in maniera univoca all’identità di tale soggetto, anche in associazione ad eventuali ulteriori informazioni che lo riguardano. Inoltre, il Trattamento di dati e informazioni relativi a soggetti diversi da persone fisiche (es. dati riguardanti un ente, un’associazione  o una società) non sono disciplinati dalla normativa sulla protezione dei dati personali.",
  "2": "Per operare in conformità alla normativa sulla protezione dei dati personali è richiesto di effettuare una selezione, prima dell’avvio del Trattamento, dei dati che è necessario acquisire e utilizzare. La normativa prevede infatti uno specifico obbligo di “minimizzazione” secondo il quale non solo dobbiamo raccogliere e trattare unicamente i dati strettamente necessari all’attività da svolgere, ma occorre anche, ogniqualvolta sia possibile, ottenerli dal “proprietario” (Titolare) del dato (ad es. un cliente) in forma anonima oppure pseudonimizzati. L’anonimizzazione rappresenta la scelta più cautelativa in quanto un dato anonimo/anominizzato, ossia che non è possibile ricondurre ad alcuno specifico individuo, perde la natura di “dato personale”. In tal caso dunque, la normativa sulla data protection non trova applicazione.",
  "3": "Il concetto di “limitazione” è correlato al più esteso obbligo di minimizzazione, previsto dalla normativa sulla protezione dei dati personali. L’obbligo di limitazione non costituisce un divieto assoluto di acquisire, utilizzare e conservare i dati, ma impone al professionista, a tutela del soggetto cui i dati si riferiscono, un rigoroso esercizio di valutazione e individuazione della tipologia e della quantità di dati da trattare, dei soggetti ai quali è consentito fornire accesso, della durata del periodo di conservazione successivo all’uso dei dati.",
  "4": "In nessun caso i dati personali possono essere utilizzati senza limitazioni. Quando utilizziamo dati personali occorre anzitutto assicurarsi che il Trattamento sia coerente alle finalità per cui sono stati raccolti. Il consenso dell’Interessato è solo una delle diverse condizioni che la normativa prevede per eseguire legittimamente il Trattamento;      infatti in alcuni casi possiamo, ad esempio, utilizzare i dati personali per adempiere ad un obbligo di legge o per eseguire un contratto. In ogni caso, occorre essere sempre consapevoli dell’uso dei dati previsto e/o consentito, consultando la documentazione (contratti, normative, informative, etc) alla quale il Trattamento si riferisce.",
  "5": "Alcuni Trattamenti comportano un livello più elevato di rischio in considerazione principalmente della tipologia di dati. A titolo di esempio, il Trattamento presenta un rischio maggiore se i dati personali sono idonei a rivelare l’origine razziale o etnica, le opinioni politiche, le convinzioni religiose o filosofiche, l’appartenenza sindacale, nonché se si tratta di dati genetici, dati relativi alla salute o dati riguardanti la sfera sessuale o       condanne penali e       reati. Un ulteriore elemento di rischio è costituito dal Trattamento di dati personali di persone fisiche particolarmente vulnerabili, quali i minori, oppure se il Trattamento riguarda una notevole quantità di dati personali e/o un vasto numero di interessati.",
  "6": "Tutti i Trattamenti di dati personali comportano dei rischi, sia per il soggetto che li utilizza, che potrebbe incorrere in gravi responsabilità in caso di uso improprio, non legittimo o non autorizzato, sia per il soggetto Interessato, che potrebbe subire rilevanti pregiudizi (es. discriminazioni, perdite economiche, lesioni della dignità personale, etc.) a causa di un uso scorretto dei suoi dati personali. Per tale motivo, occorre trattare i dati personali solo quando strettamente necessario. Tale indicazione, oltre a costituire un obbligo esplicito di legge (articolo 5, GDPR) è anche un modo per evitare eventuali violazioni dei dati personali, i c.d. data breach e, conseguentemente, l’applicazione di sanzioni. Inoltre, l’utilizzo di forme di protezione dei dati personali quali l’anonimizzazione o la pseudonimizzazione consentono di limitare i rischi derivanti da un’eventuale violazione dei dati.",
  "7": "Il caso del furto di uno zaino (o di una borsa) contenente il PC, il telefono “aziendale” o dei       documenti       rappresenta un (potenziale)      Data Breach in quanto tutti questi strumenti di lavoro      contengono normalmente una rilevante quantità di dati personali. Considerato che la normativa vigente impone, in base alla gravità dell’incidente, di notificare il fatto al Garante per la protezione dei dati personali entro 72 ore dalla rilevazione dell’episodio, occorre      comunicare con la massima tempestività tutti i dettagli del Data Breach al Team Privacy           in modo tale da consentirgli      di       intraprendere     , in maniera adeguata     , tutte le azioni necessarie per la gestione del caso nelle tempistiche previste dalla normativa.",
  "8": "A norma del GDPR, il Titolare del Trattamento è la persona fisica o giuridica, l'autorità pubblica, il servizio o altro organismo che, singolarmente o insieme ad altri, determina le finalità e i mezzi del Trattamento di dati personali; mentre il Responsabile è la persona fisica o giuridica, l'autorità pubblica, il servizio o altro organismo che tratta dati personali per conto del Titolare del Trattamento. Gli obblighi e i conseguenti adempimenti a carico del Titolare o del Responsabile sono significativamente diversi e questa circostanza va tenuta nel debito conto a seconda del ruolo assunto da i-law in occasione del conferimento dello specifico mandato e di quanto pattuito con il cliente a questo proposito.",
  "9": "In conformità al principio di «integrità e riservatezza» di cui all’articolo 5, lettera f, GDPR, i dati personali devono essere sempre trattati in maniera da garantire un'adeguata sicurezza degli stessi, ivi compresa la protezione (mediante misure tecniche e organizzative adeguate) da trattamenti non autorizzati o illeciti in modo tale da evitare altresì la perdita, la distruzione o altri utilizzi impropri. L’invio di una comunicazione massiva senza impostare la modalità “CCN” o “BCC” nel campo dei destinatari costituisce, pertanto, una violazione del principio di riservatezza imposto dalla normativa vigente oltre che una potenziale violazione dei dati personali, consentendo infatti a ciascun destinatario di visualizzare ingiustificatamente l’indirizzo di posta elettronica degli altri destinatari e, potenzialmente, di poter utilizzare tali dati in assenza di una specifica autorizzazione.",
  "10": "Quanto i-law tratta dati di rappresentanti e referenti del cliente      opera come Titolare e      ha quindi sempre       l’obbligo di fornire loro l’Informativa. Tale Informativa è presente nel      modello      contrattuale standard       di i-law     , mediante il quale      viene veicolata al soggetto Interessato (es. legale rappresentante, persone di contatto) a cura  della società cliente     . Pertanto, trasmettendo la lettera d’incarico al cliente si chiede a quest’ultimo di  fornire      agli interessati       anche la relativa Informativa. In tutti i casi in cui i-law      formalizzi un conferimento di incarico senza utilizzare il proprio  modello standard      di lettera      di incarico      (es. bandi di gara o altri contesti in cui si fa ricorso alle condizioni contrattuali del cliente), il team di lavoro dovrà provvedere, prima di iniziare a svolgere l’incarico, alla trasmissione dell’Informativa tramite apposita e autonoma comunicazione indirizzata al cliente chiedendogli di farla pervenire agli interessati oppure a inviarla direttamente a questi ultimi.",
  "11": "A differenza della cifratura e della pseudonimizzazione dei dati personali, che      costituiscono misure di protezione degli stessi, l’anonimizzazione è una procedura che      attraverso      la rimozione definitiva dei dati identificativi (es.: nome e cognome) e      l’aggregazione o generalizzazione degli altri dati personali      rende impossibile      risalire all’identità delle persone a cui ci si riferise      o ri-associare univocamente, in tutto o in parte, anche a posteriori, i dati o le informazioni trattati      a singoli soggetti.",
  "12": "L’ambito di applicazione territoriale del GDPR si articola attraverso i seguenti criteri: (i) il soggetto che esegue il Trattamento ha la propria sede principale (ossia quella dove vengono definite le finalità e le modalità di Trattamento dei dati) nell’Unione Europea indipendentemente dal fatto che il Trattamento sia effettuato o meno in un Paese europeo ed indipendentemente dal luogo di residenza/nazionalità del soggetto i cui dati vengono trattati; (ii) il soggetto i cui dati vengono trattati si trova, anche transitoriamente, in un Paese europeo nel momento di raccolta dei dati (es. cittadini dei Paesi membri, persone con residenza in tali Paesi, persone che si trovano momentaneamente in tali Paesi).",
  "13": "Il Titolare del Trattamento è un soggetto dotato di ampi margini decisionali in merito all’utilizzo dei dati personali in quanto definisce: (i) le finalità e (ii) le modalità con cui trattare tali dati; tuttavia, tale soggetto non opera in totale libertà. Tali attività      possono essere svolte dal Titolare in presenza di una “base giuridica”, ossia di condizioni che giustifichino il Trattamento dei dati (es. consenso dell’Interessato, obblighi di legge, esecuzione di un contratto cui l’Interessato è parte) e nei limiti delle attività necessarie al raggiungimento delle finalità per cui i dati sono stati raccolti (es. partecipare ad un evento di formazione, eseguire un incarico professionale). Il Titolare è soggetto ad una serie di responsabilità e obblighi (a titolo di esempio redigere e fornire l’Informativa agli Interessati, applicare il principio di minimizzazione dei dati, comunicare al Garante eventuali casi di violazione di dati personali, etc.). Il Titolare può inoltre nominare altri soggetti per effettuare alcune attività di Trattamento ossia i c.d. Responsabili del Trattamento. A differenza del Titolare, il Responsabile non determina finalità e modalità del Trattamento, deve attenersi rigorosamente alle istruzioni ricevute dal Titolare, ed è soggetto a verifiche/controlli da parte di quest’ultimo.",
  "14": "Un esempio di contitolarità è quello che si potrebbe verificare tra una società appartenente al Gruppo societario XXX che fornisce servizi      amministrativi, contabili ed organizzativi a tutte le altre società del medesimo gruppo.       Infatti, al fine di consentire l’esecuzione di alcuni trattamenti generali di interesse per tutte le società del Gruppo      (es. quelli finalizzati alla gestione del personale, all’esecuzione di attività di information technology oppure di marketing, etc.), le stesse potrebbero concludere          , ai sensi dell’articolo 26, GDPR, un Accordo di Contitolarità con la loro “società di servizi”     . Ciò in quanto tale società, fornendo i servizi amministrativi, contabili ed organizzativi menzionati in precedenza a tutte le entità del Gruppo     , potrebbe definire      congiuntamente ad esse le finalità e le modalità dei relativi trattamenti di dati personali.",
  "15": "I Trattamenti effettuati da parte di un Responsabile sono disciplinati da un contratto o da altro atto giuridico che vincola il Responsabile del Trattamento al Titolare e che definisce la materia disciplinata, la durata, la natura e la finalità del Trattamento, il tipo di dati personali e le categorie di Interessati, gli obblighi e i diritti del Titolare del Trattamento, nonché tutte le ulteriori istruzioni necessarie ai fini del Trattamento. Il mancato rispetto delle disposizioni contenute in tale atto da parte del Responsabile      costituisce, oltre ad una potenziale violazione del GDPR, un inadempimento degli obblighi contrattuali assunti verso il cliente e, pertanto, comporta il rischio di risarcimento di eventuali danni arrecati al Titolare (cliente) e/o ai soggetti i cui dati si riferiscono.",
  "16": "Qualora un Trattamento debba essere effettuato per conto del Titolare, quest’ultimo ricorre unicamente a      Responsabili del Trattamento che presentino garanzie sufficienti per mettere in atto misure tecniche e organizzative adeguate a garantire la tutela dei diritti dell’Interessato. I trattamenti effettuati da parte di un Responsabile sono disciplinati da un contratto o da altro atto giuridico (c.d. “atto di nomina ai sensi dell’articolo 28, GDPR”) che vincola il Responsabile del Trattamento al Titolare e che contiene tutte le istruzioni necessarie ai fini del Trattamento, cui il Responsabile deve scrupolosamente attenersi.",
  "17": "Ogni Titolare del Trattamento ha l’obbligo di tenere un Registro delle attività di Trattamento svolte sotto la propria responsabilità. Parallelamente ogni Responsabile deve tenere un Registro di tutte le categorie di attività relative al Trattamento svolte per conto di uno o più Titolari (soggetto/i che ha/hanno provveduto a nominare il Responsabile).",
  "18": "Il GDPR, rispetto alla   previgente normativa, ha inasprito l’impianto sanzionatorio, prevedendo due livelli di sanzioni amministrative: nel primo gruppo rientrano le violazioni cosiddette di “minore gravità”, per le quali sono previste sanzioni pecuniarie di  importi fino a 10 milioni di euro o, per le imprese, fino al 2% del fatturato globale totale annuo; il secondo gruppo di sanzioni, di ammontare più elevato in considerazione della maggiore gravità delle fattispecie a cui sono ricondotte, ammontano fino a 20 milioni di euro o, per le imprese, fino al 4% del fatturato mondiale totale annuo. Tali sanzioni sono inflitte dall’Autorità di vigilanza in ragione, inter alia, della natura, della gravità e della durata della violazione.\nLa normativa italiana prevede anche disposizioni relative a sanzioni penali, che possono essere inflitte direttamente all’autore di una violazione della normativa sul Trattamento dei dati personali.",
  "19": "Un “Data Breach” o “violazione di dati personali” si verifica ogniqualvolta, accidentalmente o volontariamente, vi è la distruzione, la perdita, la modifica, la divulgazione non autorizzata o l’accesso ai dati personali trasmessi, conservati o comunque trattati. Tenuto conto dell’ampia portata della definizione di data breach, le violazioni di dati personali più frequenti sono: il furto del pc o di dispositivi informatici/cartacei contenenti dati personali; l’impossibilità di accedere ai dati per cause accidentali o per attacchi esterni, virus, malware, ecc.; la perdita o la distruzione di dati personali a causa di incidenti, eventi avversi, incendi o altre calamità; la divulgazione non autorizzata dei dati personali.",
  "20": "Oltre alle figure del Titolare e del Responsabile del Trattamento, vi è un terzo ruolo, prettamente operativo, che il GDPR individua nella “Persona autorizzata al Trattamento” (o soggetto “Incaricato”). L’Incaricato o Persona autorizzata al Trattamento è il soggetto, persona fisica, che effettua materialmente le operazioni di Trattamento sui dati personali. Tutti i dipendenti e collaboratori di I-law vengono nominati quali persone autorizzate al Trattamento al momento della loro assunzione o avvio del rapporto professionale secondo le disposizioni contenute nell’apposita lettera di nomina sottoposta al “new joiner”. Per quanto riguarda il personale già in forza alla data di efficacia del GDPR (25 maggio 2018), sono state distribuite      apposite lettere di nomina a “Persona autorizzata al Trattamento”.",
  "21":"In conformità ai principi di limitazione e di minimizzazione di cui all’articolo 5, GDPR, devo raccogliere dal cliente/fornitore/altro soggetto terzo unicamente i dati personali che sono effettivamente necessari per poter svolgere l’incarico/ attività di mia competenza. Il cliente/fornitore, in quanto Titolare “primario” dei dati, è il soggetto tenuto a selezionarli e anonimizzarli prima della consegna. Qualora il cliente, per mera comodità operativa, trasmettesse al team di lavoro dati personali ulteriori rispetto a quelli necessari per lo svolgimento delle attività lavorative, occorrerà richiedere al cliente di agire in conformità al principio suindicato.",
  "22": "Quando      i-law opera in qualità di Titolare del Trattamento, una volta terminato l’incarico il team di lavoro deve conservare copia dei dati personali, laddove necessario, esclusivamente su server e cartelle di rete messe a disposizione da      i-law con divieto di creare cartelle di backup o copie personali dei dati trattati. Tale comportamento garantisce infatti la conservazione sicura delle informazioni di natura personale utilizzate durante l’incarico. Qualora invece      i-law operi quale Responsabile del Trattamento, occorre verificare quanto è stato stabilito con il cliente nell’atto di nomina a Responsabile del Trattamento: talvolta, infatti, il cliente potrebbe richiedere al termine dell’incarico la cancellazione o la restituzione di tutti i dati personali acquisiti che dovrà essere specificamente valutata, caso per caso, dal Team Privacy.",
  "23": "L’Incaricato, o Soggetto autorizzato, è la persona fisica che effettua materialmente le operazioni di Trattamento sui dati personali quale, ad esempio, il dipendente nei confronti della società datrice di lavoro/Titolare dei dati personali. Pur non prevedendo espressamente la figura dell'incaricato del Trattamento (presente invece nell’articolo 30, Codice Privacy), il GDPR fa riferimento alle “persone autorizzate al Trattamento dei dati personali sotto l'autorità diretta del Titolare o del Responsabile” (articolo 4, n. 10, GDPR). Il GDPR non prevede l'obbligo di nomina o designazione espressa, ma è fondamentale che il Titolare, o il Responsabile, fornisca ai Soggetti autorizzati specifiche  istruzioni operative (articolo 29, GDPR), compresa l’indicazione  degli obblighi inerenti le misure di sicurezza, e sia resa  loro la necessaria formazione. In      i-law tutti i dipendenti e collaboratori  vengono nominati quali persone autorizzate al Trattamento al momento della loro assunzione o avvio del rapporto professionale secondo le disposizioni contenute nell’apposita lettera di nomina sottoposta al “new joine”r. Per quanto riguarda il personale già in forza alla data di efficacia del GDPR (25 maggio 2018), sono state distribuite      apposite lettere di nomina a “Persona autorizzata al Trattamento”.\nInoltre ciascun dipendente/collaboratore riceve la necessaria formazione (avente natura obbligatoria) in relazione alla normativa in materia di protezione dei dati personali.",
  "24": "La Confidenzialità ha ad oggetto la tutela di dati e informazioni considerate “riservate” riguardanti indifferentemente un soggetto giuridico oppure una persona fisica. Vengono qualificate come “riservate” o  “confidenziali” le informazioni che il proprietario del dato ha interesse a mantenere “private” in quanto la rivelazione non autorizzata potrebbe arrecargli un pregiudizio (es. dati contabili, informazioni su scelte strategiche, know-how, operazioni relative ad una società, ecc.). Non esiste una normativa specifica che disciplini in maniera organica la gestione delle informazioni confidenziali, che avviene su base prevalentemente contrattuale (in aggiunta a norme professionali, deontologiche, disposizioni del codice civile e penale). La data protection, invece, tutela i dati personali riguardanti esclusivamente persone fisiche ed è disciplinata da leggi locali e Regolamenti sovranazionali (in Europa, il GDPR), oltre che da accordi specifici con Paesi non appartenenti all’Unione Europea. L’Information Security      raccoglie l’insieme di processi aziendali e attività finalizzati a prevenire e contrastare le minacce a tutte le informazioni contenute su supporti digitali e non digitali.",
  "25": "In base alla normativa vigente e alle      procedure           di I-law,      ogniqualvolta si ha      notizia, evidenza o sospetto che sia avvenuto o possa essersi verificato un “Data Breach”, occorre       contattare tempestivamente il Team Privacy che valuterà se ritiene       necessario      coinvolgere      anche      il DPO. Tali comunicazioni devono avvenire dunque anche in presenza di un “Data Breach” meramente potenziale, incluso il caso in cui il dato personale è stato anonimizzato.",
  "26": "Il dato personale non consiste solo nel nome o cognome di un individuo, ma può essere costituito anche da ogni altra informazione che lo identifica o lo  rende identificabile. Se dunque i dati indicati nel quesito consentono di risalire univocamente all’identità di una persona fisica avente le caratteristiche descritte dai dati (ad esempio: unico soggetto con qualifica di manager, di 35 anni, di sesso femminile, con sede lavorativa a Milano, appartenente ad una specifica Unità Organizzativa di una società, di cui è nota la denominazione e che ha un solo individuo avente tali caratteristiche) siamo in presenza di dati di natura personale.",
  "27": "I dati personali possono essere trattati unicamente in presenza di una delle specifiche condizioni (denominate “basi giuridiche”) previste dal GDPR. Le basi giuridiche più ricorrentemente usate dai  professionisti di I-law      sono rappresentate  dalla necessità di dare esecuzione a un contratto di cui l’Interessato è parte o è comunque coinvolto (esempio: debitore      di una società cliente/mandante), oppure un obbligo giuridico per ottemperare il quale è necessario trattare i dati personali (esempio: compliance antiriciclaggio).",
  "28": "Ai sensi delle      Procedure     di I-law, il PC è uno strumento “aziendale” di cui ogni utente è responsabile. Anche in considerazione del fatto che i PC sono collegati alla rete di i-law     , l’uso di supporti esterni per la memorizzazione dei dati potrebbe essere fonte di rischio per la sicurezza del patrimonio informativo dello Studio     . L’utente è pertanto tenuto a utilizzare esclusivamente unità esterne fornite da I-law per la memorizzazione di dati aziendali.\nNon è consentito collegare hardware ed altri apparati periferici personali (PC, chiavi USB, hard disk esterni, CD/DVD, etc.) per memorizzare e trattare dati dello Studio     , né collegare i dispositivi informatici di       i-law alla rete di terzi (anche se clienti) senza aver preventivamente accertato che le adeguate misure di sicurezza (antivirus, firewall, etc) siano state attivate e aggiornate.",
  "29": "Il principio “clean-desk” prevede che le aree di lavoro (uffici chiusi e relative scrivanie, open space, aree comuni, come pure ogni altro luogo in cui viene svolto il proprio lavoro, inclusa la sede del cliente o altro luogo idoneo allo svolgimento dell’attività lavorativa, anche in modalità smart working) devono essere costantemente riordinate e sgomberate da documenti riservati e dai relativi supporti elettronici che li contengono (es., PC, smartphone). In particolare, quando non più necessaria e, in ogni caso, a fine giornata, la documentazione utilizzata per l’attività lavorativa deve essere riposta negli appositi alloggiamenti sicuri (armadi, cassettiere), oppure deve essere eliminata in maniera definitiva.",
  "30": "L’art. 9, GDPR, definisce i dati particolari come quei dati che rivelino l’origine razziale o etnica, le opinioni politiche, le convinzioni religiose o filosofiche, o l’appartenenza sindacale, nonché i      dati genetici, i dati biometrici intesi a identificare in modo univoco una persona fisica, i dati relativi alla salute o alla vita sessuale o all’orientamento sessuale della persona. L’immagine non è invece un dato particolare",
  "31": "Ai sensi dell’art. 30, GDPR, il titolare (e il responsabile) del trattamento  riporta       all’interno del registro le attività di trattamento svolte sotto la propria responsabilità unitamente a una pluralità di informazioni stabilite dalla stessa norma",
  "32": "Secondo quanto stabilito dalla legge, Il responsabile deve essere designato con apposito atto di nomina ai sensi dell’articolo       28, GDPR",
  "33": "L’articolo      13, GDPR, richiede      al titolare di fornire l’informativa all’interessato nel momento in cui i dati personali sono ottenuti",
  "34": "Il GDPR riconosce espressamente  agli interessati il diritto di ottenere la rettifica dei propri dati personali a cura del Titolare del trattamento senza ingiustificato ritardo",
  "35": "L’articolo 20, GDPR,       GDPR, riconosce agli interessati il diritto a ricevere in un formato strutturato, di uso comune e leggibile da dispositivo automatico i dati personali che lo riguardano forniti a un titolare del trattamento",
  "36": "Il principio di privacy by design impone al titolare di osservare le previsioni dettate dal GDPR sin dal momento della progettazione dei sistemi mediante cui il trattamento verrà posto in essere",
  "37": "Un data breach è un incidente/evento che      comporta una compromissione (perdita, distruzione, indisponibilità, alterazione, etc.) dei dati personali trattati in qualsiasi formato (digitale o cartaceo)",
  }



def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            #del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True , st.session_state["username"]


A=[1,3,8,11,12,13,14,15,17,23,24,26,30,31,32,34,35]
B=[2,4,6,9,10,20,21,22,27,28,29,36]
C=[5,7,18,19,25,37,16,33]
#if "t0" not in st.session_state:
#    st.session_state["t0"] = time.time()
if "st" not in st.session_state:
    st.session_state["st"]= True
if "usercheck" not in st.session_state:
    st.session_state['usercheck']=False
if "rn" not in st.session_state:
    st.session_state["rn"] = random.sample(A, 4)+random.sample(B, 3)+random.sample(C, 3)
if "submit" not in st.session_state:
    st.session_state["submit"] = False
if "start" not in st.session_state:
    st.session_state["start"] = False
if "confirm" not in st.session_state:
    st.session_state["confirm"] = False
if "n" not in st.session_state:
    st.session_state["n"] = -2
if "dfs" not in st.session_state:
    st.session_state["dfs"]=pd.DataFrame()
if "con" not in st.session_state:
    st.session_state['con']=0
if "Q_n_emty" not in st.session_state:
    st.session_state['Q_n_emty']=0



if 'ch0' not in st.session_state:
    for i in range(0,len(st.session_state["rn"])):
        st.session_state["ch{}".format(i)]=random.sample(choices[str(st.session_state["rn"][i])],k=len(choices[str(st.session_state["rn"][i])]))                  #random.sample(choices[str(st.session_state["rn"][i])],k=len(choices[str(st.session_state["rn"][i])]))
        st.session_state["cho{}".format(i)]=[x[0] for x in st.session_state["ch{}".format(i)]]
        st.session_state["che{}".format(i)]=[x[1] for x in st.session_state["ch{}".format(i)]]


def tim():
    st.session_state["t0"] = time.time()
    return st.session_state["t0"]

@st.cache(allow_output_mutation=True)
def get_data():
    return []

log_e = st.empty()
log_c = log_e.container()
var_e= st.empty()
var_c = var_e.container()


if check_password():
    kos,st.session_state["username"]=check_password()
    DFST=get_data()
    st.session_state["dfs"]=df_user[df_user['User']==st.session_state["username"]][df_user.columns[1:-1]]
    if st.session_state['n']==-2:
        st.session_state['n']=-1



def nnum():
    st.session_state['n']+=1
    st.empty()
    #st.experimental_rerun()

def inf(new,old):
    st.session_state[new]=st.session_state[old]
    st.session_state['con']=1
    st.empty()

def cnf(c):
    if c==1:
        try:
            st.write("")
            sql = """INSERT INTO qst (Username, Nome, Cognome, q1, time1) VALUES ('{}','{}','{}','{}','{}')""".format (st.session_state["dfs"]["User"].iloc[0] ,st.session_state["Nome"] , st.session_state["Cognome"], st.session_state["che0"][st.session_state["cho0"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t0"],2))
        except:
            sql = """INSERT INTO qst (Username, Nome, Cognome, q1, time1) VALUES ('{}','{}','{}','{}','{}')""".format (st.session_state["dfs"]["User"].iloc[0] ,st.session_state["Nome"] , st.session_state["Cognome"], 'F' ,round(time.time()-st.session_state["t0"],2))
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=2
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t1"]=time.time()
        st.empty()
    elif c==2:
        try:
            st.write("")
            #(st.session_state["che1"][st.session_state["cho1"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che1"][st.session_state["cho1"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q2 = '{}',
                                   time2= '{}'
                                   where username='{}';""".format (st.session_state["che1"][st.session_state["cho1"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t1"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q2 = '{}',
                                   time2= '{}'
                                   where username='{}';""".format ('F' ,round(time.time()-st.session_state["t1"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=3
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t2"]=time.time()
        st.empty()
    elif c==3:
        try:
            st.write("")
            #(st.session_state["che2"][st.session_state["cho2"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che2"][st.session_state["cho2"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q3 = '{}',
                                   time3= '{}'
                                   where username='{}';""".format (st.session_state["che2"][st.session_state["cho2"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t2"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q3 = '{}',
                                   time3= '{}'
                                   where username='{}';""".format ('F' ,round(time.time()-st.session_state["t2"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=4
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t3"]=time.time()
        st.empty()
    elif c==4:
        try:
            st.write("")
            #(st.session_state["che3"][st.session_state["cho3"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che3"][st.session_state["cho3"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q4 = '{}',
                                   time4= '{}'
                                   where username='{}';""".format (st.session_state["che3"][st.session_state["cho3"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t3"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q4 = '{}',
                                   time4= '{}'
                                   where username='{}';""".format ('F' ,round(time.time()-st.session_state["t3"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=5
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t4"]=time.time()
        st.empty()
    elif c==5:
        try:
            st.write("")
            #(st.session_state["che4"][st.session_state["cho4"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che4"][st.session_state["cho4"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q5 = '{}',
                                   time5= '{}'
                                   where username='{}';""".format (st.session_state["che4"][st.session_state["cho4"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t4"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q5 = '{}',
                                   time5= '{}'
                                   where username='{}';""".format ('F',round(time.time()-st.session_state["t4"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=6
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t5"]=time.time()
        st.empty()
    elif c==6:
        try:
            st.write("")
            #(st.session_state["che5"][st.session_state["cho5"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che5"][st.session_state["cho5"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q6 = '{}',
                                   time6= '{}'
                                   where username='{}';""".format (st.session_state["che5"][st.session_state["cho5"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t5"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q6 = '{}',
                                   time6= '{}'
                                   where username='{}';""".format ('F' ,round(time.time()-st.session_state["t5"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=7
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t6"]=time.time()
        st.empty()
    elif c==7:
        try:
            st.write("")
            #(st.session_state["che6"][st.session_state["cho6"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che6"][st.session_state["cho6"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q7 = '{}',
                                   time7= '{}'
                                   where username='{}';""".format (st.session_state["che6"][st.session_state["cho6"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t6"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q7 = '{}',
                                   time7= '{}'
                                   where username='{}';""".format ('F' ,round(time.time()-st.session_state["t6"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=8
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t7"]=time.time()
        st.empty()
    elif c==8:
        try:
            st.write("")
            #(st.session_state["che7"][st.session_state["cho7"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che7"][st.session_state["cho7"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q8 = '{}',
                                   time8= '{}'
                                   where username='{}';""".format (st.session_state["che7"][st.session_state["cho7"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t7"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q8 = '{}',
                                   time8= '{}'
                                   where username='{}';""".format ('F' ,round(time.time()-st.session_state["t7"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=9
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t8"]=time.time()
        st.empty()
    elif c==9:
        try:
            st.write("")
            #(st.session_state["che8"][st.session_state["cho8"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che8"][st.session_state["cho8"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q9 = '{}',
                                   time9= '{}'
                                   where username='{}';""".format (st.session_state["che8"][st.session_state["cho8"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t8"],2),st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q9 = '{}',
                                   time9= '{}'
                                   where username='{}';""".format ('F',round(time.time()-st.session_state["t8"],2),st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=10
        st.session_state['con']=0
        st.session_state['Q_n_emty']=0
        st.session_state["t9"]=time.time()
        st.empty()
    elif c==10:
        try:
            st.write("")
            #(st.session_state["che9"][st.session_state["cho9"].index(st.session_state["Q_n"])]=='F') or (st.session_state["che9"][st.session_state["cho9"].index(st.session_state["Q_n"])]=='T')
            sql = """update qst set q10 = '{}',
                                   time10= '{}',
                                   time='{}'
                                   where username='{}';""".format (st.session_state["che9"][st.session_state["cho9"].index(st.session_state["Q_n"])] ,round(time.time()-st.session_state["t9"],2), round(time.time()-st.session_state["t0"],2) ,st.session_state["dfs"]["User"].iloc[0])
        except:
            sql = """update qst set q10 = '{}',
                                   time10= '{}',
                                   time='{}'
                                   where username='{}';""".format ('F' ,round(time.time()-st.session_state["t9"],2), round(time.time()-st.session_state["t0"],2) ,st.session_state["dfs"]["User"].iloc[0])
        cursor = conn.cursor()
        cursor.execute(sql)
        st.session_state['n']=11
        st.empty()


t_qu=120
#########
if st.session_state['n']==-1:
    with log_c:
        st.image(
            #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
            "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
            width=50,
        )
        st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
        st.write(st.session_state["dfs"])
        st.image("pic2.png",width=400)
        with var_c:
            st.markdown(f"##### Benvenuto a Bordo Gentile :violet[**{st.session_state['username']}**] 🚀")#.format(st.session_state["username"]))
            st.markdown(f"##### Controlla lo stato del tuo esame per favore")
            if st.button("check"):
                if st.session_state["username"] in df['Username'].to_list():
                    st.session_state['usercheck']=False
                    st.write('l\'esame gia registrato 😊.')
                elif st.session_state["username"] not in st.secrets['passwords'].keys():
                    st.write('😕 User not known')
                elif st.session_state["username"] in ds['User_In'].to_list():
                    st.session_state['usercheck']=False
                    st.write('Mi dispiace ma ha fallito! 😞 L\'esame non doveva essere interrotto!')
                else:
                    st.write('L\'esame inizia ora, ricorda che hai 2 minuti per ogni domanda.')
                    st.write('prepara il tuo tempo')
                    st.session_state['usercheck']=True
                    st.session_state['st']=True
                    st.session_state['n']=0
                    st.session_state["t0"]=tim()
                    sql = """INSERT INTO signin (User_In) VALUES ('{}')""".format (st.session_state["username"])
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    with st.spinner('Wait for it...'):
                        time.sleep(5)
                    st.experimental_rerun()

if st.session_state['usercheck']==True:
    if st.session_state["st"]==True:
        if st.session_state['n']==0:
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                st.session_state['Nome'] = st.text_input("Nome:")
                st.session_state['Cognome'] = st.text_input("Cognome:")
                st.info('Premi start da iniziare il tuo 1 ora')
                st.button('start',on_click=nnum)
                    #st.session_state['start']=not st.session_state['start']
                    #st.session_state['n']=1
                    #st.experimental_rerun()
        elif (st.session_state['n']==1) and (st.session_state['con']==0):
            #temp=slate.container()
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[1)]:green[{}]**".format(questions[str(st.session_state["rn"][0])]),st.session_state["cho0"],horizontal=False,key='Qa')
                #Qa=st.session_state['Qa']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qa'))
                #Qa=st.radio("**:red[1)]:green[{}]**".format(questions[str(st.session_state["rn"][0])]),st.session_state["cho0"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([1]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==1) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][0])])
                elif st.session_state["che0"][st.session_state["cho0"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che0"][st.session_state["cho0"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][0])])
                st.button('next',on_click=cnf,args=([1]))
        elif (st.session_state['n']==2) and (st.session_state['con']==0):
            #st.empty()
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[2)]:green[{}]**".format(questions[str(st.session_state["rn"][1])]),st.session_state["cho1"],horizontal=False,key='Qb')
                #Qb=st.session_state['Qb']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qb'))
                #Qb=st.radio("**:red[2)]:green[{}]**".format(questions[str(st.session_state["rn"][1])]),st.session_state["cho1"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([2]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==2) and (st.session_state['con']==1):
            #st.empty()
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][1])])
                elif st.session_state["che1"][st.session_state["cho1"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che1"][st.session_state["cho1"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][1])])
                st.button('next',on_click=cnf,args=([2]))
        elif (st.session_state['n']==3) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[3)]:green[{}]**".format(questions[str(st.session_state["rn"][2])]),st.session_state["cho2"],horizontal=False,key='Qc')
                #Qc=st.session_state['Qc']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qc'))
                #Qc=st.radio()
                #st.button("Confirm",on_click=cnf,args=([3]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==3) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][2])])
                elif st.session_state["che2"][st.session_state["cho2"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che2"][st.session_state["cho2"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][2])])
                st.button('next',on_click=cnf,args=([3]))
        elif (st.session_state['n']==4) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[4)]:green[{}]**".format(questions[str(st.session_state["rn"][3])]),st.session_state["cho3"],horizontal=False,key='Qd')
                #Qd=st.session_state['Qd']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qd'))
                #Qd=st.radio("**:red[4)]:green[{}]**".format(questions[str(st.session_state["rn"][3])]),st.session_state["cho3"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([4]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==4) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][3])])
                elif st.session_state["che3"][st.session_state["cho3"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che3"][st.session_state["cho3"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][3])])
                st.button('next',on_click=cnf,args=([4]))
        elif (st.session_state['n']==5) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[5)]:green[{}]**".format(questions[str(st.session_state["rn"][4])]),st.session_state["cho4"],horizontal=False,key='Qe')
                #Qe=st.session_state['Qe']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qe'))
                #Qe=st.radio("**:red[5)]:green[{}]**".format(questions[str(st.session_state["rn"][4])]),st.session_state["cho4"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([5]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==5) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][4])])
                elif st.session_state["che4"][st.session_state["cho4"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che4"][st.session_state["cho4"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][4])])
                st.button('next',on_click=cnf,args=([5]))
        elif (st.session_state['n']==6) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[6)]:green[{}]**".format(questions[str(st.session_state["rn"][5])]),st.session_state["cho5"],horizontal=False,key='Qf')
                #Qf=st.session_state['Qf']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qf'))
                #Qf=st.radio("**:red[6)]:green[{}]**".format(questions[str(st.session_state["rn"][5])]),st.session_state["cho5"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([6]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==6) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][5])])
                elif st.session_state["che5"][st.session_state["cho5"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che5"][st.session_state["cho5"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][5])])
                st.button('next',on_click=cnf,args=([6]))
        elif (st.session_state['n']==7) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[7)]:green[{}]**".format(questions[str(st.session_state["rn"][6])]),st.session_state["cho6"],horizontal=False,key='Qg')
                #Qg=st.session_state['Qg']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qg'))
                #Qg=st.radio("**:red[7)]:green[{}]**".format(questions[str(st.session_state["rn"][6])]),st.session_state["cho6"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([7]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==7) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][6])])
                elif st.session_state["che6"][st.session_state["cho6"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che6"][st.session_state["cho6"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][6])])
                st.button('next',on_click=cnf,args=([7]))
        elif (st.session_state['n']==8) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[8)]:green[{}]**".format(questions[str(st.session_state["rn"][7])]),st.session_state["cho7"],horizontal=False,key='Qh')
                #Qh=st.session_state['Qh']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qh'))
                #Qh=st.radio("**:red[8)]:green[{}]**".format(questions[str(st.session_state["rn"][7])]),st.session_state["cho7"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([8]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==8) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][7])])
                elif st.session_state["che7"][st.session_state["cho7"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che7"][st.session_state["cho7"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][7])])
                st.button('next',on_click=cnf,args=([8]))
        elif (st.session_state['n']==9) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[9)]:green[{}]**".format(questions[str(st.session_state["rn"][8])]),st.session_state["cho8"],horizontal=False,key='Qi')
                #Qi=st.session_state['Qi']
                form.form_submit_button('Confirm', on_click=inf,args=('Q_n','Qi'))
                #Qi=st.radio("**:red[9)]:green[{}]**".format(questions[str(st.session_state["rn"][8])]),st.session_state["cho8"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([9]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==9) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][8])])
                elif st.session_state["che8"][st.session_state["cho8"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che8"][st.session_state["cho8"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][8])])
                st.button('next',on_click=cnf,args=([9]))
        elif (st.session_state['n']==10) and (st.session_state['con']==0):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                form = st.form('Question')
                form.radio("**:red[10)]:green[{}]**".format(questions[str(st.session_state["rn"][9])]),st.session_state["cho9"],horizontal=False,key='Qj')
                #Qj=st.session_state['Qj']
                form.form_submit_button('Confirm',  on_click=inf,args=('Q_n','Qj'))
                #Qj=st.radio("**:red[10)]:green[{}]**".format(questions[str(st.session_state["rn"][9])]),st.session_state["cho9"],horizontal=False)
                #st.button("Confirm",on_click=cnf,args=([10]))
                countdown = st.empty()
                for i in range(t_qu,-1,-1):
                    mm, ss = i//60, i%60
                    countdown.metric("Time",f' {mm:02d}:{ss:02d} ⏳')
                    time.sleep(1)
                    if (mm==0) and (ss==0):
                        st.session_state['con']=1
                        st.session_state['Q_n_emty']=1
                        st.experimental_rerun()
                countdown.empty()
        elif (st.session_state['n']==10) and (st.session_state['con']==1):
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                if st.session_state['Q_n_emty']==1:
                    st.warning('time up!! Leggi lo spiegazione')
                    st.info(explan[str(st.session_state["rn"][9])])
                elif st.session_state["che9"][st.session_state["cho9"].index(st.session_state['Q_n'])]=='T':
                    st.success('Bravo la risposta era giusta')
                elif st.session_state["che9"][st.session_state["cho9"].index(st.session_state['Q_n'])]=='F':
                    st.error('Ha sbagliato. Leggi lo spiegazione. Lo spiegazione sparisce se stessa tra un po')
                    st.info(explan[str(st.session_state["rn"][9])])
                st.button('next',on_click=cnf,args=([10]))
        elif st.session_state['n']==11:
            with log_c:
                st.image(
                    #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                    "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                    width=50,
                )
                st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
                st.write(st.session_state["dfs"])
                st.image("pic2.png",width=400)
                st.title('la sua esame è finito 😊.')
                st.title("Grazie per la collaborazione! 😍")
                with st.spinner('Attendere prego! evaluiamo lo stato della tua esame'):
                    time.sleep(5)
                st.session_state['error']=0
                for i in ['q1','q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']:
                    if df[df['Username']==st.session_state["dfs"]['User'].iloc[0]][i].iloc[0]=='F':
                        st.session_state['error']+=1
                if st.session_state['error']<=3:
                    st.success(f"##### Congrats, Hai superato!")
                    st.balloons()
                else:
                    st.error(f"##### Riprova esame dopo un paio di giorni!")
                st.session_state["st"]=False
    else:
        with log_c:
            st.image(
                #"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
                "https://media-exp1.licdn.com/dms/image/C560BAQE17_4itIWOLw/company-logo_200_200/0/1570546904891?e=2147483647&v=beta&t=w-App-ZgjSHDlEDDFQeNB7XU2L7QgY2EF-vFj2Il8q8",
                width=50,
            )
            st.markdown(f"## 🔒 :red[Privacy] :blue[Course **Questionnaire**.] 📚💻")
            st.write(st.session_state["dfs"])
            st.image("pic2.png",width=400)
            st.title('l\'esame gia registrato 😊.')
