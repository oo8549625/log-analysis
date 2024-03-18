## 日誌分析
從 kibana alert rule 寫入的 index document，藉由 logstash 從 elasticsearch input 和 http output 到這個日誌分析的服務上。

### 目的
分析日誌內 nginx 異常訪問的次數，取唯一域名且唯一URI對不同狀態碼的訪問次數計數。

### API
<details>
 <summary><code>POST</code><code><b>/api/v1/log/write</b></code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | None      |  required | object (JSON 參考 log.json)   | N/A  |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{"message": "JSON received", "data": content}`                                |

##### Example CURL

> ```bash
> curl -X POST -H "Content-Type: application/json" --data @log.json http://localhost:5000/api/v1/log/write
> ```
</details>

### 告警發送telegram

## 開發

### 啟動虛擬環境
```bash
python -m venv venv

# 在 Windows 系統中，使用：
venv\Scripts\activate

#在 Unix 或 MacOS 系統，使用：
source venv/bin/activate

# 退出
deactivate
```

### 套件依賴取出
```bash
pip freeze > requirement.txt
```

### 測試
```bash
flask run --host=0.0.0.0 --debug
```

## 正式

### 打包
```bash
docker build -t log-analysis:latest . --no-cache
```

### 部屬
```bash
docker-compose up -d
```
