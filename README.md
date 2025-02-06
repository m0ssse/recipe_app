# Reseptisovellus

Sovelluksella käyttäjät voivat jakaa reseptejä, sekä arvostella niitä
## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään (TEHTY)
* Käyttäjä pystyy lisäämään reseptejä sekä muokkaamaan ja poistamaan lisäämiään reseptejä. Jokaisessa reseptissä lukee tarvittavat ainekset sekä valmistusohje (TEHTY)
* Käyttäjällä on käyttäjäsivu, joka näyttää kuinka monta reseptiä käyttäjä on lisännyt sekä listan käyttäjän lisäämistä resepteistä (TEHTY)
* Käyttäjä voi jättää muiden käyttäjien lisäämistä resepteistä arvosteluja, jotka sisältävät arvosanan ja kommentin. (TEHTY)
* Käyttäjä voi tarkastella kaikkia sovellukseen lisättyjä reseptejä. Jokaisesta reseptistä näytetään arvostelujen määrä sekä arvosanojen keskiarvo. Jokaisesta reseptistä on lisäksi oma sivunsa, jossa näkyvät kaikki kyseisen reseptin saamat arvostelut. (TEHTY)
* Käyttäjä pystyy etsimään reseptejä hakusanalla (TEHTY)
* Käyttäjä pystyy lisäämään resepteille luokitteluja (jälkiruoka, kasvisruoka, yms.) sekä etsimään reseptejä luokittelujen perusteella (Luokittelut lisätty, haku pitää vielä toteuttaa)
  
## Sovelluksen asennus

Asenna ```flask```-kirjasto

```$ pip install flask```

Luo tietokantaan taulut

```$ sqlite3 database.db < schema.sql```

Voit käynnistää sovelluksen komennolla

```$ flask run```

## TODO:
* Ominaisuusluottelossa mainitut puuttuvat toiminnot (luokittelut)
* Syötteille kriteerit ja kriteerien validointi
* Sivutus (ainakin reseptin saamille arvosteluille)
* CSS
