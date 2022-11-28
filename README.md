# opn-cli
[![CI](https://github.com/andeman/opn-cli/actions/workflows/build.yaml/badge.svg)](https://github.com/andeman/opn-cli/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/andeman/opn-cli/branch/main/graph/badge.svg?token=WGV66ULJT4)](https://codecov.io/gh/andeman/opn-cli)
[![PyPI version](https://badge.fury.io/py/opn-cli.svg)](https://badge.fury.io/py/opn-cli)
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
    + [Code Generator](#code-generator)
      - [API code core](#api-code-core)
      - [API code plugin](#api-code-plugin)
      - [Core command code](#core-command-code)
      - [Plugin command code](#plugin-command-code)
    + [Resolving of names to uuids](#resolving-of-names-to-uuids)
  * [Commands](#commands)
    + [Firewall](#firewall)
      - [Aliases](#aliases)
      - [Rules](#rules)
    + [Haproxy](#haproxy)
      - [Acl](#acl)
      - [Action](#action)
      - [Backend](#backend)
      - [Config](#config)
      - [CPU](#cpu)
      - [Errorfile](#errorfile)
      - [Healthcheck](#healthcheck)
      - [Lua](#lua)
      - [Mailer](#mailer)
      - [Mapfile](#mapfile)
      - [Resolver](#resolver)
      - [Server](#server)
      - [User](#user)
    + [Ipsec](#ipsec)
      - [Tunnel phase1](#tunnel-phase1)
      - [Tunnel phase2](#tunnel-phase2)
    + [Routes](#routes)
      - [Static routes](#static-routes)
      - [Gateway](#gateway)
    + [Nodeexporter](#nodeexporter)
      - [Config](#config-1)
    + [Syslog](#syslog)
      - [Syslog destination](#syslog-destination)
      - [Syslog stats](#syslog-stats)
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
3. Install required opnsense plugins
    ```
    opn-cli plugin install os-firewall
    opn-cli plugin install os-haproxy
    ```
   
## Usage

Each command and subcommand support the `-h` or `--help option to show help for the current command.

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
  completion  Output instructions for shell completion
  firewall    Execute firewall operations
  haproxy     Manage haproxy loadbalancer operations
  ipsec       Manage Ipsec  
  new         Generate scaffolding code
  openvpn     Manage OpenVPN
  plugin      Manage OPNsense plugins
  route       Manage routes
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

### Code Generator
To assist the rapid development of new opn-cli commands, the code generator generates scaffolding code which could be 
used as a **starting point** for opnsense core or plugin modules.

```
$  opn-cli new -h
Usage: opn-cli new [OPTIONS] COMMAND [ARGS]...

Generate scaffolding code

Options:
-h, --help  Show this message and exit.

Commands:
command  Generate code for a new command
```

#### API code core
This generates all necessary code to implement api calls to a core module.

For a list of all plugin api endpoints see:

https://github.com/opnsense/docs/tree/master/source/development/api/core

Or:

```
$ opn-cli new api list --module-type core
```
Example that generates code for the core module 'cron':

```
$ opn-cli new api core cron
```

This generates a class for every controller of the core module.
Every class contains methodes to call all api endpoints of the corresponding controller. 

Please move the file from the output dir to the destination folders under opnsense_cli/.
The default output path is opnsense_cli/output/api/core/ .

#### API code plugin
This generates all necessary code to implement api calls to a plugin module.

For a list of all plugin api endpoints see:

https://github.com/opnsense/docs/tree/master/source/development/api/plugins

Or:

```
$ opn-cli new api list --module-type plugin
```

Example that generates code for the plugin module 'haproxy':

```
$ opn-cli new api plugin haproxy
```

This generates a class for every controller of the plugin module.
Every class contains methodes to call all api endpoints of the corresponding controller.

Please move the file from the output dir to the destination folders under opnsense_cli/.
The default output path is opnsense_cli/output/api/plugins/ .


#### Core command code
This generates all necessary code and tests to implement a new command from a core module.

For a list of core modules see: 

https://docs.opnsense.org/development/api.html#core-api

Search model.xml files here: 

https://github.com/opnsense/core/tree/master/src/opnsense/mvc/app/models/OPNsense

To add help texts, you need to specify a form.xml for the module. For Unbound dot the form.xml url is:

https://raw.githubusercontent.com/opnsense/core/master/src/opnsense/mvc/app/controllers/OPNsense/Unbound/forms/dialogDot.xml

Make sure to pass text/plain content from raw.githubusercontent.com instead of github.com.

Examples:
```
$ opn-cli new command core unbound dot --tag dots \
-m https://raw.githubusercontent.com/opnsense/core/master/src/opnsense/mvc/app/models/OPNsense/Unbound/Unbound.xml \
-f https://raw.githubusercontent.com/opnsense/core/master/src/opnsense/mvc/app/controllers/OPNsense/Unbound/forms/dialogDot.xml

```

This generates a command class, facade class and a integration test. 

Please move them from the output dir to the destination folders under opnsense_cli/, import the files in "cli.py" and register the commands groups and commands there.

The facade use API classes which should be generated with "opn-cli new api plugin" command. 
Make sure to remove all unnecessary API classes and methods to have a proper code coverage.

After some tweaks you should be able to use the new command.


#### Plugin command code
This generates all necessary code and tests to implement a new command from a plugin module.

For a list of plugin modules see:

https://docs.opnsense.org/development/api.html#plugins-api

Search for model.xml and form.xml files here: 

https://github.com/opnsense/plugins

Make sure to pass text/plain content from raw.githubusercontent.com instead of github.com.

Examples:
```
$ opn-cli new command plugin haproxy server --tag servers \
-m https://raw.githubusercontent.com/opnsense/plugins/master/net/haproxy/src/opnsense/mvc/app/models/OPNsense/HAProxy/HAProxy.xml \
-f https://raw.githubusercontent.com/opnsense/plugins/master/net/haproxy/src/opnsense/mvc/app/controllers/OPNsense/HAProxy/forms/dialogServer.xml

```
This generates a command class, facade class and a integration test. 

Please move them from the output dir to the destination folders under opnsense_cli/, import the files in "cli.py" and register the commands groups and commands there.

The facade use API classes which should be generated with "opn-cli new api plugin" command. 
Make sure to remove all unnecessary API classes and methods to have a proper code coverage.

After some tweaks you should be able to use the new command.

### Resolving of names to uuids
If you want to link items with options, you could link them with uuids or with their names. 

If the name exists mulitple times, the uuid from the first match is used.

**Example:**
```
$ opn-cli haproxy server list -c 'uuid,name'

+--------------------------------------+----------+
|                 uuid                 |   name   |
+--------------------------------------+----------+
| 162e7c70-dbea-4813-8676-33c506e1b1e2 | server1  |
| a293d23f-5fa5-46e5-b724-47f0031d8e9b | server2  |
+--------------------------------------+----------+

$ opn-cli haproxy backend list -c 'uuid,name,Servers'

+--------------------------------------+--------+-----------------+
|                 uuid                 |  name  |     Servers     |
+--------------------------------------+--------+-----------------+
| 54def7b3-93a8-4ea9-8858-22131948fb91 | pool1  |                 |
| c30cf40b-e026-4316-ad81-32affe0c1d85 | pool2  |                 |
+--------------------------------------+--------+-----------------+

# update linked item with names
$ opn-cli haproxy backend update 54def7b3-93a8-4ea9-8858-22131948fb91 --linkedServers server1,server2

# or update linked items with uuids
$ opn-cli haproxy backend update c30cf40b-e026-4316-ad81-32affe0c1d85 --linkedServers a293d23f-5fa5-46e5-b724-47f0031d8e9b

+--------------------------------------+--------+-----------------+
|                 uuid                 |  name  |     Servers     |
+--------------------------------------+--------+-----------------+
| 54def7b3-93a8-4ea9-8858-22131948fb91 | pool1  | server1,server2 |
| c30cf40b-e026-4316-ad81-32affe0c1d85 | pool2  |     server2     |
+--------------------------------------+--------+-----------------+

# delete linked items
$ opn-cli haproxy backend update c30cf40b-e026-4316-ad81-32affe0c1d85 --linkedServers ''

+--------------------------------------+--------+-----------------+
|                 uuid                 |  name  |     Servers     |
+--------------------------------------+--------+-----------------+
| 54def7b3-93a8-4ea9-8858-22131948fb91 | pool1  | server1,server2 |
| c30cf40b-e026-4316-ad81-32affe0c1d85 | pool2  |                 |
+--------------------------------------+--------+-----------------+
```




## Commands

### Firewall
This feature needs the opnsense plugin os-firewall.
```
$ opn-cli plugin install os-firewall
```

#### Aliases
See: https://wiki.opnsense.org/manual/aliases.html

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

#### Rules
See: https://docs.opnsense.org/manual/firewall.htm

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

### Haproxy
This feature needs the opnsense plugin os-haproxy.
```
$ opn-cli plugin install os-haproxy
```

#### Acl
```
Usage: opn-cli haproxy acl [OPTIONS] COMMAND [ARGS]...

  Specify various conditions.

  Define custom rules for blocking malicious requests, choosing backends,
  redirecting to HTTPS and using cached objects.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new acl
  delete  Delete acl
  list    Show all acl
  show    Show details for acl
  update  Update a acl.
```

#### Action
```
Usage: opn-cli haproxy action [OPTIONS] COMMAND [ARGS]...

  Perform a set of actions if one or more conditions match.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new action
  delete  Delete action
  list    Show all action
  show    Show details for action
  update  Update a action.
```

#### Backend
```
Usage: opn-cli haproxy backend [OPTIONS] COMMAND [ARGS]...

  Health monitoring and load distribution for servers.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new backend
  delete  Delete backend
  list    Show all backend
  show    Show details for backend
  update  Update a backend.
```
#### Config
```
Usage: opn-cli haproxy config [OPTIONS] COMMAND [ARGS]...

  Debug haproxy configuration.

Options:
  -h, --help  Show this message and exit.

Commands:
  apply     Test and apply the haproxy configuration
  diff      Diff of running and staging config
  download  Download complete haproxy config as zip
  show      Show the running haproxy config
  test      Test current haproxy staging config
```

#### CPU
```
Usage: opn-cli haproxy cpu [OPTIONS] COMMAND [ARGS]...

  CPU affinity rules.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new cpu
  delete  Delete cpu
  list    Show all cpu
  show    Show details for cpu
  update  Update a cpu.
```

#### Errorfile
```
Usage: opn-cli haproxy errorfile [OPTIONS] COMMAND [ARGS]...

  Custom messages instead of errors generated by haproxy.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new errorfile
  delete  Delete errorfile
  list    Show all errorfile
  show    Show details for errorfile
  update  Update a errorfile.
```

#### Healthcheck
```
Usage: opn-cli haproxy healthcheck [OPTIONS] COMMAND [ARGS]...

  Determine if a server is able to respond to client request.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new healthcheck
  delete  Delete healthcheck
  list    Show all healthcheck
  show    Show details for healthcheck
  update  Update a healthcheck.
```

#### Lua
```
Usage: opn-cli haproxy lua [OPTIONS] COMMAND [ARGS]...

  Lua code/scripts to extend HAProxy's functionality.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new lua
  delete  Delete lua
  list    Show all lua
  show    Show details for lua
  update  Update a lua.
```

#### Mailer
```
Usage: opn-cli haproxy mailer [OPTIONS] COMMAND [ARGS]...

  Email alerts when the state of servers changes.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new mailer
  delete  Delete mailer
  list    Show all mailer
  show    Show details for mailer
  update  Update a mailer.
```

#### Mapfile
```
Usage: opn-cli haproxy mapfile [OPTIONS] COMMAND [ARGS]...

  Map a large number of domains to backend pools.

  A map allows to map a data in input to an other one on output. For example,
  this makes it possible to map a large number of domains to backend pools
  without using the GUI. Map files need to be used in Rules, otherwise they
  are ignored.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new mapfile
  delete  Delete mapfile
  list    Show all mapfile
  show    Show details for mapfile
  update  Update a mapfile.
```

#### Resolver
```
Usage: opn-cli haproxy resolver [OPTIONS] COMMAND [ARGS]...

  Individual name resolution configurations for backends.

  This feature allows in-depth configuration of how HAProxy handles name
  resolution and interacts with name resolvers (DNS). Each resolver
  configuration can be used in Backend Pools to apply individual name
  resolution configurations.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new resolver
  delete  Delete resolver
  list    Show all resolver
  show    Show details for resolver
  update  Update a resolver.
```

#### Server
```
Usage: opn-cli haproxy server [OPTIONS] COMMAND [ARGS]...

  Server which serves content.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new server
  delete  Delete server
  list    Show all server
  show    Show details for server
  update  Update a server.
```

#### User
```
Usage: opn-cli haproxy user [OPTIONS] COMMAND [ARGS]...

  HTTP basic authentication users.

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new user
  delete  Delete user
  list    Show all user
  show    Show details for user
  update  Update a user.
```

### Ipsec
#### Tunnel phase1
```
Usage: opn-cli ipsec tunnel phase1 [OPTIONS] COMMAND [ARGS]...

  Manage ipsec phase 1 tunnels

Options:
  -h, --help  Show this message and exit.

Commands:
  list  Show all ipsec phase1 tunnels
  show  Show details for phase 1 tunnel
```

#### Tunnel phase2
```
Usage: opn-cli ipsec tunnel phase2 [OPTIONS] COMMAND [ARGS]...

  Manage ipsec phase 2 tunnels

Options:
  -h, --help  Show this message and exit.

Commands:
  list  Show all ipsec phase2 tunnels
  show  Show details for phase 2 tunnel
```
### Routes
#### Static routes
```
Usage: opn-cli route static [OPTIONS] COMMAND [ARGS]...

  Manage static routes

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new static route
  delete  Delete static route
  list    Show all static routes
  show    Show details for a static route
  update  Update a static route
```
#### Gateway
```
Usage: opn-cli route gateway [OPTIONS] COMMAND [ARGS]...

  Manage gateway routes

Options:
  -h, --help  Show this message and exit.

Commands:
  status  Show gateway states
```
### Nodeexporter
#### Config
```
Usage: opn-cli nodeexporter config [OPTIONS] COMMAND [ARGS]...

  Manage nodeexporter config

Options:
  -h, --help  Show this message and exit.

Commands:
  edit  Edit configuration
  show  Show configuration

```

### Syslog
#### Syslog destination
```
Usage: opn-cli syslog destination [OPTIONS] COMMAND [ARGS]...

  Manage syslog destination

Options:
  -h, --help  Show this message and exit.

Commands:
  create  Create a new destination
  delete  Delete destination
  list    Show all destination
  show    Show details for destination
  update  Update a destination.
```
#### Syslog stats
```
Usage: opn-cli syslog stats list [OPTIONS]

  Show syslog statistics

Options:
  --search TEXT                   Search for this string
  -o, --output [cols|table|json|json_filter|plain|yaml]
                                  Specifies the Output format.  [default:
                                  table]
  -c, --cols TEXT                 Which columns should be printed? Pass empty
                                  string (-c ) to show all columns  [default: #
                                  ,Description,SourceName,SourceId,SourceInsta
                                  nce,State,Type,Number]
  -h, --help                      Show this message and exit.

```

### OpenVPN
```
Usage: opn-cli openvpn [OPTIONS] COMMAND [ARGS]...

  Export OpenVPN configuration.

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

  OPNsense plugins management

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

# execute a single test
scripts/unit_tests opnsense_cli/tests/command/tests/test_format.py::TestFormatter

# execute tests with coverage report
scripts/coverage
```

### Contributing
Please use the GitHub issues functionality to report any bugs or requests for new features. Feel free to fork and submit pull requests for potential contributions.

All contributions must pass all existing tests, new features should provide additional unit/acceptance tests.

