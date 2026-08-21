python
from codrone_edu.drone import *
import time, heapq, statistics

# this is the stat class
# これは統計データのクラスです
class FlightStats:
    # pilot name, the flight time, the minimum and maximum speed, the acceleration and var with average (maybe)
    # パイロットの名前、飛行時間、最低速度と最高速度、加速度、そして平均値の分散（たぶん）
    def __init__(self, pilotName, flightTime,
                 minSpeed, maxSpeed, maxAccel,
                 yaw_Var, max_Alt):
        # avg_alt just case we need average altitude
        # 平均高度が必要になった場合のためです

        self.pilotName = pilotName
        self.flightTime = flightTime
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.maxAccel = maxAccel
        self.yaw_Var = yaw_Var
        self.max_altitude = max_Alt
        # self.avg_altitude = avg_alt just in case
        # 必要になった場合のために平均高度を保存します

    # LT = less than (needed for heap comparisons)
    # LTは「less than（より小さい）」の意味です（ヒープで比較するために必要です）
    def __lt__(self, different):
        return self.flightTime < different.flightTime

    # str = string
    # f is the print of python
    # strは「string（文字列）」の意味です
    # f-stringを使ってPythonでデータを表示します
    def __str__(self):
        return (f"{self.pilotName:<12} || "  # our names
                # パイロットの名前を表示します
                f"Time: {self.flightTime:.2f}s || "  # how long the flight is
                # 飛行時間を表示します
                f"Speed(min/max): {self.minSpeed:.2f}/{self.maxSpeed:.2f} cm/s || "  # how fast the flight is
                # 飛行速度を表示します
                f"Max accel: {self.maxAccel:.2f} cm/s^2 || ")  # the acceleration of the flight
                # 飛行中の最大加速度を表示します
        # just in case we need the average -- f"Alt(avg/max): {self.avg_alti:.2f}/{self.max_alti:.2f} cm")
        # 平均高度が必要になった場合 -- 平均高度と最高高度を表示します


# minimum heap leaderboard (this is what our data goes to)
# 最小ヒープのランキングです（飛行データをここに保存します）
class flightHeap:
    def __init__(self):
        self.heap = []

    def insert(self, flightStats):
        # skip short flights Practice a.k.a (crashes)
        # 短い飛行は練習飛行、つまり墜落した可能性があるためスキップします
        if flightStats.flightTime > 2.0:  # only count real flights > 2 seconds
            # 2秒より長い実際の飛行だけを記録します
            heapq.heappush(self.heap, flightStats)

    # printing the leaderboard lb
    # ランキング（lb）を表示します
    def print_lb(self):
        print("\n===> Racing Leaderboard!!! <===")
        # sort heap by flight time (fastest first)
        # 飛行時間でヒープを並べ替えます（速い順）
        ranked = sorted(self.heap, key=lambda x: x.flightTime)
        for i, fs in enumerate(ranked, start=1):
            print(f"{i}. {fs}")  # prints each FlightStats object using __str__
            # __str__を使って各FlightStatsオブジェクトを表示します


# this is for collecting the flight data
# これは飛行データを収集するための関数です
def cfd(pilotName, practice=False):
    drone = Drone()
    drone.pair()  # connects to drone
                # ドローンに接続します

    print(f"\n Beggining the flight for {pilotName} {'(practice)' if practice else ''}...")
    speeds, yaws, alts, times = [], [], [], []  # lists to store flight data
    # 飛行データを保存するためのリストです

    startTime = time.time()

    flying = True
    landed = False
    crashed = False  # new flag for crash detection
    # 墜落を検知するためのフラグです

    #button check function
    # ボタンを確認する関数です
    def check_buttons():
        nonlocal flying, landed
        if drone.l1_pressed():
            drone.takeoff()
            print("takeoff")
            time.sleep(1)  # let it stabilize a bit
                         # ドローンを少し安定させます
        elif drone.l2_pressed():
            drone.land()
            landed = True
            flying = False
            print("land")
        elif drone.r1_pressed():
            drone.flip()
            print("flip")

    #Manual flight + data collection loop
    # 手動飛行とデータ収集のループです
    while flying:
        check_buttons()

        #read joystick values
        # ジョイスティックの値を読み取ります
        pitch = drone.get_left_joystick_y()
        roll = drone.get_left_joystick_x()
        throttle = drone.get_right_joystick_y()
        yaw_input = drone.get_right_joystick_x()

        #clamp joystick inputs to max ±60 so it doesn’t go crazy
        # ジョイスティックの入力を最大±60に制限して、ドローンが急に動きすぎないようにします
        pitch = max(min(pitch, 60), -60)
        roll = max(min(roll, 60), -60)
        throttle = max(min(throttle, 60), -60)
        yaw_input = max(min(yaw_input, 60), -60)

        #send joystick control to drone
        # ジョイスティックの操作をドローンに送ります
        drone.set_pitch(pitch)
        drone.set_roll(roll)
        drone.set_throttle(throttle)
        drone.set_yaw(yaw_input)
        drone.move()

        #collect flight data
        # 飛行データを収集します
        curTime = time.time()
        gyro = drone.get_gyro_angles()
        alt = drone.get_height()

        #rough calculation of speed
        # 速度を大まかに計算します
        if len(alts) > 0:
            speed = abs(alt - alts[-1]) / 0.2  # cm/s (ish)
            # cm/sくらいの速度です
        else:
            speed = 0

        #append adds to list in python
        # appendはPythonのリストにデータを追加します
        speeds.append(speed)
        alts.append(alt)
        times.append(curTime - startTime)
        time.sleep(0.2)

        # === crash detection ===
        # === 墜落検知 ===
        if len(alts) > 3:
            drop = alts[-2] - alts[-1]
            if drop > 30 and alt < 10:  # sudden drop of 30cm and now low altitude
                # 30cm以上急に落下して、現在の高度が10cm未満の場合
                print("⚠️ CRASH detected! emergency landing!!")
                crashed = True
                drone.land()
                flying = False
                landed = True

    #make sure it lands
    # ドローンが着陸することを確認します
    if not landed:
        drone.land()

    flightTime = time.time() - startTime

    #compute the acceleration
    # 加速度を計算します
    accel = [(speeds[i] - speeds[i - 1]) / (times[i] - times[i - 1])
             for i in range(1, len(speeds)) if times[i] != times[i - 1]]
    maxAccel = max(accel) if accel else 0

    # making stats
    # 統計データを作成します
    stats = FlightStats(
        pilotName=pilotName,
        flightTime=flightTime,
        minSpeed=min(speeds) if speeds else 0,
        maxSpeed=max(speeds) if speeds else 0,
        maxAccel=maxAccel,
        yaw_Var=statistics.variance(yaws) if len(yaws) > 1 else 0,
        max_Alt=max(alts) if alts else 0
    )

    # disconnect from the drone
    # ドローンとの接続を解除します
    drone.close()

    if crashed:
        print(f"  {pilotName} crashed!! flight data ignored.")
        return None  # don’t count crash flights
                     # 墜落した飛行は記録しません
    else:
        print(f"  {pilotName} finished the flight {'(practice)' if practice else ''}!! congrats winner/loser!! ")

    # if it's a practice/crash flight don't return stats for the leaderboard
    # 練習飛行または墜落した飛行の場合、ランキング用の統計データを返しません
    return None if practice else stats


# this is the main test
# これはメインのテストです
if __name__ == "__main__":#this is so it remains in file
    # これによって、このコードをファイルとして実行できます
    leaderboard = flightHeap()

    # list of flights
    # 飛行のリストです
    flights = [
        {"pilot": "Allen", "practice": False},#if crash its false
        # パイロットAllenの飛行です。墜落した場合はFalseです
        {"pilot": "Alfred", "practice": False},
        # パイロットAlfredの飛行です
        # you can add more pilots here
        # ここに他のパイロットを追加できます
    ]

    # collect the flights
    # 飛行データを収集します
    for flight in flights:
        stats = cfd(flight["pilot"], practice=flight["practice"])
        if stats:  # only insert real flights
            # 実際の飛行だけをランキングに追加します
            leaderboard.insert(stats)

        # pause between flights so the drone connection doesn't bug out
        # 飛行と飛行の間に3秒待って、ドローンの接続に問題が起きないようにします
        print("\nwaiting 3 seconds before next flight...")
        time.sleep(3)

    leaderboard.print_lb()  # prints the final leaderboard
                            # 最終ランキングを表示します





