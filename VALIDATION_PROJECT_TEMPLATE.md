# GitHub Project Template: Offline Validation Infrastructure

This document provides templates for creating GitHub issues and organizing them into a project board. Use this to quickly set up the validation infrastructure project.

## Project Structure

**Project Name**: Offline Validation Infrastructure

**Description**: Implement comprehensive offline validation to reduce dependency on physical robot testing. This project covers CI/CD, linting, unit testing, integration testing, dry-running, and simulation capabilities.

**Project Views**:
1. **Board**: Track work by status (Backlog, Todo, In Progress, Done)
2. **Timeline**: Visualize milestone progression
3. **Epic View**: Group by epic
4. **Priority View**: Sort by priority

## Issue Templates

### Epic 1: CI/CD Foundation

#### Issue #1: Set up GitHub Actions workflow for Python builds
```yaml
Title: Set up GitHub Actions workflow for Python builds
Labels: validation-infrastructure, ci-cd, epic-1-foundation
Milestone: Foundation
Priority: High
Epic: CI/CD Foundation

Description:
Create a GitHub Actions workflow that validates Python code builds successfully.

**Acceptance Criteria:**
- [ ] Workflow runs on all pushes and PRs
- [ ] Poetry installs dependencies successfully
- [ ] All Python files compile without syntax errors
- [ ] Workflow completes in < 5 minutes
- [ ] Status badge added to README

**Technical Details:**
- Create `.github/workflows/python-build.yml`
- Use Poetry for dependency management
- Cache Poetry dependencies for speed
- Run `python -m py_compile` on all .py files
- Verify `poetry.lock` is in sync

**Reference**: VALIDATION_ROADMAP.md - Section 1.1
```

#### Issue #2: Add React Native build validation
```yaml
Title: Add React Native build validation
Labels: validation-infrastructure, ci-cd, epic-1-foundation, javascript
Milestone: Foundation
Priority: High
Epic: CI/CD Foundation

Description:
Create a GitHub Actions workflow for the React Native app in `orion_disaster_app/`.

**Acceptance Criteria:**
- [ ] Workflow runs when `orion_disaster_app/` changes
- [ ] npm dependencies install successfully
- [ ] JavaScript/JSX files validate
- [ ] No build errors
- [ ] Workflow completes in < 5 minutes

**Technical Details:**
- Create workflow or extend existing
- Run `npm ci` to install dependencies
- Cache `node_modules` for performance
- Validate package-lock.json is current
- Consider expo-cli validation if applicable

**Reference**: VALIDATION_ROADMAP.md - Section 1.2
```

#### Issue #3: Configure multi-version Python testing
```yaml
Title: Configure multi-version Python testing
Labels: validation-infrastructure, ci-cd, epic-1-foundation, enhancement
Milestone: Foundation
Priority: Medium
Epic: CI/CD Foundation

Description:
Test builds against multiple Python versions to ensure compatibility.

**Acceptance Criteria:**
- [ ] Matrix build for Python 3.9, 3.11, 3.12
- [ ] Main version (3.9) is required
- [ ] Other versions are informational
- [ ] Matrix results clearly reported

**Technical Details:**
- Use GitHub Actions matrix strategy
- Test against project's supported Python versions
- Configure strategy.fail-fast appropriately
- Consider Pi's Python version as primary

**Reference**: VALIDATION_ROADMAP.md - Section 1.3
```

#### Issue #4: Create PR status check requirements
```yaml
Title: Create PR status check requirements
Labels: validation-infrastructure, ci-cd, epic-1-foundation, documentation
Milestone: Foundation
Priority: Medium
Epic: CI/CD Foundation

Description:
Configure branch protection rules to require CI checks before merging.

**Acceptance Criteria:**
- [ ] Main branch protected
- [ ] Build checks required for merge
- [ ] Documentation updated
- [ ] Team notified of new requirements

**Technical Details:**
- Navigate to Settings > Branches
- Add branch protection rule for main/master
- Require status checks to pass
- Document override process for maintainers

**Reference**: VALIDATION_ROADMAP.md - Gating Strategy
```

#### Issue #5: Document CI setup for contributors
```yaml
Title: Document CI setup for contributors
Labels: validation-infrastructure, documentation, epic-1-foundation
Milestone: Foundation
Priority: Medium
Epic: CI/CD Foundation

Description:
Create clear documentation for contributors about CI/CD pipeline.

**Acceptance Criteria:**
- [ ] CONTRIBUTING.md updated with CI info
- [ ] Local testing instructions provided
- [ ] Common CI errors documented
- [ ] Troubleshooting guide included

**Technical Details:**
- Explain what CI checks run
- How to run checks locally
- How to interpret CI results
- What to do if checks fail

**Reference**: VALIDATION_ROADMAP.md - Multiple sections
```

---

### Epic 2: Linting and Code Quality

#### Issue #6: Enable Ruff linting in CI
```yaml
Title: Enable Ruff linting in CI
Labels: validation-infrastructure, linting, epic-2-linting
Milestone: Foundation
Priority: High
Epic: Linting and Code Quality

Description:
Add Ruff linting to CI pipeline to enforce code quality.

**Acceptance Criteria:**
- [ ] Ruff runs in CI on all Python files
- [ ] Configuration in pyproject.toml validated
- [ ] Initial run is informational (warnings only)
- [ ] Results posted to PR comments

**Technical Details:**
- Add Ruff step to Python workflow
- Use existing pyproject.toml configuration
- Start with `--exit-zero` for existing violations
- Consider ruff check + ruff format

**Reference**: VALIDATION_ROADMAP.md - Section 2.1
```

#### Issue #7: Configure baseline for existing violations
```yaml
Title: Configure baseline for existing linting violations
Labels: validation-infrastructure, linting, epic-2-linting, technical-debt
Milestone: Core Testing
Priority: Medium
Epic: Linting and Code Quality

Description:
Create a baseline of existing linting violations to focus on new code quality.

**Acceptance Criteria:**
- [ ] Current violations documented
- [ ] Baseline file created (if using baseline approach)
- [ ] New violations block PRs
- [ ] Plan for addressing existing violations

**Technical Details:**
- Run Ruff on entire codebase
- Document current violation count
- Consider per-file ignore rules temporarily
- Create issues for fixing existing violations

**Reference**: VALIDATION_ROADMAP.md - Section 2.1
```

#### Issue #8: Add ESLint for React Native
```yaml
Title: Add ESLint for React Native app
Labels: validation-infrastructure, linting, epic-2-linting, javascript
Milestone: Core Testing
Priority: Medium
Epic: Linting and Code Quality

Description:
Implement ESLint for the React Native app in `orion_disaster_app/`.

**Acceptance Criteria:**
- [ ] ESLint configured for Expo/React Native
- [ ] Runs in CI workflow
- [ ] Basic rules enforced
- [ ] Integration with existing workflow

**Technical Details:**
- Add ESLint to package.json dev dependencies
- Create .eslintrc.js with appropriate config
- Consider Prettier integration
- Add npm run lint script

**Reference**: VALIDATION_ROADMAP.md - Section 2.2
```

#### Issue #9: Integrate pre-commit hooks with CI
```yaml
Title: Integrate pre-commit hooks with CI
Labels: validation-infrastructure, linting, epic-2-linting
Milestone: Core Testing
Priority: Low
Epic: Linting and Code Quality

Description:
Ensure CI runs the same checks as pre-commit hooks for consistency.

**Acceptance Criteria:**
- [ ] Pre-commit config reviewed
- [ ] Relevant hooks run in CI
- [ ] Documentation updated
- [ ] Consider additional hooks

**Technical Details:**
- Run pre-commit in CI via `pre-commit run --all-files`
- Or replicate key checks in CI
- Consider adding Python-specific hooks
- Document expected pre-commit setup

**Reference**: VALIDATION_ROADMAP.md - Section 2.3
```

#### Issue #10: Create linting documentation
```yaml
Title: Create linting documentation for contributors
Labels: validation-infrastructure, linting, epic-2-linting, documentation
Milestone: Core Testing
Priority: Low
Epic: Linting and Code Quality

Description:
Document linting setup, rules, and how to fix common issues.

**Acceptance Criteria:**
- [ ] Linting rules explained
- [ ] Local linting setup documented
- [ ] Common fixes documented
- [ ] How to request rule changes

**Technical Details:**
- Add to CONTRIBUTING.md or separate LINTING.md
- Explain Ruff and ESLint usage
- Provide examples of common issues
- Link to official documentation

**Reference**: VALIDATION_ROADMAP.md - Section 2
```

---

### Epic 3: Unit Testing Framework

#### Issue #11: Configure pytest and project structure
```yaml
Title: Configure pytest and project test structure
Labels: validation-infrastructure, testing, epic-3-unit-testing
Milestone: Core Testing
Priority: High
Epic: Unit Testing Framework

Description:
Set up pytest as the testing framework with proper directory structure.

**Acceptance Criteria:**
- [ ] pytest added to Poetry dev dependencies
- [ ] Test directory structure created
- [ ] pytest.ini or pyproject.toml configured
- [ ] Sample test runs successfully
- [ ] CI runs pytest

**Technical Details:**
- Add pytest, pytest-cov to dev dependencies
- Create tests/unit/, tests/integration/, tests/fixtures/
- Configure in [tool.pytest.ini_options]
- Add pytest step to CI workflow
- Document test running: `poetry run pytest`

**Reference**: VALIDATION_ROADMAP.md - Section 3.1
```

#### Issue #12: Write unit tests for PID control module
```yaml
Title: Write unit tests for PID control module
Labels: validation-infrastructure, testing, epic-3-unit-testing
Milestone: Core Testing
Priority: High
Epic: Unit Testing Framework

Description:
Create comprehensive unit tests for `robot/common/pid_control.py`.

**Acceptance Criteria:**
- [ ] PController class fully tested
- [ ] PIController class fully tested
- [ ] Edge cases covered
- [ ] 100% coverage for this module
- [ ] Tests pass in CI

**Technical Details:**
- Create tests/unit/test_pid_control.py
- Test P control output calculation
- Test PI control with integral
- Test reset functionality
- Test edge cases (zero error, large values, etc.)

**Reference**: VALIDATION_ROADMAP.md - Section 3.1
```

#### Issue #13: Create hardware mocking framework
```yaml
Title: Create hardware mocking framework
Labels: validation-infrastructure, testing, epic-3-unit-testing, infrastructure
Milestone: Core Testing
Priority: High
Epic: Unit Testing Framework

Description:
Build a framework for mocking hardware dependencies (GPIO, I2C, etc.).

**Acceptance Criteria:**
- [ ] Mock GPIO interface
- [ ] Mock I2C/SPI interfaces
- [ ] Easy to use in tests
- [ ] Documentation provided
- [ ] Example usage in tests

**Technical Details:**
- Create tests/mocks/ directory
- Mock common hardware interfaces
- Use unittest.mock or create custom mocks
- Consider using pytest fixtures
- Document mocking patterns

**Reference**: VALIDATION_ROADMAP.md - Section 3.2
```

#### Issue #14: Add coverage reporting to CI
```yaml
Title: Add code coverage reporting to CI
Labels: validation-infrastructure, testing, epic-3-unit-testing, metrics
Milestone: Core Testing
Priority: Medium
Epic: Unit Testing Framework

Description:
Generate and report code coverage metrics in CI.

**Acceptance Criteria:**
- [ ] pytest-cov configured
- [ ] Coverage report generated in CI
- [ ] Coverage posted to PR comments
- [ ] Coverage trends tracked
- [ ] Minimum coverage threshold set (optional)

**Technical Details:**
- Use pytest-cov: `pytest --cov=robot --cov-report=xml`
- Consider using codecov.io or coveralls
- Or generate report in CI comment
- Set reasonable coverage target (start at 40%)

**Reference**: VALIDATION_ROADMAP.md - Section 3.3
```

#### Issue #15: Write unit tests for settings module
```yaml
Title: Write unit tests for settings module
Labels: validation-infrastructure, testing, epic-3-unit-testing
Milestone: Core Testing
Priority: Medium
Epic: Unit Testing Framework

Description:
Create unit tests for `robot/common/settings.py`.

**Acceptance Criteria:**
- [ ] Settings loading tested
- [ ] Environment variable handling tested
- [ ] Default values tested
- [ ] Validation logic tested (if any)
- [ ] Tests pass in CI

**Technical Details:**
- Create tests/unit/test_settings.py
- Mock environment variables
- Test RobotSettings class
- Verify pydantic-settings integration
- Test edge cases

**Reference**: VALIDATION_ROADMAP.md - Section 3.2
```

#### Issue #16: Write unit tests for service base
```yaml
Title: Write unit tests for service base class
Labels: validation-infrastructure, testing, epic-3-unit-testing
Milestone: Core Testing
Priority: Medium
Epic: Unit Testing Framework

Description:
Create unit tests for `robot/common/service_base.py`.

**Acceptance Criteria:**
- [ ] ServiceBase class tested
- [ ] MQTT connection logic tested (mocked)
- [ ] Message handling tested
- [ ] JSON publishing tested
- [ ] Tests pass in CI

**Technical Details:**
- Create tests/unit/test_service_base.py
- Mock paho.mqtt.client
- Test connect() function
- Test on_connect, on_message callbacks
- Test publish_json method

**Reference**: VALIDATION_ROADMAP.md - Section 3.2
```

#### Issue #17: Set minimum coverage requirements
```yaml
Title: Set minimum code coverage requirements
Labels: validation-infrastructure, testing, epic-3-unit-testing, policy
Milestone: Core Testing
Priority: Low
Epic: Unit Testing Framework

Description:
Define and enforce minimum code coverage thresholds.

**Acceptance Criteria:**
- [ ] Coverage targets defined (e.g., 50% overall)
- [ ] Critical modules identified (e.g., 90% for PID)
- [ ] Enforcement mechanism in place
- [ ] Team agreement on targets
- [ ] Documentation updated

**Technical Details:**
- Configure pytest-cov with --cov-fail-under
- Start with achievable targets
- Plan for gradual increase
- Consider per-module targets
- Balance coverage vs quality

**Reference**: VALIDATION_ROADMAP.md - Section 3.3
```

#### Issue #18: Document testing practices
```yaml
Title: Create testing documentation for contributors
Labels: validation-infrastructure, testing, epic-3-unit-testing, documentation
Milestone: Core Testing
Priority: Medium
Epic: Unit Testing Framework

Description:
Document how to write and run tests, testing conventions, and best practices.

**Acceptance Criteria:**
- [ ] Testing guide created
- [ ] How to run tests locally
- [ ] How to write good tests
- [ ] Mocking patterns documented
- [ ] Examples provided

**Technical Details:**
- Create TESTING.md or add to CONTRIBUTING.md
- Cover: pytest usage, fixtures, mocking
- Explain test organization
- Provide test examples
- Link to pytest documentation

**Reference**: VALIDATION_ROADMAP.md - Section 3
```

---

### Epic 4: Integration Testing

#### Issue #19: Set up test MQTT broker
```yaml
Title: Set up test MQTT broker in CI
Labels: validation-infrastructure, testing, epic-4-integration, infrastructure
Milestone: Core Testing
Priority: High
Epic: Integration Testing

Description:
Configure a test MQTT broker (Mosquitto) in CI for integration tests.

**Acceptance Criteria:**
- [ ] Mosquitto runs in CI environment
- [ ] Services can connect to test broker
- [ ] Isolated from production
- [ ] Easy to reset between tests
- [ ] Documentation provided

**Technical Details:**
- Use Docker container for Mosquitto in CI
- Or install via apt-get in CI
- Configure test credentials
- Document broker configuration
- Provide connection utilities

**Reference**: VALIDATION_ROADMAP.md - Section 4.1
```

#### Issue #20: Write service integration tests
```yaml
Title: Write service integration tests
Labels: validation-infrastructure, testing, epic-4-integration
Milestone: Core Testing
Priority: High
Epic: Integration Testing

Description:
Create integration tests for service-to-service communication via MQTT.

**Acceptance Criteria:**
- [ ] 10+ integration tests
- [ ] Test MQTT message passing
- [ ] Test service interactions
- [ ] Test state management
- [ ] Tests pass in CI with test broker

**Technical Details:**
- Create tests/integration/test_services.py
- Test motor commands
- Test sensor data publishing
- Test emergency stop
- Use fixtures for service setup

**Reference**: VALIDATION_ROADMAP.md - Section 4.1
```

#### Issue #21: Mock board driver interfaces
```yaml
Title: Create mocks for board driver interfaces
Labels: validation-infrastructure, testing, epic-4-integration, infrastructure
Milestone: Core Testing
Priority: Medium
Epic: Integration Testing

Description:
Build comprehensive mocks for board hardware interfaces.

**Acceptance Criteria:**
- [ ] GPIO mocks
- [ ] I2C/SPI mocks
- [ ] Board-specific mocks
- [ ] Usable in integration tests
- [ ] Documentation provided

**Technical Details:**
- Extend hardware mocking framework
- Mock gpiozero components
- Mock board-specific libraries
- Create test fixtures
- Document usage patterns

**Reference**: VALIDATION_ROADMAP.md - Section 4.2
```

#### Issue #22: Write board integration tests
```yaml
Title: Write board driver integration tests
Labels: validation-infrastructure, testing, epic-4-integration
Milestone: Core Testing
Priority: Medium
Epic: Integration Testing

Description:
Create integration tests for board drivers with mocked hardware.

**Acceptance Criteria:**
- [ ] 15+ board integration tests
- [ ] All board types covered
- [ ] Motor control tested
- [ ] Sensor reading tested
- [ ] Tests pass in CI

**Technical Details:**
- Create tests/integration/test_boards.py
- Test each board in robot/boards/
- Use hardware mocks
- Test Robot interface compatibility
- Verify gpiozero Robot interface

**Reference**: VALIDATION_ROADMAP.md - Section 4.2
```

#### Issue #23: Create end-to-end test scenarios
```yaml
Title: Create end-to-end service test scenarios
Labels: validation-infrastructure, testing, epic-4-integration
Milestone: Advanced Validation
Priority: Medium
Epic: Integration Testing

Description:
Build comprehensive end-to-end tests for complete control flows.

**Acceptance Criteria:**
- [ ] Full service stack tested
- [ ] App → MQTT → Services → Hardware flow
- [ ] Multiple scenarios covered
- [ ] Error handling tested
- [ ] Tests run in CI

**Technical Details:**
- Create tests/integration/test_e2e.py
- Test complete command sequences
- Test joystick → motors
- Test line following → motors
- Test emergency scenarios

**Reference**: VALIDATION_ROADMAP.md - Section 4.3
```

#### Issue #24: Document integration testing approach
```yaml
Title: Document integration testing approach
Labels: validation-infrastructure, testing, epic-4-integration, documentation
Milestone: Core Testing
Priority: Low
Epic: Integration Testing

Description:
Create documentation for integration testing strategies and patterns.

**Acceptance Criteria:**
- [ ] Integration test guide created
- [ ] MQTT testing explained
- [ ] Hardware mocking documented
- [ ] Examples provided
- [ ] Best practices shared

**Technical Details:**
- Add to TESTING.md
- Explain integration vs unit tests
- Document test broker setup
- Provide example integration test
- Explain when to use integration tests

**Reference**: VALIDATION_ROADMAP.md - Section 4
```

---

### Epic 5: Dry Run Capability

#### Issue #25: Design dry-run architecture
```yaml
Title: Design and document dry-run architecture
Labels: validation-infrastructure, dry-run, epic-5-dry-run, design
Milestone: Advanced Validation
Priority: High
Epic: Dry Run Capability

Description:
Design the architecture for dry-run mode throughout the robot code.

**Acceptance Criteria:**
- [ ] Architecture documented
- [ ] Dry-run flag approach defined
- [ ] Logging strategy established
- [ ] Implementation plan created
- [ ] Team review completed

**Technical Details:**
- Design dry-run flag propagation
- Define logging format
- Plan integration points
- Consider environment variable vs parameter
- Document in design doc

**Reference**: VALIDATION_ROADMAP.md - Section 5.1
```

#### Issue #26: Implement dry-run flag in base classes
```yaml
Title: Implement dry-run flag in base classes
Labels: validation-infrastructure, dry-run, epic-5-dry-run
Milestone: Advanced Validation
Priority: High
Epic: Dry Run Capability

Description:
Add dry-run support to core base classes and utilities.

**Acceptance Criteria:**
- [ ] ServiceBase supports dry-run
- [ ] Settings support dry-run flag
- [ ] Logging framework enhanced
- [ ] Example usage provided
- [ ] Tests updated

**Technical Details:**
- Add dry_run parameter to ServiceBase
- Create dry-run logging utilities
- Update robot/common/ classes
- Ensure backward compatibility
- Document usage

**Reference**: VALIDATION_ROADMAP.md - Section 5.1
```

#### Issue #27: Add dry-run support to motor services
```yaml
Title: Add dry-run support to motor services
Labels: validation-infrastructure, dry-run, epic-5-dry-run
Milestone: Advanced Validation
Priority: High
Epic: Dry Run Capability

Description:
Implement dry-run mode in motor control services.

**Acceptance Criteria:**
- [ ] Motor commands logged in dry-run
- [ ] No actual hardware changes
- [ ] Command sequences validated
- [ ] Tests verify dry-run behavior
- [ ] Documentation updated

**Technical Details:**
- Update motor service classes
- Log instead of executing commands
- Maintain state tracking
- Validate command parameters
- Add dry-run tests

**Reference**: VALIDATION_ROADMAP.md - Section 5.1
```

#### Issue #28: Add dry-run support to sensor services
```yaml
Title: Add dry-run support to sensor services
Labels: validation-infrastructure, dry-run, epic-5-dry-run
Milestone: Advanced Validation
Priority: Medium
Epic: Dry Run Capability

Description:
Implement dry-run mode in sensor reading services.

**Acceptance Criteria:**
- [ ] Sensor reads logged in dry-run
- [ ] Mock sensor values returned
- [ ] Sensor services testable
- [ ] Tests verify behavior
- [ ] Documentation updated

**Technical Details:**
- Update sensor service classes
- Provide mock sensor data
- Log sensor read attempts
- Consider pre-configured scenarios
- Add dry-run tests

**Reference**: VALIDATION_ROADMAP.md - Section 5.1
```

#### Issue #29: Create dry-run test scenarios
```yaml
Title: Create dry-run test scenarios
Labels: validation-infrastructure, dry-run, epic-5-dry-run, testing
Milestone: Advanced Validation
Priority: High
Epic: Dry Run Capability

Description:
Build test scenarios that exercise robot code in dry-run mode.

**Acceptance Criteria:**
- [ ] 5-10 test scenarios created
- [ ] Cover key robot behaviors
- [ ] Validate command sequences
- [ ] Check for errors
- [ ] Tests run in CI

**Technical Details:**
- Create tests/dry_run/ directory
- Test navigation sequences
- Test line following
- Test emergency stops
- Validate log output

**Reference**: VALIDATION_ROADMAP.md - Section 5.2
```

#### Issue #30: Integrate dry-run tests in CI
```yaml
Title: Integrate dry-run tests in CI pipeline
Labels: validation-infrastructure, dry-run, epic-5-dry-run, ci-cd
Milestone: Advanced Validation
Priority: Medium
Epic: Dry Run Capability

Description:
Add dry-run tests to CI workflow.

**Acceptance Criteria:**
- [ ] Dry-run tests run automatically
- [ ] Triggered on control logic changes
- [ ] Results clearly reported
- [ ] Failures block merge
- [ ] Completes in < 10 minutes

**Technical Details:**
- Add dry-run test step to CI
- Configure triggers
- Parse and report results
- Set up gating rules
- Optimize execution time

**Reference**: VALIDATION_ROADMAP.md - Section 5.2
```

#### Issue #31: Create dry-run reporting
```yaml
Title: Create dry-run test result reporting
Labels: validation-infrastructure, dry-run, epic-5-dry-run, reporting
Milestone: Advanced Validation
Priority: Low
Epic: Dry Run Capability

Description:
Generate and display dry-run test results in PRs.

**Acceptance Criteria:**
- [ ] Summary report generated
- [ ] Command sequences shown
- [ ] Issues highlighted
- [ ] Posted to PR comments
- [ ] Easy to interpret

**Technical Details:**
- Parse dry-run logs
- Generate summary report
- Create GitHub Actions comment
- Include statistics
- Highlight anomalies

**Reference**: VALIDATION_ROADMAP.md - Section 5.3
```

#### Issue #32: Document dry-run usage
```yaml
Title: Document dry-run mode usage
Labels: validation-infrastructure, dry-run, epic-5-dry-run, documentation
Milestone: Advanced Validation
Priority: Medium
Epic: Dry Run Capability

Description:
Create comprehensive documentation for dry-run mode.

**Acceptance Criteria:**
- [ ] Dry-run guide created
- [ ] How to enable dry-run
- [ ] Example scenarios
- [ ] Limitations documented
- [ ] Troubleshooting included

**Technical Details:**
- Create DRY_RUN.md or add to TESTING.md
- Explain dry-run concept
- Show usage examples
- Document environment variables
- Explain when to use dry-run

**Reference**: VALIDATION_ROADMAP.md - Section 5
```

---

### Epic 6: Simulation

#### Issue #33: Research and select simulation approach
```yaml
Title: Research simulation options and select approach
Labels: validation-infrastructure, simulation, epic-6-simulation, research
Milestone: Advanced Validation
Priority: High
Epic: Simulation

Description:
Evaluate simulation options and select the best approach for this project.

**Acceptance Criteria:**
- [ ] 3+ options evaluated
- [ ] Pros/cons documented
- [ ] Recommendation made
- [ ] Team consensus reached
- [ ] POC plan created

**Technical Details:**
- Evaluate: Custom 2D, PyBullet, Gazebo, Webots
- Consider: complexity, features, performance
- Test POC of top choice
- Document findings
- Present to team

**Reference**: VALIDATION_ROADMAP.md - Section 6.1
```

#### Issue #34: Design simulation architecture
```yaml
Title: Design simulation architecture
Labels: validation-infrastructure, simulation, epic-6-simulation, design
Milestone: Advanced Validation
Priority: High
Epic: Simulation

Description:
Create detailed design for simulation system.

**Acceptance Criteria:**
- [ ] Architecture documented
- [ ] Component interfaces defined
- [ ] Integration plan created
- [ ] Technical challenges identified
- [ ] Team review completed

**Technical Details:**
- Define simulator components
- Plan MQTT integration
- Design sensor simulation
- Plan environment representation
- Document in design doc

**Reference**: VALIDATION_ROADMAP.md - Section 6.1
```

#### Issue #35: Implement basic 2D robot simulator
```yaml
Title: Implement basic 2D robot simulator
Labels: validation-infrastructure, simulation, epic-6-simulation
Milestone: Refinement
Priority: High
Epic: Simulation

Description:
Build MVP of 2D robot simulator with basic physics.

**Acceptance Criteria:**
- [ ] Robot movement simulation
- [ ] Basic 2D physics
- [ ] Position and rotation tracking
- [ ] Command interface
- [ ] Basic visualization (optional for CI)

**Technical Details:**
- Create simulation/ directory
- Implement robot.py with movement
- Implement physics.py with calculations
- Basic collision detection
- Document API

**Reference**: VALIDATION_ROADMAP.md - Section 6.2
```

#### Issue #36: Create simulated environment/arena
```yaml
Title: Create simulated arena environment
Labels: validation-infrastructure, simulation, epic-6-simulation
Milestone: Refinement
Priority: Medium
Epic: Simulation

Description:
Build arena and obstacle representation for simulator.

**Acceptance Criteria:**
- [ ] Arena boundaries defined
- [ ] Obstacles supported
- [ ] Line course representation
- [ ] Configurable layouts
- [ ] Visualization available

**Technical Details:**
- Create environment.py
- Define arena dimensions
- Support obstacle placement
- Implement line track
- Use configuration files

**Reference**: VALIDATION_ROADMAP.md - Section 6.2
```

#### Issue #37: Implement simulated sensors
```yaml
Title: Implement simulated sensors
Labels: validation-infrastructure, simulation, epic-6-simulation
Milestone: Refinement
Priority: High
Epic: Simulation

Description:
Create simulated sensor implementations for testing.

**Acceptance Criteria:**
- [ ] Distance sensors
- [ ] Line sensors
- [ ] Sensors return realistic values
- [ ] Noise simulation (optional)
- [ ] Configurable parameters

**Technical Details:**
- Create sensors.py
- Implement distance sensor (ultrasonic/IR)
- Implement line follower sensor
- Calculate based on robot position
- Add realistic noise

**Reference**: VALIDATION_ROADMAP.md - Section 6.2
```

#### Issue #38: Integrate simulator with MQTT
```yaml
Title: Integrate simulator with MQTT services
Labels: validation-infrastructure, simulation, epic-6-simulation, integration
Milestone: Refinement
Priority: High
Epic: Simulation

Description:
Connect simulator to robot services via MQTT.

**Acceptance Criteria:**
- [ ] Simulator publishes sensor data
- [ ] Simulator receives motor commands
- [ ] Simulation loop runs smoothly
- [ ] Compatible with existing services
- [ ] Documentation provided

**Technical Details:**
- Integrate paho-mqtt in simulator
- Publish to sensor topics
- Subscribe to motor topics
- Implement simulation time step
- Handle MQTT reconnection

**Reference**: VALIDATION_ROADMAP.md - Section 6.2
```

#### Issue #39: Create headless simulation mode
```yaml
Title: Create headless simulation mode for CI
Labels: validation-infrastructure, simulation, epic-6-simulation, ci-cd
Milestone: Refinement
Priority: High
Epic: Simulation

Description:
Enable simulator to run without GUI for CI environments.

**Acceptance Criteria:**
- [ ] Simulator runs without display
- [ ] All functionality available headless
- [ ] Results exported to files
- [ ] Fast execution
- [ ] CI compatible

**Technical Details:**
- Add --headless flag
- Disable visualization in headless mode
- Export results to JSON/CSV
- Optimize for speed
- Test in CI environment

**Reference**: VALIDATION_ROADMAP.md - Section 6.3
```

#### Issue #40: Write simulation test scenarios
```yaml
Title: Write simulation test scenarios
Labels: validation-infrastructure, simulation, epic-6-simulation, testing
Milestone: Refinement
Priority: High
Epic: Simulation

Description:
Create test scenarios that run robot code in simulation.

**Acceptance Criteria:**
- [ ] 5-10 test scenarios
- [ ] Cover key robot behaviors
- [ ] Validate against expected outcomes
- [ ] Automated pass/fail
- [ ] Documentation provided

**Technical Details:**
- Create tests/simulation/ directory
- Test straight line movement
- Test line following
- Test obstacle avoidance
- Test complete course runs

**Reference**: VALIDATION_ROADMAP.md - Section 6.3
```

#### Issue #41: Add simulation to CI (optional)
```yaml
Title: Add simulation tests to CI pipeline
Labels: validation-infrastructure, simulation, epic-6-simulation, ci-cd, optional
Milestone: Refinement
Priority: Low
Epic: Simulation

Description:
Integrate simulation tests into CI workflow (if stable enough).

**Acceptance Criteria:**
- [ ] Simulation tests run in CI
- [ ] Headless mode works reliably
- [ ] Results clearly reported
- [ ] Reasonable execution time
- [ ] Not blocking initially

**Technical Details:**
- Add simulation test step
- Run in headless mode
- Parse results
- Post to PR comments
- Set as informational initially

**Reference**: VALIDATION_ROADMAP.md - Section 6.3
```

#### Issue #42: Create simulation documentation
```yaml
Title: Create simulation documentation
Labels: validation-infrastructure, simulation, epic-6-simulation, documentation
Milestone: Refinement
Priority: Medium
Epic: Simulation

Description:
Document simulation system, usage, and limitations.

**Acceptance Criteria:**
- [ ] Simulation guide created
- [ ] How to run simulator
- [ ] How to create scenarios
- [ ] Limitations documented
- [ ] Examples provided

**Technical Details:**
- Create SIMULATION.md
- Explain architecture
- Show usage examples
- Document API
- List known limitations

**Reference**: VALIDATION_ROADMAP.md - Section 6.4
```

#### Issue #43: Enhance physics simulation
```yaml
Title: Enhance physics simulation realism
Labels: validation-infrastructure, simulation, epic-6-simulation, enhancement, future
Milestone: Refinement
Priority: Low
Epic: Simulation

Description:
Improve physics simulation for more realistic behavior (future enhancement).

**Acceptance Criteria:**
- [ ] More realistic acceleration
- [ ] Friction modeling
- [ ] Momentum simulation
- [ ] Better collision response
- [ ] Validated against hardware

**Technical Details:**
- Improve physics calculations
- Add friction coefficients
- Model motor characteristics
- Test against real robot
- Document improvements

**Reference**: VALIDATION_ROADMAP.md - Section 6.4
```

#### Issue #44: Add visualization tools
```yaml
Title: Add simulation visualization tools
Labels: validation-infrastructure, simulation, epic-6-simulation, enhancement, future
Milestone: Refinement
Priority: Low
Epic: Simulation

Description:
Create visualization tools for simulation development and debugging.

**Acceptance Criteria:**
- [ ] Real-time visualization
- [ ] Sensor data display
- [ ] Path tracking
- [ ] Performance metrics
- [ ] Recording capability

**Technical Details:**
- Use pygame or matplotlib
- Show robot position/orientation
- Display sensor readings
- Plot paths
- Optional: export video

**Reference**: VALIDATION_ROADMAP.md - Section 6.4
```

---

### Epic 7: Documentation and Training

#### Issue #45: Create testing guide for contributors
```yaml
Title: Create comprehensive testing guide
Labels: validation-infrastructure, documentation, epic-7-documentation
Milestone: Refinement
Priority: High
Epic: Documentation and Training

Description:
Create complete guide for contributors on testing practices.

**Acceptance Criteria:**
- [ ] Testing philosophy explained
- [ ] All test types documented
- [ ] How to write tests
- [ ] How to run tests locally
- [ ] Best practices shared

**Technical Details**:
- Create TESTING.md
- Cover unit, integration, dry-run, simulation
- Include examples
- Link to pytest docs
- Keep updated

**Reference**: VALIDATION_ROADMAP.md - Section 7
```

#### Issue #46: Document CI/CD pipeline
```yaml
Title: Document CI/CD pipeline
Labels: validation-infrastructure, documentation, epic-7-documentation, ci-cd
Milestone: Refinement
Priority: Medium
Epic: Documentation and Training

Description:
Create comprehensive CI/CD pipeline documentation.

**Acceptance Criteria:**
- [ ] Pipeline stages explained
- [ ] Workflow files documented
- [ ] Triggers documented
- [ ] How to debug failures
- [ ] How to modify pipeline

**Technical Details**:
- Create CI_CD.md or add to CONTRIBUTING.md
- Explain each workflow
- Document environment variables
- Explain status checks
- Link to GitHub Actions docs

**Reference**: VALIDATION_ROADMAP.md - Section 7
```

#### Issue #47: Create troubleshooting guide
```yaml
Title: Create validation troubleshooting guide
Labels: validation-infrastructure, documentation, epic-7-documentation
Milestone: Refinement
Priority: Medium
Epic: Documentation and Training

Description:
Document common issues and how to resolve them.

**Acceptance Criteria:**
- [ ] Common errors documented
- [ ] Solutions provided
- [ ] FAQ section
- [ ] Contact points identified
- [ ] Kept up to date

**Technical Details**:
- Create TROUBLESHOOTING.md
- Document common CI failures
- Explain test failures
- Linting issues
- How to get help

**Reference**: VALIDATION_ROADMAP.md - Section 7
```

#### Issue #48: Document mocking strategies
```yaml
Title: Document hardware mocking strategies
Labels: validation-infrastructure, documentation, epic-7-documentation, testing
Milestone: Refinement
Priority: Medium
Epic: Documentation and Training

Description:
Create guide for mocking hardware in tests.

**Acceptance Criteria:**
- [ ] Mocking philosophy explained
- [ ] Available mocks documented
- [ ] How to create new mocks
- [ ] Examples provided
- [ ] Best practices shared

**Technical Details**:
- Add to TESTING.md
- Explain mock framework
- Show examples
- Document fixtures
- Link to unittest.mock docs

**Reference**: VALIDATION_ROADMAP.md - Section 7
```

#### Issue #49: Create video tutorials (optional)
```yaml
Title: Create video tutorials for validation tools
Labels: validation-infrastructure, documentation, epic-7-documentation, optional, future
Milestone: Refinement
Priority: Low
Epic: Documentation and Training

Description:
Create video walkthroughs of testing and validation (future enhancement).

**Acceptance Criteria:**
- [ ] 3-5 short videos
- [ ] Cover key topics
- [ ] High quality
- [ ] Hosted publicly
- [ ] Linked from docs

**Technical Details**:
- Running tests locally
- Writing tests
- Debugging CI failures
- Using simulation
- Share on YouTube

**Reference**: VALIDATION_ROADMAP.md - Section 7
```

---

## Project Milestones

### Milestone 1: Foundation (Weeks 1-4)
**Goal**: Basic CI infrastructure in place

**Issues**: #1-5, #6, #11

**Success Criteria**:
- ✓ CI runs on all PRs
- ✓ Build checks working
- ✓ Basic linting enabled
- ✓ Pytest configured

---

### Milestone 2: Core Testing (Weeks 5-10)
**Goal**: Comprehensive test coverage

**Issues**: #7-10, #12-18, #19-20

**Success Criteria**:
- ✓ 50+ tests
- ✓ 40%+ coverage
- ✓ Integration tests running
- ✓ Mocking framework ready

---

### Milestone 3: Advanced Validation (Weeks 11-16)
**Goal**: Dry-run and simulation MVP

**Issues**: #21-24, #25-32, #33-34

**Success Criteria**:
- ✓ Dry-run implemented
- ✓ Simulation architecture designed
- ✓ Advanced integration tests
- ✓ Validation mature

---

### Milestone 4: Refinement (Weeks 17-24+)
**Goal**: Polish and expand

**Issues**: #35-44, #45-49

**Success Criteria**:
- ✓ Simulation working
- ✓ 70%+ coverage
- ✓ Documentation complete
- ✓ Team proficient

---

## Priority Levels

### P0 - Critical (Must Have)
- Build checks
- Basic linting
- Unit test framework
- Core unit tests (PID, settings)

### P1 - High (Should Have)
- Integration tests
- Coverage reporting
- Hardware mocks
- Dry-run MVP
- Documentation

### P2 - Medium (Nice to Have)
- Advanced linting
- Simulation design
- Simulation implementation
- Enhanced reporting

### P3 - Low (Future)
- Simulation enhancements
- Video tutorials
- Advanced visualization
- Performance optimization

---

## Labels to Create

Create these labels in GitHub for organization:

- `validation-infrastructure` - All validation-related work
- `ci-cd` - CI/CD pipeline work
- `testing` - Test-related work
- `linting` - Linting and code quality
- `simulation` - Simulation-related work
- `dry-run` - Dry-run capability
- `documentation` - Documentation work
- `epic-1-foundation` - Foundation epic
- `epic-2-linting` - Linting epic
- `epic-3-unit-testing` - Unit testing epic
- `epic-4-integration` - Integration testing epic
- `epic-5-dry-run` - Dry-run epic
- `epic-6-simulation` - Simulation epic
- `epic-7-documentation` - Documentation epic
- `infrastructure` - Infrastructure work
- `enhancement` - Enhancements
- `research` - Research work
- `design` - Design work
- `optional` - Optional work
- `future` - Future enhancements
- `javascript` - JavaScript/React Native work
- `metrics` - Metrics and reporting
- `policy` - Policy decisions
- `reporting` - Reporting features
- `integration` - Integration work
- `technical-debt` - Technical debt

---

## Getting Started

1. **Create the GitHub Project**: 
   - Go to Projects → New Project
   - Choose "Board" template
   - Name: "Offline Validation Infrastructure"

2. **Create Milestones**:
   - Settings → Milestones → New
   - Create all 4 milestones listed above

3. **Create Labels**:
   - Settings → Labels
   - Create labels from list above

4. **Create Issues**:
   - Copy issue templates above
   - Create issues for Phase 1 (Foundation)
   - Add to project board
   - Assign to team members

5. **Configure Branch Protection**:
   - Settings → Branches
   - Add rule for main branch
   - Require status checks (after CI set up)

6. **Start Implementation**:
   - Begin with Issue #1
   - Work through Foundation milestone
   - Review and adjust as needed

---

## Notes

- **Adjust estimates**: Time estimates are guidelines, adjust based on team capacity
- **Dependencies**: Some issues depend on others, shown in issue descriptions
- **Flexibility**: This is a roadmap, not a rigid plan - adapt as needed
- **Communication**: Discuss in team meetings, adjust priorities
- **Celebrate**: Acknowledge progress, it's a significant undertaking!

---

**Last Updated**: November 19, 2024
**Document Version**: 1.0
**Related**: VALIDATION_ROADMAP.md
