pkg = {
    'postgresql-server': {
        'debian': 'postgresql',  # Different package name on Debian
    },
    'postgresql-contrib': {},
}

svc_systemd = {
    'postgresql': {
        'enabled': True,
        'running': True,
        'needs': [
            'pkg:postgresql-server',
            'pkg:postgresql-contrib',
        ]
    }
}

if node.os in node.OS_FAMILY_REDHAT:
    # Debian do this while install package
    actions = {
            'init_database': {
                'command': 'postgresql-setup initdb',
                'needs': [
                    'pkg:postgresql-server',
                    'pkg:postgresql-contrib',
                  ],
                'needs_by': [
                    'postgres_roles:',
                    'postgres_dbs:',
                ],
                'triggers': [
                ],
                'unless': 'test -f /var/lib/pgsql/initdb.log',
            },
    }

postgres_roles = {}
for role,config in node.metadata.get('postgresql', {}).get('role', {}).items():
    postgres_roles[role] = {
        'password': config.get('password', repo.vault.password_for('postgresql_{}_{}'.format(role, node.name))),
        'needs': [
            'pkg:postgresql-server',
            'pkg:postgresql-contrib',
            'svc_systemd:postgresql'
        ],
    }

postgres_dbs = {}
for database,config in node.metadata.get('postgresql', {}).get('database',{}).items():
    postgres_dbs[database] = {
        'owner': config.get('owner', database),
        'needs': [
            'pkg:postgresql-server',
            'pkg:postgresql-contrib',
            'svc_systemd:postgresql'
        ],
    }