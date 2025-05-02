
> [!IMPORTANT]
> # DEPRECATED
> Please use https://github.com/shorst/bw.bundle.postgres

# Bundle to install PostgreSQL on Debian

## Sample config
```python
'postgresql': {
    'role': {
        'me': {
            'password': 'postgresql_me_nodeName',
        },
    },
    'database': {
        'myDatabase': {
            'owner': 'myDatabase',
        }
    },
}
```
