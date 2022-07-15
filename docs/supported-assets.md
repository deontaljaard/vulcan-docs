# Supported Assets

By default, Vulcan is able to manage and scan the following asset types.

| Asset Type    | Example Identifier                                | Example Checks                      |
|---------------|---------------------------------------------------|-------------------------------------|
| IP            |                                         127.0.0.1 | Exposed and vulnerable services.    |
| IPRange       |                                       10.0.0.0/16 | Exposed and vulnerable services.    |
| Hostname      |                                   www.example.com | Exposed and vulnerable services.    |
| DomainName    |                                       example.com | Phishing prevention and takeover.   |
| WebAddress    |                           https://www.example.com | Web application scanning and leaks. |
| AWSAccount    |                    arn:aws:iam::111111111111:root | Security misconfiguration.          |
| DockerImage   | registry.hub.docker.com/organisation/image:latest | Vulnerable libraries and packages.  |
| GitRepository |    https://github.com/organisation/repository.git | Vulnerable libraries and secrets.   |

Note that the difference between a `Hostname` and a `DomainName` is that the first is a DNS name that resolves to a specific IP address (via A or AAAA records) and the second is a registered DNS name (with a SOA record) that does not need to resolve to any specific address but may contain other DNS records such as TXT, MX or CNAME.

## Asset Creation

Since the Vulcan API (and the UI) allows assets to be provided without a type, it will attempt to guess its type based on the format, even going as far as to extract and create multiple assets from a single identifier. For example, Vulcan would create three assets from the `https://www.example.com` identifier: a `WebAddress` (`https://www.example.com`), a `Hostname` (`www.example.com`) and a `DomainName` (`example.com`). Vulcan also provide endpoints to supply an asset with its associated type so that just that specific assets is added to Vulcan.
