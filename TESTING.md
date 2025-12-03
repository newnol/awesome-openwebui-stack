# Testing Diagram Generator Tool Locally

This guide shows you how to test the `diagram_generator.py` tool on your local machine.

## Prerequisites

1. **Activate virtual environment** (if using one):
   ```bash
   source .env/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install diagrams
   ```

3. **Install Graphviz** (system dependency):
   - macOS: `brew install graphviz`
   - Ubuntu/Debian: `sudo apt-get install graphviz`
   - Windows: Download from https://graphviz.org/download/

## Method 1: Using a Python File (Recommended)

### Step 1: Create a test file

Create a file `test_diagram.py` with diagram code:

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Test Architecture"):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
```

### Step 2: Run the tool

```bash
python3 tools/diagram_generator.py test_diagram.py \
    --output-dir ./output \
    --format png \
    --filename test_result
```

**Options:**
- `--output-dir` or `-o`: Output directory (default: temporary directory)
- `--format` or `-f`: Output format - `png`, `jpg`, `jpeg`, `pdf`, `svg` (default: `png`)
- `--filename` or `-n`: Filename prefix (default: `diagram`)

### Step 3: Check the result

The diagram will be saved to `./output/test_result.png`

## Method 2: Using stdin (Quick Test)

You can pipe code directly to the tool:

```bash
cat << 'EOF' | python3 tools/diagram_generator.py - --output-dir ./output
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("Quick Test"):
    EC2("Server") >> RDS("Database")
EOF
```

## Method 3: Using the Helper Script

A helper script is provided for convenience:

```bash
# Make sure test_diagram.py exists
./test_diagram_helper.sh
```

## Example: E-commerce Architecture

Create `test_ecommerce.py`:

```python
from diagrams import Diagram, Cluster
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis

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

Run:
```bash
python3 tools/diagram_generator.py test_ecommerce.py \
    --output-dir ./output \
    --format png \
    --filename ecommerce
```

## Troubleshooting

### Error: "No such file or directory: './output'"
- Create the output directory first: `mkdir -p output`
- Or use absolute path: `--output-dir /full/path/to/output`

### Error: "Failed to import diagrams library"
- Install diagrams: `pip install diagrams`
- Make sure virtual environment is activated

### Error: "Graphviz not found"
- Install Graphviz system package (see Prerequisites)

### Diagram not created
- Check that code uses `with Diagram(...)` context manager
- Ensure code has no syntax errors
- Check write permissions for output directory

## More Examples

See `tools/examples/diagram_example.py` for more complex examples.

