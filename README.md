# opn-cli
[![CI](https://github.com/andeman/opn-cli/actions/workflows/build.yaml/badge.svg)](https://github.com/andeman/opn-cli/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/andeman/opn-cli/branch/main/graph/badge.svg?token=WGV66ULJT4)](https://codecov.io/gh/andeman/opn-cli)
[![Downloads](https://pepy.tech/badge/opn-cli)](https://pepy.tech/project/opn-cli)

opn-cli - the OPNsense CLI written in python.

- [opn-cli](#opn-cli)
  * [Install](#install)
  * [Configure](#configure)
  * [Usage](#usage)
  * [Features](#features)
    + [Shell Completion](#shell-completion)
    + [Output formats](#output-formats)
      - [cols](#cols)
      - [table](#table)
      - [json](#json)
      - [json_filter](#json-filter)
      - [plain](#plain)
      - [yaml](#yaml)
    + [Firewall aliases](#firewall-aliases)
    + [Firewall rules](#firewall-rules)
    + [OpenVPN](#openvpn)
    + [Plugins](#plugins)
  * [Development](#development)
    + [Setup development environment](#setup-development-environment)
    + [Testing](#testing)
    + [Contributing](#contributing)

## Install
```
pip install opn-cli
```

## Configure
1. Generate an api_key and api_secret. See: https://docs.opnsense.org/development/how-tos/api.html#creating-keys.

2. Create the default config file `~/.opn-cli/conf.yaml`
```
---
api_key: your_api_key
api_secret: your_api_secret
url: https://opnsense.example.com/api
timeout: 60
ssl_verify: true
ca: ~/.opn-cli/ca.pem
```

## Usage
```
$ opn-cli --help

Usage: opn-cli [OPTIONS] COMMAND [ARGS]...

  OPNsense CLI - interact with OPNsense via the CLI

  API key + secret:

  You need a valid API key and secret to interact with the API. Open your
  browser and go to System->Access->Users and generate or use an existing
  Api Key. 
  
  See: https://docs.opnsense.org/development/how-tos/api.html#creating-keys.

  SSL verify / CA:

  If you use ssl verification (--ssl-verify), make sure to specify a valid
  ca with --ca <path_to_bundle>.

  To download the default self-signed cert, open the OPNsense Web Gui and go to 
  System->Trust->Certificates. Search for the Name: "Web GUI SSL certificate" and 
  press the "export user cert" button. 
  
  If you use a ca signed certificate, go to System->Trust->Authorities and 
  press the "export CA cert" button to download the ca.

  Save the cert or the ca as ~/.opn-cli/ca.pem.

  Configuration:

  You can set the required options as environment variables. See --help
  "[env var: [...]"

  Or use a config file passed with -c option.

  The configuration cascade from highest precedence to lowest:

  1. argument & options

  2. environment variables

  3. config file


  Happy automating!

Options:
  -c, --config FILE               path to the config file  [env var:
                                  OPN_CONFIG; default: ~/.opn-cli/conf.yaml]

  --ca FILE                       path to the ca bundle file for ssl
                                  verification  [env var: OPN_SSL_VERIFY_CA;
                                  default: ~/.opn-cli/ca.pem]

  -k, --api-key TEXT              Your API key for the OPNsense API  [env var:
                                  OPN_API_KEY]

  -s, --api-secret TEXT           Your API secret for the OPNsense API  [env
                                  var: OPN_API_SECRET]

  -u, --url TEXT                  The Base URL for the OPNsense API  [env var:
                                  OPN_API_URL]

  -t, --timeout INTEGER           Set timeout for API Calls in seconds.  [env
                                  var: OPN_API_TIMEOUT; default: 60]

  --ssl-verify / --no-ssl-verify  Enable or disable SSL verification for API
                                  communication.  [env var: OPN_SSL_VERIFY;
                                  default: True]

  -h, --help                      Show this message and exit.

Commands:
  completion  Output Instructions for shell completion
  firewall    Execute firewall operations
  openvpn     Manage OpenVPN
  plugin      Manage OPNsense plugins
  version     Show the CLI version and exit.
```

## Features
### Shell Completion
```
$ opn-cli completion

Instructions for shell completion:

See: https://click.palletsprojects.com/en/latest/shell-completion/

Bash (invoked every time a shell is started):
echo '# shell completion for opn-cli' >> ~/.bashrc
echo 'eval "$(_OPN_CLI_COMPLETE=bash_source opn-cli)"' >> ~/.bashrc

Bash (current shell):
_OPN_CLI_COMPLETE=bash_source opn-cli > ~/.opn-cli/opn-cli-complete.bash
source ~/.opn-cli/opn-cli-complete.bash

Zsh (invoked every time a shell is started):
echo '# shell completion for opn-cli' >> ~/.zshrc
echo 'eval "$(_OPN_CLI_COMPLETE=zsh_source opn-cli)"' >> ~/.zshrc

Zsh (current shell):
_OPN_CLI_COMPLETE=zsh_source opn-cli >! ~/.opn-cli/opn-cli-complete.zsh
source ~/.opn-cli/opn-cli-complete.zsh
```

### Output formats
Each command has a default output format. For lists and details the table output format and for create / update / delete the plain output formatis used.

You can always specify the output format with the `-o` output and show or hide columns with the `-c` output.

#### cols
Show which default columns will be shown 
```
$ opn-cli plugin installed -o cols
name,version,comment,locked
```

Show which columns are available. You could always pass an empty string to show all columns.
```
$ opn-cli plugin installed -o cols -c ''
name,version,comment,flatsize,locked,automatic,license,repository,origin,provided,installed,path,configured
```

#### table
Show output as pretty table.

```
$ opn-cli plugin installed -o table
+-----------------+---------+-----------------------------------+--------+
|       name      | version |              comment              | locked |
+-----------------+---------+-----------------------------------+--------+
|   os-firewall   |  1.0_2  | Firewall API supplemental package |  N/A   |
|     os-iperf    |  1.0_1  |      Connection speed tester      |  N/A   |
|  os-virtualbox  |  1.0_1  |     VirtualBox guest additions    |  N/A   |
| os-zabbix-agent |  1.8_2  |      Zabbix monitoring agent      |  N/A   |
+-----------------+---------+-----------------------------------+--------+

```
#### json
Always returns the complete json output. The `-c` output will be ignored.

```
$ opn-cli plugin installed -o json 
[{"name": "os-firewall", "version": "1.0_2", "comment": "Firewall API supplemental package", "flatsize": "56.0KiB", "locked": "N/A", "automatic": "N/A", "license": "BSD2CLAUSE", "repository": "OPNsense", "origin": "opnsense/os-firewall", "provided": "1", "installed": "1", "path": "OPNsense/opnsense/os-firewall", "configured": "1"}, {"name": "os-iperf", "version": "1.0_1", "comment": "Connection speed tester", "flatsize": "24.6KiB", "locked": "N/A", "automatic": "N/A", "license": "BSD2CLAUSE", "repository": "OPNsense", "origin": "opnsense/os-iperf", "provided": "1", "installed": "1", "path": "OPNsense/opnsense/os-iperf", "configured": "1"}, {"name": "os-virtualbox", "version": "1.0_1", "comment": "VirtualBox guest additions", "flatsize": "525B", "locked": "N/A", "automatic": "N/A", "license": "BSD2CLAUSE", "repository": "OPNsense", "origin": "opnsense/os-virtualbox", "provided": "1", "installed": "1", "path": "OPNsense/opnsense/os-virtualbox", "configured": "1"}, {"name": "os-zabbix-agent", "version": "1.8_2", "comment": "Zabbix monitoring agent", "flatsize": "49.2KiB", "locked": "N/A", "automatic": "N/A", "license": "BSD2CLAUSE", "repository": "OPNsense", "origin": "opnsense/os-zabbix-agent", "provided": "1", "installed": "1", "path": "OPNsense/opnsense/os-zabbix-agent", "configured": "1"}]
```

#### json_filter
Filter the json output and return the columns specified with the `-c` output.
```
$ opn-cli plugin installed -o json_filter -c name,version
[{"name": "os-firewall", "version": "1.0_2"}, {"name": "os-virtualbox", "version": "1.0_1"},
```

#### plain
Show the output separated by space.
```
$ opn-cli  plugin installed -o plain 
os-firewall 1.0_2 Firewall API supplemental package N/A
os-iperf 1.0_1 Connection speed tester N/A
os-virtualbox 1.0_1 VirtualBox guest additions N/A
os-zabbix-agent 1.8_2 Zabbix monitoring agent N/A
```

#### yaml
Show yaml output.
```
$ opn-cli plugin installed -o yaml 
- name: os-firewall
  version: '1.0_2'
  comment: Firewall API supplemental package
  locked: N/A
- name: os-iperf
  version: '1.0_1'
  comment: Connection speed tester
  locked: N/A
- name: os-virtualbox
  version: '1.0_1'
  comment: VirtualBox guest additions
  locked: N/A
- name: os-zabbix-agent
  version: '1.8_2'
  comment: Zabbix monitoring agent
  locked: N/A

```



### Firewall aliases
```
Usage: opn-cli firewall alias [OPTIONS] COMMAND [ARGS]...

  Manage OPNsense firewall aliases.

  See: https://wiki.opnsense.org/manual/aliases.html

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new alias.
  delete  Delete an alias
  list    Show all aliases
  show    Show details for alias
  table   Show pf table entries for alias
  update  Update an alias.
```

### Firewall rules
```
Usage: opn-cli firewall rule [OPTIONS] COMMAND [ARGS]...

  Manage OPNsense firewall rules.

  See: https://docs.opnsense.org/manual/firewall.html

  This Feature need the plugin: os-firewall

  With the new plugin on version 20.1.5 for the firewall API, it adds a new
  menu item under the "Firewall" section called "Automation" under that is
  the "Filter" menu item.

  All the created firewall rules are above all other rules. The order of
  execution for the firewall rules goes: Automation -> Floating ->
  Interface.

  Before you modify a rule, an automatic config savepoint will be created.
  if you lock yourself out, the config will be rollbacked after 60 seconds.

  See:
  https://docs.opnsense.org/development/api/plugins/firewall.html#concept

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new firewall rule.
  delete  Delete a firewall rule
  list    Show all firewall rules
  show    Show firewall rule details
  update  Update firewall rule.

```

### OpenVPN
```
Usage: opn-cli openvpn [OPTIONS] COMMAND [ARGS]...

  Manage OpenVPN

Options:
  -h, --help  Show this message and exit.

Commands:
  accounts   Show all accounts for an OpenVPN server.
  download   Download client config for chosen OpenVPN server and account.
  providers  Show all available OpenVPN servers.
  templates  Show all available export templates.
```

### Plugins
```
Usage: opn-cli plugin [OPTIONS] COMMAND [ARGS]...

  Manage OPNsense plugins

Options:
  -h, --help  Show this message and exit.

Commands:
  install    Install plugin by name
  installed  Show installed plugins.
  list       Show all available plugins.
  lock       Lock plugin.
  reinstall  Reinstall plugin by name.
  show       Show plugin details.
  uninstall  Uninstall plugin by name.
  unlock     Unlock plugin.
```

## Development

### Setup development environment

Requirements:
* vagrant
* virtualbox

This will install opn-cli, add it to your PATH and setup an opnsense vm with vagrant:
```
# setup 
scripts/create_test_env

# test opn-cli
opn-cli plugin list

# teardown 
scripts/remove_test_env
```

### Testing
```
# lint your code
scripts/lint

# execute all unit tests
scripts/unit_tests

# execute the TestFormatter tests
scripts/unit_tests opnsense_cli/tests/command/tests/test_format.py::TestFormatter

# execute tests with coverage report
scripts/coverage
```

### Contributing
Please use the GitHub issues functionality to report any bugs or requests for new features. Feel free to fork and submit pull requests for potential contributions.

All contributions must pass all existing tests, new features should provide additional unit/acceptance tests.




