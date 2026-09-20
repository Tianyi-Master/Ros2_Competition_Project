"""巡检任务状态机的状态常量。

状态机（在 mission_server.py 中驱动）::

    IDLE ──启动──> PATROL ──到达巡检点──> INSPECT
      ^                                    │
      │                                    ├──发现异常──> ALERT ──处理完──> PATROL
      │                                    │
      └──────────任务结束 / 触发返航 <──────┴──结束──> PARK

    - IDLE      ：空闲，等待启动指令
    - PATROL    ：巡逻，沿路线行驶（交给 Nav2）
    - INSPECT   ：巡检，停在巡检点执行各感知任务
    - ALERT     ：告警，检测到异常，上报/记录（高危则立即停靠）
    - PARK      ：泊车，返回预定义泊车点
"""

IDLE = 'IDLE'
PATROL = 'PATROL'
INSPECT = 'INSPECT'
ALERT = 'ALERT'
PARK = 'PARK'

ALL_STATES = (IDLE, PATROL, INSPECT, ALERT, PARK)
