# ndlocrmd

https://github.com/ndl-lab/ndlocr-lite により生成されたXMLファイルから、mdファイルを作成するソフトです。

XMLファイルの`TYPE`が`タイトル本文`となっている文を、mdファイルの見出しとします。

文字の大きさで、見出しのサイズを変えます。

ndlocr-liteは、複数ページのpdfファイルを複数のXMLファイルにしますが、それらを1つのmdファイルにします。

### ndlxml2md.exe

usage: ndlxml2md [-h] [--sourcedir SOURCEDIR] [--sourcexml SOURCEXML] [--comma] --output OUTPUT

--sourcedir SOURCEDIR XMLファイルがあるディレクトリ名を指定します。

--sourcexml SOURCEXML XMLファイル名を指定します。

--comma 指定すると、文書内の`,` を `、` に変換します。

--output OUTPUT mdファイルを作成するフォルダ名を指定します。

### ndlxml2mdclick.exe

ファイルエクスプローラーなどで、ファイルやフォルダを右クリックすることにより、mdファイルを作成します。

文書内の`,` を `、` に変換します。

ndlxml2mdclick.exe を、
