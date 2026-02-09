#!/bin/env python3

if __name__ != "__main__":
    exit(1)

import os
import sys


if (len(sys.argv) != 4):
    print("Wrong number of arguments!")
    exit(1)

outfile_code = sys.argv[1]
outfile_header = sys.argv[2]
root = os.path.abspath(sys.argv[3])

components = []

for p in os.scandir(root):
    if not p.is_dir():
        continue
    i = p.name
    if i.lower() != i:
        continue
    path = f"{root}/{i}/{i}.h"
    if os.path.exists(path):
        components.append(i)

components.sort()

names = []
for c in components:
    names.append(c.capitalize())

def callIfExist(f, name):
    f.write(f"\textern void {name}() __attribute__((weak));\n".encode())
    f.write(f"\tif ({name}) {name}();\n".encode())


with open(outfile_header, "wb") as f:
    f.write("// Auto-generated file. Do not edit!\n\n".encode())
    for comp in components:
        f.write(f"#include \"{comp}/{comp}.h\"\n".encode())


defineName = os.path.basename(outfile_header)

with open(outfile_code, "wb") as f:
    f.write("// Auto-generated file. Do not edit!\n\n".encode())
    f.write(f"#include \"{defineName}\"\n\n".encode())

    f.write(f"__attribute__((noreturn, noinline))\nint main();\n".encode())
    f.write(f"__attribute__((noinline))\nvoid init();\n".encode())
    f.write(f"__attribute__((noinline))\nvoid loop();\n".encode())
    f.write(f"__attribute__((noinline))\nvoid tick();\n".encode())

    f.write(f"\n".encode())

    f.write("int main() {\n".encode())
    f.write("\tinit();\n".encode())
    f.write("\twhile (1) {\n".encode())
    f.write("\t\tloop();\n".encode())
    f.write("\t}\n".encode())
    f.write("}\n\n".encode())

    f.write("void init() {".encode())
    f.write("\n/* Stage 1: Comonent_Init() */\n".encode())
    for comp in names:
        callIfExist(f, f"{comp}_Init")
    f.write("\n/* Stage 2: Comonent_InitHW() */\n".encode())
    for comp in names:
        callIfExist(f, f"{comp}_InitHW")
    f.write("\n/* Stage 3: Comonent_InitSW() */\n".encode())
    for comp in names:
        callIfExist(f, f"{comp}_InitSW")
    f.write("\n/* Stage 4: Comonent_Start() */\n".encode())
    for comp in names:
        callIfExist(f, f"{comp}_Start")
    f.write("}\n\n".encode())

    f.write("void loop() {".encode())
    f.write("\n/* Stage 1: Comonent_Main() */\n".encode())
    for comp in names:
        callIfExist(f, f"{comp}_Main")
    f.write("\n/* Stage 2: Comonent_PostMain() */\n".encode())
    for comp in names:
        callIfExist(f, f"{comp}_PostMain")
    f.write("}\n\n".encode())

    f.write("void tick() {\n".encode())
    for comp in names:
        callIfExist(f, f"{comp}_Tick")
    f.write("}\n\n".encode())

exit(0)
