#define IP_REGISTER 4
#define REGISTERS { 1, 0, 0, 0, 0, 0 }
#define CODE_LEN 36

inline void instr_0(long* registers) {
    registers[4] = registers[4] + 16;
}
inline void instr_1(long* registers) {
    registers[3] = 1;
}
inline void instr_2(long* registers) {
    registers[1] = 1;
}
inline void instr_3(long* registers) {
    registers[2] = registers[3] * registers[1];
}
inline void instr_4(long* registers) {
    if (registers[2] == registers[5]) { registers[2] = 1; } else { registers[2] = 0; }
}
inline void instr_5(long* registers) {
    registers[4] = registers[2] + registers[4];
}
inline void instr_6(long* registers) {
    registers[4] = registers[4] + 1;
}
inline void instr_7(long* registers) {
    registers[0] = registers[3] + registers[0];
}
inline void instr_8(long* registers) {
    registers[1] = registers[1] + 1;
}
inline void instr_9(long* registers) {
    if (registers[1] > registers[5]) { registers[2] = 1; } else { registers[2] = 0; }
}
inline void instr_10(long* registers) {
    registers[4] = registers[4] + registers[2];
}
inline void instr_11(long* registers) {
    registers[4] = 2;
}
inline void instr_12(long* registers) {
    registers[3] = registers[3] + 1;
}
inline void instr_13(long* registers) {
    if (registers[3] > registers[5]) { registers[2] = 1; } else { registers[2] = 0; }
}
inline void instr_14(long* registers) {
    registers[4] = registers[2] + registers[4];
}
inline void instr_15(long* registers) {
    registers[4] = 1;
}
inline void instr_16(long* registers) {
    registers[4] = registers[4] * registers[4];
}
inline void instr_17(long* registers) {
    registers[5] = registers[5] + 2;
}
inline void instr_18(long* registers) {
    registers[5] = registers[5] * registers[5];
}
inline void instr_19(long* registers) {
    registers[5] = registers[4] * registers[5];
}
inline void instr_20(long* registers) {
    registers[5] = registers[5] * 11;
}
inline void instr_21(long* registers) {
    registers[2] = registers[2] + 4;
}
inline void instr_22(long* registers) {
    registers[2] = registers[2] * registers[4];
}
inline void instr_23(long* registers) {
    registers[2] = registers[2] + 5;
}
inline void instr_24(long* registers) {
    registers[5] = registers[5] + registers[2];
}
inline void instr_25(long* registers) {
    registers[4] = registers[4] + registers[0];
}
inline void instr_26(long* registers) {
    registers[4] = 0;
}
inline void instr_27(long* registers) {
    registers[2] = registers[4];
}
inline void instr_28(long* registers) {
    registers[2] = registers[2] * registers[4];
}
inline void instr_29(long* registers) {
    registers[2] = registers[4] + registers[2];
}
inline void instr_30(long* registers) {
    registers[2] = registers[4] * registers[2];
}
inline void instr_31(long* registers) {
    registers[2] = registers[2] * 14;
}
inline void instr_32(long* registers) {
    registers[2] = registers[2] * registers[4];
}
inline void instr_33(long* registers) {
    registers[5] = registers[5] + registers[2];
}
inline void instr_34(long* registers) {
    registers[0] = 0;
}
inline void instr_35(long* registers) {
    registers[4] = 0;
}

inline void run_instr(int idx, long* registers) {
    switch (idx) {
        case 0: instr_0(registers); break;
        case 1: instr_1(registers); break;
        case 2: instr_2(registers); break;
        case 3: instr_3(registers); break;
        case 4: instr_4(registers); break;
        case 5: instr_5(registers); break;
        case 6: instr_6(registers); break;
        case 7: instr_7(registers); break;
        case 8: instr_8(registers); break;
        case 9: instr_9(registers); break;
        case 10: instr_10(registers); break;
        case 11: instr_11(registers); break;
        case 12: instr_12(registers); break;
        case 13: instr_13(registers); break;
        case 14: instr_14(registers); break;
        case 15: instr_15(registers); break;
        case 16: instr_16(registers); break;
        case 17: instr_17(registers); break;
        case 18: instr_18(registers); break;
        case 19: instr_19(registers); break;
        case 20: instr_20(registers); break;
        case 21: instr_21(registers); break;
        case 22: instr_22(registers); break;
        case 23: instr_23(registers); break;
        case 24: instr_24(registers); break;
        case 25: instr_25(registers); break;
        case 26: instr_26(registers); break;
        case 27: instr_27(registers); break;
        case 28: instr_28(registers); break;
        case 29: instr_29(registers); break;
        case 30: instr_30(registers); break;
        case 31: instr_31(registers); break;
        case 32: instr_32(registers); break;
        case 33: instr_33(registers); break;
        case 34: instr_34(registers); break;
        case 35: instr_35(registers); break;
    };
}
