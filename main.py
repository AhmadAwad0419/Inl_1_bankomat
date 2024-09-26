from termcolor import colored
import os  # en modell, kan arbeta med filer, mappar.....
import datetime


# skapa filer om det inte finns.
konton_fil = 'konton.txt'
transaktioner_fil = 'transaktioner.txt'
if not os.path.exists(konton_fil):
    open(konton_fil, 'w') .close()

if not os.path.exists(transaktioner_fil):
    open(transaktioner_fil, 'w') .close()

konton = {}  # en tom dictionary
# detta kommer läsa varje rad som innehåller ett kontonummer, ---->
# saldo och lösenord

with open(konton_fil, 'r') as f:
    for line in f:
        if line.strip():
            kontonummer, saldo, losenord = line.strip().split(',')
            konton[kontonummer] = {'saldo': saldo, 'lösenord': losenord}


# huvud program, inkluderar loop.

print(colored('   VÄLLKOMMEN    ', 'black', 'on_green'))
while True:
    # skapa huvudmeny för bankomat
    print(colored('****HUVUDMENY****', 'white', 'on_green'))
    print(colored('1. Skapa konto ', 'white', 'on_green'))
    print(colored('2. Adminstrera konto ', 'white', 'on_green'))
    print(colored('3. Avsluta ', 'white', 'on_green'))
    meny_val = input(
        colored('Ange ett val av huvud meny> ', 'white', 'on_green')
        )

    if meny_val == '1':  # skapa konto
        konto_nummer = (input(
            colored('Ange ett kontonummer> ', 'white', 'on_green'))
                        ).strip()
        # kontrollera att kontonummer är siffror och inte redan finns...
        if not konto_nummer.isdigit() or konto_nummer == '':
            print(colored('ogiltigt kontonummer., Kontonumret måste vara numeriskt.', 'red', 'on_green'))
        elif konto_nummer in konton:
            print(colored('Kontonummer finns redan.', 'red', 'on_green'))
        else:
            lösenord = (input
                        (
                            colored('Ange ett lösenord> ', 'white', 'on_green')
                            )
                        ).strip()
            # Kontrollera att lösenordet kan inte vara sträng och ska inte vara tomt...
            if not lösenord.isdigit() or lösenord == '':
                print(colored(' ogiltigt lösenord, och får inte vara tomt.', 'red', 'on_green'))
            else:
                konton[konto_nummer] = {'saldo': 0.0, 'lösenord': lösenord}
                print(colored('ditt konto är skapad', 'black', 'on_green'))

                # skapad konton sparas i filen.
                with open(konton_fil, 'a', encoding='utf-8') as f:
                    f.write(f'{konto_nummer},{0.0},{lösenord}\n')

    elif meny_val == '2':

        # adminstrera kontot
        konto_nummer = (input(colored('Ange ett kontonummer> ', 'white', 'on_green'))).strip()
        if konto_nummer not in konton:  # kontrollera om konton finns inte..
            print(colored('kontonummer finns inte..', 'red', 'on_green'))
        else:
            lösenord = (input(colored('Ange ett lösenord> ', 'white', 'on_green'))).strip()

            # om lösenordet är fel..
            if lösenord.strip() != konton[konto_nummer]['lösenord']:
                print(colored('felaktigt lösenord..', 'red', 'on_green'))
            else:
                # användare går vidare till konto meny när det är inloggat..

                print(colored(f'****KONTOMENY**** - konto: {konto_nummer}', 'black', 'on_green'))
                while True:
                    # konto meny...
                    print(colored('1. Ta ut pengar ', 'white', 'on_green'))
                    print(colored('2. Sätt in pengar ', 'white', 'on_green'))
                    print(colored('3. Visa saldo ', 'white', 'on_green'))
                    print(colored('4. Lista transaktioner ', 'white', 'on_green'))
                    print(colored('5. Avsluta ', 'white', 'on_green'))
                    meny_val_1 = input(colored('Ange ett val av konto meny> ', 'white', 'on_green'))

                    if meny_val_1 == '1':  # ta ut pengar..
                        try:
                            ta_ut_pengar = float(input(colored('Ange ett belopp att ta ut: ', 'white', 'on_green')))
                            # kovertera saldo från sträng till float..
                            konton[konto_nummer]['saldo'] = float(konton[konto_nummer]['saldo'])
                            # kontrolera om användare ger ett negativt belopp..
                            if ta_ut_pengar <= 0:
                                print(colored('ogiltigt belopp. Ange ett positivt belopp.', 'red', 'on_green'))

                            # kontrolera om användare ta ut belopp som är större än vad som finns i kontonummer(saldo)..
                            elif ta_ut_pengar > konton[konto_nummer]['saldo']:
                                print(colored('tyvärr, beloppet är större än in ditt saldo', 'red', 'on_green'))

                            else:
                                konton[konto_nummer]['saldo'] -= ta_ut_pengar
                                print(colored(f'{ta_ut_pengar} kr har tagits ut, ditt nya saldo är {konton[konto_nummer]["saldo"]} kr', 'light_blue', 'on_green'))

                                # här spara transaktion till transaktion fil..

                                with open(transaktioner_fil, 'a', encoding='utf-8') as f:
                                    datum = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    f.write(f'{datum},{konto_nummer},{ta_ut_pengar}, uttag\n')
                        except ValueError:
                            print(colored('tyvärr, ogiltigt belopp, ange ett numeriskt värde', 'red', 'on_green'))

                    elif meny_val_1 == '2':  # sätt in pengar..
                        try:
                            sätt_in_pengar = (float(input(colored('Ange ett belopp att sätta in: ', 'white', 'on_green'))))
                            if sätt_in_pengar > 0:
                                konton[konto_nummer]['saldo'] = float(konton[konto_nummer]['saldo']) + sätt_in_pengar
                                print(colored(f'{sätt_in_pengar} kr har satts in, ditt nya saldo är {konton[konto_nummer]['saldo']} kr', 'white', 'on_green'))

                                # här spara transaktion till transaktion fil..

                                with open(transaktioner_fil, 'a', encoding='utf-8') as f:
                                    datum = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    f.write(f'{datum},{konto_nummer},{sätt_in_pengar}, insättning\n')
                            else:
                                print(colored('felaktigt belopp', 'red', 'on_green'))
                        except ValueError:
                            print(colored('tyvärr, ogiltigt belopp, ange ett numeriskt värde', 'red', 'on_green'))

                    elif meny_val_1 == '3':  # visa saldo..
                        print(colored(f'Ditt aktuella saldo är {float(konton[konto_nummer]['saldo'])}, kr', 'blue', 'on_green'))

                    elif meny_val_1 == '4':  # lista transaktioner..

                        print(colored(f'*****Transaktioner för kontonummer***** **{konto_nummer}**', 'blue', 'on_green'))
                        with open(transaktioner_fil, 'r', encoding='utf-8') as f:
                            for line in f:
                                if konto_nummer in line:
                                    datum, konto, belopp, typ = line.strip().split(',')
                                    print(f' Datum: {datum} - Typ: {typ}, Belopp: {belopp} kr')

                    elif meny_val_1 == '5':  # avsluta och gå tillbaka till huvudmenyn
                        break
                    # Spara konton till fil efter varje ändring

                    with open(konton_fil, 'w', encoding='utf-8') as f:
                        for nummer, data in konton.items():
                            f.write(f'{nummer},{data["saldo"]},{data["lösenord"]}\n')

    elif meny_val == '3':  # avsluta programmet..
        break

    else:
        print(colored('ogiltigt val', 'red', 'on_green'))
print(konton)
