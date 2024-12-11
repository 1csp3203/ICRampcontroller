from Phidget22.Phidget import *
from Phidget22.Devices.RCServo import *
import time
import subprocess

class PhidgetServoController:
    def __init__(self, channel0=0, channel1=1 ,channel2=2, channel3=3):
        # モーター（サーボ）のチャンネルを作成
        self.rcServo0 = RCServo()  # 1つ目のモーター（チャンネル0）
        self.rcServo1 = RCServo()  # 2つ目のモーター（チャンネル1）
        self.rcServo2 = RCServo()  # 3つ目のモーター（チャンネル2）
        self.rcServo3 = RCServo()  # 4つ目のモーター（チャンネル3）

        # モーターのチャンネルを設定
        self.rcServo0.setChannel(channel0)
        self.rcServo1.setChannel(channel1)
        self.rcServo2.setChannel(channel2)
        self.rcServo3.setChannel(channel3)

        # # エラーハンドラを設定
        # self.rcServo0.setOnErrorHandler(self.onError)
        # self.rcServo1.setOnErrorHandler(self.onError)

        # モーターを開き、接続が完了するまで待機
        self.rcServo0.openWaitForAttachment(5000)
        self.rcServo1.openWaitForAttachment(5000)
        self.rcServo2.openWaitForAttachment(5000)
        self.rcServo3.openWaitForAttachment(5000)


    # def onError(self, code, description):
    #     # エラーが発生した場合の処理
    #     print(f"エラー発生: チャンネル {self.rcServo0.getChannel()} - コード: {ErrorEventCode.getName(code)}, 説明: {description}")
    #     print("----------")

    def initialize_motors(self):
        # モーターの初期位置を設定（例: 0度）
        self.set_position0(0)
        self.set_position1(0)
        self.set_position2(0)
        self.set_position3(0)

    @property
    def position0(self):
        return self.rcServo0.getPosition()

    @property
    def position1(self):
        return self.rcServo1.getPosition()

    @property
    def position2(self):
        return self.rcServo2.getPosition()

    @property
    def position3(self):
        return self.rcServo3.getPosition()

    def get_position0(self):
        # モーター0の現在の位置を取得
        return self.rcServo0.getPosition()

    def get_position1(self):
        # モーター1の現在の位置を取得
        return self.rcServo1.getPosition()

    def get_position2(self):
        # モーター2の現在の位置を取得
        return self.rcServo2.getPosition()

    def get_position3(self):
        # モーター2の現在の位置を取得
        return self.rcServo3.getPosition()

    def set_position0(self, position):
        # 1つ目のモーターの位置を設定
        self.rcServo0.setTargetPosition(position)
        self.rcServo0.setEngaged(True)  # モーターを作動状態にする

    def set_position1(self, position):
        # 2つ目のモーターの位置を設定
        self.rcServo1.setTargetPosition(position)
        self.rcServo1.setEngaged(True)  # モーターを作動状態にする

    def set_position2(self, position):
        # 3つ目のモーターの位置を設定
        self.rcServo2.setTargetPosition(position)
        self.rcServo2.setEngaged(True)  # モーターを作動状態にする

    def set_position3(self, position):
        # 4つ目のモーターの位置を設定
        self.rcServo3.setTargetPosition(position)
        self.rcServo3.setEngaged(True)  # モーターを作動状態にする

    def stop(self):
        # モーターを停止し、接続を閉じる
        self.rcServo0.setEngaged(False)
        self.rcServo1.setEngaged(False)
        self.rcServo2.setEngaged(False)
        self.rcServo3.setEngaged(False)
        self.rcServo0.close()
        self.rcServo1.close()
        self.rcServo2.close()
        self.rcServo3.close()

    def onPositionChange(self, position):
        # モーターの位置が変わった際に呼ばれる
        print(f"Position Changed: {position}")
        # ここでEPICS側に新しい位置を通知

    def get_SWR():
        try:
            # EPICSのレコードをcagetで取得
            swr = subprocess.check_output(["caget", "-t", "SWR"])
            swr = float(swr.strip())  # 結果を数値に変換
            return swr
        except Exception as e:
            print(f"Error getting SWR value: {e}")
            return None

    def optimize_reflection(self):
        step = 0.0001  # 微分ステップ
        e = 0.0001  # 収束条件
        tau = 0.5  # ラインサーチ用パラメータ
        beta = 0.5  # 学習率の縮小係数
        x = [self.get_position0()]  # 初期位置
        k = 1000  # 最大反復回数

        def calc(x):
            # 現在のモーター位置に基づいて反射値を取得
            self.set_position0(x[0])
            # self.set_position1(x[1])
            # self.set_position2(x[2])
            # self.set_position3(x[3])
            time.sleep(0.5)  # モーターが動くのを待つ
            return self.get_SWR()

        def bibun(step, x, k):
            high = []
            for i in range(len(x)):
                if i != k:
                    high.append(x[i])
                else:
                    high.append(x[i] + step)
            return (calc(high) - calc(x)) / step


        for i in range(k):
            #メインループ
            judge = False
            for j in range(len(x)):
                if abs(bibun(step, x, j)) > e:
                    judge = True
                    break
            if judge == False:
                break

            # ラインサーチ
            a = 1
            tempx = []
            for j in range(len(x)):
                tempx.append(x[j] - a * bibun(step, x, j))
            tempy = calc(tempx)
            tempgx = []
            for j in range(len(x)):
                tempgx.append(x[j] - step * bibun(step, x, j))
            tempgy = calc(x) + tau * ((calc(tempgx) - calc(x)) / step) * a

            while tempy > tempgy :
                a = a * beta
                for j in range(len(x)):
                    tempx[j] = (x[j] - a * bibun(step, x, j))
                tempy = calc(tempx)
                for j in range(len(x)):
                    tempgx[j] = (x[j] - step * bibun(step, x, j))
                tempgy = calc(x) + tau * ((calc(tempgx) - calc(x)) / step) * a

            # モーター位置を更新
            for j in range(len(x)):
                x[j] = x[j] - a * bibun(step, x, j)

        # 最終位置に移動
        self.set_position0(x[0])
        # self.set_position1(x[1])
        # self.set_position2(x[2])
        # self.set_position3(x[3])
        print(f"最小反射: {calc(x)}, 最適位置: {x}")
        