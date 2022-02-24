
import platform


def make_template():
    pf = platform.system()
    if pf == 'Windows':
        font = 'ＭＳ 明朝'
    elif pf == 'Darwin':
        font = 'ヒラギノ明朝 ProN '
    elif pf == 'Linux': #Linux環境の場合はOSごとに標準でインストールされてるフォントが違うので要改善
        font = 'Noto Serif CJK JP'
    else: #その他の結果が出た場合
        font = 'Noto Serif CJK JP'
    return (
    r"""
<w:r>
<w:ruby>
<w:rubyPr>
<w:rubyAlign w:val="distributeSpace"/>
<w:hps w:val="10"/>
<w:hpsRaise w:val="18"/>
<w:hpsBaseText w:val="21"/>
<w:lid w:val="ja-JP"/>
</w:rubyPr>
<w:rt>
<w:r w:rsidR="00E95970" w:rsidRPr="00E95970">
<w:rPr>
<w:rFonts w:ascii="{0}" w:eastAsia="{0}" w:hAnsi="{0}" w:hint="eastAsia"/>
<w:sz w:val="10"/>
</w:rPr>
<w:t>
""".format(font),  # ここにルビ文字列（例：ふりがな）
    r"""
</w:t>
</w:r>
</w:rt>
<w:rubyBase>
<w:r w:rsidR="00E95970">
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
""",  # ここにルビを振る文字列（例：振仮名）
    r"""
</w:t>
</w:r>
</w:rubyBase>
</w:ruby>
</w:r>
""",  # ルビ振り処理対象外の余った文字列を↓に（ここには何も入れない）
    r"""
<w:r><w:rPr><w:rFonts w:hint="eastAsia"/></w:rPr><w:t>
""",  # ルビ振り処理対象外の余った文字列をここに
    r"""</w:t></w:r>""")

# <w:r>タグで囲まれた文字列（<w:r>を含む）を取得するパターン
get_wr = r'<w:r>(?:(?!<w:r>|</w:r>).)*</w:r>'
# 《》内の文字列取得用パターン
get_ruby = r'(?<=《).*?(?=》)'
# 《》の前後で文字列分割
split_reg = r'《.*?》'
# タグにマッチするパターン
tag_reg = r'<[^<>]*>'
