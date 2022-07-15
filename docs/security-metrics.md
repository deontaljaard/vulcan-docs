# Security Metrics

Vulcan can be used to query dynamically calculated security metrics for any of its teams, an arbitrary aggregation of teams or globally for the whole organization. These metrics can be used to answer questions about the security status of the organization and to set specific and measurable goals that teams can track themselves. Metrics for a specific team are made directly available to the team through the Vulcan API so they can be tracked as they see fit. Global metrics are only available to Vulcan administrators.

Currently, the [Vulcan API](/vulcan-api/) exposes the following metrics:

- Mean time to remediate fixed findings by vulnerability severity. Filterable by date and score.
- Current exposure time of open findings by percentiles. Filterable by date and score.
- Number of vulnerabile assets by severity. Filterable by a list of asset identifiers.
- Number of open findings by severity. Filterable by date and score.
- Number of fixed findings by severity. Filterable by date and score.

All metrics can be aggregated by an arbitrary selection of teams.

Below are just some examples of how these metrics can be retrieved. For more comprehensive examples, refer to the `stats` and `global-stats` sections of the [Vulcan API specification](/vulcan-api/).

## Team Examples

The Vulcan API can be used to retrieve metrics for a team using the stats endpoint for the team.

### How many open vulnerabilities does a specific team have?
 
```bash
# Retrieve currently open findings.
curl -H "Authorization: Bearer $VULCAN_API_TOKEN" \
"www.vulcan.example.com/api/v1/teams/$TEAM_ID/stats/open"

{
  "open_issues": {
    "critical": 2,
    "high": 4,
    "medium": 9,
    "low": 11,
    "informational": 21
  }
}
```

### How long have critical vulnerabilities in a specific team been open for?

```bash
# Retrieve current exposure (in hours) of open findings.
curl -H "Authorization: Bearer $VULCAN_API_TOKEN" \
"www.vulcan.example.com/api/v1/teams/$TEAM_ID/stats/exposure/current?minScore=9"

{
  "current_exposure": {
    "mean": 41.209448947762005,
    "percentile_10": 36.78803730882772,
    "percentile_25": 50.75172645112574,
    "percentile_50": 54.29089680729741,
    "percentile_75": 72.78236287555608,
    "percentile_90": 98.52142968051862
  }
}
```

### How long does it take a specific team to resolve vulnerabilities on average?

```bash
# Retrieve Mean Time To Remediate (in hours) of fixed findings.
curl -H "Authorization: Bearer $VULCAN_API_TOKEN" \
"www.vulcan.example.com/api/v1/teams/$TEAM_ID/stats/mttr"

{
  "mttr": {
    "critical": 32.91856414183523,
    "high": 82.43581388518908,
    "medium": 140.39820739887437,
    "low": 265.17825863008089,
    "informational": 360.2830379559806,
    "total": 103.571544865095874
  }
}
```

## Global Examples

The Vulcan API can be used to retrieve the same metrics globally using the global stats endpoint.

### How long does it take our organization to resolve vulnerabilities on average?

```bash
# Retrieve Mean Time To Remediate (in hours) of fixed findings.
curl -H "Authorization: Bearer $VULCAN_API_TOKEN" \
"www.vulcan.example.com/api/v1/stats/mttr"

{
  "mttr": {
    "critical": 44.91856414183523,
    "high": 86.43581388518908,
    "medium": 139.39820739887437,
    "low": 267.17825863008089,
    "informational": 362.2830379559806,
    "total": 106.571544865095874
  }
}
```

### How many vulnerabilities has our organization fixed in the last quarter?

```bash
# Retrieve fixed findings between a date range.
curl -H "Authorization: Bearer $VULCAN_API_TOKEN" \
"www.vulcan.example.com/api/v1/stats/fixed?minDate=2021-09-01&maxDate=2021-12-01"

{
  "fixed_issues": {
    "critical": 19,
    "high": 43,
    "medium": 91,
    "low": 265,
    "informational": 141
  }
}
```
