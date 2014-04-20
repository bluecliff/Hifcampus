#!/bin/bash
#curl -i -H "Content-Type: application/json" -X POST -d '{"author_id":1013,"content":"测试评论"}' http://0.0.0.0:8000/api/comment/news/1013/
#curl -i http://0.0.0.0:8000/api/list/news/
#curl -i http://0.0.0.0:8000/api/list/lecture/
curl -i http://0.0.0.0:8000/api/list/activity/
#curl -i http://0.0.0.0:8000/api/list/job/
#curl -i http://0.0.0.0:8000/api/list/grapevine/
#curl -i http://0.0.0.0:8000/api/list/weekperson/
#curl -i http://0.0.0.0:8000/api/detail/news/1014/
curl -i http://0.0.0.0:8000/api/detail/news/1014/
