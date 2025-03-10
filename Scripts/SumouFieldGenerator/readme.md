DCS Worldの空対空ミッション生成ツールです。

# 使用方法:
    python3 SumouFileGenerator.py [map名]

## 例：  

    python3 SumouFileGenerator.py --theatre=Caucasus,Nevada,PersianGulf,Syria  
Caucasus,Nevada,PersianGulf,Syriaの中からランダムにマップを選択しミッションを生成  


    python3 SumouFileGenerator.py --theatre=Caucasus


マップをCaucasusに固定しミッションを生成  


    python3 SumouFileGenerator.py


引数を省略した場合はSumouFileGenerator.pyが現在対応しているマップの中からランダムに選択される  


    python3 SumouFileGenerator.py --theatre=Caucasus


マップをCaucasusに固定しミッションを生成、交戦距離60nm  


    python3 SumouFileGenerator.py --theatre=Caucasus --distance=60


マップをCaucasusに固定しミッションを生成、交戦距離60nm、AWACSの距離150nm  


    python3 SumouFileGenerator.py --theatre=Caucasus --distance=60 --AWACSdistance=150


## 引数：
現在、以下のマップに対応  
    [Caucasus, Nevada, PersianGulf, Syria]


基地名　--airport
    引数無しでランダム配置。
    allで全ての基地からランダムに選ばれた2つの中間地点
    1つのみの指定の場合は指定された基地の位置
    基地名1,基地名2で基地の中間地点。3つ以上の基地が指定された場合は、指定された中からランダムに選ばれた2つの中間地点。

---
# Advanced:
TemplateMission内にDCSで作成したミッション(.miz)をzipで展開したものが入っており、
その中身を変更すればミッションの内容も変更されます。
    
    
SumouFieldGenerator.pyではTemplateMissionのミッションから以下の修正を加えたファイルを生成します。
    
* ブルズアイをランダムな位置に設定  
* ブルズアイを中心にランダムな角度、一定の距離になるようBLUE,REDのclient機体を再配置  
* client機体の後ろにそれ以外の機体を再配置  
* すべての基地に対し、陣営を変更  
    
    
TemplateMissionを差し替えれば機体の追加、武装の変更が可能なはずです(未テスト)
    
