testcode = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
独立した漢字《かんじ》のテスト。
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
独立した
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
漢字《かんじ》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
のテスト。
</w:t>
</w:r>
</w:p>
'''.splitlines()

testcode2 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
連続する漢字《てすと》漢字《てすと》のテスト。
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode2 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
連続する
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
漢字《てすと》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
漢字《てすと》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
のテスト。
</w:t>
</w:r>
</w:p>
'''.splitlines()

testcode3 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
独立した漢字《いっこめ》のテスト。#1
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
独立した漢字《にこめ》のテスト。#2
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode3 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
独立した
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
漢字《いっこめ》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
のテスト。#1
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
独立した
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
漢字《にこめ》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
のテスト。#2
</w:t>
</w:r>
</w:p>
'''.splitlines()


testcode4 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
|パイプつき漢字《文章っぽい》のテスト。
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
パイプつき|漢字《漢字だけ》のテスト。
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode4 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
|パイプつき漢字《文章っぽい》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
のテスト。
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
パイプつき
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
|漢字《漢字だけ》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
のテスト。
</w:t>
</w:r>
</w:p>
'''.splitlines()