
import modules.arg as arg
import modules.fileproc as fpc

cmd = arg.CmdArg()

template = cmd.args.filename
input = ''
output = cmd.args.output

p = fpc.FileProc(template, input, output)

p.process()
