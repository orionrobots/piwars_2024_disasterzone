# Validation Roadmap for PiWars 2024 Disaster Zone

A phased approach to implementing offline validation, reducing dependency on physical robot testing.

## Current State

- **Build System**: Poetry (Python), npm (React Native)
- **Pre-commit Hooks**: Basic checks configured
- **Testing**: Manual scripts only, no automated framework
- **CI/CD**: None

## Validation Strategies

### 1. Build & Compile Checks

**Python**:
- GitHub Actions workflow with Poetry
- Verify all Python files compile
- Test on multiple Python versions (3.9, 3.11, 3.12) to ensure compatibility across Pi and development environments

**React Native** (Android only):
- `npm ci` to install dependencies
- Build validation for Android target

**Triggers**: Every push, every PR  
**Gating**: Yes - block merge on failure

### 2. Linting

Use **MegaLinter** for comprehensive multi-language linting:
- Python (Ruff already configured)
- JavaScript/JSX (ESLint)
- Markdown, YAML, JSON validation
- Dockerfile linting
- Shell script checking

**Triggers**: Every push, every PR  
**Gating**: Gradual - informational initially, then enforced

### 3. Unit Testing

**Python** (pytest):
- Test pure logic modules: PID control, settings, service base
- Mock hardware dependencies (GPIO, I2C, SPI)
- Coverage reporting with pytest-cov

**React Native** (Jest):
- Test component logic
- Test utility functions
- Mock native modules

**Target**: < 2 minutes execution  
**Triggers**: Every push, every PR  
**Gating**: Yes

### 4. Integration Testing

- Test MQTT service communication with test broker
- Mock board driver interfaces
- End-to-end service stack tests (without hardware)

**Target**: < 5 minutes execution  
**Triggers**: Every push, every PR  
**Gating**: Yes (with mocked hardware)

### 5. Dry Running

- Add `--dry-run` flag to services
- Log actions instead of executing
- Validate command sequences without hardware

**Triggers**: PRs affecting robot control logic  
**Gating**: Yes

### 6. Simulation

- Lightweight 2D Python-based simulator
- Basic physics, sensors, arena representation
- Headless mode for CI
- MQTT integration with real services

**Triggers**: Major changes, releases  
**Gating**: Informational initially

## Trigger Matrix

| Change Type | Build | Lint | Unit | Integration | Dry Run | Simulation |
|-------------|-------|------|------|-------------|---------|------------|
| Python code | ✓ | ✓ | ✓ | ✓ | If control | If control |
| React Native | ✓ | ✓ | ✓ | - | - | - |
| Config files | ✓ | ✓ | - | - | - | - |
| Documentation | - | ✓ | - | - | - | - |
| Tests | ✓ | ✓ | ✓ | ✓ | - | - |
| Deployment | ✓ | ✓ | - | - | ✓ | - |

## Gating Strategy

**Phase 1**: Gate on build failures only; linting and tests informational  
**Phase 2**: Gate on build, critical lint errors, test failures  
**Phase 3**: Gate on all checks except simulation; require minimum coverage

## Implementation Order

### Phase 1: Foundation
1. GitHub Actions workflow for Python builds
2. MegaLinter integration
3. pytest setup with initial unit tests
4. React Native build validation (Android)

### Phase 2: Core Testing
1. Expand unit tests (Python and React Native)
2. Hardware mocking framework
3. Integration tests with MQTT
4. Coverage reporting

### Phase 3: Advanced
1. Dry-run implementation
2. Simulation architecture design
3. Basic 2D simulator
4. Dry-run in CI

### Phase 4: Refinement
1. Simulation in CI
2. Enhanced coverage
3. Documentation
4. Team training

## GitHub Issues Structure

### Epic 1: CI/CD Foundation
- Set up GitHub Actions for Python builds
- Add React Native Android build validation
- Configure multi-version Python testing (3.9, 3.11, 3.12)
- Create PR status check requirements
- Document CI setup

### Epic 2: Linting
- Set up MegaLinter
- Configure baseline for existing violations
- Create linting documentation

### Epic 3: Unit Testing
- Configure pytest
- Write tests for PID control, settings, service base
- Create hardware mocking framework
- Add coverage reporting
- Configure Jest for React Native
- Write React Native unit tests

### Epic 4: Integration Testing
- Set up test MQTT broker
- Write service integration tests
- Mock board driver interfaces
- Create end-to-end test scenarios

### Epic 5: Dry Run
- Design dry-run architecture
- Implement dry-run flag in base classes
- Add dry-run to motor and sensor services
- Create test scenarios
- Integrate in CI

### Epic 6: Simulation
- Research and select approach
- Implement basic 2D simulator
- Create simulated sensors and arena
- Headless mode for CI
- Write simulation test scenarios

### Epic 7: Documentation
- Testing guide for contributors
- CI/CD pipeline documentation
- Troubleshooting guide

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Hardware dependencies | Comprehensive mocking, dry-run mode |
| Simulator complexity | Start simple 2D, iterate based on needs |
| Test maintenance | Keep tests focused, good documentation |
| CI too slow | Parallel execution, caching, separate fast/slow tests |

## Success Criteria

- 100% PRs validated by CI
- 70%+ code coverage
- < 5% PRs require hardware testing
- CI completes in < 10 minutes
