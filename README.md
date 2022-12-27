volcengine data/predict api sdk, python version
<br>
```python
import uuid
from datetime import datetime, timedelta

from byteair import ClientBuilder, Client
from byteair.protocol.volcengine_byteair_pb2 import *
from core import Region, Option, NetException, BizException, metrics

# 必传,租户id.
TENANT_ID = "xxx"
# 必传,应用id.
APPLICATION_ID = "xxx"
# 必传,密钥AK,获取方式:【火山引擎控制台】->【个人信息】->【密钥管理】中获取.
AK = "xxx"
# 必传,密钥SK,获取方式：【火山引擎控制台】->【个人信息】->【密钥管理】中获取.
SK = "xxx"

client: Client = ClientBuilder() \
    .tenant_id(TENANT_ID) \
    .application_id(APPLICATION_ID) \
    .ak(AK) \
    .sk(SK) \
    .region(Region.AIR_CN) \
    .build()
# metrics上报初始化.建议开启,方便火山侧排查问题.
metrics.init(())


def write():
    # 此处为测试数据，实际调用时需注意字段类型和格式
    data_list = [
        {
            "id": "item_id1",
            "title": "test_title1",
            "status": 0,
            "brand": "volcengine",
            "pub_time": 1583641807,
            "current_price": 1.1,
        },
        {
            "id": "item_id2",
            "title": "test_title2",
            "status": 1,
            "brand": "volcengine",
            "pub_time": 1583641503,
            "current_price": 2.2,
        }
    ]
    # topic为枚举值，请参考API文档
    topic = "item"
    # 传输天级数据
    opts = (
        # 预同步("pre_sync"), 历史数据同步("history_sync"), 增量天级同步("incremental_sync_daily"),
        # 增量实时同步("incremental_sync_streaming")
        Option.with_stage("pre_sync"),
        # 必传，数据产生日期，实际传输时需修改为实际日期
        Option.with_data_date(datetime(year=2022, month=1, day=1)),
        Option.with_timeout(timedelta(milliseconds=1000)),
        Option.with_request_id(str(uuid.uuid1())),
    )
    try:
        write_response = client.write_data(data_list, topic, *opts)
    except BizException as e:
        print("[write] occur err, msg: %s" % e)
        return
    if not write_response.status.success:
        print("[write] failure")
        return
    print("[write] success")
    return


def done():
    date_list = [datetime(year=2022, month=1, day=1)]
    # topic为枚举值，请参考API文档
    topic = "item"
    opts = (
        # 预同步("pre_sync"), 历史数据同步("history_sync"), 增量天级同步("incremental_sync_daily"),
        # 增量实时同步("incremental_sync_streaming")
        Option.with_stage("pre_sync"),
        Option.with_timeout(timedelta(milliseconds=1000)),
        Option.with_request_id(str(uuid.uuid1())),
    )
    try:
        done_response = client.done(date_list, topic, *opts)
    except BizException as e:
        print("[done] occur err, msg: %s" % e)
        return
    if not done_response.status.success:
        print("[done] failure")
        return
    print("[done] success")
    return


def predict():
    # 构造predict请求体
    predict_request = PredictRequest()
    user = predict_request.user
    user.uid = 'uid1'
    context = predict_request.context
    context.spm = "1$##$2$##$3$##$4"
    context.extra["extra_key"] = "extra_value"
    
    feature = context.feature
    feature.stringFeature["key"] = "value1"
    feature.stringFeature["key"] = "value2"
    feature.stringArrayFeature["array_key"].values.append("array_value1")
    feature.stringArrayFeature["array_key"].values.append("array_value2")
    filter = context.filter
    filter.stringFilter["key"] = "value"
    filter.stringArrayFilter["array_key"].values.append("array_value1")
    filter.stringArrayFilter["array_key"].values.append("array_value2")
    
    candidate_item1 = predict_request.candidateItems.add()
    candidate_item1.id = "item_id1"
    candidate_item2 = predict_request.candidateItems.add()
    candidate_item2.id = "item_id2"
    opts = (
        Option.with_request_id(str(uuid.uuid1())),
        Option.with_scene("default"),
        Option.with_timeout(timedelta(milliseconds=1000)),
        Option.with_headers({"Enable-Spm-Route": "true"})
    )
    try:
        rsp = client.predict(predict_request, *opts)
    except (NetException, BizException) as e:
        print("[predict] occur error, msg: %s" % e)
        return
    if not rsp.success:
        print("[predict] failure")
        return
    print("[predict] success")


def callback():
    # 构造callback请求体
    callback_request = CallbackRequest()
    # 对应的predict请求的request id
    callback_request.predict_request_id = "xxx"
    # 对应的predict请求的uid
    callback_request.uid = "uid1"
    # 对应的predict请求的scene.
    callback_request.scene = "default"
    # 对应的predict请求的items列表
    callback_item1 = callback_request.items.add()
    callback_item1.id = "item_id1"
    callback_item1.pos = "position1"
    callback_item1.extra = "{\"reason\":\"exposure\"}"
    callback_item2 = callback_request.items.add()
    callback_item2.id = "item_id2"
    callback_item2.pos = "position2"
    callback_item2.extra = "{\"reason\":\"filter\"}"
    # callback请求上下文
    callback_context = CallbackContext()
    callback_context.spm = "1$##$2$##$3$##$4"
    callback_request.context = callback_context
    opts = (
        Option.with_request_id(str(uuid.uuid1())),
        Option.with_timeout(timedelta(milliseconds=1000)),
    )
    try:
        rsp = client.callback(callback_request, *opts)
    except (NetException, BizException) as e:
        print("[callback] occur error, msg: %s" % e)
        return
    if not rsp.success:
        print("[callback] failure")
        return
    print("[callback] success")
```

