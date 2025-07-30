# Recovery Compass Docker Clone Instructions

## For Contributors

Since the Docker configuration lives as a subdirectory in the main repository, cloning is straightforward:

```bash
# Clone the main repository
git clone https://github.com/EssenceAlignment/WFD-Sunrise-Path.git
cd WFD-Sunrise-Path/recovery-compass-docker

# Initialize secrets
make init-secrets

# Start services
make up-min
```

## For CI/CD Systems

The GitHub Actions workflow handles this automatically:

```yaml
- name: Checkout code
  uses: actions/checkout@v4
```

## For Partner Organizations

If partners need only the Docker configuration:

```bash
# Option 1: Sparse checkout (recommended)
git clone --filter=blob:none --sparse https://github.com/EssenceAlignment/WFD-Sunrise-Path.git
cd WFD-Sunrise-Path
git sparse-checkout set recovery-compass-docker

# Option 2: Download as archive
curl -L https://github.com/EssenceAlignment/WFD-Sunrise-Path/archive/main.zip -o wfd.zip
unzip wfd.zip "WFD-Sunrise-Path-main/recovery-compass-docker/*"
cd WFD-Sunrise-Path-main/recovery-compass-docker
```

## Future Migration to Submodule

If we later decide to use a submodule:

```bash
# In parent repo
git submodule add https://github.com/Recovery-Compass/recovery-compass-docker.git
git submodule update --init --recursive

# In CI
- name: Checkout with submodules
  uses: actions/checkout@v4
  with:
    submodules: recursive
```

Currently, the subdirectory approach avoids this complexity while maintaining force multiplication benefits.
