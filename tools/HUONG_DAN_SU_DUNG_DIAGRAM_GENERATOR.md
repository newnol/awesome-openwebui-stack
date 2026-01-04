# Hướng Dẫn Sử Dụng Diagram Generator

## Giới Thiệu

**Diagram Generator** là một công cụ tạo sơ đồ kiến trúc hệ thống cloud bằng thư viện `diagrams` của Python. Tool này cho phép bạn tạo các sơ đồ kiến trúc đẹp mắt cho AWS, GCP, Azure, Kubernetes và nhiều nền tảng khác.

## Tại Sao Tool Này Hoạt Động Trên Open WebUI?

Open WebUI có một hệ thống tích hợp tools rất linh hoạt. Tool `diagram_generator.py` hoạt động được vì nó tuân theo **chuẩn cấu trúc** mà Open WebUI yêu cầu:

### 1. **Metadata Header (Docstring)**

Open WebUI đọc metadata từ docstring ở đầu file để hiển thị thông tin tool:

```python
"""
title: Diagram Generator (diagrams)
author: newnol
description: A tool that generates cloud system architecture diagrams...
requirements: diagrams
version: 0.1.0
"""
```

Open WebUI sẽ:
- Hiển thị tên tool từ `title`
- Hiển thị mô tả từ `description`
- Kiểm tra `requirements` để nhắc user cài đặt dependencies
- Hiển thị thông tin author và version

### 2. **Class `Tools` với Method Async**

Open WebUI tự động tìm class tên `Tools` và các method async bên trong:

```python
class Tools:
    async def create_diagram(
        self,
        code: str,
        __event_emitter__: Callable[[dict], Any] | None = None,
        __user__: dict = {},
    ) -> str:
        # ...
```

**Cách hoạt động:**
- Open WebUI quét file Python và tìm class `Tools`
- Tìm các method `async def` (trong trường hợp này là `create_diagram`)
- Tự động tạo API endpoint cho method này
- Khi AI gọi tool, Open WebUI sẽ execute method `create_diagram()`

### 3. **Event Emitter - Streaming Status Updates**

Open WebUI cung cấp callback `__event_emitter__` để tool có thể gửi status updates về UI:

```python
async def create_diagram(
    self,
    code: str,
    __event_emitter__: Callable[[dict], Any] | None = None,  # ← Callback từ Open WebUI
    __user__: dict = {},
) -> str:
    emitter = EventEmitter(__event_emitter__)
    
    await emitter.progress_update("Validating diagram code...")  # ← Hiển thị trên UI
    await emitter.success_update("Diagram created successfully!")  # ← Cập nhật status
```

**Kết quả:** User sẽ thấy progress updates trong chat interface khi tool đang chạy!

### 4. **User Configuration (UserValves)**

Open WebUI cho phép user cấu hình tool thông qua `UserValves`:

```python
class UserValves(BaseModel):
    OUTPUT_DIR: str = Field(default="", description="Directory to save diagram files...")
    OUTPUT_FORMAT: str = Field(default="png", description="Output format...")
    FILENAME_PREFIX: str = Field(default="diagram", description="Filename prefix...")
```

**Cách hoạt động:**
- Open WebUI tự động tạo UI form từ `UserValves`
- User có thể cấu hình trong Settings
- Giá trị được truyền vào tool qua `__user__["valves"]`

### 5. **Return String - Hiển Thị Kết Quả**

Open WebUI yêu cầu tool method phải return `str`:

```python
return f"Diagram generated successfully!\n\nFile: {output_path}\nSize: {file_size_kb:.2f} KB"
```

**Kết quả:** String này sẽ được hiển thị trong chat response.

### 6. **Gửi Hình Ảnh Về Chat**

Tool có thể gửi hình ảnh về chat thông qua `EventEmitter.send_image()`:

```python
await emitter.send_image(output_path, "Architecture Diagram")
```

**Cách hoạt động:**
- Tool đọc file ảnh và convert sang base64
- Gửi qua `event_emitter` với format markdown image
- Open WebUI tự động render hình ảnh trong chat

### Quy Trình Hoạt Động Tổng Thể

```
1. User nhập trong chat: "Tạo sơ đồ AWS với EC2 và RDS"
   ↓
2. AI model phân tích và quyết định gọi tool `create_diagram`
   ↓
3. Open WebUI nhận request, load file `diagram_generator.py`
   ↓
4. Open WebUI tìm class `Tools` và method `create_diagram`
   ↓
5. Open WebUI tạo instance: tools = Tools()
   ↓
6. Open WebUI gọi: await tools.create_diagram(code="...", __event_emitter__=callback, __user__={...})
   ↓
7. Tool thực thi:
   - Gửi progress update: "Validating diagram code..."
   - Validate code
   - Execute diagram code
   - Gửi success update: "Diagram created successfully!"
   - Gửi hình ảnh về chat
   - Return string kết quả
   ↓
8. Open WebUI nhận kết quả và hiển thị trong chat:
   - Progress updates (real-time)
   - Hình ảnh sơ đồ
   - Text response
```

### Tóm Tắt: Điều Kiện Để Tool Hoạt Động

✅ **Metadata header** với title, description, requirements  
✅ **Class `Tools`** (tên chính xác)  
✅ **Method `async def`** với signature đúng  
✅ **Parameter `__event_emitter__`** để gửi updates  
✅ **Parameter `__user__`** để nhận user config  
✅ **Return `str`** để hiển thị kết quả  
✅ **Error handling** đầy đủ  

Khi tool đáp ứng các điều kiện trên, Open WebUI sẽ tự động:
- Đăng ký tool vào hệ thống
- Tạo API endpoint
- Hiển thị trong UI
- Cho phép AI gọi tool từ chat

## Cài Đặt

### 1. Cài đặt Python package

```bash
pip install diagrams
```

### 2. Cài đặt Graphviz (phụ thuộc hệ thống)

**macOS:**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**Windows:**
Tải và cài đặt từ: https://graphviz.org/download/

### 3. Thêm tool vào Open WebUI

Copy file `diagram_generator.py` vào thư mục tools của Open WebUI hoặc cấu hình đường dẫn đến file này.

## Cách Sử Dụng

### Trong Open WebUI Chat

Bạn có thể yêu cầu AI tạo sơ đồ bằng cách mô tả hoặc cung cấp code Python:

**Ví dụ 1: Yêu cầu AI tạo sơ đồ**
```
Tạo sơ đồ kiến trúc AWS đơn giản với Load Balancer, Web Server và Database
```

**Ví dụ 2: Cung cấp code trực tiếp**
```
Tạo sơ đồ với code này:
```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Architecture"):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
```
```

### Sử Dụng Qua Command Line

Bạn cũng có thể test tool từ command line:

```bash
# Tạo file test_diagram.py với code sơ đồ
cat > test_diagram.py << 'EOF'
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("Test"):
    EC2("Server") >> RDS("DB")
EOF

# Chạy tool
python tools/diagram_generator.py test_diagram.py --output-dir ./output --format png
```

## Cấu Hình (UserValves)

Tool hỗ trợ các cấu hình sau trong Open WebUI:

- **OUTPUT_DIR**: Thư mục lưu file sơ đồ (mặc định: thư mục tạm)
- **OUTPUT_FORMAT**: Định dạng file (png, jpg, pdf, svg) - mặc định: png
- **FILENAME_PREFIX**: Tiền tố tên file - mặc định: "diagram"

## Các Ví Dụ Code

### Ví Dụ 1: Sơ Đồ AWS Đơn Giản

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Web Architecture"):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
```

### Ví Dụ 2: Sơ Đồ Với Clusters

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3

with Diagram("Serverless Architecture"):
    with Cluster("API"):
        api = Lambda("API Function")
    with Cluster("Data"):
        db = Dynamodb("Database")
        storage = S3("Storage")
    api >> db
    api >> storage
```

### Ví Dụ 3: Kiến Trúc Multi-Cloud

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.gcp.compute import ComputeEngine
from diagrams.azure.compute import VM

with Diagram("Multi-Cloud Setup"):
    with Cluster("AWS"):
        aws_vm = EC2("AWS Instance")
    
    with Cluster("GCP"):
        gcp_vm = ComputeEngine("GCP Instance")
    
    with Cluster("Azure"):
        azure_vm = VM("Azure VM")
    
    aws_vm >> gcp_vm >> azure_vm
```

### Ví Dụ 4: Kiến Trúc Kubernetes

```python
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PV, PVC

with Diagram("Kubernetes Architecture"):
    ingress = Ingress("Ingress")
    
    with Cluster("Services"):
        svc = Service("Service")
    
    with Cluster("Pods"):
        deployment = Deployment("Deployment")
        pod = Pod("Pod")
    
    with Cluster("Storage"):
        pv = PV("Persistent Volume")
        pvc = PVC("PVC")
    
    ingress >> svc >> deployment >> pod
    pod >> pvc >> pv
```

### Ví Dụ 5: Kiến Trúc On-Premises

```python
from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis  # Lưu ý: Redis nằm trong inmemory, không phải database!
from diagrams.onprem.monitoring import Prometheus, Grafana

with Diagram("On-Premises Infrastructure"):
    with Cluster("Web Tier"):
        nginx = Nginx("Nginx")
        web = Server("Web Server")
    
    with Cluster("Application Tier"):
        app = Server("App Server")
    
    with Cluster("Data Tier"):
        postgres = PostgreSQL("PostgreSQL")
        mongo = MongoDB("MongoDB")
        cache = Redis("Cache")  # Redis từ inmemory
    
    with Cluster("Monitoring"):
        prom = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
    
    nginx >> web >> app >> postgres
    app >> mongo
    app >> cache
    prom >> grafana
```

### Ví Dụ 6: Kiến Trúc Microservices Phức Tạp

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import APIGateway, ALB
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis

with Diagram("Microservices Architecture"):
    api = APIGateway("API Gateway")
    
    with Cluster("Load Balancing"):
        alb = ALB("Application Load Balancer")
    
    with Cluster("Services"):
        with Cluster("User Service"):
            user_lambda = Lambda("User Lambda")
            user_db = Dynamodb("User DB")
        
        with Cluster("Order Service"):
            order_ecs = ECS("Order Service")
            order_db = RDS("Order DB")
        
        with Cluster("Payment Service"):
            payment_lambda = Lambda("Payment Lambda")
    
    with Cluster("Storage"):
        s3 = S3("File Storage")
    
    with Cluster("Streaming"):
        kinesis = Kinesis("Event Stream")
    
    api >> alb
    alb >> user_lambda >> user_db
    alb >> order_ecs >> order_db
    alb >> payment_lambda
    user_lambda >> kinesis
    order_ecs >> kinesis
    payment_lambda >> s3
```

### Ví Dụ 7: E-commerce với Redis Cache

```python
from diagrams import Diagram, Cluster
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis  # QUAN TRỌNG: Redis nằm trong inmemory!

with Diagram("E-commerce Architecture"):
    lb = ELB("Load Balancer")
    with Cluster("Web Servers"):
        web = [Server("Web1"), Server("Web2"), Server("Web3")]
    cache = Redis("Cache")
    db = PostgreSQL("Database")
    storage = S3("Storage")
    
    lb >> web >> cache >> db
    web >> storage
```

## Các Provider Được Hỗ Trợ

### AWS (`diagrams.aws.*`)
- **compute**: EC2, Lambda, ECS, EKS, Fargate, Batch
- **database**: RDS, Aurora, Dynamodb, Redshift, ElastiCache
- **network**: ELB, ALB, NLB, CloudFront, Route53, VPC, APIGateway
- **storage**: S3, EBS, EFS
- **integration**: SQS, SNS, EventBridge, StepFunctions
- **analytics**: Kinesis, Athena, EMR, Glue

### GCP (`diagrams.gcp.*`)
- **compute**: ComputeEngine, Functions, Run, GKE
- **database**: SQL, Spanner, Firestore, Bigtable
- **network**: LoadBalancing, CDN, DNS
- **storage**: GCS

### Azure (`diagrams.azure.*`)
- **compute**: VM, FunctionApps, AKS, ContainerInstances
- **database**: SQLDatabases, CosmosDb

### Kubernetes (`diagrams.k8s.*`)
- **compute**: Pod, Deployment, ReplicaSet, StatefulSet, DaemonSet
- **network**: Service, Ingress, NetworkPolicy
- **storage**: PV, PVC, StorageClass

### On-Premises (`diagrams.onprem.*`)
- **compute**: Server, Nomad
- **database**: PostgreSQL, MySQL, MongoDB, Cassandra, MariaDB
- **inmemory**: Redis, Memcached (**QUAN TRỌNG**: Redis nằm trong `inmemory`, không phải `database`!)
- **network**: Nginx, HAProxy, Traefik, Kong
- **queue**: Kafka, RabbitMQ, Celery
- **monitoring**: Prometheus, Grafana, Datadog
- **container**: Docker, Containerd
- **ci**: Jenkins, GitlabCI, GithubActions

### Các Provider Khác
- Alibaba Cloud (`diagrams.alibabacloud.*`)
- OCI (`diagrams.oci.*`)
- Và nhiều provider khác (xem [diagrams documentation](https://diagrams.mingrammer.com/))

## Các Toán Tử Luồng (Flow Operators)

- `>>` : Luồng từ trái sang phải
- `<<` : Luồng từ phải sang trái
- `-` : Luồng hai chiều (dùng Edge cho labels)

**Ví dụ:**
```python
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("Flow Example"):
    server = EC2("Server")
    db = RDS("Database")
    
    server >> db  # Luồng từ server đến database
    server << db  # Luồng từ database đến server
    server - db   # Luồng hai chiều
```

## Lưu Ý Quan Trọng

### 1. Sử Dụng Context Manager

**BẮT BUỘC** phải sử dụng `with Diagram(...)`:

```python
# ✅ ĐÚNG
with Diagram("My Diagram"):
    EC2("Server") >> RDS("DB")

# ❌ SAI
diagram = Diagram("My Diagram")
EC2("Server") >> RDS("DB")
```

### 2. Redis Nằm Trong Module `inmemory`

**QUAN TRỌNG**: Redis không nằm trong `diagrams.onprem.database`, mà nằm trong `diagrams.onprem.inmemory`:

```python
# ✅ ĐÚNG
from diagrams.onprem.inmemory import Redis

# ❌ SAI
from diagrams.onprem.database import Redis  # Sẽ lỗi!
```

### 3. Không Cần Chỉ Định Filename và Show

Tool sẽ tự động thêm các tham số `filename`, `show=False`, và `outformat` vào Diagram context manager. Bạn không cần chỉ định chúng trong code:

```python
# ✅ ĐÚNG - Tool sẽ tự động thêm filename, show=False, outformat
with Diagram("My Diagram"):
    EC2("Server") >> RDS("DB")

# ✅ CŨNG ĐÚNG - Nhưng không cần thiết
with Diagram("My Diagram", filename="diagram", show=False, outformat="png"):
    EC2("Server") >> RDS("DB")
```

## Xử Lý Lỗi

### Lỗi: "Failed to import diagrams library"
- **Nguyên nhân**: Chưa cài đặt thư viện diagrams
- **Giải pháp**: Chạy `pip install diagrams`

### Lỗi: "Graphviz not found"
- **Nguyên nhân**: Chưa cài đặt Graphviz
- **Giải pháp**: Cài đặt Graphviz theo hướng dẫn ở phần Cài Đặt

### Sơ đồ không được tạo
- **Nguyên nhân 1**: Code không sử dụng `with Diagram(...)` context manager
- **Giải pháp**: Đảm bảo sử dụng `with Diagram(...):`

- **Nguyên nhân 2**: Code có lỗi cú pháp
- **Giải pháp**: Kiểm tra lại code Python

- **Nguyên nhân 3**: Không có quyền ghi vào thư mục output
- **Giải pháp**: Kiểm tra quyền ghi của thư mục output

### Lỗi: "Code contains potentially dangerous..."
- **Nguyên nhân**: Code chứa các import hoặc function không được phép (os, sys, subprocess, eval, exec, etc.)
- **Giải pháp**: Chỉ sử dụng thư viện `diagrams` và các module an toàn

## Bảo Mật

Tool có cơ chế validation để ngăn chặn:
- Các import nguy hiểm (os, sys, subprocess, etc.)
- Các function call nguy hiểm (eval, exec, open, etc.)
- Code injection attacks

Chỉ code sử dụng thư viện `diagrams` và các module an toàn mới được phép thực thi.

## Tài Liệu Tham Khảo

- [diagrams GitHub](https://github.com/mingrammer/diagrams)
- [diagrams Documentation](https://diagrams.mingrammer.com/)
- [diagrams Examples](https://diagrams.mingrammer.com/docs/getting-started/examples)

## Ví Dụ Đầy Đủ

Xem file `tools/examples/diagram_example.py` để xem các ví dụ code đầy đủ.

