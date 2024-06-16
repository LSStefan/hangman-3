#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//structura pentru lista SIMPLU INLANTUITA folosita
typedef struct element
{
    char litera;
    struct element *urmator;
} nod;


typedef struct intrebari
{
    char *intrebare;
    char *var_A;
    char *var_AA;
    char *var_B;
    char *var_BB;
    char *var_C;
    char *var_CC;
    char *var_D;
    char *var_DD;
    
    char *raspuns;
} intrebare;

//functie de extragere aleatorie a cuvantului de ghicit din lista de cuvinte
char* extrag_cuvant()
{
    FILE *fisier_text;
    int index_cuvant_exp; //marcheaza randul in care e afla cuvantul propus de ghicit
    fisier_text = fopen("cuvinte.txt", "rt");
    char *word_hangman = (char *)malloc(100 * sizeof(char));
    if (fisier_text == NULL) //se verifica daca se poate efectua citirea din fisierul de cuvinte
    {
        printf("ERROR! THE WORD LIST FILE COULD NOT BE READ!");
        return 0;
    }
    else
    {
        srand(time(0)); //Se asigura ca la fiecare utilizare / timp de executie se alege cu cuvant diferit din cadrul generatorului de cuvinte
        index_cuvant_exp = rand() % 100;

        for (int indice = 1; indice < index_cuvant_exp; indice++)
        {
            fgets(word_hangman, 100, fisier_text);
        }

        fgets(word_hangman, 100, fisier_text);
        word_hangman[strcspn(word_hangman, "\n")] = '\0'; //inlocuieste caracterul '\n' cu terminatorul de sir ('\0')
        fclose(fisier_text);
    }
    FILE *fisier_cuvant;
    fisier_cuvant = fopen("cuvant.txt", "w");
    fprintf(fisier_cuvant, "%s", word_hangman);
    fflush(fisier_cuvant);
    return word_hangman;

}


// functie de extragere string-uri necesare intrebarii pentru puncte bonus
void extrag_intrebare(char intrebari_hangman[], intrebare *intrebatoare)
{
    FILE *fisier_text;
    char *expresie;
    int index_intrebare_exp; // marcheaza randul in care se afla intrebarea
    fisier_text = fopen("Intrebari_reformat.csv", "rt");
    if (fisier_text == NULL) // se verifica daca se poate efectua citirea din fisierul de cuvinte
    {
        printf("ERROR! IMPOSIBLE TO READ THIS FILE!");
        exit(1); // Iesirea din program daca citirea fisierului esueaza
    }
    else
    {
        srand(time(0));                        // Asigurarea alegerii unui cuvant diferit la fiecare utilizare/timp de executie
        index_intrebare_exp = rand() % 20 + 1; // se evita primul rand, introductiv al fisierului csv

        for (int indice = 0; indice < index_intrebare_exp; indice++)
        {
            fgets(intrebari_hangman, 1000, fisier_text);
        }

        fgets(intrebari_hangman, 1000, fisier_text);
        fclose(fisier_text);

        expresie = strtok(intrebari_hangman, ",");
        int column = 0; // indică coloana curentă (1 - intrebare, 2 - var_A, 3 - var_B, 4 - var_C, 5 - var_D, 6 - raspuns)

        while (expresie != NULL)
        {
            switch (column) // extragere string-uri pe coloane adecvate / impartirea pe expresii separate prin virgula
            {
            case 1:
                intrebatoare->intrebare = strdup(expresie); // duplicare de string
                printf("\n%s", intrebatoare->intrebare);
                break;
            case 2:
                intrebatoare->var_A = strdup(expresie);
                printf("\nA) %s", intrebatoare->var_A);
                break;
            case 3:
                intrebatoare->var_AA = strdup(expresie);
                break;
            case 4:
                intrebatoare->var_B = strdup(expresie);
                printf("\nB) %s", intrebatoare->var_B);
                break;
            case 5:
                intrebatoare->var_BB = strdup(expresie);
                break;
            case 6:
                intrebatoare->var_C = strdup(expresie);
                printf("\nC) %s", intrebatoare->var_C);
                break;
            case 7:
                intrebatoare->var_CC = strdup(expresie);
                break;
            case 8:
                intrebatoare->var_D = strdup(expresie);
                printf("\nD) %s", intrebatoare->var_D);
                break;
            case 9:
                intrebatoare->var_DD = strdup(expresie);
                break;
            case 10:
                intrebatoare->raspuns = strdup(expresie);
                size_t len = strlen(intrebatoare->raspuns); // Obtine lungimea șirului
                if (len > 0 && intrebatoare->raspuns[len - 1] == '\n')
                {
                    intrebatoare->raspuns[len - 1] = '\0'; // Eliminare '\n' de la sfarsitul sirului
                    // pentru a se face compararea corespunz cu raspunsul tastat
                }
                break;
            default:
                break;
            }
            expresie = strtok(NULL, ",");
            column++;
        }
    }
    FILE *fisier_intrebare;
    FILE *fisier_rapuns;
    fisier_intrebare = fopen("intrebare.txt", "w");
    fisier_rapuns = fopen("raspuns.txt", "w");
    fprintf(fisier_intrebare, "%s\n", intrebatoare->intrebare);
    fprintf(fisier_intrebare, "A)%s\n", intrebatoare->var_A);
    fprintf(fisier_intrebare, "A)%s\n", intrebatoare->var_AA);
    fprintf(fisier_intrebare, "B)%s\n", intrebatoare->var_B);
    fprintf(fisier_intrebare, "B)%s\n", intrebatoare->var_BB);
    fprintf(fisier_intrebare, "C)%s\n", intrebatoare->var_C);
    fprintf(fisier_intrebare, "C)%s\n", intrebatoare->var_CC);
    fprintf(fisier_intrebare, "D)%s\n", intrebatoare->var_D);
    fprintf(fisier_intrebare, "D)%s\n", intrebatoare->var_DD);
    fprintf(fisier_rapuns, "%s", intrebatoare->raspuns);

    fflush(fisier_intrebare);
    fflush(fisier_rapuns);
    fclose(fisier_intrebare);
    fclose(fisier_rapuns);
}


//funnctie de adaugare caracter cuvant in lista simplu inlantuita (creare lista)
void adaug_in_lista(char word_hangman[], int dimensiune, nod **inceput)
{
    nod *intermediar = NULL;

    for (int indice = 0; indice < dimensiune; indice++)
    {
        if (*inceput == NULL)
        {
            (*inceput) = malloc(sizeof(nod));
            (*inceput)->litera = word_hangman[0];
            (*inceput)->urmator = NULL;
            intermediar = (*inceput);
        }
        else
        {
            intermediar->urmator = malloc(sizeof(nod));
            intermediar = intermediar->urmator;
            intermediar->litera = word_hangman[indice];
            intermediar->urmator = NULL;
        }
    }
}

char* afisare_element_lista_CODIFICAT(nod *inceput)
{
    nod *curent;
    int i = 0;
    char *elementcodificat = (char *)malloc(100 * sizeof(char));
    for (curent = inceput; curent != NULL; curent = curent->urmator)
    {
        if (curent->litera == ' ')
        {
            printf(" | ");
            elementcodificat[i] = ' ';
            i++;
        }
        else
        {
            printf("%c", curent->litera);
            elementcodificat[i] = curent->litera;
            i++;
        }

    }
    return elementcodificat;
}

void modificare(nod **inceput2)
{
    nod *curent;
    for (curent = (*inceput2); curent != NULL; curent = curent->urmator)
    {
        if (curent->litera != ' ')
        {
            curent->litera = '_';
        }
        
    }
}

void modificare2(nod **inceput2, nod *inceput, char caracter, int *ghicit, int *nr_litere_ghicite)
{
    nod *curent, *curent2;
    for (curent = inceput, curent2 = *inceput2; curent != NULL && curent2 != NULL; curent = curent->urmator, curent2 = curent2->urmator)
    {
        if (curent->litera == caracter)
        {
            curent2->litera = caracter;
            *ghicit = 1;
            (*nr_litere_ghicite)++;
        }
    }
}

// functie de ghicire caracter + implementare mod salvare cu intrebari si raspunsuri pentru doua vieti extra
void ghicire_si_sansa(nod *inceput, nod *inceput2, int dimensiune, int nr_sanse, char word_hangman[], intrebare *intrebatoare, char intrebari_hangman[], char caractere_introduse[])
{
    char caracter, alegere, variante_alese[10];
    int nr_greseli = 0, ghicit, nr_litere_ghicite = 0;
    nod *curent;

    // ghicirea se termina cand numarul de vieti (nr_sanse) e mai mic decat cel de greseli sau cand au fost ghicite toate seturile de litere
    while (nr_greseli < nr_sanse && nr_litere_ghicite < dimensiune)
    {
        nr_litere_ghicite = 0;
        ghicit = 0;
        printf("\nCHOOSE A LETTER & GUESS!\n");

        char input[100]; // Presupunem ca input-ul NU va depasi 100 de caractere
        fgets(input, sizeof(input), stdin);

        // Extragerea primului caracter
        caracter = input[0];

        // Verificare daca caracterul/ inputul introdus este o litera (intre A si Z)
        if ((caracter < 'A' || caracter > 'Z') && (caracter < 'a' || caracter > 'z'))
        {
            printf("Invalid input! Please enter a letter (A-Z).\n");
            continue; // Trecere la urmatoarea iteratie, fara a scadea din sanse daca caracterul tastat NU e litera
        }

        // Convertire lowercase - uppercase
        if (caracter >= 'a' && caracter <= 'z')
            caracter -= 'a' - 'A';

        // Verificare daca litera respectiva a fost anterior ghicita / introdusa
        if (caractere_introduse[caracter - 'A'] == 1)
        {
            printf("You have already typed this letter. Please choose another one.\n");
            continue; // Trecere la urmatoarea iteratie
        }

        // marcare litera ghicita in cadrul vectorului de litere (alfabet englez, cu 26 de litere)
        caractere_introduse[caracter - 'A'] = 1;

        // Actualizare modificare2
        modificare2(&inceput2, inceput, caracter, &ghicit, &nr_litere_ghicite);
        afisare_element_lista_CODIFICAT(inceput2);

        if (ghicit == 1)
        {
            printf("\n\nYou guessed: %c\n--------------------\n", caracter);
        }
        else
        {
            int numar_vieti = nr_sanse - nr_greseli - 1;
            printf("\n\nWrong guess! Lives: %d | TRY AGAIN!\n--------------------------\n", numar_vieti);
            nr_greseli++;
        }
    }

    // daca s-a epuizat numarul de vieti, jucatorul poate alege sa paraseasca jocul
    // sau sa raspunda la o intrebare pentru doua vieti extra
    if (nr_greseli >= nr_sanse)
    {
        printf("YOU HAVE NO LIVES LEFT! WOULD YOU LIKE TO ANSWER A QUESTION TO GET 2 (EXTRA) LIVES? [y/n]\n");
        scanf("%c", &alegere);
        if (alegere == 'n')
        {
            printf("GAME OVER! The word/expression you had to guess was: %s.", word_hangman);
        }
        else
        {
            extrag_intrebare(intrebari_hangman, intrebatoare);
            printf("\n\nTO ANSWER, PRESS ONE OR MORE KEYS (LETTERS) (FOLLOWED BY <<&>>, FROM LETTER A TO D - IF THERE ARE MULTIPLE CORRECT CHOISES) - EXAMPLE: <<X&Y&Z>>: ");
            scanf("%s", variante_alese);
            if (strcmp(variante_alese, intrebatoare->raspuns) == 0)
            {
                printf("YOU ANSWERED CORRECTLY! 2 BONUS LIVES ADDED! LET'S CONTINUE...");
                getchar(); // se preia caracterul '\n' din buffer
                ghicire_si_sansa(inceput, inceput2, dimensiune, 2, word_hangman, intrebatoare, intrebari_hangman, caractere_introduse);
            }
            else
            {
                printf("INCORRECT ANSWER! ANSWER: %s", intrebatoare->raspuns);
                printf("\nGAME OVER! The word/expression you had to guess was: %s.", word_hangman);
            }
        }
    }

    // mesaj specific in cazul in care cuvantul e ghicit in intregime
    else if (nr_greseli < nr_sanse && nr_litere_ghicite == dimensiune)
    {
        printf("CONGRATULATIONS! YOU GUESSED THE ENTIRE WORD / EXPRESSION: %s", word_hangman);
    }
}

char* codificare_cuvant(char cuvant_hangman[100], int dimensiune)
{
    char *elementcodificat = malloc(100 * sizeof(char));

    for (int indice = 0; indice < dimensiune; indice++)
    {
        if (cuvant_hangman[indice] == ' ')
        {
            elementcodificat[indice] = ' ';

        }
        else
        {
            elementcodificat[indice] = '_';
            elementcodificat[indice + 1] = ' ';
        }
    }

    return elementcodificat;
}

typedef struct Node {
    char letter;
    struct Node* next;
} Node;



Node* create_node(char letter) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->letter = letter;
    new_node->next = NULL;
    return new_node;
}

// Append a new node at the end of the list
void append(Node** head_ref, char new_letter) {
    Node* new_node = create_node(new_letter);
    if (*head_ref == NULL) {
        *head_ref = new_node;
        return;
    }
    Node* last = *head_ref;
    while (last->next != NULL) {
        last = last->next;
    }
    last->next = new_node;


}

char* list_to_string(Node* head) {
    static char buffer[256];
    int pos = 0;
    Node* current = head;
    while (current != NULL && pos < sizeof(buffer) - 2) {
        buffer[pos++] = current->letter;
        buffer[pos++] = ' ';
        current = current->next;
    }
    buffer[pos] = '\0';
    return buffer;
}

int main()
{

    
    return 0;
}