# Diagram Generator Tool

Tool này cho phép AI tạo ra các cloud system architecture diagrams sử dụng thư viện [diagrams](https://github.com/mingrammer/diagrams).

## Cài đặt

### 1. Cài đặt Python package

```bash
pip install diagrams
```

### 2. Cài đặt Graphviz (system dependency)

**macOS:**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**Windows:**
Download và cài đặt từ: https://graphviz.org/download/

### 3. Thêm tool vào Open WebUI

Copy file `diagram_generator.py` vào thư mục tools của Open WebUI hoặc cấu hình đường dẫn đến file này.

## Cách sử dụng

### Trong Open WebUI Chat

Bạn có thể yêu cầu AI tạo diagram bằng cách cung cấp mô tả hoặc code Python:

**Ví dụ 1: Yêu cầu AI tạo diagram**
```
Tạo một diagram kiến trúc AWS đơn giản với Load Balancer, Web Server và Database
```

**Ví dụ 2: Cung cấp code trực tiếp**
```
Tạo diagram với code này:
```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Architecture"):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
```
```

### Cấu hình User Settings

Tool hỗ trợ các UserValves sau (có thể cấu hình trong Open WebUI):

- **OUTPUT_DIR**: Thư mục lưu file diagram (mặc định: thư mục tạm)
- **OUTPUT_FORMAT**: Định dạng file (png, jpg, pdf, svg) - mặc định: png
- **FILENAME_PREFIX**: Tiền tố tên file - mặc định: "diagram"

## Ví dụ Code

Xem file `tools/examples/diagram_example.py` để có các ví dụ đầy đủ.

### Ví dụ đơn giản

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Architecture"):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
```

### Ví dụ với Clusters

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

## Các Provider được hỗ trợ

- **AWS**: `diagrams.aws.*`
- **GCP**: `diagrams.gcp.*`
- **Azure**: `diagrams.azure.*`
- **Kubernetes**: `diagrams.k8s.*`
- **On-Premises**: `diagrams.onprem.*`
- **Alibaba Cloud**: `diagrams.alibabacloud.*`
- **OCI**: `diagrams.oci.*`
- Và nhiều provider khác (xem [diagrams documentation](https://diagrams.mingrammer.com/))

## Lưu ý bảo mật

Tool này có validation để ngăn chặn:
- Các import nguy hiểm (os, sys, subprocess, etc.)
- Các function calls nguy hiểm (eval, exec, open, etc.)
- Code injection attacks

Chỉ code sử dụng thư viện `diagrams` và các module an toàn mới được phép thực thi.

## Testing từ CLI

Bạn có thể test tool từ command line:

```bash
# Tạo file test_diagram.py với code diagram
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

## Troubleshooting

### Lỗi: "Failed to import diagrams library"
- Đảm bảo đã cài đặt: `pip install diagrams`

### Lỗi: "Graphviz not found"
- Cài đặt Graphviz system package (xem phần Cài đặt ở trên)

### Diagram không được tạo
- Kiểm tra code có sử dụng `with Diagram(...)` context manager
- Đảm bảo code không có syntax errors
- Kiểm tra quyền ghi vào thư mục output

## Tài liệu tham khảo

- [diagrams GitHub](https://github.com/mingrammer/diagrams)
- [diagrams Documentation](https://diagrams.mingrammer.com/)
- [diagrams Examples](https://diagrams.mingrammer.com/docs/getting-started/examples)

