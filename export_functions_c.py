# Export all functions
#@author Gustavo Litovsky
#@category Argenox
#@keybinding 
#@menupath 
#@toolbar

# More information:
# https://www.argenox.com
# License: Apache License 2.0

import ghidra.app.decompiler as decomp
from ghidra.program.model.data import Structure, StructureDataType, UnsignedIntegerDataType, DataTypeConflictHandler
from ghidra.program.model.data import UnsignedShortDataType, ByteDataType, UnsignedLongLongDataType
from ghidra.program.model.mem import MemoryBlockType
from ghidra.program.model.address import AddressFactory
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.mem import MemoryConflictException
import os


# Get Output directory
directory1 = askDirectory("Choose Output Dir", "Choose directory:")

# get all functions
functions = currentProgram.getFunctionManager().getFunctions(True)
for function in functions:   

    print("Function: " + function.getName())

    fname = function.getName()

    # Filter functions that are unnamed
    if( 'FUN_' in function.getName() or 'thunk_FUN_' in function.getName()):
        continue

    ## get the decompiler interface
    iface = decomp.DecompInterface()

    ## decompile the function
    iface.openProgram(function.getProgram())
    d = iface.decompileFunction(function, 5, monitor)

    ## get the C code as string
    if not d.decompileCompleted():
        print(d.getErrorMessage())
    else:
        code = d.getDecompiledFunction()
        ccode = code.getC()
        #print(ccode)    

        if( '?' in fname):
            fname = fname.replace("?", "")

        f = open(str(directory1) + "/" + fname + ".c", "w")

        ccode_no_empt_line = ccode.replace("\n", "")
        f.write(ccode_no_empt_line)
        f.close()
