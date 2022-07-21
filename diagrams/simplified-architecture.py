# Copyright 2022 Adevinta

from diagrams import Cluster, Diagram
from diagrams.aws.general import User
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS, SNS
from diagrams.onprem.container import Docker

with Diagram("", outformat="png", filename="docs/img/simplified-architecture", show=False):
        result_queue = SQS("result-queue")

        with Cluster("Agents"):
                agents = [ EC2("agent-1"), EC2("agent-2"), EC2("agent-N") ]
                with Cluster("Checks"):
                        checks = [ Docker("check-1"), Docker("check-2"), Docker("check-N") ]
                agents[0] >> checks

        with Cluster("Vulnerability DB"):
                vulndb_consumer = EC2("vulndb-consumer")
                vulndb_api = EC2("vulndb-api")
                vulndb_db = RDS("vulndb-db")
                vulndb_consumer >> vulndb_db
                vulndb_api >> vulndb_db
       
        scan_engine = EC2("scan-engine")
        check_queue = SQS("check-queue")
        
        with Cluster("Vulcan API"):
                vulcan_api = EC2("vulcan-api")
                vulcan_api_db = RDS("vulcan-api-db")
                vulcan_api >> vulcan_api_db

        user = User("user")

        vulcan_api >> vulndb_api
        user >> vulcan_api >> scan_engine
        scan_engine >> check_queue >> agents
        checks >> result_queue >> vulndb_consumer
