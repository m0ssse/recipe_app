# Reseptisovellus

Sovelluksella käyttäjät voivat jakaa reseptejä, sekä arvostella niitä
## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään (TEHTY)
* Käyttäjä pystyy lisäämään reseptejä sekä muokkaamaan ja poistamaan lisäämiään reseptejä. Jokaisessa reseptissä lukee tarvittavat ainekset sekä valmistusohje (TEHTY)
* Käyttäjällä on käyttäjäsivu, joka näyttää kuinka monta reseptiä käyttäjä on lisännyt sekä listan käyttäjän lisäämistä resepteistä (TEHTY)
* Käyttäjä voi jättää muiden käyttäjien lisäämistä resepteistä arvosteluja, jotka sisältävät arvosanan ja kommentin. (TEHTY)
* Käyttäjä voi tarkastella kaikkia sovellukseen lisättyjä reseptejä. Jokaisesta reseptistä näytetään arvostelujen määrä sekä arvosanojen keskiarvo. Jokaisesta reseptistä on lisäksi oma sivunsa, jossa näkyvät kaikki kyseisen reseptin saamat arvostelut. (TEHTY)
* Käyttäjä pystyy etsimään reseptejä hakusanalla (TEHTY)
* Käyttäjä pystyy lisäämään resepteille luokitteluja (jälkiruoka, kasvisruoka, yms.) sekä näyttämään reseptin luokittelut (TEHTY)
  
## Sovelluksen asennus

Asenna ```flask```-kirjasto

```$ pip install flask```

Luo tietokantaan taulut

```$ sqlite3 database.db < schema.sql```

Lisää tietokantaan tunnisteet komennolla

```$ sqlite3 database.db < init.sql```

Voit käynnistää sovelluksen komennolla

```$ flask run```

Mikäli haluat luoda testidataa tietokantaan, voit suorittaa skriptin ```create_dummy_data.py```, joka luo tietokantaan skriptissä määritellyn määrän käyttäjiä ja arvostelijoita, skriptissä määritellyn määrän reseptejä sekä skriptissä määritellyn määrän arvosteluja. Huomaa, että skriptin ajaminen poistaa tietokannasta sinne aiemmin lisätyt käyttäjät ja reseptit. Skripti suoritetaan komennolla ```$ python3 create_dummy_data.py```

## Testi suurella datamäärällä

Sovellusta testattiin suurella datamäärällä skriptin ```create_dummy_data.py```. Testejä tehtiin kaiken kaikkiaan kuusi kappaletta, tietokantaan lisättiin joko `10**5`, `*10**6` tai `10**7` arvostelua satunnaisille resepteille. Kaikki kolme testiä tehtiin ilman indeksiä ja indeksin kanssa. Yksittäisessä testissä tehtiin 10 pyyntöä sivulle `"http://127.0.0.1:5000/recipe/1"` ja mitattiin näihin kuluva aika. Tulokset on esitetty alla. Ajat on ilmoitettu sekunteina:

| reviews | no index | with index |
| --------| -------- | ---------- |
| 10000   | 0.142    | 0.089      |
| 100000  | 0.733    | 0.190      |
| 1000000 | 6.668    | 1.693      |
