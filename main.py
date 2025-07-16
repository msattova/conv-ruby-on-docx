
from pathlib import Path

from modules.arg import CmdArg
from modules.fileproc import FileProc

cmd = CmdArg()

input = Path(cmd.args.inputfile)
template = Path('')
output = Path(cmd.args.output)
ruby_font = cmd.args.font
ruby_size = cmd.args.size
em_style = cmd.args.em

p = FileProc(template, input, output, ruby_font, ruby_size, em_style)

p.process()
