# Developing Checks

Developing checks using the Go programming language is made simple using the Vulcan Check SDK. There is a [large library of checks](https://github.com/adevinta/vulcan-checks/tree/master/cmd) that can be taken as a reference. This page will show a commented skeleton to develop a simple check from scratch.

The main code of the check is found in the `main.go` file.

```go title="main.go"
package main

import (
  "context"
  "errors"

  check "github.com/adevinta/vulcan-check-sdk"
  "github.com/adevinta/vulcan-check-sdk/helpers"
  checkstate "github.com/adevinta/vulcan-check-sdk/state"
  report "github.com/adevinta/vulcan-report"
)

var (
  checkName  = "vulcan-example"
  logger     = check.NewCheckLog(checkName)
  heartbleedVuln = report.Vulnerability{
    CWEID:   326, // The applicable CWE ID for the vulnerability class.
    Summary: "Example Vulnerability", // A title summary for the vulnerability.
    Description: "A comprehensive description of the vulnerability.",
    Score: 8.9, // The severity of the vulnerability.
    ImpactDetails: "Details about the potential impact of the vulnerability.",
    References: []string{ // Links to references with more information.
      "https://cve.mitre.org/", // It is common to link the advisory.
    },
    Recommendations:  []string{"A specific recommendation."},
    Labels:           []string{"issue", "ssl"}, // Labels for filtering.
    AffectedResource: "443/tcp", // Specific target resource checked.
    // Fingerprint to separate instances of the same vulnerability.
    // Used to re-open false positives if the circumstances change.
    // No arguments indicate that the circumstances cannot change.
    Fingerprint:      helpers.ComputeFingerprint(),
  }
)

func isVulnerable(host string) (bool, error) {
  // Add the actual logic to check for the vulnerability here.
  return true, nil
}

func main() {
  run := func(ctx context.Context, target, assetType, 
    optJSON string, state checkstate.State) (err error) {
   
    // Verify that the check has a target. 
    if target == "" {
      return errors.New("check target missing")
    }

    // Use the SDK to verify if the check can reach the target.
    // Reachability is defined differently depending on the asset type.
    isReachable, err := helpers.IsReachable(target, assetType, nil)
    if err != nil {
      logger.Warnf("cannot check asset reachability: %v", err)
    }
    if !isReachable {
      return checkstate.ErrAssetUnreachable
    }

    // Call the actual function that will assess the target.
    vulnerable, err := isVulnerable(target)
    if err != nil {
      state.Notes = err.Error()
    }

    if vulnerable {
      // Add the defined vulnerability to the state of the check.
      state.AddVulnerabilities(vulnerability)
    }

    return nil
  }

  c := check.NewCheckFromHandler(checkName, run)
  c.RunAndServe()
}
```

The `manifest.toml` file contains the metadata of the check.

```toml title="manifest.toml"
# The visible description of the check.
Description = "Checks if an asset is vulnerable to an example vulnerability."
# The asset types that the check will be used for by default.
AssetTypes = ["Hostname", "IP"]
```

The `local.toml` file can be used to specify an example target for the check. This information is used when running the check binary on testing mode as we will see below.

```toml title="local.toml"
[Check]
Target = "example.com" # Relevant target for the check.
AssetType = "Hostname" # Asset type of the target.
```

To use the `local.toml` file to test a check before deploying it, you can just compile the binary and run it with the `-t` parameter from the same directory as the `local.toml` file.

```bash
go build -o vulcan-example main.go
./vulcan-example -t
```

The `Dockerfile` file specifies how to package the check into a container image. This is specially relevant when the check requires to run in an specific environment such as when the Go code must execute third-party commands or interact with other applications. Otherwise, it will just copy and set the Go binary as the entry point for the container.

```Dockerfile title="Dockerfile"
FROM alpine
ADD vulcan-example /vulcan-example
CMD ["/vulcan-example"]
```

The container can be built, tested and deployed using the [Vulcan Check Build System](https://github.com/adevinta/vulcan-checks-bsys). In a complete Vulcan deployment, this should happen automatically as part of the CI/CD process.
