# **Logo Similarity Project**

## **Descriere**
Acest proiect are ca scop gruparea site-urilor pe baza similarității logo-urilor lor. Folosind tehnici de web scraping, procesare de imagini și algoritmi de clustering, am dezvoltat o soluție care extrage logo-urile de pe site-uri, le procesează și le grupează în funcție de caracteristicile lor vizuale.

---

## **Cum Funcționează?**

### **1. Web Scraping pentru Extragerea Logo-urilor**
- Am folosit **Selenium** pentru a naviga pe site-uri și a extrage URL-urile logo-urilor.
- Am identificat logo-urile folosind XPath, căutând elemente `<img>` cu clase sau atribute specifice (ex: `class="logo"`, `alt="logo"`).
- Am descărcat logo-urile local folosind `requests` și `PIL`.

### **2. Procesarea Logo-urilor**
- Am redimensionat logo-urile la o dimensiune standard (128x128 px) folosind **OpenCV**.
- Am convertit imaginile în grayscale pentru a uniformiza culorile.
- Am aplicat thresholding pentru a elimina fundalul și a izola logo-ul.

### **3. Extragerea Caracteristicilor**
- Am folosit algoritmul **ORB** (Oriented FAST and Rotated BRIEF) pentru a extrage caracteristici vizuale din logo-uri.
- ORB detectează puncte cheie (keypoints) și calculează descriptorii acestora, care sunt folosiți pentru a compara logo-urile.

### **4. Clustering**
- Am calculat o matrice de similaritate între descriptorii logo-urilor folosind **Brute-Force Matching**.
- Am aplicat algoritmul **Agglomerative Clustering** pentru a grupa logo-urile în funcție de similaritatea lor.
- Am salvat grupurile într-un fișier JSON (`grouped_logos.json`).

---

## **Decizii de Design**

### **De ce Selenium?**
- Am ales **Selenium** pentru că oferă o modalitate robustă de a naviga pe site-uri dinamice și de a extrage elemente din HTML.
- Alternativa ar fi fost să folosesc **BeautifulSoup**, dar Selenium este mai potrivit pentru site-uri care folosesc JavaScript pentru a încărca logo-urile.

### **De ce ORB?**
- **ORB** este un algoritm rapid și eficient pentru detectarea caracteristicilor vizuale.
- Alternativa ar fi fost să folosesc **SIFT** sau **SURF**, dar ORB este mai rapid și nu necesită licențiere.

### **De ce Agglomerative Clustering?**
- **Agglomerative Clustering** este un algoritm ierarhic care permite gruparea datelor fără a fi necesar să specificăm un număr fix de clustere.
- Alternativa ar fi fost să folosesc **KMeans**, dar Agglomerative Clustering oferă mai multă flexibilitate în identificarea grupurilor naturale.

---

## **Cum S-a Desfășurat Procesul de Analiză?**

### **1. Identificarea Problemelor**
- Cum să extrag logo-urile de pe site-uri ?
- Cum să procesez logo-urile pentru a le face comparabile?
- Cum să măsor similaritatea dintre logo-uri?
- Cum să grupez logo-urile în funcție de similaritate?

### **2. Explorarea Soluțiilor**
- Am testat mai multe abordări pentru extragerea logo-urilor, inclusiv parsarea HTML și detectarea elementelor `<img>`.
- Am experimentat cu diferiti algoritmi de procesare a imaginilor (ex: redimensionare, grayscale, thresholding).
- Am comparat ORB cu alți algoritmi de extragere a caracteristicilor (ex: SIFT, SURF) și am ales ORB pentru viteza sa.
- Am testat mai mulți algoritmi de clustering (ex: KMeans, DBSCAN) și am ales Agglomerative Clustering pentru flexibilitatea sa.

### **3. Îmbunătățirea Soluției**
- Am ajustat parametrii algoritmilor pentru a obține rezultate mai bune (ex: numărul de clustere, pragul de similaritate).
- Am adăugat verificări suplimentare pentru a gestiona cazurile de eroare (ex: site-uri inaccesibile, logo-uri lipsă).

---

## **Rezultate**

### **1. Gruparea Logo-urilor**
- Am obținut mai multe grupuri de logo-uri similare, salvate în fișierul `grouped_logos.json`.
- Exemplu de grup:
  ```json
  {
      "0": [
          "https://mazda-autohaus-hellwig-hoyerswerda.de",
          "https://kia-moeller-wunstorf.de"
      ],
      "1": [
          "https://toyota-buchreiter-eisenstadt.at"
      ]
  }