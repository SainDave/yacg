<%
    # the template create a krakend config file from one or more loaded openapi files
    import yacg.model.model as model
    import yacg.model.openapi as openapi
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.jsonFuncs as jsonFuncs

    templateFile = 'krakend.mako'
    templateVersion = '1.0.0'

    pathTypes = []
    for type in modelTypes:
        if isinstance(type, openapi.PathType):
            pathTypes.append(type)

    gatewayName = templateParameters.get('gatewayName','My example gatewy')
    gatewayPort = templateParameters.get('gatewayPort','8080')
%>{
    "version": 2,
    "name": "${gatewayName}",
    "port": ${gatewayPort},
    "cache_ttl": "3600s",
    "timeout": "3s",
    "extra_config": {
      "github_com/devopsfaith/krakend-gologging": {
        "level":  "DEBUG",
        "prefix": "[KRAKEND]",
        "syslog": false,
        "stdout": true
      },
      "github_com/devopsfaith/krakend-metrics": {
        "collection_time": "60s",
        "proxy_disabled": false,
        "router_disabled": false,
        "backend_disabled": false,
        "endpoint_disabled": false,
        "listen_address": ":8090"
      }
    },
    "endpoints": [
        % for type in pathTypes:
            % for command in type.commands:
        ${'' if (type == pathTypes[0]) and (command == type.commands[0]) else ','}{
            "endpoint": "${type.pathPattern}",
            "method": "${openapi.CommandCommandEnum.valueAsString(command.command)}",
        }
            % endfor
        % endfor
    ]
}