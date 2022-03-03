
import modules.arg as arg
import modules.fileproc as fpc

cmd = arg.CmdArg()

input = cmd.args.inputfile
template = ''
output = cmd.args.output
ruby_font = cmd.args.font

p = fpc.FileProc(template, input, output, ruby_font)

p.process()
