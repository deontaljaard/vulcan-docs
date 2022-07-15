# Security Checks in CI/CD

By using [Vulcan Local](https://github.com/adevinta/vulcan-local/), engineers are able to check the security of their services before even commiting new changes. Vulcan Local be integrated into the CI/CD process by uploading a simple YAML file into the repository, which will allow Vulcan Local to not only detect issues in code, but also in the artifacts created during the build process (e.g. libraries, Docker images...) and even run as part of the end-to-end tests to dynamically find vulnerabilities in web applications. Vulcan Local can report its output in various formats and can return an error code if some security criteria is met; it also allows teams to exclude specific findings if needed.

## Build Example

This YAML file can be added into any repository to instruct Vulcan Local on how to scan it.

```yaml title="vulcan.yaml"
# Policy to use, can be an HTTP URL.
conf:
  repositories:
    - file://./script/checktypes-stable.json

# List of targets to scan with all relevant checks.
targets:
  - target: .
  - target: http://localhost:1234/

# List of specific checks to run.
checks:
  - type: vulcan-gitleaks
    target: .

  - type: vulcan-zap
    target: http://localhost:1234
```

Note that the `repositories` attribute allows developers to refer to an external security policy that will be used to decide which [checks to run and which configuration to use](https://github.com/adevinta/vulcan-local/blob/master/script/checktypes-stable.json) for any of the targets provided, besides the checks specified in the YAML file itself. This allows developers to fall back to a default policy defined by the organization.

With this file, invoking Vulcan Local in any build worker is as simple as executing two commands:

```bash
# Install Vulcan Local.
curl -sfL \
 https://raw.githubusercontent.com/adevinta/vulcan-local/master/script/get | sh
# Run it using the YAML configuration.
vulcan-local -c vulcan.yaml
```

## Local Example

Security engineers and software engineers can also use Vulcan Local to check the security of any reachable asset. This can be used to perform a quick security check or as part of the development process. For example, as a pre-commit hook to avoid pushing secrets to Github.

```bash
# Install Vulcan Local.
curl -sfL \
 https://raw.githubusercontent.com/adevinta/vulcan-local/master/script/get | sh
# Run all checks that match the "exposed" keyword (e.g. "vulcan-exposed-ftp")
# following the default policy against the target "http://www.example.com".
vulcan-local -t http://www.example.com -i exposed \
 -checktypes file://./script/checktypes-stable.json
```
