# opn-cli
![CI](https://github.com/andeman/opn-cli/actions/workflows/integration.yaml/badge.svg)

opn-cli - the OPNsense CLI written in python.

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
  firewall  Manage the OPNsense firewall
  plugin    Manage OPNsense plugins
  version   Show the CLI version and exit.

```


