# NetForge

NetForge is a networking and performance testing learning project built with Python, Linux networking tools, Docker, and GitHub Actions.

It includes network checks, HTTP/ping/iperf3 benchmarking, performance regression detection, Docker-based integration testing, and Linux `tc` fault injection for latency, packet loss, and bandwidth scenarios.

## Performance CI Architecture

Performance measurements on standard GitHub-hosted runners are inherently noisy because the jobs run on shared, virtualized infrastructure whose CPU scheduling and available resources can vary between runs.

NetForge reduces that noise by using **relative performance benchmarking** instead of treating one absolute benchmark result as a stable machine-wide baseline.

For each CI run, NetForge:

1. Benchmarks the baseline commit on the GitHub-hosted runner.
2. Runs each benchmark multiple times.
3. Aggregates the repeated measurements using the median.
4. Checks out the current commit on the **same runner**.
5. Repeats the same benchmark process.
6. Compares the current result against the baseline using configurable regression thresholds.
7. Uploads both benchmark reports as GitHub Actions artifacts for inspection.

The current benchmark set covers:

- HTTP response latency (`p95`)
- Ping latency (`p95`)
- Network throughput using `iperf3`

This design does not eliminate CI noise, but it reduces cross-runner variability and makes large performance regressions more meaningful than comparing unrelated absolute results from different virtual machines.

### Why the thresholds are intentionally broad

The current GitHub-hosted CI performance gate is intended to detect **large regressions**, not small percentage-level performance changes. Tight thresholds on shared runners would create false failures caused by temporary CPU, scheduler, virtualization, or networking variability rather than real code regressions.

For that reason, the CI thresholds remain deliberately conservative until measurements are collected in a more controlled environment.

### Future strict performance testing

If NetForge later needs to detect small performance changes reliably, the appropriate next step is a dedicated or self-hosted performance runner with controlled hardware and workload conditions. Strict absolute throughput or latency guarantees should not rely on general-purpose GitHub-hosted runners.

The existing `tc` fault-injection functionality remains focused on validating behavior under controlled network degradation such as latency, packet loss, and bandwidth limits; it is separate from the relative performance-regression gate.
