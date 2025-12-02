"""
Example diagram code that can be used with the diagram_generator tool.

This file contains example Python code snippets that create diagrams using
the diagrams library. You can copy these examples and use them with the
create_diagram tool in Open WebUI.
"""

# Example 1: Simple AWS Architecture
example_1_simple_aws = """
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Web Architecture", show=False):
    ELB("Load Balancer") >> EC2("Web Server") >> RDS("Database")
"""

# Example 2: AWS Architecture with Clusters
example_2_aws_clusters = """
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront, APIGateway

with Diagram("Serverless Architecture", show=False):
    with Cluster("Frontend"):
        cdn = CloudFront("CDN")
    
    with Cluster("API"):
        api = APIGateway("API Gateway")
        func = Lambda("Lambda Function")
    
    with Cluster("Data"):
        db = Dynamodb("DynamoDB")
        storage = S3("S3 Bucket")
    
    cdn >> api >> func >> db
    func >> storage
"""

# Example 3: Multi-Cloud Architecture
example_3_multicloud = """
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.gcp.compute import ComputeEngine
from diagrams.azure.compute import VM

with Diagram("Multi-Cloud Setup", show=False):
    with Cluster("AWS"):
        aws_vm = EC2("AWS Instance")
    
    with Cluster("GCP"):
        gcp_vm = ComputeEngine("GCP Instance")
    
    with Cluster("Azure"):
        azure_vm = VM("Azure VM")
    
    aws_vm >> gcp_vm >> azure_vm
"""

# Example 4: Kubernetes Architecture
example_4_k8s = """
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.storage import PV, PVC

with Diagram("Kubernetes Architecture", show=False):
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
"""

# Example 5: On-Premises Architecture
example_5_onprem = """
from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Prometheus, Grafana

with Diagram("On-Premises Infrastructure", show=False):
    with Cluster("Web Tier"):
        nginx = Nginx("Nginx")
        web = Server("Web Server")
    
    with Cluster("Application Tier"):
        app = Server("App Server")
    
    with Cluster("Data Tier"):
        postgres = PostgreSQL("PostgreSQL")
        mongo = MongoDB("MongoDB")
    
    with Cluster("Monitoring"):
        prom = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
    
    nginx >> web >> app >> postgres
    app >> mongo
    prom >> grafana
"""

# Example 6: Complex Microservices Architecture
example_6_microservices = """
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import APIGateway, ALB
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis

with Diagram("Microservices Architecture", show=False):
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
"""

if __name__ == "__main__":
    print("Diagram Examples for diagram_generator tool")
    print("=" * 50)
    print("\nExample 1: Simple AWS Architecture")
    print(example_1_simple_aws)
    print("\nExample 2: AWS Architecture with Clusters")
    print(example_2_aws_clusters)
    print("\nExample 3: Multi-Cloud Architecture")
    print(example_3_multicloud)
    print("\nExample 4: Kubernetes Architecture")
    print(example_4_k8s)
    print("\nExample 5: On-Premises Architecture")
    print(example_5_onprem)
    print("\nExample 6: Complex Microservices Architecture")
    print(example_6_microservices)

