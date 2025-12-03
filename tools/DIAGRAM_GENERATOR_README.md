# Diagram Generator Tool

This tool allows AI to create cloud system architecture diagrams using the [diagrams](https://github.com/mingrammer/diagrams) library.

## Installation

### 1. Install Python package

```bash
pip install diagrams
```

### 2. Install Graphviz (system dependency)

**macOS:**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**Windows:**
Download and install from: https://graphviz.org/download/

### 3. Add tool to Open WebUI

Copy the `diagram_generator.py` file to the Open WebUI tools directory or configure the path to this file.

## Usage

### In Open WebUI Chat

You can ask AI to create diagrams by providing a description or Python code:

**Example 1: Ask AI to create a diagram**
```
Create a simple AWS architecture diagram with Load Balancer, Web Server and Database
```

**Example 2: Provide code directly**
```
Create a diagram with this code:
```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Architecture"):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
```
```

### User Settings Configuration

The tool supports the following UserValves (configurable in Open WebUI):

- **OUTPUT_DIR**: Directory to save diagram files (default: temporary directory)
- **OUTPUT_FORMAT**: File format (png, jpg, pdf, svg) - default: png
- **FILENAME_PREFIX**: Filename prefix - default: "diagram"

## Code Examples

See `tools/examples/diagram_example.py` for complete examples.

### Simple Example

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Architecture"):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
```

### Example with Clusters

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

## Supported Providers

- **AWS**: `diagrams.aws.*`
- **GCP**: `diagrams.gcp.*`
- **Azure**: `diagrams.azure.*`
- **Kubernetes**: `diagrams.k8s.*`
- **On-Premises**: `diagrams.onprem.*`
- **Alibaba Cloud**: `diagrams.alibabacloud.*`
- **OCI**: `diagrams.oci.*`
- And many other providers (see [diagrams documentation](https://diagrams.mingrammer.com/))

## Security Notes

This tool has validation to prevent:
- Dangerous imports (os, sys, subprocess, etc.)
- Dangerous function calls (eval, exec, open, etc.)
- Code injection attacks

Only code using the `diagrams` library and safe modules is allowed to execute.

## CLI Testing

You can test the tool from the command line:

```bash
# Create test_diagram.py file with diagram code
cat > test_diagram.py << 'EOF'
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("Test"):
    EC2("Server") >> RDS("DB")
EOF

# Run the tool
python tools/diagram_generator.py test_diagram.py --output-dir ./output --format png
```

## Troubleshooting

### Error: "Failed to import diagrams library"
- Make sure you have installed: `pip install diagrams`

### Error: "Graphviz not found"
- Install Graphviz system package (see Installation section above)

### Diagram not created
- Check that code uses `with Diagram(...)` context manager
- Ensure code has no syntax errors
- Check write permissions for output directory

## References

- [diagrams GitHub](https://github.com/mingrammer/diagrams)
- [diagrams Documentation](https://diagrams.mingrammer.com/)
- [diagrams Examples](https://diagrams.mingrammer.com/docs/getting-started/examples)
