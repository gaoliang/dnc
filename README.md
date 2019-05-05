# socket.io接口定义 初步

鉴于机床和dnc服务器端需要频繁的双向通信，所以采用socket.io的方式来实现数据传输较为方便。

下面是我现在想到的接口，参数有些还没定下来, 不确定的地方我标记了问号， server目前尚未实现

1. server端emit `"start"`, 机床启动
2. server端emit `"shutdown"`, 机床关机
3. server端emit `"reset"`, 机床重置
4. 机床端emit `"register"`, 向server注册设备，参数为device_id, 可以取mac地址？
5. server端emit `"need_program_list"`,  请求机床上传当前机床中的程序列表
6. 在 5 之后，机床端emit `"upload_program_list"`, 参数为当前机床的device_id和程序列表 list, json格式
7. server端emit `"need_program"`,  请求机床上传当前机床中的指定程序内容，参数为program_id
8. 在 7 之后， 机床端emit `"upload_program"`,  参数为 7 中的program_id，和程序详细内容json
9. server端emit `"download"`, 参数为json， 包含program_id和content两个字段
10. server端emit  `"delete_program"`, 参数为program_id, 删除机床中的某个程序
11. 机床端应定时emit `"refresh_status"`, 向server报告当前状态，参数为device_id和状态信息json， 参数目前参考附的论文中的？

```javascript
/**
 * 1) 机床工作模式、启动状态、急停开关状态、报警状态；
 * 2) 绝对坐标、相对坐标、机械坐标、剩余移动量；
 * 3) 主轴和进给轴的速度、倍率；
 * 4) 主轴和进给轴的负载；
 * 5) 实时报警, 类型、编号、内容及报警数量
 * 6) 当前执行程序、当前行、下一行、当前刀号。
 */
```