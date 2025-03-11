import subprocess

# **要依次执行的脚本**
scripts = [
    "check_player_performance.py",
    "predict_name_by_points.py",
    "predict_name_by_appearances.py",
    "predict_name_by_KNN_same_home_team_members.py",
    "predict_name_by_KNN_same_team_member.py"
]

def run_script(script):
    """ 直接执行 Python 脚本，让其标准输出直接显示在终端 """
    print(f"✅ Run: {script} ...")
    try:
        # 让子进程的输出直接显示在终端，而不是捕获
        result = subprocess.run(["python", script], check=True)
        print(f"{script} finished\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ {script} error\n")
        exit(1)  # 终止程序

# **按顺序执行所有脚本**
for script in scripts:
    run_script(script)

print("ALL FINISHED!")
