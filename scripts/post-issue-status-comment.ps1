param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,

    [Parameter(Mandatory = $true)]
    [int]$IssueNumber,

    [Parameter(Mandatory = $true)]
    [ValidateSet("completed", "in-progress")]
    [string]$Status,

    [Parameter(Mandatory = $true)]
    [string[]]$ProgressItems,

    [Parameter(Mandatory = $true)]
    [string[]]$Artifacts,

    [Parameter(Mandatory = $true)]
    [string[]]$Decisions,

    [string[]]$NextActions = @(),

    [string]$Date = (Get-Date).ToString("yyyy-MM-dd"),

    [switch]$PreviewOnly
)

$gh = "C:\Program Files\GitHub CLI\gh.exe"
if (-not (Test-Path $gh)) {
    throw "GitHub CLI executable not found at: $gh"
}

if ($Status -eq "in-progress" -and $NextActions.Count -eq 0) {
    throw "In-progress status requires at least one item in -NextActions."
}

$lines = New-Object System.Collections.Generic.List[string]
$statusTitle = if ($Status -eq "completed") { "Completed" } else { "In progress" }

$lines.Add("Status update: $statusTitle ($Date)")
$lines.Add("")

if ($Status -eq "completed") {
    $lines.Add("## What was done")
} else {
    $lines.Add("## Current progress")
}

foreach ($item in $ProgressItems) {
    $lines.Add("- $item")
}

$lines.Add("")
if ($Status -eq "completed") {
    $lines.Add("## Artifacts")
} else {
    $lines.Add("## In-progress artifact")
}

foreach ($artifact in $Artifacts) {
    $lines.Add("- $artifact")
}

$lines.Add("")
if ($Status -eq "completed") {
    $lines.Add("## Decisions")
} else {
    $lines.Add("## Decisions made")
}

foreach ($decision in $Decisions) {
    $lines.Add("- $decision")
}

if ($Status -eq "in-progress") {
    $lines.Add("")
    $lines.Add("## Next actions")
    for ($i = 0; $i -lt $NextActions.Count; $i++) {
        $lines.Add("$($i + 1). $($NextActions[$i])")
    }
}

$body = [string]::Join("`n", $lines)

if ($PreviewOnly) {
    Write-Output "--- Issue comment preview ---"
    Write-Output $body
    exit 0
}

& $gh issue comment $IssueNumber --repo $Repo --body $body
if ($LASTEXITCODE -ne 0) {
    throw "Failed to post issue comment."
}

Write-Output "Posted formatted status comment to issue #$IssueNumber in $Repo"