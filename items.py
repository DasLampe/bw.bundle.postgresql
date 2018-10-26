pkg_yum = {
    'postgresql-server': {
        'installed': True,
    },
    'postgresql-contrib': {
        'installed': True,
    }
}

svc_systemd = {
    'postgresql': {
        'enabled': True,
        'running': True,
        'needs': [
            'pkg_yum:postgresql-server',
            'pkg_yum:postgresql-contrib',
        ]
    }
}

actions = {
    'init_database': {
        'command': 'postgresql-setup initdb',
        'needs': [
            'pkg_yum:postgresql-server',
            'pkg_yum:postgresql-contrib',
        ],
        'triggers': [
        ],
        'unless': 'test -f /var/lib/pgsql/initdb.log',
    },
}

postgres_roles = {}
for role,config in node.metadata.get('postgresql', {}).get('role', {}).items():
    postgres_roles[role] = {
        'password': config.get('password', repo.vault.password_for('postgres_{}_{}'.format(role, node.name))),
        'needs': [
            'pkg_yum:postgresql-server',
            'pkg_yum:postgresql-contrib',
            'action:init_database',
            'svc_systemd:postgresql'
        ],
    }

postgres_dbs = {}
for database,config in node.metadata.get('postgresql', {}).get('database',{}).items():
    postgres_dbs[database] = {
        'owner': config.get('owner', database),
        'needs': [
            'pkg_yum:postgresql-server',
            'pkg_yum:postgresql-contrib',
            'action:init_database',
            'svc_systemd:postgresql'
        ],
    }