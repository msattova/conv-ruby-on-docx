

testcode2 = ['<w:p w14:paraId="27E1BD8D" w14:textId="77777777" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t xml:space="preserve">',
             '　ただの地の文。',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '|',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '親文字',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '《',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             'おやもじ',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '》',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '　地の文2',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '|',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '文章《ぶんしょう》の中のルビ',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '|',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '親文字がひらがな',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '《',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '二重に読みがあるやつ',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '》',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             'のテスト。',
             '</w:t>',
             '</w:r>',
             '</w:p>',
             '<w:p w14:paraId="1A318B7D" w14:textId="77777777" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t xml:space="preserve">',
             '　',  # 行頭に|親文字が来るパターン
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '|',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '行頭親文字《',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             'しょっぱなからくる',
             '</w:t>',
             '</w:r>',
             '<w:r>',
             '<w:rPr>',
             '<w:rFonts w:hint="eastAsia"/>',
             '</w:rPr>',
             '<w:t>',
             '》',
             '</w:t>',
             '</w:r>',
             '</w:p>']


idealcode2 = ['<w:p w14:paraId="27E1BD8D" w14:textId="77777777" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t xml:space="preserve">',
              '　ただの地の文。',
              '</w:t>',
              '</w:r>',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t>',
              '|親文字《おやもじ》',
              '</w:t>',
              '</w:r>',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t>',
              '　地の文2',
              '</w:t>',
              '</w:r>',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t>',
              '|文章《ぶんしょう》の中のルビ',
              '</w:t>',
              '</w:r>',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t>',
              '|親文字がひらがな《二重に読みがあるやつ》',
              '</w:t>',
              '</w:r>',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t>',
              'のテスト。',
              '</w:t>',
              '</w:r>',
              '</w:p>',
              '<w:p w14:paraId="1A318B7D" w14:textId="77777777" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t xml:space="preserve">',
              '　',  # 行頭に|親文字が来るパターン
              '</w:t>',
              '</w:r>',
              '<w:r>',
              '<w:rPr>',
              '<w:rFonts w:hint="eastAsia"/>',
              '</w:rPr>',
              '<w:t>',
              '|行頭親文字《しょっぱなからくる》',
              '</w:t>',
              '</w:r>',
              '</w:p>']


testcode3 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
　鮮血が吹き上がる――倉持《
</w:t>
</w:r>
<w:r w:rsidR="00552D32">
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
てすと
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
|
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
廻《めぐる》は身構えたが、そうはならなかった。
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
<w:t xml:space="preserve">　鮮血が吹き上がる――倉持《てすと》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
|
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
廻《めぐる》は身構えたが、そうはならなかった。
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
<w:t xml:space="preserve">
　鮮血が吹き上がる――倉持《
</w:t>
</w:r>
<w:r w:rsidR="00552D32">
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
てすと
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
|
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
廻《めぐる》は身構えたが、そうはならなかった。
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
<w:t xml:space="preserve">　鮮血が吹き上がる――倉持《てすと》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
|廻《めぐる》は身構えたが、そうはならなかった。
</w:t>
</w:r>
</w:p>
'''.splitlines()


testcode5 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
傍点がある《《場合について》》テスト
</w:t>
</w:r>
<w:r w:rsidR="00552D32">
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
《《
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
さらにテスト
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
》》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
普通のやつ漢字《おまけ》。
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode5 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
傍点がある《《場合について》》テスト
</w:t>
</w:r>
<w:r w:rsidR="00552D32">
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
《《さらにテスト》》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
普通のやつ漢字《おまけ》。
</w:t>
</w:r>
</w:p>
'''.splitlines()


testcode6 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
文章が途中でなんか《《途切れ
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
てる感じ》》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
ルビの場合についても|やっておく
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
ことにする《チェック》。
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode6 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
文章が途中でなんか《《途切れてる感じ》》
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
ルビの場合についても|やっておくことにする《チェック》。
</w:t>
</w:r>
</w:p>
'''.splitlines()


testcode7 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
間になんか《《タブ文字
</w:t>
</w:r>
<w:r>
<w:rPr>
<w:tab/>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t>
が挟まっている》》奴
</w:t>
</w:r>
</w:p>
'''.splitlines()

idealcode7 = '''
<w:p w14:paraId="1A318B7D" w14:textId="6C78F7B3" w:rsidR="00EE3670" w:rsidRDefault="00EE3670" w:rsidP="00EE3670">
<w:r>
<w:rPr>
<w:rFonts w:hint="eastAsia"/>
</w:rPr>
<w:t xml:space="preserve">
間になんか《《タブ文字\tが挟まっている》》奴
</w:t>
</w:r>
</w:p>
'''.splitlines()


