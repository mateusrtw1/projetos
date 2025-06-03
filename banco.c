#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>

#define NUM_CONTAS 3

typedef struct {
    char id[10];
    char senha[5];
    float saldo;
} Conta;

int main() {
    setlocale(LC_ALL, "Portuguese");

    Conta contas[NUM_CONTAS] = {
        {"Mateus", "1234", 5000.00},
        {"Felipe", "1111", 3000.00},
        {"Antonio", "5375", 100000.00}
    };

    char idDigitado[10];
    char senhaDigitada[5];
    int tentativas = 0;
    const int MAX_TENTATIVAS = 3;
    int logado = -1;
    int i;
    int menu;
    float saque, deposito;
    int dia = 03;
    int mes = 06;
    int ano = 2025;
    float valores[50];
    char tipo[50];
    int p = 0;

    // Login
    while (tentativas < MAX_TENTATIVAS && logado == -1) {
        printf("Digite o nome do seu usúario: ");
        scanf("%9s", idDigitado);

        printf("Digite sua senha: ");
        scanf("%4s", senhaDigitada);

        for (i = 0; i < NUM_CONTAS; i++) {
            if (strcasecmp(idDigitado, contas[i].id) == 0 && strcmp(senhaDigitada, contas[i].senha) == 0) {
                logado = i;
                break;
            }
        }

        if (logado == -1) {
            tentativas++;
            if (tentativas >= MAX_TENTATIVAS) {
                printf("Número máximo de tentativas excedido. Encerrando o programa.\n");
                return 0;
            }
            printf("nome de usúario ou senha incorretos! Tentativas restantes: %i.\n", MAX_TENTATIVAS - tentativas);
        }
    }

        printf("\n\t BEM VINDO AO BANCO, %s!\n\n", contas[logado].id);

    while (1) {
        printf("\t=========== MENU ===========\n");
        printf("\t-------- SALDO = 2 ---------\n");
        printf("\t---- SACAR DINHEIRO = 3 ----\n");
        printf("\t-- DEPOSITAR DINHEIRO = 4 --\n");
        printf("\t------ EXTRATO = 5 ---------\n");
        printf("\t--------- SAIR = 0 ---------\n");

        printf("\nDigite o número para continuar:\n");
        scanf("%i", &menu);

        switch (menu) {
            case 0:
                printf("\nEncerrando Programa...\n\n");
                return 0;

            case 2:
                printf("\n\tSALDO!!\n");
                printf("Seu saldo total é: R$%.2f\n", contas[logado].saldo);
                printf("\n\nData: %02d/%02d/%d  17:30\n\n", dia,mes,ano);
                printf("--------------------------------------\n\n");
                break;

            case 3:
                printf("\n\tSAQUE DE DINHEIRO!!\n\n");
                printf("Qual valor deseja retirar?\n");
                scanf("%f", &saque);

                if (saque > 0 && saque <= contas[logado].saldo) {
                    contas[logado].saldo -= saque;
                    valores[p] = saque;
                    tipo[p] = 'S';
                    p++;
                    printf("\nVocê sacou R$%.2f da sua conta.\n\n", saque);
                    printf("Saldo atual:R$%.2f.\n", contas[logado].saldo);
                } else {
                    printf("Valor inválido ou saldo insuficiente.\n");
                }
                printf("\n\nData: %02d/%02d/%d  17:30\n\n", dia,mes,ano);
                printf("--------------------------------------\n\n");
                break;

            case 4:
                printf("\n\tDEPÓSITO DE DINHEIRO!!\n\n");
                printf("Qual valor deseja depositar?\n");
                scanf("%f", &deposito);

                if (deposito > 0) {
                    contas[logado].saldo += deposito;
                    valores[p] = deposito;
                    tipo[p] = 'D';
                    p++;
                    printf("\nVocê depositou R$%.2f na sua conta.\n\n", deposito);
                    printf("Saldo atual:R$%.2f. \n", contas[logado].saldo);
                    printf("\n\nData: %02d/%02d/%d  17:30\n\n", dia,mes,ano);
                } else {
                    printf("Valor inválido.\n");
                }
                printf("--------------------------------------\n\n");
                break;

            case 5:
                printf("\n\tEXTRATO!!\n\n");
                if (p == 0) {
                    printf("Nenhuma movimentação registrada.\n");
                } else {
                    for (int i = 0; i < p; i++) {
                        if (tipo[i] == 'D') {
                            printf("Depósito:  +R$%.2f %02d/%02d/%d  17:30\n\n", valores[i], dia,mes,ano);
                        } else if (tipo[i] == 'S') {
                            printf("Saque:  -R$%.2f %02d/%02d/%d  17:30\n\n", valores[i], dia,mes,ano);
                        }
                    }
                }
                printf("\nSaldo atual: R$%.2f\n", contas[logado].saldo);
                printf("\n--------------------------------------\n\n");
                break;

            default:
                printf("Opção inválida. Tente novamente.\n\n");
        }
    }

    return 0;
}
