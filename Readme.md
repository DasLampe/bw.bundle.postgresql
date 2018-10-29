# Bundle to install PostgreSQL on Debian or CentOs

## Dependencies
* pkg_wrapper: https://github.com/DasLampe/bw.item.pkg_wrapper

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