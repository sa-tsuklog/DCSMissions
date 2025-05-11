DCS Worldの空対空ミッション生成ツールです。
テンプレートとなるミッションを元に以下の設定が可能です。
・戦闘空域を指定した場所、もしくはランダムな位置に移動します
・Blueの機体をRedにコピー
・1番機の武装・塗装を2～4番機にコピー　　→ミッションの武装等の管理について、Blueの1番機のみの設定で済みます。
・スポーン時点での距離を指定した値へ変更
・スポーン時点でのAI機の距離を指定した値へ変更
・スポーン時点での高度を指定した値へ変更
・時刻、天候などを変更
・BDAのON/OFF


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


マップをCaucasusに固定し、ミッションを生成、交戦距離60nm、AWACSの距離150nm、交戦地点TbilishiとSukhumiの中間地点に設定


    python3 SumouFieldGenerator.py --theatre Caucasus --distance 60 --AWACSdistance 150 --airport Tbilishi,Sukhumi


マップをCaucasusに固定し、ミッションを生成、交戦距離60nm、AWACSの距離150nm、交戦地点の座標をKobuleti空港座標(-328299,631261)に設定


    python3 SumouFieldGenerator.py --theatre Caucasus --distance 60 --AWACSdistance 150  --ccspos " -328299,631261,90"


マップをCaucasusに固定し、ミッションを生成、交戦距離60nm、AWACSの距離150nm、交戦地点の座標をKobuleti空港座標(-328299,631261)、Blueの位置を90度方向に設定


    python3 SumouFieldGenerator.py --theatre Caucasus --distance 60 --AWACSdistance 150  --ccspos " -328299,631261,90"



マップをCaucasusに固定し、ミッションを生成、生成するファイル名のprefixとして"BVR_PLAIN"を設定、SatacMissionBase_v1.5.0を元に生成。
交戦距離80nm、AWACSの距離140nm、全ての季節から選択。雲無し、BDA ON、交戦地点TbilishiとSukhumiの中間地点に設定


    python3 SumouFieldGenerator.py --theatre Ca --fileprefix BVR_PLAIN --template SatacMissionBase_v1.5.0 --cloud clear  --wind 0.0 --distance 80 --AWACSdistance 140 --date all --bda ture --airport Tbilishi,Sukhumi



## 引数：
マップ　--theatre
　　現在、以下のマップに対応  
    [Caucasus, Nevada, PersianGulf, Syria]

基地名　--airport
    引数無しでランダム配置。
    allで全ての基地からランダムに選ばれた2つの中間地点
    1つのみの指定の場合は指定された基地の位置
    基地名1,基地名2で基地の中間地点。3つ以上の基地が指定された場合は、指定された中からランダムに選ばれた2つの中間地点。

座標　--ccspos
    戦闘空域の座標による指定。X,YもしくはX,Y,方位の2パターンにて指定可能。
    CCS座標はミッションエディタにて、左下に表示される座標の形式をCCSとすることで取得可能。

距離　--distance
    ユーザー機のスタート時点での距離 [nm]

AI機の距離　--AWACSdistance
    AI機のスタート時点での距離 [nm]

雲　--cloud
    雲の指定。clear|cloudy|rainy|allの何れか

風　--wind
    風速 [m/s]

テンプレート  --template
    テンプレートとなるミッションファイルの指定。mizファイルをzipとして展開したディレクトリ名を指定する。

出力ファイル名  --fileprefix
    出力ファイル名のprefixを指定する

季節  --data
    ミッションの季節を指定する。today|spring|summer|autumn|winter|allの何れか

高度  --alt
    スタート時点での高度[ft]を指定する。

BDA --bda
    BDAのON/OFFを指定する。default(元ミッションから変更なし)|true(BDA有効へ変更)|false(無効へ変更)の何れか

---
# Advanced:
TemplateMission内にDCSで作成したミッション(.miz)をzipで展開したものが入っており、
その中身を変更すればミッションの内容も変更されます。
    
