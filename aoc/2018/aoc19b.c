#include <stdio.h>
#include "aoc19_code.c"

void print_registers(long *registers)
{
    int i;
    for (i = 0; i < 6; i++)
    {
        printf("%ld ", registers[i]);
    }
    printf("\n");
}

int main(void)
{
    long registers[] = REGISTERS;
    int ip = 0;
    int cnt = 0;
    int subcnt = 0;
    int opt = 1;
    while (ip < CODE_LEN)
    {
        if (ip == 4 && 0)
        {
            if (registers[2] < registers[5] - 10)
            {
                registers[2] = registers[5] - 10;
            }
        }
        if (ip == 8)
        {
            if (registers[1] < registers[5] - 10)
            {
                registers[1] = registers[5] - 10;
            }
        }
        if (ip == 12)
        {
            if (registers[3] < registers[5] - 10)
            {
                registers[3] = registers[5] - 10;
            }
        }

        printf("[%d]\t", ip);
        print_registers(registers);

        registers[IP_REGISTER] = ip;
        run_instr(ip, registers);
        ip = registers[IP_REGISTER];
        ip++;
        // print_registers(registers);
        if (subcnt == 100000000)
        {
            subcnt = 0;
            printf("%d\n", cnt);
            cnt++;
        }
        subcnt++;
    }
    printf("%d\n", ip);
    print_registers(registers);
    return 0;
}