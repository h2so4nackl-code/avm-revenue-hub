# AVM Revenue Hub — proiectul nou

Acesta este un proiect separat de Bounty Escrow. Are trei tipuri de contracte:

1. **Seif de venituri:** împarte venituri repetate după cote fixe și permite
   retrageri individuale către adresele stabilite.
2. **Receptor de plată:** confirmă primirea și poate simula erori pentru teste.
3. **Registru de audit:** procesează rapoarte în loturi și împiedică dublarea lor.

Oprirea, reluarea și schimbarea rezervei de execuție cer voturi de la doi dintre
trei administratori și respectarea perioadei de așteptare. Administratorii nu pot
schimba cotele și nu pot redirecționa principalul prin aceste metode.

Verificările locale includ 74 teste ale proiectului + 12 ale SDK-ului. Demonstrația
AVM se încheie cu 10.010 unități locale distribuite astfel: 5.005 + 3.003 + 2.002.
Receptorii și registrul de audit confirmă aceleași sume; replay-ul este concordant.

Pentru Codex pe Windows: extrage arhiva într-un proiect separat, folosește WSL2
(Linux x86-64) și urmează `README.md`. Comenzile principale:

```bash
bash scripts/install_runtime.sh
bash scripts/install_binaryen.sh
bash scripts/check.sh
```

Rust 1.93.0, rustfmt, clippy și ținta wasm32 trebuie instalate mai întâi, conform
instrucțiunilor din README. Native tests folosesc exclusiv dependențele incluse.

În `docs/COMPARISON.md` găsești comparația exactă cu proiectul anterior. Pentru
dezvoltatorii SDK, descrierea și integrarea sunt în `docs/SDK-INTEGRATION.md`.

Proiectul este verificat într-un mediu AVM local. Nu este o integrare cu o licență
BM, un miner sau un token NACKL live. Nu este auditat pentru bani reali.
Repository public: https://github.com/h2so4nackl-code/avm-revenue-hub
Rezultatele verificărilor automate sunt în fila GitHub Actions.
