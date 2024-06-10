# 验证结果

验证结果如下：

| 函数         | 备注                                | 不超时                         | 超时                                           |
| ------------ | ----------------------------------- | ------------------------------ | ---------------------------------------------- |
| run_cmd1     | os.system                           | **实时打印**到终端             | 实时打印到终端，**无法停止**                   |
| run_cmd2     | os.popen                            | 打印到终端（执行完毕后打印）   | **无法停止**，终端不显示，在后台运行           |
| run_cmd3     | subprocess.Popen                    | 打印到终端（执行完毕后打印）   | 打印到终端（执行完毕后打印，会出现超时提醒）   |
| run_cmd3_new | subprocess.Popen,保存到文件         | 终端不显示，但是文**件中存在** | **终端不显示**，但是文件中存在，会出现超时提醒 |
| run_cmd4     | subprocess.call                     | **实时打印**到终端             | **实时打印**到终端，会出现超时提醒             |
| run_cmd5     | exec                                | **实时打印**到终端             | 实时打印到终端，**无法停止**                   |
| run_cmd6     | subprocess.run                      | 打印到终端（执行完毕后打印）   | 打印到终端（执行完毕后打印，会出现超时提醒）   |
| run_cmd7     | subprocess.check_call               | **实时打印**到终端             | **实时打印**到终端，会出现超时提醒             |
| run_cmd8     | subprocess.check_output             | 打印到终端（执行完毕后打印）   | 打印到终端（执行完毕后打印，会出现超时提醒）   |
| run_cmd9     | os.execv                            | -                              | -                                              |
| run_cmd10    | create_subprocess_shell，管道       | 打印到终端（执行完毕后打印）   | **终端不显示**，会出现超时提醒                 |
| run_cmd11    | create_subprocess_shell, 保存到文件 | 终端不显示，保存到文件         | **终端不显示**，保存到文件，会出现超时提醒     |
| run_cmd12    | create_subprocess_exec，管道        | 打印到终端（执行完毕后打印）   | **终端不显示**，会出现超时提醒                 |
| run_cmd13    | create_subprocess_exec, 保存到文件  | 终端不显示，保存到文件         | **终端不显示**，保存到文件，会出现超时提醒     |

推荐：

subprocess.call -> subprocess.check_call （实时展示）

subprocess.run  -> subprocess.check_output （不考虑展示信息）



其中的一些相关性如下：

```
				 -> os.popen
subprocess.Popen -> subprocess.call -> subprocess.check_call
				 -> subprocess.run  -> subprocess.check_output
			
# 总结：run_cmd4和run_cmd7一致
run_cmd6和run_cmd8一致

os.system

os.execv

loop.subprocess_exec -> asyncio.create_subprocess_exec
loop.subprocess_shell -> asyncio.create_subprocess_shell

```

