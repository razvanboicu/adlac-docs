# ADLAC — pagini individuale, meniu lateral si cautare

## Ce include pachetul

- 25 de pagini individuale pentru toate sectiunile din `Section reference` (inclusiv Announcement bar, Slideshow, Newsletter, Product stage, Main product, Header, Footer etc.).
- 15 ghiduri individuale pentru functii precum mega menu, compact dropdown, product tabs, swatches, filtre si cart drawer.
- Grupuri extensibile in meniul din stanga, pe toate paginile ADLAC.
- 40 de rezultate noi in cautare: numele setarilor si blocurilor sunt incluse in cuvintele-cheie.
- Sitemap completat cu paginile noi.

## Publicare sigura — foloseste varianta PATCH

1. Fa un backup al repository-ului documentatiei sau creeaza un commit inainte de aplicare.
2. Descarca si dezarhiveaza acest ZIP intr-un folder separat.
3. Deschide CMD in folderul local al repository-ului GitHub Pages. Trebuie sa vezi acolo folderele `adlac`, `assets` si fisierul `sitemap.xml`.
4. Ruleaza (inlocuieste calea catre folderul dezarhivat):

   `py "D:\\Downloads\\adlac-docs-expansion\\apply_adlac_expansion.py" .`

   Daca ai extras ZIP-ul in alt loc, foloseste acea cale. Ultimul punct (`.`) inseamna repository-ul curent.

5. Verifica fisierele modificate, apoi fa `git add .`, `git commit -m "Expand ADLAC feature documentation"`, `git push` (sau publica prin metoda ta GitHub obisnuita).
6. Dupa publicarea GitHub Pages, foloseste `Ctrl + Shift + R` pentru a forta actualizarea cache-ului.

## Teste dupa publicare

- Deschide `https://docs.boicusolutions.com/adlac/sections/announcement-bar/` — trebuie sa afiseze o pagina dedicata.
- Din meniul stanga deschide **Section guides → Navigation & layout → Announcement bar**.
- Cauta `announcement`, `slideshow`, `swatches`, `variant picker` sau `mega menu`. Rezultatele trebuie sa deschida paginile corecte.
- Verifica meniul pe telefon (butonul `Menu`).
- Deschide `/adlac/support/` si verifica widget-ul Turnstile, fara sa retrimiti un ticket daca nu ai nevoie.
- Deschide `/privacy/` si confirma ca datele operatorului sunt cele completate de tine.

## Important

Acest patch **nu rescrie** formularul de suport, codul Turnstile, pagina Privacy Policy, configuratia Resend sau Worker-ul Cloudflare. Modifica meniul lateral, indexul cautarii, stiluri CSS asociate, sitemap-ul si adauga cele 40 de pagini.

Textele pentru setarile sectiunilor provin din documentatia ADLAC 1.0.0 existenta (`Section reference`), nu dintr-o versiune noua a codului temei. Daca tema a fost schimbata intre timp, actualizeaza paginile dupa schema versiunii finale.
