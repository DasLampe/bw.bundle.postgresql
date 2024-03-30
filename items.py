pkg_apt = {
    'postgresql': {
        'installed': True,
    },
    'postgresql-contrib': {},
}

svc_systemd = {
    'postgresql': {
        'enabled': True,
        'running': True,
        'needs': [
            'pkg_apt:postgresql',
            'pkg_apt:postgresql-contrib',
        ]
    }
}

postgres_roles = {}
for role,config in node.metadata.get('postgresql', {}).get('role', {}).items():
    postgres_roles[role] = {
        'password': config.get('password', repo.vault.password_for(f'postgresql_{role}_{node.name}')),
        'superuser': config.get('superuser', False),
        'delete': config.get('delete', False),
        'needs': [
            'pkg_apt:postgresql',
            'pkg_apt:postgresql-contrib',
            'svc_systemd:postgresql'
        ],
    }

postgres_dbs = {}
for database,config in node.metadata.get('postgresql', {}).get('database',{}).items():
    postgres_dbs[database] = {
        'owner': config.get('owner', database),
        'when_creating': config.get('when_creating', {}),
        'delete': config.get('delete', False),
        'needs': [
            'pkg_apt:postgresql',
            'pkg_apt:postgresql-contrib',
            'svc_systemd:postgresql'
        ],
    }

