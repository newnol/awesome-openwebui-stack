"""
title: Diagram Generator (diagrams)

author: newnol

author_url: https://newnol.io.vn

git_url: https://github.com/newnol/open-webui-tools

description: A tool that generates cloud system architecture diagrams using the diagrams library. Accepts Python code to create diagrams and renders them as image files.

requirements: diagrams

version: 0.1.0

license: MIT
"""

from __future__ import annotations

from typing import Any, Callable, Optional
import asyncio
import os
import tempfile
import importlib.util
import sys
from pathlib import Path
from pydantic import BaseModel, Field


class EventEmitter:
    def __init__(self, event_emitter: Callable[[dict], Any] | None = None):
        self.event_emitter = event_emitter

    async def progress_update(self, description: str) -> None:
        await self.emit(description)

    async def error_update(self, description: str) -> None:
        await self.emit(description, "error", True)

    async def success_update(self, description: str) -> None:
        await self.emit(description, "success", True)

    async def emit(
        self,
        description: str = "Unknown State",
        status: str = "in_progress",
        done: bool = False,
    ) -> None:
        if self.event_emitter:
            await self.event_emitter(
                {
                    "type": "status",
                    "data": {
                        "status": status,
                        "description": description,
                        "done": done,
                    },
                }
            )

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
        
        # Check if diagram was created (check both with and without extension)
        possible_paths = [
            output_path,
            os.path.join(output_dir, f"{filename}.{format}"),
            os.path.join(output_dir, filename),
        ]
        
        # Also check for files created without explicit filename
        created_files = [f for f in os.listdir(output_dir) if f.endswith(f".{format}")]
        
        if created_files:
            # Use the most recently created file
            created_files.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
            output_path = os.path.join(output_dir, created_files[0])
            return True, output_path, ""
        elif os.path.exists(output_path):
            return True, output_path, ""
        else:
            # Check if any diagram file was created
            for path in possible_paths:
                if os.path.exists(path):
                    return True, path, ""
            return False, "", "Diagram file was not created. Make sure your code uses Diagram context manager correctly."
            
    except Exception as e:
        return False, "", f"Error executing diagram code: {str(e)}"
    finally:
        # Restore original working directory
        os.chdir(original_cwd)


class Tools:
    class Valves(BaseModel):
        CITATION: bool = Field(
            default=True, description="True or false for citation (not used yet)."
        )

    class UserValves(BaseModel):
        OUTPUT_DIR: str = Field(
            default="",
            description="Directory to save diagram files. Leave empty to use temporary directory.",
        )
        OUTPUT_FORMAT: str = Field(
            default="png",
            description="Output format for diagrams (png, jpg, pdf, svg). Default: png",
        )
        FILENAME_PREFIX: str = Field(
            default="diagram",
            description="Prefix for generated diagram filenames. Default: diagram",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.citation = self.valves.CITATION

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

        try:
            await emitter.progress_update("Validating diagram code...")

            if not code or not code.strip():
                raise ValueError("Code parameter cannot be empty")

            # Validate code safety
            is_valid, error_msg = _validate_diagram_code(code)
            if not is_valid:
                raise ValueError(error_msg)

            # Determine output directory
            user_valves = __user__["valves"]
            output_dir = user_valves.OUTPUT_DIR.strip()
            if not output_dir:
                # Use temporary directory
                output_dir = tempfile.mkdtemp(prefix="diagrams_")
            else:
                # Create directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)

            output_format = user_valves.OUTPUT_FORMAT.lower() or "png"
            if output_format not in ["png", "jpg", "jpeg", "pdf", "svg"]:
                output_format = "png"

            filename_prefix = user_valves.FILENAME_PREFIX.strip() or "diagram"

            await emitter.progress_update(f"Generating diagram ({output_format.upper()})...")

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

            # Execute diagram code in thread (blocking I/O)
            success, output_path, error_msg = await asyncio.to_thread(
                _execute_diagram_code,
                modified_code,
                output_dir,
                filename_prefix,
                output_format,
            )

            if not success:
                raise RuntimeError(error_msg or "Failed to generate diagram")

            await emitter.success_update(f"Diagram created successfully!")
            
            # Get file info
            file_size = os.path.getsize(output_path)
            file_size_kb = file_size / 1024
            
            # Send the image to chat
            await emitter.send_image(output_path, "Architecture Diagram")
            
            return f"Diagram generated successfully!\n\nFile: {output_path}\nSize: {file_size_kb:.2f} KB\nFormat: {output_format.upper()}"

        except ValueError as e:
            error_message = f"Validation error: {str(e)}"
            await emitter.error_update(error_message)
            return error_message
        except Exception as e:
            error_message = f"Error creating diagram: {str(e)}"
            await emitter.error_update(error_message)
            return error_message


if __name__ == "__main__":
    # CLI testing support
    import argparse

    parser = argparse.ArgumentParser(description="Generate diagram from Python code.")
    parser.add_argument(
        "code_file",
        help="Path to Python file containing diagram code, or '-' to read from stdin",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="",
        help="Output directory (default: temporary directory)",
    )
    parser.add_argument(
        "--format",
        "-f",
        default="png",
        choices=["png", "jpg", "jpeg", "pdf", "svg"],
        help="Output format (default: png)",
    )
    parser.add_argument(
        "--filename",
        "-n",
        default="diagram",
        help="Output filename prefix (default: diagram)",
    )
    args = parser.parse_args()

    # Read code
    if args.code_file == "-":
        code = sys.stdin.read()
    else:
        with open(args.code_file, "r", encoding="utf-8") as f:
            code = f.read()

    # Create tool instance
    tools = Tools()
    user_valves = tools.UserValves()
    user_valves.OUTPUT_DIR = args.output_dir
    user_valves.OUTPUT_FORMAT = args.format
    user_valves.FILENAME_PREFIX = args.filename

    # Run async function
    import asyncio

    result = asyncio.run(
        tools.create_diagram(code, __user__={"valves": user_valves})
    )
    print(result)

