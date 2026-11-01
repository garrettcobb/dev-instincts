> Template. Replace `<APP>` with your application's name. Written for an offline desktop web app; drop the offline sections if yours isn't one.

# <APP> — 100% FUNCTIONALITY, DEFECT, LOGIC, UI COMPLIANCE, AND OFFLINE CONFINEMENT AUDIT & REMEDIATION

## MISSION

Conduct a comprehensive, end-to-end review of the entire <APP> application to identify, document, correct, and verify every discoverable defect, bug, glitch, bottleneck, broken workflow, logical inconsistency, architectural weakness, usability issue, and deviation from established UI/UX guidance.

Additionally, establish and verify that <APP> is a completely offline, locally confined desktop application.

This is not a superficial code review, static analysis exercise, or cosmetic cleanup.

This is a full application functionality, security, offline architecture, and quality assurance assignment.

**The objective is to make <APP> a thoroughly tested, internally consistent, reliable, maintainable, production-ready application that operates entirely within its designated PC environment without requiring or initiating external network communications.**

Do not assume existing code is correct simply because it compiles, existing functionality is present, or a workflow appears to work under normal conditions.

---

## 1. ESTABLISH THE APPLICATION BASELINE

Before making changes:

1. Examine the entire repository and understand its structure.
2. Review the architecture, technology stack, dependencies, configuration, and application entry points.
3. Review existing documentation, requirements, architectural decisions, UI guidance, and development conventions.
4. Identify all modules, features, pages, components, services, APIs, database entities, background processes, and integrations.
5. Map dependencies and interactions between components.
6. Identify existing tests and determine their actual coverage.
7. Establish the current build, test, and runtime baseline.
8. Identify known limitations and areas where requirements are ambiguous.
9. Identify every component capable of accessing the network, filesystem, operating system, or external resources.

Create a complete functionality inventory and establish a traceable relationship between requirements, implementation, and tests.

Do not begin broad modifications before understanding the existing system.

## 2. COMPLETE FUNCTIONALITY AUDIT

Examine every feature, module, page, component, control, process, and user workflow.

Verify that:

- Every feature performs its intended function.
- Every button, link, menu, form, field, selector, filter, and action works correctly.
- Every input is validated appropriately.
- Every output displays accurate information.
- Navigation works consistently.
- State changes propagate correctly.
- Data is saved, retrieved, updated, and deleted correctly.
- Errors are handled appropriately.
- Loading, empty, success, and failure states are implemented.
- User permissions are enforced.
- Session management behaves correctly.
- No controls or features are decorative, misleading, disconnected, or nonfunctional.
- No functionality is inaccessible through its intended workflow.

Test both individual features and complete workflows across modules.

Test normal, abnormal, boundary, and failure conditions.

## 3. DEFECT AND CODE QUALITY AUDIT

Identify and correct all discoverable:

- Functional defects.
- Runtime exceptions.
- Compilation and type errors.
- Incorrect business logic.
- Incorrect calculations.
- Null reference errors.
- Race conditions.
- Incorrect asynchronous behavior.
- Resource leaks.
- Unhandled exceptions.
- Dead or unreachable code.
- Duplicate or conflicting logic.
- Incorrect error propagation.
- Broken integrations.
- Incomplete implementations.
- Incorrect conditional behavior.
- Unexpected application behavior.

Correct identified defects rather than merely reporting them.

## 4. BUSINESS LOGIC AND PROCESS VALIDATION

Examine whether every process makes operational sense.

For every major workflow:

1. Identify the intended starting condition.
2. Identify required inputs and prerequisites.
3. Examine every decision point.
4. Verify operation sequencing.
5. Identify valid and invalid state transitions.
6. Examine failure behavior.
7. Verify resulting data and application state.
8. Confirm appropriate user feedback.

Identify contradictory rules, unnecessary complexity, circular dependencies, redundant operations, missing safeguards, and processes that technically execute but produce illogical results.

Do not preserve flawed logic merely because it is already implemented.

Document ambiguous business requirements instead of inventing them.

## 5. DATABASE AND DATA INTEGRITY

Examine all database interactions, schemas, relationships, constraints, migrations, queries, and transaction boundaries.

Verify:

- Referential integrity.
- Appropriate uniqueness constraints.
- Required field validation.
- Null handling.
- Accurate persistence.
- Correct update and deletion behavior.
- Duplicate submission protection.
- Transaction rollback behavior.
- Concurrent modification handling.
- Consistency across related records.

**CRITICAL REQUIREMENT — TRANSACTIONAL AUDIT INTEGRITY**

Every successful procurement state change and its corresponding audit event must be committed atomically within the same database transaction.

Neither may persist independently.

Verify that:

- Successful state changes always produce corresponding audit events.
- Failed state changes do not leave successful-looking audit records.
- Failed audit writes roll back associated procurement changes.
- Transaction failures never leave partially completed operations.
- Retries do not create duplicate audit events.
- Audit events accurately represent committed operations.
- Historical audit information is preserved.

Treat this as a mandatory architectural and functional invariant.

## 6. PERFORMANCE AND BOTTLENECK ANALYSIS

Examine:

- Slow database queries.
- Excessive database calls.
- Unnecessary API requests.
- Inefficient processing.
- Memory consumption.
- Resource utilization.
- Blocking operations.
- Unnecessary rendering.
- Excessive component updates.
- Large payloads.
- Inefficient algorithms.
- Unnecessary dependencies.

Measure performance where possible.

Identify the bottleneck, establish its impact, implement an appropriate correction, and verify the improvement.

## 7. UI/UX COMPLIANCE AND CORRECTION

Conduct a complete review against all established <APP> UI guidance, design conventions, and documented requirements.

Evaluate:

**Consistency**
- Layouts, spacing, alignment, typography, colors, components, navigation, and terminology.

**Usability**
- Information hierarchy.
- Intuitive workflows.
- Clear labels and instructions.
- Appropriate validation.
- Understandable error messages.
- Appropriate confirmation for consequential actions.

**Visual integrity**
- Overlapping elements.
- Clipped content.
- Broken layouts.
- Incorrect sizing.
- Unexpected scrolling.
- Misaligned components.
- Visual glitches.
- Inconsistent component states.

**Responsive behavior**
- Supported screen sizes.
- Layout adaptation.
- Functional controls.
- No unintended horizontal overflow.

**Accessibility**
- Semantic elements.
- Keyboard navigation.
- Visible focus indicators.
- Appropriate contrast.
- Accessible labels.
- Logical tab order.

Correct all identified deviations.

Do not introduce arbitrary design changes or redesign functioning components without justification.

## 8. MANDATORY 100% OFFLINE AND LOCAL PC CONFINEMENT

This is a non-negotiable architectural requirement.

<APP> must operate entirely within the designated PC environment.

It must not require internet connectivity or communicate with external systems to perform any application functionality.

### 8.1 Prohibited external dependencies

Identify and eliminate dependencies on:

- Cloud hosting.
- Remote application servers.
- Remote databases.
- Cloud storage.
- External APIs.
- Internet-hosted JavaScript, CSS, fonts, images, or other assets.
- CDN resources.
- Remote authentication providers.
- Cloud-based logging.
- External analytics.
- Telemetry services.
- Crash-reporting services that transmit data externally.
- Remote configuration services.
- Internet-based licensing checks.
- External update services required for normal operation.
- Any other external service required for application functionality.

All necessary application resources must be available locally.

### 8.2 Network isolation

Examine the entire codebase for:

- HTTP and HTTPS requests.
- WebSocket connections.
- DNS lookups.
- External socket connections.
- Background network activity.
- Automatic update checks.
- Telemetry and tracking.
- Remote resource loading.
- Third-party service initialization.
- Unnecessary outbound connections.
- Hidden network dependencies.

Inspect dependencies and application configuration for functionality that initiates external communications.

Do not assume that network access is absent simply because the application does not visibly use the internet.

### 8.3 Local data confinement

Verify that:

- All application data is stored locally.
- All database operations use local resources.
- All application documents and files remain within approved local storage locations.
- All logs remain local.
- All backups remain local unless explicitly authorized otherwise.
- No data is silently transmitted externally.
- No cloud synchronization occurs.
- No external database is required.
- Application functionality remains available without internet access.

Identify every location where <APP> reads, writes, caches, or stores information.

Document the approved local storage architecture.

### 8.4 Dependency confinement

Inspect every direct and transitive dependency.

Determine whether any dependency:

- Requires internet access during normal execution.
- Downloads resources dynamically.
- Sends telemetry.
- Performs remote validation.
- Communicates with third-party services.
- Requires a cloud-hosted component.

Replace unnecessary remote dependencies with suitable local alternatives.

Package required assets and runtime resources locally.

Do not introduce unnecessary dependencies when existing local capabilities are sufficient.

### 8.5 Authentication and licensing

Verify that application authentication and authorization operate locally.

<APP> must not require:

- Online account authentication.
- External identity providers.
- Remote license validation.
- Cloud-based session management.
- Internet connectivity for application startup or normal use.

Preserve appropriate local authentication and authorization safeguards.

### 8.6 Offline operation testing

Conduct actual offline testing.

At minimum:

1. Build and install <APP> in its intended PC environment.
2. Disconnect the PC from the internet.
3. Launch <APP>.
4. Navigate every major application module.
5. Execute every critical workflow.
6. Create, update, retrieve, and delete permitted records.
7. Verify database operations.
8. Verify audit logging.
9. Verify file operations.
10. Verify application startup, shutdown, and restart.
11. Verify that no feature unexpectedly requires network connectivity.
12. Verify that no external network communication is attempted during normal operation.

Use operating-system network monitoring, firewall logs, or equivalent tools to verify network behavior.

Where possible, perform testing with outbound network access blocked.

**Acceptance requirement: Zero required external network dependencies and zero unauthorized outbound communications during normal application operation.**

If any external communication is detected, identify its origin, purpose, data involved, and whether it is necessary. Remove or disable unauthorized communication and retest.

Development-time package retrieval and installation must be distinguished from runtime application behavior. Required dependencies must be available locally for deployment and normal execution.

## 9. SECURITY AND ERROR HANDLING

Review:

- Authentication.
- Authorization.
- Input validation.
- Injection vulnerabilities.
- Sensitive information exposure.
- Insecure configuration.
- Session handling.
- Error information disclosure.
- Logging.
- File handling.
- Dependency vulnerabilities.
- Protection around consequential operations.

Verify that failures are handled safely and predictably.

Never silently swallow exceptions or disguise failures as successful operations.

## 10. AUTOMATED AND MANUAL TESTING

Build or improve the test suite as necessary.

Perform:

- Unit testing.
- Integration testing.
- API testing.
- Database testing.
- End-to-end testing.
- UI interaction testing.
- Regression testing.
- Negative testing.
- Boundary-condition testing.
- Concurrency testing where applicable.
- Performance testing.
- Offline operation testing.
- Network isolation testing.
- Local data confinement testing.

Include scenarios involving:

- Missing information.
- Invalid information.
- Duplicate submissions.
- Interrupted operations.
- Database failures.
- API failures.
- Permission restrictions.
- Unexpected user actions.
- Concurrent operations.
- Session expiration.
- Recovery and retry behavior.
- Internet disconnection.
- Network access blocked.
- Application restart while offline.

Every corrected defect should have an appropriate regression test whenever practical.

A passing build is not proof of application correctness.

## 11. IMPLEMENT CORRECTIONS

After identifying defects:

1. Prioritize by severity and operational impact.
2. Correct critical functional and data-integrity defects first.
3. Correct workflow and business-logic problems.
4. Correct integration and performance issues.
5. Correct UI/UX inconsistencies.
6. Correct offline architecture violations.
7. Eliminate unauthorized external communications.
8. Improve maintainability where justified.
9. Add or update automated tests.
10. Revalidate affected modules and dependent workflows.

Preserve established architectural decisions unless a demonstrable defect requires a change.

Do not:
- Introduce unnecessary frameworks or dependencies.
- Rewrite functioning code without justification.
- Remove features to make tests pass.
- Weaken security controls.
- Introduce hardcoded workarounds.
- Conceal defects.
- Modify requirements without authorization.
- Introduce cloud or internet dependencies.

## 12. FINAL REGRESSION AND ACCEPTANCE REVIEW

After corrections:

1. Rebuild the entire application.
2. Run the complete automated test suite.
3. Run all critical end-to-end workflows.
4. Verify database integrity.
5. Verify procurement and audit transaction integrity.
6. Verify UI compliance.
7. Verify security-related corrections.
8. Verify local data storage.
9. Verify offline operation.
10. Verify outbound network isolation.
11. Recheck application startup and shutdown.
12. Confirm that no regressions were introduced.

Repeat failed tests after corrections and record their final results.

## 13. REQUIRED DELIVERABLES

Produce a comprehensive final audit report containing:

**A. Application coverage**
- Modules examined.
- Features examined.
- Workflows tested.
- Areas not accessible or testable.

**B. Defect register**
- Unique identifier.
- Affected module.
- Description.
- Severity.
- Root cause.
- Correction implemented.
- Verification performed.
- Final status.

**C. UI/UX compliance report**
- Identified deviations.
- Applicable guidance.
- Corrections implemented.
- Remaining discrepancies.

**D. Performance report**
- Bottlenecks.
- Measurements.
- Corrections.
- Verified results.

**E. Offline architecture report**
- External dependencies identified.
- Dependencies eliminated or replaced.
- Local database and storage architecture.
- Network activity examination.
- Offline testing results.
- Firewall or network isolation verification.
- Remaining network-related risks.

**F. Testing report**
- Tests executed.
- Tests passed.
- Tests failed.
- Tests not executed.
- Coverage gaps.
- Offline verification results.

**G. Outstanding issues**
- Unresolved defects.
- Known limitations.
- Unverified assumptions.
- External dependencies.
- Required human decisions.

**H. Final readiness assessment**
Provide an evidence-based determination of whether <APP> is ready for its intended operating environment.

## 14. EXECUTION RULES — NON-NEGOTIABLE

1. Be exhaustive, methodical, and evidence-driven.
2. Examine the entire application, not just recently modified files.
3. Never assume functionality works without testing it.
4. Never report a defect as corrected until verified.
5. Never report a test as passed unless it was actually executed successfully.
6. Never conceal failed tests or incomplete coverage.
7. Never make unsupported assumptions about business requirements.
8. Preserve existing functionality and architectural intent.
9. Record significant changes and explain why they were necessary.
10. Prioritize correctness, data integrity, security, reliability, and maintainability.
11. Treat complete offline operation and PC confinement as mandatory acceptance criteria.
12. Do not claim offline compliance without actual network-isolation testing.

If an issue cannot be safely corrected without additional direction, document it and explain the required decision.

If the environment prevents testing, explicitly identify the limitation.

Do not stop after identifying problems. Implement appropriate corrections, test them, and continue until all accessible and actionable defects have been addressed.

## DEFINITION OF DONE

The assignment is complete only when:

- Every accessible application module has been examined.
- Every identified feature has been evaluated.
- All discovered and actionable defects have been corrected and verified.
- All critical workflows pass their applicable tests.
- Procurement state changes and audit events satisfy the atomic transaction invariant.
- UI components comply with established <APP> guidance or have documented exceptions.
- No known critical or high-severity defects remain unresolved.
- The application operates without internet access.
- All required application data remains local.
- No unauthorized outbound network communications occur during normal operation.
- No external service is required for normal application functionality.
- Regression testing has been completed.
- Remaining limitations and unverified areas are explicitly documented.
- A final evidence-based audit report has been delivered.

**FINAL DIRECTIVE: <APP> must be a fully functional, locally confined, offline desktop application. Do not claim 100% functionality or offline compliance based on assumptions, successful compilation, or superficial testing. Demonstrate compliance through actual examination, execution, and verification evidence.**