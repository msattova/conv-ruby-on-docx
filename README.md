# conv-ruby-on-docx

カクヨム記法で示されたルビをWordのルビにするツールです。

![sample](./picts/sample.png)

だいたいこんな感じのことができます（文章は拙作[『誰が為の歴史改変』](https://note.com/msattova/n/n5981d867920d?magazine_key=mb9a82abba305)より）

開発中につき、様々な問題を抱えています。ご了承下さい。

## プログラムの実行に必要なもの

* python : v3.10.1
* beautifulsoup4 : v4.10.0
* lxml : v4.8.0

（バージョンは製作者の環境のもの。このバージョンでないといけないというわけではありませんが、現在、他のバージョンで動作するかは確認できていません）

requirements.txtをダウンロードして`pip install -r requirements.txt`コマンドを実行すれば必要なパッケージを一括でインストールできます。

## 使い方

`py main.py input.docx`

`input.docx`はカクヨム記法でルビを振ったdocxファイルです。

このプログラムを実行するとカクヨム記法でルビを振った箇所がWordのルビに変換されたファイル`out.docx`が生成されます。

### 利用上の注意点

* 本プログラムを実行する際は、実行ディレクトリに`'_rels','customXml','docProps','word', '[Content_Types].xml'`がないことを確認の上で実行してください。
* 変換元のdocxファイルの解析が上手くいかなる可能性があるため、Wordファイル上での編集作業は極力避けてください。**別のツール（テキストエディタ等）で書いた文章をWord上にコピペすることを推奨します**。
* カクヨムでは`漢字《かんじ》`としてもきちんとルビが振られますが、本プログラムは現在、`|漢字《かんじ》`という記法にしか対応していません。（今後修正予定）
* 本プログラムは現在、`《《傍点を振る》》`のような、テキストを`《《`と`》》`で囲んで傍点をふる記法に対応していません。（今後修正予定）

## 今後のアップデート予定

* OSごとにルビのフォント設定を変更 （issue #1）
* ~~行頭の空白文字が削除される問題の解決 (issue #3)~~
* `漢字《かんじ》`記法への対応
* `《《傍点を振る》》`記法への対応
* 小説の文章が書かれたtxtファイルとテンプレートdocxファイルを入力として受け取ってdocxファイルを出力するような使い方もできるようにする（pandocみたいな感じ）
* GUI化する
* exeファイルにする
