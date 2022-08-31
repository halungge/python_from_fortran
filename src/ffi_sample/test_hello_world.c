// used as comparison for test_hello_world.f90: calling an cffi example form C
#include <stdio.h>
#include "../../build/hello_plugin.h"

int main(int argc, char *argv[]) {
    int limit = 5;
    hello_world();

    printf("call from c: sum up to %i =%i \n", limit, sumup(5));
    return 0;
}