# Diagram Generator Tool - Workflow Documentation

## Overview

This document explains the complete workflow of the `diagram_generator.py` tool, from user request to final diagram image.

## High-Level Workflow

```
User Request → AI Assistant → Tool Call → Code Generation → Validation → Execution → Rendering → Image Display
```

## Detailed Workflow Steps

### Phase 1: User Request & AI Processing

```
┌─────────────┐
│   User      │
│  Prompt:    │
│ "Tạo diagram│
│  e-commerce"│
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  Open WebUI Chat Interface       │
│  - User types request            │
│  - Request sent to AI model      │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  AI Assistant (LLM)             │
│  1. Reads tool docstring         │
│  2. Understands diagrams API    │
│  3. Generates Python code        │
│  4. Calls create_diagram()       │
└──────┬──────────────────────────┘
       │
       │ Python code string
       ▼
```

**Example AI-generated code:**
```python
from diagrams import Diagram, Cluster
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis

with Diagram("E-commerce Architecture"):
    lb = ELB("Load Balancer")
    web = [Server("Web1"), Server("Web2"), Server("Web3")]
    cache = Redis("Cache")
    db = PostgreSQL("Database")
    storage = S3("Storage")
    
    lb >> web >> cache >> db
    web >> storage
```

---

### Phase 2: Tool Entry Point

```
┌─────────────────────────────────┐
│  create_diagram() Method         │
│  Input:                          │
│  - code: str (Python code)       │
│  - __event_emitter__: Callable   │
│  - __user__: dict (config)       │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Step 1: Initialize             │
│  - Create EventEmitter           │
│  - Load UserValves (config)      │
│  - Set output_dir, format, etc.  │
└──────┬──────────────────────────┘
       │
       ▼
```

**Code Reference:**
```331:460:tools/diagram_generator.py
    async def create_diagram(
        self,
        code: str,
        __event_emitter__: Callable[[dict], Any] | None = None,
        __user__: dict = {},
    ) -> str:
        """
        Creates a cloud system architecture diagram using the diagrams library.
        
        The code parameter should contain Python code that uses the diagrams library
        to create a diagram. The code will be executed in a controlled environment.
        
        **Important Notes:**
        - The code must use the Diagram context manager (with statement)
        - You don't need to specify filename or show parameters - they will be set automatically
        - Supported providers: AWS, GCP, Azure, Kubernetes, On-Premises, and more
        - Output format can be configured via UserValves (default: PNG)
        
        **Example code:**
        ```python
        from diagrams import Diagram
        from diagrams.aws.compute import EC2
        from diagrams.aws.database import RDS
        from diagrams.aws.network import ELB
        
        with Diagram("Simple Architecture"):
            ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
        ```
        
        **Example with clusters:**
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
        
        **Available Providers and Common Components:**
        
        AWS (diagrams.aws.*):
        - compute: EC2, Lambda, ECS, EKS, Fargate, Batch
        - database: RDS, Aurora, Dynamodb, Redshift, ElastiCache
        - network: ELB, ALB, NLB, CloudFront, Route53, VPC, APIGateway
        - storage: S3, EBS, EFS
        - integration: SQS, SNS, EventBridge, StepFunctions
        - analytics: Kinesis, Athena, EMR, Glue
        
        GCP (diagrams.gcp.*):
        - compute: ComputeEngine, Functions, Run, GKE
        - database: SQL, Spanner, Firestore, Bigtable
        - network: LoadBalancing, CDN, DNS
        - storage: GCS
        
        Azure (diagrams.azure.*):
        - compute: VM, FunctionApps, AKS, ContainerInstances
        - database: SQLDatabases, CosmosDb
        
        Kubernetes (diagrams.k8s.*):
        - compute: Pod, Deployment, ReplicaSet, StatefulSet, DaemonSet
        - network: Service, Ingress, NetworkPolicy
        - storage: PV, PVC, StorageClass
        
        On-Premises (diagrams.onprem.*):
        - compute: Server, Nomad
        - database: PostgreSQL, MySQL, MongoDB, Cassandra, MariaDB
        - inmemory: Redis, Memcached (IMPORTANT: Redis is in inmemory, NOT database!)
        - network: Nginx, HAProxy, Traefik, Kong
        - queue: Kafka, RabbitMQ, Celery
        - monitoring: Prometheus, Grafana, Datadog
        - container: Docker, Containerd
        - ci: Jenkins, GitlabCI, GithubActions
        
        **Flow operators:**
        - >> : left to right flow
        - << : right to left flow
        - - : bidirectional (use Edge for labels)
        
        **Example with multiple servers:**
        ```python
        from diagrams import Diagram, Cluster
        from diagrams.aws.compute import EC2
        from diagrams.aws.database import RDS
        from diagrams.aws.network import ELB
        
        with Diagram("Scaled Architecture"):
            lb = ELB("Load Balancer")
            with Cluster("Web Tier"):
                servers = [EC2("Web1"), EC2("Web2"), EC2("Web3")]
            db = RDS("Database")
            lb >> servers >> db
        ```
        
        **Example E-commerce with Redis cache (IMPORTANT - Redis is in inmemory module!):**
        ```python
        from diagrams import Diagram, Cluster
        from diagrams.aws.network import ELB
        from diagrams.aws.storage import S3
        from diagrams.onprem.compute import Server
        from diagrams.onprem.database import PostgreSQL
        from diagrams.onprem.inmemory import Redis  # Redis is in inmemory, NOT database!
        
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
        
        :param code: Python code string that creates a diagram using the diagrams library.
                     Must use Diagram context manager. Filename and show parameters are optional.
        :return: Path to the generated diagram file with file info, or an error message
        """
        emitter = EventEmitter(__event_emitter__)

        if "valves" not in __user__:
            __user__["valves"] = self.UserValves()
```

---

### Phase 3: Code Validation

```
┌─────────────────────────────────┐
│  Step 2: Validate Code           │
│  - Check for dangerous imports   │
│  - Check for dangerous functions │
│  - Syntax validation              │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  _validate_diagram_code()       │
│  Blocks:                        │
│  - os, sys, subprocess          │
│  - eval, exec, open             │
│  - Code injection attempts      │
└──────┬──────────────────────────┘
       │
       │ ✅ Valid
       ▼
```

**Code Reference:**
```94:191:tools/diagram_generator.py
def _validate_diagram_code(code: str) -> tuple[bool, str]:
    """
    Validate that the code only uses safe imports and patterns.
    Returns (is_valid, error_message)
    """
    import re
    
    # Dangerous function calls to block (must be actual function calls, not in strings/comments)
    dangerous_functions = [
        "__import__",
        "eval(",
        "exec(",
        "compile(",
        "open(",
        "file(",
        "input(",
        "raw_input(",
    ]
    
    # Dangerous imports to block
    dangerous_imports = [
        r"import\s+os\b",
        r"import\s+sys\b",
        r"import\s+subprocess\b",
        r"import\s+shutil\b",
        r"import\s+pickle\b",
        r"import\s+socket\b",
        r"import\s+urllib\b",
        r"import\s+requests\b",
        r"import\s+http\b",
        r"from\s+os\s+import",
        r"from\s+sys\s+import",
        r"from\s+subprocess\s+import",
        r"os\.system",
        r"os\.popen",
        r"subprocess\.",
    ]
    
    # Remove comments and strings to avoid false positives
    lines = code.split('\n')
    cleaned_lines = []
    in_string = False
    string_char = None
    
    for line in lines:
        cleaned_line = ""
        i = 0
        while i < len(line):
            char = line[i]
            
            # Handle string detection
            if not in_string and char in ('"', "'"):
                # Check if it's not escaped
                if i == 0 or line[i-1] != '\\':
                    in_string = True
                    string_char = char
                    cleaned_line += ' '  # Replace string content with space
                    i += 1
                    continue
            elif in_string and char == string_char:
                # Check if it's not escaped
                if i == 0 or line[i-1] != '\\':
                    in_string = False
                    string_char = None
                    cleaned_line += ' '
                    i += 1
                    continue
            
            if in_string:
                cleaned_line += ' '  # Replace string content
            else:
                # Remove comments
                if char == '#' and (i == 0 or line[i-1] != '\\'):
                    break  # Rest of line is comment
                cleaned_line += char
            i += 1
        
        cleaned_lines.append(cleaned_line)
    
    cleaned_code = '\n'.join(cleaned_lines)
    
    # Check for dangerous function calls
    for func in dangerous_functions:
        if func in cleaned_code:
            return False, f"Code contains potentially dangerous function call: {func}"
    
    # Check for dangerous imports using regex
    for pattern in dangerous_imports:
        if re.search(pattern, cleaned_code, re.IGNORECASE):
            return False, f"Code contains potentially dangerous import: {pattern}"
    
    # Basic syntax check
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        return False, f"Syntax error in code: {str(e)}"
    
    return True, ""
```

---

### Phase 4: Code Modification & Preparation

```
┌─────────────────────────────────┐
│  Step 3: Modify Code            │
│  - Inject filename parameter    │
│  - Inject show=False            │
│  - Inject outformat            │
└──────┬──────────────────────────┘
       │
       ▼
```

**Before modification:**
```python
with Diagram("E-commerce Architecture"):
    ...
```

**After modification:**
```python
with Diagram("E-commerce Architecture", filename="diagram", show=False, outformat="png"):
    ...
```

**Code Reference:**
```491:530:tools/diagram_generator.py
            # Modify code to ensure Diagram has correct parameters
            # We'll wrap the code to set filename and format if not specified
            import re
            
            modified_code = code
            
            # Check if Diagram is used in the code
            if 'Diagram(' in code:
                # Try to inject filename and format if not present
                # Pattern: Diagram(...) -> Diagram(..., filename="...", show=False, outformat="...")
                def inject_params(match):
                    content = match.group(1)
                    params_to_add = []
                    
                    # Check and add filename if not present
                    if 'filename=' not in content:
                        params_to_add.append(f'filename="{filename_prefix}"')
                    
                    # Check and add show=False if not present
                    if 'show=' not in content:
                        params_to_add.append('show=False')
                    
                    # Check and add outformat if not present
                    if 'outformat=' not in content:
                        params_to_add.append(f'outformat="{output_format}"')
                    
                    # Build the new content
                    if params_to_add:
                        content = content.rstrip().rstrip(',')
                        content = f'{content}, {", ".join(params_to_add)}'
                    
                    return f'Diagram({content})'
                
                # Replace first occurrence of Diagram(...)
                modified_code = re.sub(
                    r'Diagram\(([^)]+)\)',
                    inject_params,
                    code,
                    count=1
                )
```

---

### Phase 5: Code Execution

```
┌─────────────────────────────────┐
│  Step 4: Execute Code           │
│  - Run in asyncio.to_thread()    │
│  - Change to output directory    │
│  - Prepare namespace             │
│  - exec(code, namespace)         │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  _execute_diagram_code()         │
│  1. Change working directory    │
│  2. Create namespace dict        │
│  3. Import diagrams modules      │
│  4. Execute user code            │
└──────┬──────────────────────────┘
       │
       ▼
```

**Code Reference:**
```194:274:tools/diagram_generator.py
def _execute_diagram_code(
    code: str,
    output_dir: str,
    filename: str = "diagram",
    format: str = "png",
) -> tuple[bool, str, str]:
    """
    Execute diagram code and render to image file.
    Returns (success, output_path, error_message)
    """
    original_cwd = os.getcwd()
    try:
        # Change to output directory so diagrams saves files there
        os.chdir(output_dir)
        
        # Create a temporary module namespace
        namespace = {
            "__name__": "__diagram_module__",
            "__file__": "<diagram_code>",
        }
        
        # Add diagrams imports to namespace
        try:
            from diagrams import Diagram, Cluster, Edge
            namespace["Diagram"] = Diagram
            namespace["Cluster"] = Cluster
            namespace["Edge"] = Edge
            
            # Import common providers - make them available in namespace
            try:
                from diagrams.onprem import compute, database, network, storage, inmemory, queue
                namespace.update({
                    "compute": compute,
                    "database": database,
                    "network": network,
                    "storage": storage,
                    "inmemory": inmemory,
                    "queue": queue,
                })
            except ImportError:
                pass
            
            try:
                from diagrams.aws import compute as aws_compute, database as aws_database, storage as aws_storage, network as aws_network
                namespace.update({
                    "aws_compute": aws_compute,
                    "aws_database": aws_database,
                    "aws_storage": aws_storage,
                    "aws_network": aws_network,
                })
            except ImportError:
                pass
            
            try:
                from diagrams.gcp import compute as gcp_compute, database as gcp_database, storage as gcp_storage
                namespace.update({
                    "gcp_compute": gcp_compute,
                    "gcp_database": gcp_database,
                    "gcp_storage": gcp_storage,
                })
            except ImportError:
                pass
            
            try:
                from diagrams.azure import compute as azure_compute, database as azure_database
                namespace.update({
                    "azure_compute": azure_compute,
                    "azure_database": azure_database,
                })
            except ImportError:
                pass
                
        except ImportError as e:
            return False, "", f"Failed to import diagrams library: {str(e)}. Please install it with: pip install diagrams"
        
        # Set output path
        output_path = os.path.join(output_dir, f"{filename}.{format}")
        namespace["__output_path__"] = output_path
        
        # Execute the code
        exec(code, namespace)
```

---

### Phase 6: Diagram Rendering

```
┌─────────────────────────────────┐
│  Step 5: diagrams Library       │
│  - Parse Diagram context        │
│  - Create component nodes        │
│  - Calculate layout             │
│  - Generate Graphviz DOT file   │
│  - Render to PNG/SVG/PDF         │
└──────┬──────────────────────────┘
       │
       │ File created: diagram.png
       ▼
```

**What happens inside `with Diagram(...):`:**

1. **Context Manager Entry:**
   - `Diagram.__enter__()` is called
   - Creates a Graphviz graph object
   - Sets up rendering parameters

2. **Component Creation:**
   - Each component (ELB, Server, Redis, etc.) creates a node
   - Nodes are added to the graph

3. **Connection Creation:**
   - `>>` operator creates edges between nodes
   - Flow direction is determined

4. **Context Manager Exit:**
   - `Diagram.__exit__()` is called
   - Graphviz renders the graph to file
   - File saved to output directory

---

### Phase 7: Image Processing & Display

```
┌─────────────────────────────────┐
│  Step 6: Process Image          │
│  - Read image file              │
│  - Convert to Base64            │
│  - Determine MIME type          │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Step 7: Send to UI             │
│  - Create data URI              │
│  - Emit via EventEmitter        │
│  - Display in chat              │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Open WebUI Chat                │
│  - Image displayed inline        │
│  - User sees diagram! 🎉        │
└─────────────────────────────────┘
```

**Code Reference:**
```62:91:tools/diagram_generator.py
    async def send_image(self, image_path: str, alt_text: str = "Diagram") -> None:
        """Send an image to be displayed in the chat."""
        if self.event_emitter:
            import base64
            
            # Read image and convert to base64
            with open(image_path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode("utf-8")
            
            # Determine MIME type based on file extension
            ext = image_path.lower().split(".")[-1]
            mime_types = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "gif": "image/gif",
                "svg": "image/svg+xml",
                "pdf": "application/pdf",
            }
            mime_type = mime_types.get(ext, "image/png")
            
            # Emit message with image
            await self.event_emitter(
                {
                    "type": "message",
                    "data": {
                        "content": f"![{alt_text}](data:{mime_type};base64,{image_data})"
                    },
                }
            )
```

---

## Complete Flow Diagram

```
┌──────────────┐
│ User Request │
└──────┬───────┘
       │
       ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  AI Assistant    │─────▶│  Generate Code    │─────▶│  Call Tool       │
│  (LLM)           │      │  (Python string)  │      │  create_diagram()│
└──────────────────┘      └──────────────────┘      └──────┬───────────┘
                                                              │
                                                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Tool Processing                               │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Validate Code │───▶│ Modify Code  │───▶│ Execute Code  │       │
│  │ (Security)    │    │ (Add params) │    │ (exec())      │       │
│  └──────────────┘    └──────────────┘    └──────┬─────────┘       │
│                                                   │                 │
└───────────────────────────────────────────────────┼─────────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    diagrams Library                                  │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │ Parse Graph  │───▶│ Calculate    │───▶│ Render Image │         │
│  │ Components   │    │ Layout       │    │ (Graphviz)   │         │
│  └──────────────┘    └──────────────┘    └──────┬─────────┘       │
│                                                   │                 │
└───────────────────────────────────────────────────┼─────────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Image Processing                                  │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │ Read File    │───▶│ Base64      │───▶│ Send to UI   │         │
│  │ (PNG/SVG)    │    │ Encode      │    │ (EventEmitter)│        │
│  └──────────────┘    └──────────────┘    └──────┬─────────┘       │
│                                                   │                 │
└───────────────────────────────────────────────────┼─────────────────┘
                                                    │
                                                    ▼
┌──────────────────┐
│  Display Image   │
│  in Chat UI      │
│  ✅ Success!     │
└──────────────────┘
```

---

## Key Components

### 1. **EventEmitter** - Status Updates
- `progress_update()`: Shows "Validating...", "Generating..."
- `success_update()`: Shows "Diagram created successfully!"
- `error_update()`: Shows error messages
- `send_image()`: Sends Base64-encoded image to UI

### 2. **Code Validation** - Security
- Blocks dangerous imports (os, sys, subprocess)
- Blocks dangerous functions (eval, exec, open)
- Syntax checking

### 3. **Code Execution** - Sandboxed
- Runs in isolated namespace
- Only diagrams library available
- Output directory isolation

### 4. **diagrams Library** - Rendering
- Parses Python code
- Creates graph structure
- Renders with Graphviz

---

## Error Handling Flow

```
Error occurs
    │
    ▼
┌──────────────────┐
│ Exception caught │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ error_update()   │
│ Send error msg   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Return error     │
│ message string   │
└──────────────────┘
```

---

## Configuration (UserValves)

Users can configure:

- **OUTPUT_DIR**: Where to save diagrams (default: temp directory)
- **OUTPUT_FORMAT**: png, jpg, pdf, svg (default: png)
- **FILENAME_PREFIX**: Filename prefix (default: "diagram")

---

## Summary

The workflow is:
1. **User** requests diagram → **AI** generates code
2. **Tool** validates code → **Tool** modifies code
3. **Tool** executes code → **diagrams** renders image
4. **Tool** processes image → **Tool** sends to UI
5. **User** sees diagram in chat!

The entire process is **async**, **secure**, and **user-friendly** with real-time status updates.

