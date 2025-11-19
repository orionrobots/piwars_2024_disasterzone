# Validation Roadmap for PiWars 2024 Disaster Zone

## Executive Summary

This document outlines a comprehensive strategy for implementing offline validation in the PiWars 2024 Disaster Zone repository. Currently, all validation requires deploying to the physical robot, which is time-consuming and inefficient. This roadmap provides a phased approach to introduce various validation strategies, from basic CI checks to simulation capabilities.

## Current State Assessment

### Existing Infrastructure
- **Build System**: Poetry for Python, npm for React Native app
- **Pre-commit Hooks**: Basic checks (trailing whitespace, EOF, YAML validation, large files)
- **Testing**: Minimal - a few manual test scripts exist but no automated test framework
- **Linting**: Ruff configured in `pyproject.toml` but not enforced in CI
- **CI/CD**: None - no GitHub Actions workflows

### Repository Structure
- **Python Code**: Robot services, board drivers, common utilities
- **React Native App**: `orion_disaster_app/` - mobile control interface
- **Deployment**: PyInfra-based deployment to Raspberry Pi
- **Hardware Dependencies**: Multiple board configurations (Adafruit, Pimoroni, DFRobot)

## Validation Strategy Overview

### Validation Pyramid

```
                    [Simulation]
                   /            \
            [Integration Tests]  [Dry Running]
           /                                  \
     [Unit Tests]                        [System Tests]
    /                                                  \
[Linting & Code Quality]          [Build & Compile Checks]
```

## 1. Simple CI - Build and Compile Checks

### Objective
Ensure code compiles/builds successfully before merging.

### Implementation Strategy

#### Phase 1.1: Python Build Validation (MVP)
**Estimated Effort**: 2-4 hours

- Create GitHub Actions workflow for Python
- Install dependencies via Poetry
- Verify all Python files compile (`python -m py_compile`)
- Check Poetry lock file is in sync

**Triggers**: Every push, every PR
**Gating**: Yes - block PR merge on failure

**Deliverable**: `.github/workflows/python-build.yml`

#### Phase 1.2: React Native Build Validation
**Estimated Effort**: 4-6 hours

- Create workflow for `orion_disaster_app/`
- Run `npm ci` to install dependencies
- Run `npm run` build/validation (if applicable)
- Check for TypeScript/JavaScript compilation errors

**Triggers**: Every push to `orion_disaster_app/`, every PR touching that directory
**Gating**: Yes - block PR merge on failure

**Deliverable**: `.github/workflows/react-native-build.yml` or extend Python workflow

#### Phase 1.3: Multi-Platform Build Matrix
**Estimated Effort**: 2-3 hours

- Test builds on multiple Python versions (3.9, 3.11, 3.12)
- Ensure compatibility across versions

**Triggers**: Every push, every PR
**Gating**: Yes for main Python version, no for additional versions (informational)

**Success Metrics**:
- Zero compilation/build failures on main branch
- Build time < 5 minutes
- 100% of PRs validated before merge

## 2. Linting - Code Quality and Style

### Objective
Enforce code quality standards and catch common errors before runtime.

### Implementation Strategy

#### Phase 2.1: Python Linting (MVP)
**Estimated Effort**: 3-5 hours

**Tools to Enable**:
- **Ruff**: Already configured, need to enforce in CI
  - Line length: 120 (already set)
  - Enable additional rules incrementally
- **Black** (optional): Code formatting
- **isort**: Import sorting
- **mypy**: Type checking (optional, advanced)

**Workflow**:
1. Start with Ruff with minimal rules
2. Run on all Python files
3. Allow existing violations initially (use `--exit-zero` or baseline)
4. Gradually fix existing issues
5. Enable stricter checking for new code

**Triggers**: Every push, every PR
**Gating**: 
- Phase 1: No (informational only)
- Phase 2: Yes for new violations only
- Phase 3: Yes for all violations

**Deliverable**: Add linting step to `.github/workflows/python-build.yml`

#### Phase 2.2: JavaScript/React Native Linting
**Estimated Effort**: 3-4 hours

**Tools to Enable**:
- **ESLint**: JavaScript/JSX linting
- **Prettier**: Code formatting

**Triggers**: Changes to `orion_disaster_app/`
**Gating**: Yes for errors, no for warnings initially

**Deliverable**: Add linting to React Native workflow

#### Phase 2.3: Pre-commit Hook Integration with CI
**Estimated Effort**: 1-2 hours

- Ensure CI runs same checks as pre-commit hooks
- Add pre-commit to CI workflow
- Consider additional hooks:
  - Python syntax checking
  - JSON/YAML validation
  - Markdown linting

**Success Metrics**:
- Linting runs in < 2 minutes
- < 5% false positive rate
- Gradually decreasing violation count

## 3. Unit Testing

### Objective
Test individual components in isolation without hardware dependencies.

### Implementation Strategy

#### Phase 3.1: Test Framework Setup (MVP)
**Estimated Effort**: 4-6 hours

**Framework**: pytest (Python standard)

**Initial Setup**:
1. Add pytest to Poetry dev dependencies
2. Create `tests/unit/` directory structure
3. Set up pytest configuration in `pyproject.toml`
4. Create example test for `robot/common/pid_control.py` (good candidate - pure logic)

**Test Structure**:
```
tests/
├── unit/           # Unit tests (no hardware)
├── integration/    # Integration tests (may need mocks)
├── system/         # System tests (may need hardware/simulation)
└── fixtures/       # Shared test data and fixtures
```

**Deliverable**: 
- pytest configuration
- 3-5 initial unit tests
- GitHub Actions workflow step

#### Phase 3.2: Mock Hardware Dependencies
**Estimated Effort**: 8-12 hours

**Strategy**:
- Create mock classes for hardware interfaces
- Mock GPIO, I2C, SPI, etc.
- Use dependency injection where possible
- Create test fixtures for common scenarios

**Priority Areas for Unit Tests**:
1. **`robot/common/pid_control.py`**: Pure logic, no dependencies (HIGH PRIORITY)
2. **`robot/common/settings.py`**: Configuration management
3. **`robot/common/service_base.py`**: MQTT service base (mock MQTT)
4. Board driver logic (with mocked hardware)
5. Control algorithms and calculations

**Deliverable**: 
- Mock hardware module
- 20+ unit tests covering core logic

#### Phase 3.3: Coverage Reporting
**Estimated Effort**: 2-3 hours

- Add pytest-cov
- Generate coverage reports
- Set minimum coverage thresholds
- Post coverage reports to PRs

**Triggers**: Every push, every PR
**Gating**: No initially, gradually introduce minimum coverage requirements

**Success Metrics**:
- 50% code coverage initially
- 70%+ coverage within 6 months
- Critical paths (PID control, safety) at 90%+

## 4. Integration Testing

### Objective
Test interactions between components without requiring full hardware.

### Implementation Strategy

#### Phase 4.1: Service Integration Tests (MVP)
**Estimated Effort**: 6-10 hours

**Approach**:
- Test service communication via MQTT
- Use test MQTT broker (Mosquitto test instance)
- Verify message passing between services
- Test state management

**Test Scenarios**:
1. Motor service receives and processes commands
2. Line following service publishes correct data
3. Joystick service translates inputs correctly
4. Emergency stop propagates to all services

**Deliverable**: 
- Integration test suite
- Test MQTT broker setup in CI
- 10+ integration tests

#### Phase 4.2: Board Driver Integration
**Estimated Effort**: 8-12 hours

**Challenge**: Board drivers require hardware

**Solutions**:
1. **Mock Hardware Interfaces**: Create comprehensive mocks for GPIO, I2C, etc.
2. **Hardware Abstraction Layer**: Refactor to allow easier mocking
3. **Conditional Testing**: Skip hardware tests in CI, run locally

**Test Coverage**:
- Motor control logic
- Sensor reading and processing
- Communication protocols

**Triggers**: Every push, every PR
**Gating**: Yes (with mocked hardware)

**Deliverable**: 
- Mocked board interfaces
- 15+ board integration tests

#### Phase 4.3: End-to-End Service Tests
**Estimated Effort**: 10-15 hours

**Scope**:
- Full service stack running (without hardware)
- App → MQTT → Robot Services → Mocked Hardware
- Test complete control flows
- Verify error handling and edge cases

**Success Metrics**:
- All service interactions tested
- Integration tests run in < 5 minutes
- 80%+ coverage of integration points

## 5. Dry Running

### Objective
Execute robot code in a non-destructive mode for validation.

### Implementation Strategy

#### Phase 5.1: Dry Run Mode Implementation (MVP)
**Estimated Effort**: 8-12 hours

**Implementation**:
- Add `--dry-run` flag to services
- Services log actions instead of executing
- Validate command sequences
- Check for illegal states

**Application**:
- Test deployment scripts
- Validate motor command sequences
- Check control flow logic

**Example**:
```python
class Robot:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
    
    def forward(self, speed):
        if self.dry_run:
            logger.info(f"DRY RUN: Would move forward at speed {speed}")
        else:
            # Actual motor control
            pass
```

**Deliverable**:
- Dry run flag in core classes
- Logging framework
- Dry run test suite

#### Phase 5.2: Dry Run in CI
**Estimated Effort**: 4-6 hours

**Workflow**:
1. Run robot services in dry-run mode
2. Send test command sequences
3. Validate expected log output
4. Check for errors or warnings

**Test Scenarios**:
- Autonomous navigation sequences
- Line following algorithms
- Emergency stop procedures
- Complex maneuvers

**Triggers**: PRs affecting robot control logic
**Gating**: Yes

**Deliverable**: 
- Dry run GitHub Actions workflow
- Test scenario library
- Output validation scripts

#### Phase 5.3: Dry Run Reporting
**Estimated Effort**: 3-5 hours

- Generate dry run reports
- Show command sequences executed
- Highlight potential issues
- Post reports to PRs

**Success Metrics**:
- 95% of control logic testable via dry run
- Catch 70%+ of logic errors before hardware testing
- Dry run tests complete in < 10 minutes

## 6. Simulation

### Objective
Create a simulated environment for comprehensive robot testing without hardware.

### Implementation Strategy

#### Phase 6.1: Architecture Planning (MVP)
**Estimated Effort**: 8-12 hours (research and design)

**Simulation Scope**:
- **Robot Physics**: Movement, momentum, collision
- **Sensors**: Distance, line sensors, camera (simplified)
- **Environment**: Arena, obstacles, lines
- **Services**: Full service stack

**Technology Options**:

**Option A: Lightweight Custom Simulator** (RECOMMENDED)
- Python-based
- 2D physics (simplified)
- Visual representation (pygame/matplotlib)
- Fast execution
- Easy to extend

**Option B: Gazebo/Webots** 
- Full 3D physics simulation
- ROS integration possible
- Higher complexity
- Longer setup time

**Option C: PyBullet**
- 3D physics engine
- Python-native
- Good middle ground

**Recommendation**: Start with **Option A** for MVP, evaluate Option C for future.

**Deliverable**: 
- Simulation architecture document
- Technology selection
- Proof of concept

#### Phase 6.2: Basic Simulator Implementation
**Estimated Effort**: 20-40 hours

**MVP Features**:
- 2D robot representation
- Basic movement physics
- Simple obstacle detection
- Line following capability
- MQTT integration

**Components**:
```
simulation/
├── __init__.py
├── robot.py           # Simulated robot
├── environment.py     # Arena and obstacles
├── sensors.py         # Simulated sensors
├── physics.py         # Movement calculations
└── visualizer.py      # Display (optional for CI)
```

**Deliverable**:
- Basic simulator
- Sample arena configurations
- Integration with robot services

#### Phase 6.3: Simulator in CI
**Estimated Effort**: 6-10 hours

**Workflow**:
1. Start simulator in headless mode
2. Run robot code against simulator
3. Execute test scenarios (courses)
4. Validate robot behavior
5. Generate test reports

**Test Scenarios**:
- Straight line navigation
- Line following
- Obstacle avoidance
- Complete course runs

**Triggers**: 
- PRs affecting navigation/control
- Weekly scheduled runs
- Release testing

**Gating**: 
- No initially (informational)
- Yes after stability proven

**Deliverable**:
- Headless simulation mode
- Automated test scenarios
- CI workflow integration

#### Phase 6.4: Advanced Simulation Features
**Estimated Effort**: 30-60 hours (ongoing)

**Enhancements**:
- More realistic physics
- Sensor noise simulation
- Battery simulation
- Camera image simulation
- Multiple robot support
- Performance profiling

**Deliverable**: Enhanced simulator capabilities

**Success Metrics**:
- 80% of robot behaviors testable in simulation
- < 10% difference between simulation and hardware
- Complete course runs in simulation
- Simulation tests run in < 15 minutes

## Validation Triggers and PR Gating

### Trigger Matrix

| Change Type | Build | Lint | Unit | Integration | Dry Run | Simulation |
|-------------|-------|------|------|-------------|---------|------------|
| Python code | ✓ | ✓ | ✓ | ✓ | If control | If control |
| React Native | ✓ | ✓ | − | − | − | − |
| Config files | ✓ | ✓ | − | − | − | − |
| Documentation | − | ✓ | − | − | − | − |
| Tests | ✓ | ✓ | ✓ | ✓ | − | − |
| Deployment | ✓ | ✓ | − | − | ✓ | − |

### Gating Strategy

#### Phase 1: Initial Setup (Months 1-2)
- **Gate on**: Build failures only
- **Informational**: Linting, test results

#### Phase 2: Basic Enforcement (Months 2-4)
- **Gate on**: Build, critical linting errors, test failures
- **Informational**: Coverage, advanced linting

#### Phase 3: Full Enforcement (Months 4+)
- **Gate on**: All checks except simulation
- **Informational**: Simulation results
- **Required**: Minimum test coverage

### PR Comment Strategy

**Automated Comments Should Include**:
- Build status
- Linting summary (errors, warnings)
- Test results (passed, failed, skipped)
- Coverage change (+/- %)
- Dry run summary (if applicable)
- Simulation results (if applicable)

**Example PR Comment**:
```
🤖 Validation Results

✅ Build: Passed
⚠️  Linting: 2 warnings (0 errors)
✅ Tests: 45 passed, 0 failed
📊 Coverage: 68.5% (+2.3%)
✅ Dry Run: All sequences valid
ℹ️  Simulation: Not required for this change

Details: [View full report](#)
```

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
**Goal**: Basic CI infrastructure

1. Create GitHub Actions workflows
2. Implement build checks
3. Enable basic linting
4. Set up pytest framework
5. Write 5-10 initial unit tests

**Deliverables**:
- Working CI pipeline
- Build and lint checks passing
- Test framework ready

**Success Criteria**:
- All builds automated
- Developers can run tests locally
- CI runs in < 10 minutes

### Phase 2: Core Testing (Weeks 5-10)
**Goal**: Comprehensive test coverage

1. Expand unit test suite (50+ tests)
2. Create hardware mocks
3. Implement integration tests
4. Add coverage reporting
5. Begin dry-run implementation

**Deliverables**:
- 50+ unit tests
- 20+ integration tests
- Coverage reporting
- Dry-run flag in core classes

**Success Criteria**:
- 40%+ code coverage
- All services have basic tests
- Integration tests cover key paths

### Phase 3: Advanced Validation (Weeks 11-16)
**Goal**: Dry-run and simulation MVP

1. Complete dry-run implementation
2. Design simulation architecture
3. Build basic simulator
4. Integrate dry-run in CI
5. POC simulation tests

**Deliverables**:
- Full dry-run capability
- Basic 2D simulator
- Dry-run in CI
- Simulation POC

**Success Criteria**:
- Dry-run catches logic errors
- Simulator runs basic scenarios
- < 15 minute total CI time

### Phase 4: Refinement (Weeks 17-24+)
**Goal**: Mature validation pipeline

1. Expand test coverage (70%+)
2. Enhance simulator features
3. Add simulation to CI
4. Performance optimization
5. Documentation and training

**Deliverables**:
- 70%+ coverage
- Full simulation in CI
- Complete documentation
- Developer guides

**Success Criteria**:
- Simulation tests standard practice
- < 5% PRs require hardware testing
- Team confident in validation

## MVP Definition by Validation Type

### 1. Build Checks MVP
- ✅ Python files compile
- ✅ Poetry dependencies install
- ✅ npm packages install
- ✅ Runs in < 5 minutes

### 2. Linting MVP
- ✅ Ruff runs on Python code
- ✅ Basic rules enforced
- ✅ Existing violations tracked
- ✅ New violations blocked

### 3. Unit Testing MVP
- ✅ pytest configured
- ✅ 5-10 tests for core logic
- ✅ PID control fully tested
- ✅ Tests run in CI
- ✅ Local test running documented

### 4. Integration Testing MVP
- ✅ Test MQTT broker setup
- ✅ 5-10 service interaction tests
- ✅ Basic message passing verified
- ✅ Runs in < 5 minutes

### 5. Dry Run MVP
- ✅ Dry-run flag implemented
- ✅ Core services support dry-run
- ✅ 3-5 test scenarios
- ✅ Command sequences logged
- ✅ Output validation

### 6. Simulation MVP
- ✅ 2D robot movement
- ✅ Basic physics
- ✅ One sensor type (distance or line)
- ✅ Simple arena
- ✅ One complete test scenario
- ✅ Headless mode

## Resource Requirements

### Development Time
- **Phase 1**: 40-60 hours
- **Phase 2**: 80-120 hours
- **Phase 3**: 100-150 hours
- **Phase 4**: 100-200 hours (ongoing)

**Total Initial Investment**: 320-530 hours (8-13 weeks for one developer)

### Infrastructure
- GitHub Actions minutes (free tier likely sufficient)
- No additional hosting required
- Potentially: test hardware for integration tests

### Skills Required
- Python development (intermediate)
- Testing frameworks (pytest)
- CI/CD (GitHub Actions)
- MQTT protocol
- Simulation (advanced feature)

## Risks and Mitigations

### Risk 1: Hardware Dependencies
**Impact**: High
**Likelihood**: High

**Mitigation**:
- Comprehensive mocking strategy
- Hardware abstraction layer
- Dry-run mode for hardware interactions
- Focus on testable logic first

### Risk 2: Simulator Complexity
**Impact**: Medium
**Likelihood**: Medium

**Mitigation**:
- Start with simple 2D simulator
- Iterate based on needs
- Don't try to simulate everything
- Accept some differences from hardware

### Risk 3: Test Maintenance Burden
**Impact**: Medium
**Likelihood**: Medium

**Mitigation**:
- Keep tests simple and focused
- Good naming and documentation
- Regular test review and cleanup
- Balance coverage vs. maintenance

### Risk 4: CI Pipeline Too Slow
**Impact**: Medium
**Likelihood**: Low

**Mitigation**:
- Parallel test execution
- Optimize long-running tests
- Separate fast/slow tests
- Cache dependencies

### Risk 5: False Positives/Negatives
**Impact**: Medium
**Likelihood**: Medium

**Mitigation**:
- Tune linting rules
- Regular test review
- Easy override process (with justification)
- Monitor validation effectiveness

## Success Metrics

### Short Term (3 months)
- ✓ 100% PRs validated by CI
- ✓ < 10 minute CI pipeline
- ✓ 40%+ code coverage
- ✓ 50+ automated tests
- ✓ Zero build failures on main

### Medium Term (6 months)
- ✓ 60%+ code coverage
- ✓ 100+ automated tests
- ✓ Dry-run validation standard
- ✓ < 20% PRs require hardware testing
- ✓ Simulation MVP operational

### Long Term (12 months)
- ✓ 70%+ code coverage
- ✓ Full simulation testing
- ✓ < 5% PRs require hardware testing
- ✓ Team confidence in validation
- ✓ Faster development cycle
- ✓ Measurable reduction in bugs

## Recommended GitHub Issues/Project Structure

### Project: "Offline Validation Infrastructure"

**Milestones**:
1. Foundation (Weeks 1-4)
2. Core Testing (Weeks 5-10)
3. Advanced Validation (Weeks 11-16)
4. Refinement (Weeks 17-24)

**Labels**:
- `validation-infrastructure`
- `ci-cd`
- `testing`
- `linting`
- `simulation`
- `documentation`

### Epic 1: CI/CD Foundation
- [ ] #1: Set up GitHub Actions workflow for Python builds
- [ ] #2: Add React Native build validation
- [ ] #3: Configure multi-version Python testing
- [ ] #4: Create PR status check requirements
- [ ] #5: Document CI setup for contributors

### Epic 2: Linting and Code Quality
- [ ] #6: Enable Ruff linting in CI
- [ ] #7: Configure baseline for existing violations
- [ ] #8: Add ESLint for React Native
- [ ] #9: Integrate pre-commit hooks with CI
- [ ] #10: Create linting documentation

### Epic 3: Unit Testing Framework
- [ ] #11: Configure pytest and project structure
- [ ] #12: Write unit tests for PID control module
- [ ] #13: Create hardware mocking framework
- [ ] #14: Add coverage reporting to CI
- [ ] #15: Write unit tests for settings module
- [ ] #16: Write unit tests for service base
- [ ] #17: Set minimum coverage requirements
- [ ] #18: Document testing practices

### Epic 4: Integration Testing
- [ ] #19: Set up test MQTT broker
- [ ] #20: Write service integration tests
- [ ] #21: Mock board driver interfaces
- [ ] #22: Write board integration tests
- [ ] #23: Create end-to-end test scenarios
- [ ] #24: Document integration testing

### Epic 5: Dry Run Capability
- [ ] #25: Design dry-run architecture
- [ ] #26: Implement dry-run flag in base classes
- [ ] #27: Add dry-run support to motor services
- [ ] #28: Add dry-run support to sensor services
- [ ] #29: Create dry-run test scenarios
- [ ] #30: Integrate dry-run tests in CI
- [ ] #31: Create dry-run reporting
- [ ] #32: Document dry-run usage

### Epic 6: Simulation
- [ ] #33: Research and select simulation approach
- [ ] #34: Design simulation architecture
- [ ] #35: Implement basic 2D robot simulator
- [ ] #36: Create simulated environment/arena
- [ ] #37: Implement simulated sensors
- [ ] #38: Integrate simulator with MQTT
- [ ] #39: Create headless simulation mode
- [ ] #40: Write simulation test scenarios
- [ ] #41: Add simulation to CI (optional)
- [ ] #42: Create simulation documentation
- [ ] #43: Enhance physics simulation
- [ ] #44: Add visualization tools

### Epic 7: Documentation and Training
- [ ] #45: Create testing guide for contributors
- [ ] #46: Document CI/CD pipeline
- [ ] #47: Create troubleshooting guide
- [ ] #48: Document mocking strategies
- [ ] #49: Create video tutorials (optional)

## Conclusion

This roadmap provides a comprehensive, phased approach to implementing offline validation for the PiWars 2024 Disaster Zone robot. By following this plan, the team can significantly reduce the need for hardware testing, catch bugs earlier, and accelerate development.

**Key Recommendations**:
1. **Start with the Foundation**: Get basic CI and linting working first
2. **Iterate Quickly**: Implement MVPs and improve over time
3. **Focus on Value**: Prioritize tests that catch real issues
4. **Keep It Simple**: Avoid over-engineering, especially simulation
5. **Maintain Momentum**: Regular progress, even if incremental

**Next Steps**:
1. Review and approve this roadmap
2. Create GitHub project from recommended issues
3. Prioritize Phase 1 tasks
4. Assign initial implementation work
5. Begin implementation

This validation infrastructure will be a force multiplier for the team, enabling faster, more confident development with less reliance on physical hardware testing.
