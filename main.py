

import modules.fileproc as fpc

#template = './docx/template.docx'
template = 'docx/texted_copipe.docx'
input = './text.txt'
output = './output.docx'

p = fpc.FileProc(template, input, output)

p.process()

