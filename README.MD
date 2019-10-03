# Hayaoshi on Raspi

ラズパイ を使って簡単な早押し機を作る．



## 概要

* Raspberry Piを用いて早押しクイズの装置を作成．
* 子機はボタン+LED,親機はターミナルで操作．
* 最初に押した人のLEDのみが点滅するが，2着目以降も記録しており，$i$着目が誤答した時には，$i+1$着目のLEDが点滅．



## 試した環境

* Device: Raspberry Pi 3 Model B+ (2018)
* Distribution: Raspbian GNU/Linux 9.11
* Python: Python 3.5.3



## 操作方法

* main.py の30行目あたりの3種類の変数を設定します．
  * N: 子機の数
  * inpin: スイッチの入力に使うGPIOのピン番号を書きます．
  * output: LEDの出力に使うGPIOのピン番号を書きます．
* main.pyを実行します．子機のボタンを押すと色々変化すると思います．
* ターミナルで標準入力を行なって操作します．
  * o: 正解してリセット
  * x:誤答．次に押した人のLEDが点滅
  * r:リセット
  * e:終了

※ ボタンはプルダウン抵抗にしています．



## 今後の予定

* 音をつける．
* PCに状態などを送り，それを得点表示などに反映できるようにする．
