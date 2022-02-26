
import modules.arg as arg
import modules.fileproc as fpc

cmd = arg.CmdArg()

input = cmd.args.inputfile
template = ''
output = cmd.args.output

p = fpc.FileProc(template, input, output)

p.process()
