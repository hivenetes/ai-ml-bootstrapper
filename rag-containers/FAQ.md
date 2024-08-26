# Troubleshooting

## Broken packages

```bash
#!/bin/bash

# Get a list of all held packages
held_packages=$(dpkg --get-selections | grep 'hold$' | awk '{print $1}')

# Check if there are any held packages
if [ -z "$held_packages" ]; then
    echo "No held packages found."
else
    # Unhold each package
    for package in $held_packages; do
        echo "Unholding package: $package"
        sudo apt-mark unhold $package
    done
    echo "All held packages have been unheld."
fi

sudo apt-get install -f
```
