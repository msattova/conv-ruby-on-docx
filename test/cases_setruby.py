import platform


def make_template(font="") -> tuple:
    if font == '':
        pf = platform.system()
        if pf == 'Windows':
            font = 'ＭＳ 明朝'
        elif pf == 'Darwin':
            font = 'ヒラギノ明朝 ProN '
        elif pf == 'Linux':  # Linux環境の場合はOSごとに標準でインストールされてるフォントが違うので要改善
            font = 'Noto Serif CJK JP'
        else:  # その他の結果が出た場合
            font = 'Noto Serif CJK JP'
    return tuple(''.join(s) for s in (
        (r'<w:r>', r'<w:ruby>', r'<w:rubyPr>',
         r'<w:rubyAlign w:val="distributeSpace"/>',
         r'<w:hps w:val="10"/>',
         r'<w:hpsRaise w:val="18"/>',
         r'<w:hpsBaseText w:val="21"/>',
         r'<w:lid w:val="ja-JP"/>',
         r'</w:rubyPr>',
         r'<w:rt>',
         r'<w:r w:rsidR="00E95970" w:rsidRPr="00E95970">',
         r'<w:rPr>',
         rf'<w:rFonts w:ascii="{font}" w:eastAsia="{font}" w:hAnsi="{font}" w:hint="eastAsia"/>',
         r'<w:sz w:val="10"/>',
         r'</w:rPr>',
         r'<w:t>'),  # 0 close
        # ここにルビ文字列（例：ふりがな）
        (r'</w:t>',
         r'</w:r>',
         r'</w:rt>',
         r'<w:rubyBase>',
         r'<w:r w:rsidR="00E95970">',
         r'<w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         r'</w:rPr>',
         r'<w:t>'),  # 1 close
        # ここにルビを振る文字列（例：振仮名）
        (r'</w:t>', r'</w:r>', r'</w:rubyBase>',
         r'</w:ruby>', r'</w:r>'),  # ルビ関連のタグここまで # 2 close
        (r'<w:r><w:rPr>',
         r'<w:rFonts w:hint="eastAsia"/>',
         r'</w:rPr><w:t>'),  # 3 close
        # ルビ振り処理対象外の余った文字列をここに
        (r'</w:t>', r'</w:r>')))  # 4 close

template = make_template()

testcode = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">連続する漢字《てすと》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
漢字《てすと》のテスト。
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode = f'''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
連続する
</w:t>
</w:r>
{template[0]}
てすと
{template[1]}
漢字
{template[2]}
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
</w:t>
</w:r>
{template[0]}
てすと
{template[1]}
漢字
{template[2]}
{template[3]}
のテスト。
{template[4]}
</w:p>
'''.splitlines()
