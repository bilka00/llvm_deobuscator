import json
import os
import sys
import subprocess
import re
from lief import PE
import lief
import shutil

"""
-march [x86, x86-64]
"""
LLC_PATH = "llc.exe"

PYTHON_PATH = "C:\\python\\Python_3.10.0_x64\\python.exe"
RETDEC_PATH = "C:\\Users\\Admin\\PycharmProjects\\llvm_deobuscator\\retdec\\bin\\retdec-decompiler.py"


def get_use_labels(asm_code):
    exception_list = list()
    exception_list.extend(re.findall(r"jne\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jmp\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"je\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"call\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jnz\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jz\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jb\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jnb\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jle\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jcc\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"ljmp\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jo\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jno\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"js\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jns\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"je\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jne\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jnz\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jb\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jc\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jnb\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jae\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"ja\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jnbe\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jl\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jge\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jnl\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jp\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jpe\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jnp\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jpo\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jcxz\s+(.+)", asm_code))
    exception_list.extend(re.findall(r"jecxz\s+(.+)", asm_code))
    return exception_list


def llc_filter(asm_code):
    list_asm_code = asm_code.split("\n")
    filtered_code = ""
    exception_list = get_use_labels(asm_code)
    for line in list_asm_code:
        try:
            """
            >>> a = [1,2,3,4]
            >>> b = [2,7]
            >>> any(x in a for x in b)
            True
            """
            if line.strip()[0] != '.' and line.strip()[0] != '#':
                filtered_code += "%s\n" % line
            elif any(x in line for x in exception_list):
                filtered_code += "%s\n" % line
        except:
            pass
    return filtered_code


def compile_fix(asm_code, function_start, arch):
    if arch == "x86":
        header = "use32\norg 0x%02x\n" % function_start
    elif arch == "x86-64":
        header = "use64\norg 0x%02x\n" % function_start

    # Fix function call
    asm_code = re.sub(r"function_(.+)@PLT", "0x\\1", asm_code)
    asm_code = re.sub(r"call\s+function_(\S+)", "call 0x\\1", asm_code)
    # Filer comments
    asm_code = re.sub("#.*", "", asm_code)
    # Fix masm to fasm
    asm_code = re.sub("dword ptr", "dword", asm_code)
    asm_code = re.sub("word ptr", "word", asm_code)
    asm_code = re.sub("byte ptr", "byte", asm_code)
    asm_code = re.sub("qword ptr", "qword", asm_code)
    # TODO: dword or qword for x64
    if arch == "x86":
        asm_code = re.sub(r"offset\s+global_var_(.+)", "dword[0x\\1]", asm_code)
    if arch == "x86-64":
        asm_code = re.sub(r"offset\s+global_var_(.+)", "qword[0x\\1]", asm_code)
    asm_code = re.sub(r"\[global_var_(.+)\]", "[0x\\1]", asm_code)

    return header+asm_code


def fix_imports(asm_code):
    functions = re.findall(r"call\s+(\S+)@PLT", asm_code)
    json_object = json.load(open("work.config.json"))
    for function in functions:
        for json_function in json_object["functions"]:
            if function == json_function["name"]:
                asm_code = re.sub(r"call\s+(\S+)@PLT", "call dword[%s]" % json_function["startAddr"], asm_code)
    return asm_code


def optimize_function(filename, function_start, function_end, binary, arch):
    shutil.copyfile(filename, "work.exe")
    select_ranges = "0x%02x-0x%02x" % (function_start, function_end)

    result = subprocess.run([PYTHON_PATH, RETDEC_PATH,
                             "work.exe",
                             "--select-ranges", select_ranges,
                             "--select-decode-only",
                             "--stop-after", "bin2llvmir",
                             # "--backend-no-symbolic-names",
                             # "--backend-keep-library-funcs",
                             # "--backend-no-var-renaming",
                             # "--backend-var-renamer", "address",
                             # "--no-config",
                             # "--fileinfo-verbose",
                             # "--cleanup",
                             "-o", "work.ll"])

    result = subprocess.run([LLC_PATH,
                             "-o", "work.asm",
                             "-x86-asm-syntax=intel",
                             "-filetype=asm",
                             "-march=%s" % arch,
                             "-mtriple", "x86_64-win32", # горите сука в аду
                             "work.ll"])

    asm_code = open("work.asm").read()
    asm_code = llc_filter(asm_code)
    asm_code = compile_fix(asm_code, function_start, arch)
    asm_code = fix_imports(asm_code)
    open("work2.asm", "w").write(asm_code)

    os.system(os.getcwd() + r"\fasm\FASM.EXE work2.asm")
    compiled_function = list(open("work2.bin", "rb").read())
    original_size = function_end - function_start
    if len(compiled_function) < original_size:
        ext = [ord(c) for c in ("\xCC" * (original_size - len(compiled_function) + 1))]
        compiled_function.extend(ext)
    binary.patch_address(function_start, list(compiled_function))
    os.remove("work2.bin")
    # os.remove("work.asm")
    # os.remove("work.ll")
    # os.remove("work.dsm")
    # os.remove("work.config.json")
    # os.remove("work.bc")
    os.remove("work.exe")


def main():
    # function_start = 0x401000
    # function_end = 0x401060

    binary = lief.parse("testx64.exe")

    optimize_function("testx64.exe", 0x140001000, 0x140001068, binary, "x86-64")
    # optimize_function("testx64.exe", 0x4018C5, 0x401A95, binary, "x86-64")
    binary.write("testx64_fix.exe")


if __name__ == '__main__':
    main()
