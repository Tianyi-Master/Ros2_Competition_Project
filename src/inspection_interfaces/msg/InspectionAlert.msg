# 统一巡检告警：所有感知节点通过此消息上报异常，
# mission_server 订阅 /perception/alert 汇总处理。
std_msgs/Header header

uint8 INFO=0       # 提示
uint8 WARNING=1    # 警告
uint8 ERROR=2      # 错误（需立即处理，如火灾、异常高温）

string module       # 来源模块名，如 "fire" / "bin_status" / "temperature"
uint8 severity      # 告警等级：INFO / WARNING / ERROR
string message      # 人类可读的告警描述
