# 移动端API文档

## 数据格式

- 所有API接口均返回标准json格式，以UTF-16编码
- 所有时间域均是一个整数，GMT时间，utc标准时间，使用时需要在客户端转成本地时区时间
- 请求错误时返回相应的错误编码。
- 所有API的前缀是http:://hifcampus.henhentui.com/api/

## 错误码格式

```python
        'ERROR_REQUEST':{'msg':3000,'detail':'invalid request'},
        'ERROR_NOMORE':{'msg':3001,'detail':'no more items'},
        'ERROR_NOITEM':{'msg':3002,'detail':'no this item'},
        'ERROR_INSERT':{'msg':3003,'detail':'failed to add item'},
```

## API

### list接口

列出指定模块的信息列表

### 格式

```
/list/<model>/
/list/<model>/<int:id>/
/list/<model>/<int:perpage>/<int:id>/
```
model是相关模块的名称，包括以下可选项：

- news
- activity
- job
- lecture
- grapevine
- weekperson

id是某一个整数，标示某一个特定的消息的编号。perpage是指定请求消息的数量，默认是10。

不指定id和perpage时，默认返回最新的10调消息。指定id不指定perpage时默认返回次ID之前10条消息。
同时指定perpage和id时返回指定ID之前的perpage条消息。

### 返回数据格式

- news

```
{
  "data": [
    {
      "_id": 1013,
      "author": 1013,
      "author_name": "admin",
      "author_thumbnail": 0,
      "create_time": {
        "$date": 1395955353000
      },
      "tags": [],
      "thumbnail": 1014,
      "title": "Test"
    }
  ],
  "msg": 0
}
```
- lecture
```
{
  "data": [
    {
      "_id": 1007,
      "attend": [],
      "author": 1013,
      "author_name": "admin",
      "author_thumbnail": 0,
      "create_time": {
        "$date": 1396780404000
      },
      "person": "Test",
      "place": "Test",
      "thumbnail": 1017,
      "title": "Test"
    }
  ],
  "msg": 0
}
```
- grapevine
```
{
  "data": [
    {
      "_id": 1009,
      "author": 1013,
      "author_name": "admin",
      "author_thumbnail": 0,
      "create_time": {
        "$date": 1395934775000
      },
      "thumbnail": 1013,
      "title": "Test"
    }
  ],
  "msg": 0
}
```

- weekperson

```
{
  "data": [
    {
      "_id": 1011,
      "create_time": {
        "$date": 1395766156000
      },
      "person_name": "\u674e\u53cc\u6c5f",
      "proverbes": "to be or not to be",
      "thumbnail1": 1009,
      "thumbnail2": 1010,
      "time": 1,
      "title": "to be or not to be"
    }
  ],
  "msg": 0
}
```
若出错，msg域为对应错误码。

## detail接口

detail接口返回具体某一个条目的具体内容

### 格式

GET

/detail/<model>/<int:id>/

## comment 接口

comment接口返回对用消息的comment列表

### 格式

GET

/comment/<model>/<int:id>/

## thumbnail接口

返回对应id的图像

### 格式

GET

/thumbnail/<size>/<int:id>/

size选项为：small，mid，normal。分别对应小，中，大型的图像



