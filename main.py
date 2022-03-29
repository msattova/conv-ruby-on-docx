
from pathlib import Path

import modules.arg as arg
import modules.fileproc as fpc

cmd = arg.CmdArg()

input = Path(cmd.args.inputfile)
template = Path('')
output = Path(cmd.args.output)
ruby_font = cmd.args.font
em_style = cmd.args.em

p = fpc.FileProc(template, input, output, ruby_font, em_style)

p.process()
