# Copyright 2022 Adevinta

from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.compute import Pod
from diagrams.onprem.client import User, Client
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.engagement import SES
from diagrams.aws.integration import SNS, SQS
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis

with Diagram("Detailed Vulcan Architecture", outformat="png", filename="docs/img/detailed-architecture", show=False):
        with Cluster("Clients"):
                user = User("user")
                vulcan_ui = Pod("vulcan-ui")

        with Cluster("Vulcan Service"):
                with Cluster("Vulcan API"):
                        vulcan_api = Pod("vulcan-api")
                        vulcan_api_db = RDS("vulcan-api-db")
                        vulcan_api >> vulcan_api_db

                with Cluster("Vulnerability DB"):
                        vulndb_consumer = Pod("vulndb-consumer")
                        vulndb_api = Pod("vulndb-api")
                        vulndb_db = RDS("vulndb-db")
                        vulndb_consumer >> vulndb_db
                        vulndb_api >> vulndb_db

                with Cluster("Vulcan Crontinuous"):
                        vulcan_crontinuous = Pod("vulcan-crontinuous")
                        vulcan_crontinuous_storage = S3("vulcan-crontinuous-storage")
                        vulcan_crontinuous >> vulcan_crontinuous_storage

                with Cluster("Vulcan Reports Generator"):
                        vulcan_reports_generator = Pod("vulcan-reports-generator")
                        vulcan_reports = SES("vulcan-reports")

                reports_queue = SQS("reports-queue")

        with Cluster("Vulcan Core"):
                scan_engine_queue = SQS("scan-engine-queue")
                check_queue = SQS("check-queue")

                with Cluster("Vulcan Stream"):
                        vulcan_stream= Pod("vulcan-stream")
                        vulcan_stream_cache = Redis("vulcan-stream-cache")
                        vulcan_stream >> vulcan_stream_cache

                with Cluster("Vulcan Persistence"):
                        vulcan_persistence = Pod("vulcan-persistence")
                        vulcan_persistence_db = RDS("vulcan-persistence")
                        vulcan_persistence >> vulcan_persistence_db

                with Cluster("Vulcan Results"):
                        vulcan_results = Pod("vulcan-results")
                        vulcan_results_storage = S3("vulcan-results-storage")
                        vulcan_results >> vulcan_results_storage

                with Cluster("Vulcan Scan Engine"):
                        vulcan_scan_engine = Pod("vulcan-scan-engine")
                        vulcan_scan_engine_db = RDS("vulcan-scan-engine-db")
                        scan_engine_queue >> vulcan_scan_engine
                        vulcan_scan_engine >> vulcan_scan_engine_db

                with Cluster("Vulcan Agent Cluster"):
                        vulcan_agents = AutoScaling("vulcan-agents")
                        vulcan_agents >> scan_engine_queue
                        with Cluster("Vulcan Check Cluster"):
                                vulcan_checks = Docker("vulcan-checks")

        with Cluster("Result Forwarding"):
                scan_result_topic = SNS("scan-result-topic")
                scan_result_queue = SQS("scan-result-queue")
                check_result_topic = SNS("check-result-topic")
                check_result_queue = SQS("check-result-queue")

        user >> vulcan_api
        user >> vulcan_ui
        vulcan_ui >> vulcan_api

        vulcan_api >> vulcan_scan_engine
        vulcan_api >> vulndb_api
        vulcan_api >> vulcan_crontinuous
        vulcan_api >> reports_queue
        vulcan_api >> vulcan_reports_generator

        reports_queue >> vulcan_reports_generator
        vulcan_reports_generator >> vulcan_reports
        vulcan_reports >> user

        scan_result_topic >> scan_result_queue
        scan_result_queue >> vulcan_api
        check_result_topic >> check_result_queue
        check_result_queue >> vulndb_consumer
        vulndb_consumer >> vulcan_results

        vulcan_scan_engine >> vulcan_persistence
        vulcan_scan_engine >> vulcan_stream
        vulcan_scan_engine >> check_queue
        vulcan_scan_engine >> scan_result_topic
        vulcan_scan_engine >> check_result_topic

        check_queue >> vulcan_agents
        vulcan_agents >> vulcan_results
        vulcan_agents >> vulcan_stream
        vulcan_agents >> vulcan_checks
        vulcan_checks >> vulcan_agents
