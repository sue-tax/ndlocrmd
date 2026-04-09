# ndlocrmd

https://github.com/ndl-lab/ndlocr-lite により生成されたXMLファイルから、MDファイルを作成するソフトです。

XMLファイルの`TYPE`が`タイトル本文`となっている文を、MDファイルの見出しとします。

MDファイルその他のファイルのファイル名を、最初のタイトル本文に変更するかなどは、ダイアログボックスで指定します。

文字の大きさで、見出しのサイズを変えます。

ndlocr-liteは、複数ページのPDFファイルを複数のXMLファイルにしますが、それらを1つのMDファイルにします。

version0.12 複数ページをソートしてから処理するように変更

### ndlxml2md.exe

usage: ndlxml2md [-h] [--sourcedir SOURCEDIR] [--sourcexml SOURCEXML] [--comma] --output OUTPUT

--sourcedir SOURCEDIR XMLファイルがあるディレクトリ名を指定します。

--sourcexml SOURCEXML XMLファイル名を指定します。

--comma 指定すると、文書内の`,` を `、` に変換します。

--output OUTPUT MDファイルを作成するフォルダ名を指定します。

### ndlxml2mdclick.exe

ファイルエクスプローラーなどで、ファイルやフォルダを右クリックすることにより、MDファイルを作成します。

文書内の`,` を `、` に変換します。

#### インストール方法

ndlxml2mdclick.exe を、下記などを参考に`SendTo`フォルダにコピーしてください。

https://atmarkit.itmedia.co.jp/ait/articles/1109/30/news131.html
