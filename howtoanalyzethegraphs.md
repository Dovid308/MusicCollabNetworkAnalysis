- Questo era letteralemente quello che avevo fatto per la presentazione 1
  collapsed:: true
	- # The Influence of Major Labels on Artist Collaborations
	- The goal of this project is to build a **collaboration network** using **labels** to analyze if major record companies (Universal, Sony, Warner) influence collaborations in the music industry.
	- ##  Graph Structure:
		- **Nodes**: **Artists**
		  Each **artist** is represented as a node in the graph.
		- **Edges**: **Collaborations****
		  Collaboration Type**: Focus on **featuring** artists
		- **Node Attributes**:**
		  Label**: The label associated with the artist’s **latest album**.**
	- ## 📁 Data Sources:
	  Spotify API
	  
	  We need to understand what type of data we could download, for example i don't know how much possible it could be do the same for the past years really, considered the logic behind the extraction of the feat from the last relaased album.
	- Small problem to address
		- The structure of the labels divided in major minor and stuff.
		  We need to recconnect the minor to the major label.
		- ![image.png](../assets/image_1744669443063_0.png)
		- ![image.png](../assets/image_1744666976426_0.png)
	- ### Key Questions:**
		- Collaboration Clusters**: Do artists collaborate mostly **within their own label**? How do collaborations form between different labels?**
		  Homophily**: Are **independent artists** isolated from major labels, or do they collaborate with major-label artists?**
		  Temporal Comparison**: How have collaboration patterns changed over time?**
		  Geograpichal Comparison:** How they change bases on the market?
-
- [[Apr 28th, 2025]]
- Questo sarebbe da ripetere per tutti i grafi che vogliamo analizzare. Io nel farlo ho pensato a quello con genere come attributo.
- Che poi a questo punto forse eliminerei l'idea di filtrare per genere e quindi avere i grafi con attributo label divisi per genere (dobbiamo capire se ha senso, chiederei anche questo quasi quasi)
- ## Come gestire i nodi di genere other/unknown
	- ### 1.  **Trattare "Other" come un genere normale**
		- Consideri "Other" come un'etichetta normale (tipo Rock, Pop, Other).
		  
		  ✅ Facile.
		  
		  🚫 Però rischi che "Other" distorca il valore medio, perché di solito non ha un pattern di collaborazione chiaro.
		  
		  ---
	- ### 2.  **Rimuovere "Other" dai calcoli di omofilia**
		- Quando fai l'analisi, **escludi** tutti i nodi che hanno il genere "Other" o "Unknown".
		- ✅ Più pulito: misuri veramente l'omofilia tra generi reali.
		  
		  🚫 Perdi un po' di nodi (dipende quanto pesano).
		  
		  **In pratica:** prima del calcolo, filtri via i nodi "Other".
		- IO sarei per il secondo sinc.
	-
- ## Parte 1 Metriche base e null model
	- Questi sono per il grafo nell'interezza
		- **EI Index** -> poco parlante, uno per classe (credo).
  		- **Blau's Heterogeneity Index** measures the diversity in the neighborhood of a node
		- **Homophily Ratio**
		  è la percentuale di archi che collegano due nodi dello stesso genere, diviso per tutti gli archi.
		- **Mixing Matrix**
		  → è una matrice (genere × genere) che conta le connessioni tra generi.
		- > questi sono solo numerici, non comprendono devono essere confrontati con null model.
  ### Null Model based metrics
  - **Modularity (Q)**: is a measure of how well a network is divided into **communities** (or modules). It compares the **actual density of links within communities** to the **expected density of links** if the network were random.
  - **Attribute Assortativity Coefficient**
  	It is based on Modularity.
	     → misura globale quanto il grafo è assortativo rispetto a un attributo (es: `genre`).
		  (Valori da -1 a +1) ->
			- A quanto ho capito ci sono vari modi di calcolare questa quantità, ~va capito bene quale usare.
			- O se bisogna usare dei Null Model che dobbiamo creare di base noi e poi performare delle operazioni oppure no, forse lo chiederei anche ai prof oggi.
			- TODO vedere meglio questa parte.~ Si è basato su Null Model
# Null Model -> giusto per ricordarmi
##   **1:Configuration Model (Mantenere Gradi)**
- **Cosa fai**: crei un grafo nuovo random mantenendo il **grado di ogni nodo** (quanti archi ha) ma rimescolando i collegamenti.
- **A cosa serve**: capire se la struttura di grado (es: artisti molto popolari) genera omofilia artificiale.
  
  ✅ Utile se il tuo grafo ha nodi molto hub o squilibrati.
  
## **2 :Attribute Shuffling (Attribute Randomization)**
- **Cosa fai**: tieni fisso il grafo (stessa rete), ma rimescoli gli attributi sui nodi (nel tuo caso i "generi musicali").
- **A cosa serve**: capire se l'omofilia è dovuta agli attributi o è casuale rispetto alla struttura di collaborazione reale.
  
  ✅ Molto usato per studiare omofilia.
  
  ✅ Facile e veloce.
	- > anche qui sarebbe da capire se lo hanno mai presentato nel corso e con quale nome
   
   **S:** forse lo ha accettato a voce, non ce l'ho negli appunti.

## **3: Erdős–Rényi Model (G(n,p))**
- **Cosa fai**: crei un grafo completamente casuale, ogni coppia di nodi ha una probabilità p di essere collegata.
- **A cosa serve**: baseline completamente random (nessuna struttura locale o di grado).
  
  🚫 NON è perfetto per reti reali tipo social/music network: troppo semplice.

## Mechanistic Model
They have a **strong causal logic**: they follow **explicit rules** on _how_ connections are formed.
- > 🛠 Quando usare il **Barabási–Albert** model come null model?
  Non è proprio un "null model classico" per testare l'omofilia, **ma** puoi usarlo:
  **Se vuoi simulare una rete con proprietà simili a reti reali** (molti hub, pochi nodi isolati).
  **Se vuoi vedere se la sola struttura di rete "naturale" (senza omofilia a priori)** produce assortatività o no.
  **Ma attenzione:**
  **Il BA Model non conserva il tuo grafo reale** (né i generi né le collaborazioni vere).
  **Crea un grafo da zero**, che può avere **molto meno clustering** o **community structure** rispetto alla tua rete vera.

# Parte 2 - Comunity Detenction
- Nelle note di comunity detenction vengono presentati due metodi per clusterare il grafo
	- ### 1.  **Girvan–Newman (Edge Betweenness)**
		- Divisive: removes high-betweenness edges to break apart the graph.
		- Outputs a **dendrogram**.
		- You **must choose** where to cut (i.e., the number of communities kkk) to get a final partition.
	- ### 2.  **Louvain**
		- Greedy optimization of **modularity**.
		- No need to specify k — the algorithm **automatically finds** the number of communities that best maximize modularity.
		  
		  >So: **Use Louvain** unless you have a good reason to control k manually.
	- Hai due clusterizzazioni:
		- Una **"reale"** basata su attributi (es. `genre` o altra label).
		- Una **"strutturale"** ottenuta da Louvain.
	- Dobbiamo confrontarle tra loro:
		- ## a.  **Normalized Mutual Information (NMI)**  o  **Adjusted Rand Index (ARI)**
		  
		  Ti dicono **quanto la partizione trovata somiglia a quella attesa (basata sull'attributo)**.
		  
		  > Se `genre` rappresenta gruppi "naturali", ci aspettiamo che il clustering Louvain somigli a questa divisione. Se sono molto diversi → le connessioni non riflettono bene quell'attributo.
		- ## b. Modularità dei cluster
			- ### 🔍 1.  **Modularità della partizione reale (es. `genre`)**
				- Usi il tuo grafo `g` e come `membership_vector` passi il vettore che dice a quale "genere" appartiene ogni nodo.
				- Questo ti dice:
				  
				  → “Se considero i generi come comunità, quanto bene sono separati tra loro nel grafo?”
				  
				  > 💡 Se ottieni una modularità **alta**, significa che i nodi dello stesso genere tendono effettivamente a connettersi tra loro → il `genre` è strutturalmente significativo.
				  
				  ---
			- ### 🔍 2.  **Modularità della partizione Louvain**
				- Qui calcoli la modularità della partizione trovata automaticamente da Louvain.
				- Serve come **baseline**: Louvain è pensato proprio per massimizzare questa misura.
				  
				  > 💡 Se la partizione basata su `genre` ha una **modularità simile o più alta** di quella di Louvain, vuol dire che l’attributo spiega *molto bene* la struttura.
