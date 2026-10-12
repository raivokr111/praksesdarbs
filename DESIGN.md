**NOSAUKUMS** - Blind Snake, Snake

**MĒRĶIS** - Iegūt pēc iespējas vairāk punktu, ēdot ēdienu un izvairoties no sadursmēm,
lai gan čūska redz tikai nelielu apli ap galvu. Spēlētājs izpēta tumšo karti,
izmanto power-up, lai uz laiku redzētu vairāk, un sacenšas ar citiem globālajā
rezultātu tabulā.

**VADĪBA** - Bultinas = Čūskas virziens, SPACE = jauna spēle pēc Game Over, ESC = Iziet
Čūska nevar apgriezties par 180° (uzreiz pretējā virzienā).

**PAMATA CIKLS** -
1. Nolasa ievadi (taustiņi, loga aizvēršana).
2. Pabīda čūsku vienu rūtiņu virzienā.
3. Pārbauda sadursmes (siena, pati čūska), ēdienu un power-up.
4. Atjauno aktīvo power-up effektu taimerus.
5. Uzzīmē tikai to, kas ir redzamības aplī.
6. Parāda kadru un gaida nākamo.
7. Sākums > Spēle > Game Over > rezultāta nosūtīšana >
rezultātu tabula > jauna spēle.

**MEHĀNIKAS** -
Ierobežota redzamība: redzams tikai aplis ar rādiusu 'VISION' (sākumā 4 rūtiņas), pārējais ir melns.
Ēdiens: parādās nejaušā vietā, bet redzams tikai tuvumā. Apēdot čūska kļūst garāka.
Sadursmes: siena vai pati čūska = Game Over.
Power-up (parādās kartē, jāatrod un jāpaņem): Lukturis (palielina redzamības rādiusu); Radars (parāda visu karti) Slowness (Čūska kustas lēnāk) x2 punkti (ediens dod x2)

**LĪMEŅI** - Līmenis pieaug ik pēc 5 apēstiem ēdieniem:
- ātrums (FPS) nedaudz pieaug,
- pamata redzamības rādiuss samazinās (minimums 2),
- power-up parādās retāk.
Spēle kļūst grūtāka, un power-up kļūst vērtīgāki.

**PUNKTI** - Ēdiens: +10
- Ēdiens ar Dubultpunktiem: +20
- Power-up paņemšana: +5
- Līmeņa bonuss: +level × 10

**SAGLABĀ** - pēc game Over spēle nosūta rezultātu uz serveri
  Globāla tabula: serveri ievieto publiski, un spēle rāda top 10.
- Ja serveris nav pieejams, spēle turpina darboties un rezultātu saglabā
  lokāli (`highscore.txt`).
- Spēlētāja vārds: līdz 20 rakstzīmēm.
