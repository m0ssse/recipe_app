# Reseptisovellus

Sovelluksella käyttäjät voivat jakaa reseptejä, sekä arvostella niitä
## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään (TEHTY)
* Käyttäjä pystyy lisäämään reseptejä sekä muokkaamaan ja poistamaan lisäämiään reseptejä. Jokaisessa reseptissä lukee tarvittavat ainekset sekä valmistusohje (TEHTY)
* Käyttäjällä on käyttäjäsivu, joka näyttää kuinka monta reseptiä käyttäjä on lisännyt sekä listan käyttäjän lisäämistä resepteistä (TODO)
* Käyttäjä voi jättää muiden käyttäjien lisäämistä resepteistä arvosteluja, jotka sisältävät arvosanan ja kommentin. (Tehty, mutta tällä hetkellä arvostelut eivät näy vielä missään)
* Käyttäjä voi tarkastella kaikkia sovellukseen lisättyjä reseptejä. Jokaisesta reseptistä näytetään arvosanojen keskiarvo sekä kommentit (Ensimmäinen osa tehty, jälkimmäinen puuttuu)
* Käyttäjä pystyy etsimään reseptejä hakusanalla (TEHTY)
* Käyttäjä pystyy lisäämään resepteille luokitteluja (jälkiruoka, kasvisruoka, yms.) sekä etsimään reseptejä luokittelujen perusteella (TODO)
  
## Sovelluksen asennus

Asenna ´flask´-kirjasto

$ pip install flask

Luo tietokantaan taulut

$ sqlite3 database.db < schema.sql

Voit käynnistää sovelluksen komennolla

$ flask run

TODO:
Ominaisuusluottelossa mainitut puuttuvat toiminnot (arvostelujen näyttäminen, luokittelut)
Tietoturva
Syötteille kriteerit ja kriteerien validointi
CSS
