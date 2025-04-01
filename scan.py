from subprocess import getoutput
from pathlib import Path
import os, time, shutil
DEBUG = False
def main():
    bin_path = Path("scan.exe")
    if bin_path.exists():
        os.remove(bin_path)
    build_cmd = r"cargo fmt && cargo build"
    if DEBUG:
        dir_name = "debug"
    else:
        dir_name = "release"
        build_cmd += " -r"
    print(getoutput(build_cmd))
    
    shutil.move(Path(r"target\{}\atcoder.exe".format(dir_name)), bin_path)
    assert(bin_path.exists())
    score_sum = 0
    score_norm = 0
    score_max = -1
    score_max_i = -1
    dt_max = -1
    dt_max_i = -1
    csv_path = Path("score1.csv")
    with open(csv_path, "w") as f:
        for i in range(100):
            cmd = r"tester.exe"
            cmd += r" " + str(bin_path)
            cmd += r" < tools\in\{0:04d}.txt".format(i)
            cmd += r" > tools\out\{0:04d}.txt".format(i)
            t0 = time.time()
            ret = getoutput(cmd)
            t1 = time.time()
            dt = int(1000 * (t1 - t0))
            try:
                score = int(ret.split()[-1])
            except:
                print(i)
                print(ret)
                return
            if score_max < score:
                score_max = score
                score_max_i = i
            if dt_max < dt:
                dt_max = dt
                dt_max_i = i
            score_sum += score
            score_norm += 1
            print(i, score, dt, "MAX:{}({})".format(score_max, score_max_i), "SLOW:{}({})".format(dt_max, dt_max_i), int(score_sum / score_norm))
            f.write("{}\n".format(score))
    print(int(score_sum / score_norm))
    getoutput("explorer {}".format(csv_path))

if __name__ == "__main__":
    main()