# Continuous Scanning

Teams can create their own Vulcan team and add their assets there simply by pasting a list of identifiers (e.g. web addresses, hostnames, Github URL, AWS account ARN...) through the Vulcan user interface. By default, Vulcan will automatically start scanning those assets on a weekly schedule with checks that have been assessed to be not intrussive. Teams can manage their members and recipients, which will automatically receive a weekly report of the changes in the security of their assets. Through that report or directly on the Vulcan user interface, the team will be able to see which issues have been found in their assets and which assets need attention. All findings are accompanied with clear descriptions and information to help with remmediation. Users can autonomously mark findings as false positive and provide a rationale for it.

## Examples

<figure markdown>
  [![Periodic Scans](img/screenshots/periodic-scans.png)](img/screenshots/periodic-scans.png)
  <figcaption>Vulcan web interface showing periodic scans for a team.</figcaption>
</figure>

<figure markdown>
  [![Vulcan Report](img/screenshots/vulcan-report.png)](img/screenshots/vulcan-report.png)
  <figcaption>Vulcan web interface showing currently open findings for a team.</figcaption>
</figure>

<figure markdown>
  [![Finding Details](img/screenshots/finding-details.png)](img/screenshots/finding-details.png)
  <figcaption>Vulcan web interface showing the details of a specific finding.</figcaption>
</figure>
