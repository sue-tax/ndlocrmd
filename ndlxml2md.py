
# https://github.com/ndl-lab/ndlocr-lite により生成された
# XMLファイルから、mdファイルを作成する

__version__ = 0.10

from lxml import etree 
import glob
import os
import re

# import c
# import d

# TEXTBLOCKを重視する？　ORDERは無視？
# 図版も不要かも

# ファイル名をトップタイトルに変更する
# pdfへのハイパーリンクを設定する
# TODO 範囲指定　右側の法人税を外すなど

# `,` を置換する文字
CHANGE_COMMA = '、'

FONT_SIZE_1 = 70
FONT_SIZE_2 = 55
FONT_SIZE_3 = 40
FONT_SIZE_4 = 25
FONT_SIZE_5 = 15

# rawinputpathlist 対象となるファイルのリスト
# change_comma `,` を置換する文字
# output_dir MDファイルを出力するディレクトリ
def process_main(rawinputpathlist, change_comma, output_dir):
    # ndlocr-liteは、`xxxxx.pdf`というPDFファイルを
    # `xxxxx_0000.xml`, `xxxxx_0001.xml`のように、
    # ページごとにXMLファイルを生成する 
    
    # ただし、元々がxxx.yyy.pdfならば、
    # ndlocr-lite は,xxx.xmlとして最後のページだけになる
    
    # dict_group : 同じPDFファイルに対応するXMLファイルのグループ
    dict_group = {}
    # cnt_file : 対象となるXMLファイルの数
    cnt_file = 0
    for inputpath in rawinputpathlist:
        # 拡張子
        ext=inputpath.split(".")[-1]
        if ext in ["xml","XML"]:
            # ディレクトリ名とファイル名
            base_dir_pair = os.path.split(inputpath)
            # 拡張子を除いたファイル名
            basename_without_ext = os.path.splitext(base_dir_pair[1])
            m = re.search(r"(.+)(_[0-9]+)", basename_without_ext[0])
            if m:
                # `xxxxx_nnnnn`という形式のファイル名
                # m.group(1) : xxxxx
                list_xml_file = dict_group.get(m.group(1))
                if list_xml_file == None:
                    list_xml_file = [inputpath]
                else:
                    list_xml_file.append(inputpath)
                dict_group[m.group(1)] = list_xml_file
                cnt_file += 1
    if cnt_file == 0:
        print("xml file are not found.")
        return

    # 確認済フラグをクリア
    flag_confirm = False
    
    for base, list_xml_file in dict_group.items():
        # 同じPDFファイルに対応するXMLファイルのグループ
        # 毎に処理する
        
        # base : xxxxx PDFファイル名（拡張子なし）
        
        # allmdlist : 作成するMDファイルに書き込む文字列のリスト
        allmdlist = []

        # 複数の行を１つの行に纏めるための変数
        # 纏める処理は完全ではない
        flag_top = True
        flag_title = False
        size_title = 0
        flag_honbun = False
        flag_touten = True # 「。」で終わったか
        flag_zuban = False

        # 最初のタイトル本文をファイル名候補にする
        # ためのフラグ
        flag_top_title = True

        # TODO list_fileのソート
        # path\xxxxx_nnnnn.xml を nnnnn でソートする

        # 最初のタイトル本文をファイル名候補にする
        # dirname : XMLファイルがあるディレクトリ名
        dirname = os.path.dirname(list_xml_file[0])
        
        file_title = base   # タイトル本文がないときのため
        
        for xml_file in list_xml_file:
            # xml_file : XMLファイルのファイルパス名
            
            tree = etree.parse(xml_file)
            root = tree.getroot()
            
            # 「図版」毎にまとめて処理したかったが、
            # それほど上手く機能していない
            nodes_zuban = root.xpath(".//*[@TYPE='図版']")
            list_zuban = []
            for node_zuban in nodes_zuban:
                d.dprint(node_zuban)
                list_zuban.append((
                        int(node_zuban.attrib["X"]),
                        int(node_zuban.attrib["Y"]),
                        int(node_zuban.attrib["X"])
                                +int(node_zuban.attrib["WIDTH"]),
                        int(node_zuban.attrib["Y"])
                                +int(node_zuban.attrib["HEIGHT"])
                        ))
            
            # nodes : MDファイルに書き出す対象となる文字列のノード
            nodes = root.xpath(".//*[@TYPE='本文'" \
                    " or @TYPE='タイトル本文'"\
                    " or @TYPE='キャプション']")
            nodes.sort(key=sort_order)
            
            for node in nodes:
                left = int(node.attrib["X"])
                top = int(node.attrib["Y"])
                right = left + int(node.attrib["WIDTH"])
                bottom = top + int(node.attrib["HEIGHT"])
                check_zuban = False
                for zuban in list_zuban:
                    # if (left >= zuban[0]) and (right <= zuban[2]) \
                    #         and (top >= zuban[1]) \
                    #         and (bottom <= zuban[3]):
                    if (left < zuban[2]) and (right > zuban[0]) \
                            and (top < zuban[3]) \
                            and (bottom > zuban[1]):
                        # 少しでも、引っかかれば
                        check_zuban = True
                if check_zuban:
                    # 図版内の文字列は前後に`---`を付ける
                    d.dprint("図版内")
                    if not flag_zuban:
                        allmdlist.append("\n")
                        allmdlist.append("---")
                        flag_zuban = True
                        flag_title = False
                        flag_honbun = False
                    str_change = node.attrib["STRING"] \
                            .replace(',', change_comma)
                    allmdlist.append(str_change)
                    
                elif node.attrib["TYPE"] == 'タイトル本文':
                    if flag_top_title:
                        # file_title : 候補となるファイル名
                        file_title = node.attrib["STRING"] \
                                .replace(' ', '_')
                        flag_top_title = False
                    if flag_zuban:
                        allmdlist.append("\n")
                        allmdlist.append("---")
                        flag_zuban = False
                    height = int(node.attrib["HEIGHT"])
                    width = int(node.attrib["WIDTH"])
                    font_size = min(height, width)
                    if not flag_title:
                        if not flag_top:
                            allmdlist.append("\n")
                        str_change = node.attrib["STRING"] \
                                .replace(',', change_comma)
                        # フォントサイズにより、見出しのレベルを決める
                        # サイズの区切りに、根拠はない
                        if font_size > FONT_SIZE_1:
                            allmdlist.append("# " + str_change)
                        elif font_size > FONT_SIZE_2:
                            allmdlist.append("## " + str_change)
                        elif font_size > FONT_SIZE_3:
                            allmdlist.append("### " + str_change)
                        elif font_size > FONT_SIZE_4: #30:
                            allmdlist.append("#### " + str_change)
                        elif font_size >= FONT_SIZE_5: #> 20:
                            allmdlist.append("##### " + str_change)
                        else:
                            allmdlist.append("###### "  + str_change)
                        size_title = font_size
                    else:
                        # 前の行とほぼ同じフォントサイズならば、
                        # １行として結合する
                        if (font_size <= size_title+1) \
                                and (font_size >= size_title-1):
                            str_title = allmdlist.pop(-1)
                            str_title += node.attrib["STRING"] \
                                    .replace(',', change_comma)
                            allmdlist.append(str_title)
                        else:
                            str_change = node.attrib["STRING"] \
                                    .replace(',', change_comma)
                            # フォントサイズにより、見出しのレベルを決める
                            # サイズの区切りに、根拠はない
                            if font_size > FONT_SIZE_1:
                                allmdlist.append("# " + str_change)
                            elif font_size > FONT_SIZE_2:
                                allmdlist.append("## " + str_change)
                            elif font_size > FONT_SIZE_3:
                                allmdlist.append("### " + str_change)
                            elif font_size > FONT_SIZE_4: #30:
                                allmdlist.append("#### " + str_change)
                            elif font_size >= FONT_SIZE_5: #> 20:
                                allmdlist.append("##### " + str_change)
                            else:
                                allmdlist.append("###### "  + str_change)
                            size_title = font_size
                    flag_title = True
                    flag_honbun = False
                elif node.attrib["TYPE"] == '本文':
                    if flag_zuban:
                        allmdlist.append("\n")
                        allmdlist.append("---")
                        flag_zuban = False
                    if not flag_honbun:
                        allmdlist.append("\n")
                    if flag_honbun and (not flag_touten):
                        # 前の行も本文で、
                        # 前の行の最後が`。`でなければ
                        # １つの行として結合する
                        # 適切でない場合もある。
                        str_title = allmdlist.pop(-1)
                        str_title += node.attrib["STRING"] \
                                .replace(',', change_comma)
                        allmdlist.append(str_title)
                    else:
                        if flag_touten:
                            # 前の行の最後が`。`ならば、
                            # 先頭に全角空白を入れる
                            # 適切でない場合もある
                            allmdlist.append(
                                    "　" + node.attrib["STRING"])
                        else:
                            str_change = node.attrib["STRING"] \
                                    .replace(',', change_comma)
                            allmdlist.append(str_change)
                    flag_honbun = True
                    if node.attrib["STRING"][-1] == "。":
                        flag_touten = True
                    else:
                        flag_touten = False
                    flag_title = False
                else:
                    if flag_zuban:
                        allmdlist.append("\n")
                        allmdlist.append("---")
                        flag_zuban = False
                    allmdlist.append("\n")
                    str_change = node.attrib["STRING"].replace(',', change_comma)
                    allmdlist.append(str_change)
                    flag_title = False
                    flag_honbun = False
                flag_top = False
                
        if not flag_confirm:
            dialog_rename(base, file_title)
            if flag_ok:
                file_title = new_file_name
                if flag_all:
                    flag_confirm = True
            else:
                if flag_all:
                    break
                else:
                    continue
        else:
            if flag_ok:
                 pass

        # pdf_file_name : 想定したPDFファイルパス名
        pdf_file_name = os.path.join(dirname,
                file_title+".pdf")

        if flag_pdf:
            try:
                os.rename(os.path.join(dirname, base+".pdf"), \
                        pdf_file_name)
                allmdlist.append("\n[pdf]({0})\n".
                        format(file_title+".pdf"))
            except Exception as e:
                allmdlist.append("\n[pdf]({0})\n".
                        format(base+".pdf"))
        else:
                allmdlist.append("\n[pdf]({0})\n".
                        format(base+".pdf"))
            
        if flag_xml:
            rename_all(dirname, base, "xml", file_title)
        if flag_txt:
            rename_all(dirname, base, "txt", file_title)
        if flag_jpg:
            rename_all_jpg(dirname, base, file_title)

        if flag_md:
            md_file_title = file_title
        else:
            md_file_title = base
        with open(os.path.join(output_dir,
                md_file_title+".md"),"w",encoding="utf-8") as wtf:
            wtf.write("\n".join(allmdlist))


def rename_all( dirname, old_name, ext, new_name ):
    file_name = os.path.join(dirname, old_name+"_?????."+ext)
    files = glob.glob(file_name)
    for file in files:
        new_file = file.replace(old_name, new_name)
        os.rename(file, new_file)

def rename_all_jpg( dirname, old_name, new_name ):
    file_name = os.path.join(dirname,
            "viz_"+old_name+"_?????.jpg")
    files = glob.glob(file_name)
    for file in files:
        new_file = file.replace("viz_"+old_name, new_name)
        os.rename(file, new_file)

    
def sort_order( node ):
    return int(node.attrib["ORDER"])

def dialog_rename( base, new_file_name ):
    global flag_ok, flag_all
    flag_ok = False
    flag_all = False
    
    import tkinter as tk

    root = tk.Tk()
    
    root.title('ファイル名変更')
    root.geometry('500x130')
    
    old_label = tk.Label(text='現在ファイル名')
    old_label.grid(row=1, column=1, padx=10)
    
    old_file = tk.Entry(width=50)
    old_file.insert(0, base)
    old_file.config(state='readonly')
    old_file.grid(row=1, column=2)
    
    new_label = tk.Label(text='候補ファイル名')
    new_label.grid(row=2, column=1, padx=10)
    
    new_file = tk.Entry(width=50)
    new_file.insert(0, new_file_name)
    new_file.grid(row=2, column=2)
    
    ValPdf = tk.BooleanVar()
    ValMd = tk.BooleanVar()
    ValXml = tk.BooleanVar()
    ValTxt = tk.BooleanVar()
    ValJpg = tk.BooleanVar()
    
    ValPdf.set(True)
    ValMd.set(True)
    ValXml.set(False)
    ValTxt.set(False)
    ValJpg.set(False)
    
    CheckBoxPdf = tk.Checkbutton(text=u"PDF", variable=ValPdf)
    CheckBoxPdf.grid(row=3, column=1)
    
    CheckBoxMd = tk.Checkbutton(text=u"MD", variable=ValMd)
    CheckBoxMd.grid(row=3, column=2)
    
    CheckBoxXml = tk.Checkbutton(text=u"XML", variable=ValXml)
    CheckBoxXml.grid(row=3, column=3)

    CheckBoxTxt = tk.Checkbutton(text=u"TXT", variable=ValTxt)
    CheckBoxTxt.grid(row=4, column=1)
    
    CheckBoxJpg = tk.Checkbutton(text=u"JPG", variable=ValJpg)
    CheckBoxJpg.grid(row=4, column=3)

    buttonAll = tk.Button(text='  All OK  ',
            command=lambda: close_window(root, True, True,
            new_file, ValPdf, ValMd, ValXml, ValTxt, ValJpg))
    buttonAll.place(x=40, y=100)
    
    button = tk.Button(text='    OK    ',
            command=lambda: close_window(root, True, False,
            new_file, ValPdf, ValMd, ValXml, ValTxt, ValJpg))
    button.place(x=140, y=100)
    
    buttonCancel = tk.Button(text='  Cancel  ',
            command=lambda: close_window(root, False, False,
            new_file, ValPdf, ValMd, ValXml, ValTxt, ValJpg))
    buttonCancel.place(x=240, y=100)
    
    buttonCancelAll = tk.Button(text='Cancel All',
            command=lambda: close_window(root, False, True,
            new_file, ValPdf, ValMd, ValXml, ValTxt, ValJpg))
    buttonCancelAll.place(x=340, y=100)
    
    root.mainloop()


def close_window(root, flagOK, flagAll,
            new_file, ValPdf, ValMd, ValXml, ValTxt, ValJpg):
    global flag_ok, flag_all
    global new_file_name
    global flag_pdf, flag_md, flag_xml, flag_txt, flag_jpg
    flag_ok = flagOK
    flag_all = flagAll
    new_file_name = new_file.get()
    flag_pdf = ValPdf.get()
    flag_md = ValMd.get()
    flag_xml = ValXml.get()
    flag_txt = ValTxt.get()
    flag_jpg = ValJpg.get()
    root.destroy()


def main():
    import argparse
    from pathlib import Path
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Arguments for NdlXml2md")
    parser.add_argument("--sourcedir", type=str, required=False, help="Path to xml directory")
    parser.add_argument("--sourcexml", type=str, required=False, help="Path to xml file")
    parser.add_argument("--comma", action='store_true', required=False, help="`,` を `、` に変換")
    parser.add_argument("--output", type=str, required=True, help="Path to output directory")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        print("Output Directory is not found.")
        return

    # 対象となるファイルのリスト
    rawinputpathlist=[]
    if args.sourcedir is not None:
        for inputpath in glob.glob(os.path.join(args.sourcedir,"*")):
            rawinputpathlist.append(inputpath)
    if args.sourcexml is not None:
        rawinputpathlist.append(args.sourcexml)
    change_comma = ','
    if args.comma is not None:
        change_comma = CHANGE_COMMA

    process_main(rawinputpathlist, change_comma, args.output)

if __name__=="__main__":
    main()
