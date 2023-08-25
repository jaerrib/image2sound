default: black isort

# Format with black formatter
black:
    black src/

# Sort imports using isort
isort:
    isort src/

# Remove unused imports using unimport
unimport:
    unimport src/