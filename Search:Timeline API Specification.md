# 搜索/推荐相关的API标准

## 搜索

约定：搜索结果是分页的，每次请求只返回一页（10条）的搜索结果。返回的搜索结果一律按发布时间从近到远排序。得到搜索结果的时候，前端会知道总共有多少条搜索内容，并在需要的时候请求后续页的搜索结果。对于一条对第i页的搜索请求，后端能够检索并返回排在第[i\*10 + 1, i\*10+10]的搜索结果。

### URL

```
/search/
```

### Request JSON

``` 
{
    "dir": "request",
    "content_type": "search",
    "content": {
        "keyword": String, //默认只检索标题是否含关键词
        "search_description": Boolean, //是否检索正文
        "search_lab": Boolean, //是否检索实验室信息
        "search_seminar": Boolean,
        "search_project": Boolean,
        "curr_page": Number, //本次请求的页面号
    }
}
```

### Response JSON

```
{
    "dir": "response",
    "content_type": "search",
    "content": {
        "total_results": Number, //搜索结果总数
        "last_page": Number, //搜索结果最后一页的页面号
        "result": [
            {
              "content_type": "lab" | "seminar" | "project",
              "id": Number 
            }
         ]
    }
}
```

### 备注

1. `result`是一个Object数组，每个数组成员拥有`content_type`和`id`两个域，指明是哪种类型的结果。这么做的考量是便于在前端直接将三类信息合并渲染成一个列表。
2. 当`keyword`值为`""`时，表示不指定关键词，此时返回的是按发布时间从最新到最老排序的所有结果。
3. 约定搜索的页号从1开始计数。

## 推荐

如果不考虑实现某种个性化推荐算法，那么直接发送如下搜索请求即可

```
{
    "dir": "request",
    "content_type": "search",
    "content": {
        "keyword": "",
        "search_description": true,
        "search_lab": true, 
        "search_seminar": true,
        "search_project": true,
        "curr_page": 1,
    }
}
```

此时，甚至可以直接将推荐与搜索在一个页面实现。在以上API的基础上可以很容易实现只显示某一类信息的页面。