{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.services.passworts;
  pkg = cfg.package;
  systemd-settings = {
    User = "passworts";
    DynamicUser = true;
    Restart = "on-failure";

    BindReadOnlyPaths = [
      "${config.environment.etc."ssl/certs/ca-certificates.crt".source}:/etc/ssl/certs/ca-certificates.crt"
      builtins.storeDir
      "-/etc/resolv.conf"
      "-/etc/nsswitch.conf"
      "-/etc/hosts"
      "-/etc/localtime"
    ];
    CapabilityBoundingSet = "";
    LockPersonality = true;
    MemoryDenyWriteExecute = true;
    PrivateDevices = true;
    PrivateUsers = true;
    ProtectClock = true;
    ProtectControlGroups = true;
    ProtectHome = true;
    ProtectHostname = true;
    ProtectKernelLogs = true;
    ProtectKernelModules = true;

    ProtectKernelTunables = true;
    RestrictAddressFamilies = [ "AF_UNIX" "AF_INET" "AF_INET6" ];
    RestrictNamespaces = true;
    RestrictRealtime = true;
    SystemCallArchitectures = "native";
    # gunicorn needs setuid
    SystemCallFilter = [ "@system-service" "~@privileged" "@resources" "@setuid" "@keyring" ];
    UMask = "0066";
  } // lib.optionalAttrs (cfg.port < 1024) {
    AmbientCapabilities = [ "CAP_NET_BIND_SERVICE" ];
    CapabilityBoundingSet = [ "CAP_NET_BIND_SERVICE" ];
  };
in
{
  options.services.passworts = {
    enable = mkEnableOption (mdDoc "Passworts generator web-service");

    address = mkOption {
      type = types.str;
      default = "localhost";
      description = mdDoc "Web interface address.";
    };

    port = mkOption {
      type = types.port;
      default = 8080;
      description = mdDoc "Web interface port.";
    };

    package = mkOption {
      type = types.package;
      default = pkgs.passworts;
      defaultText = literalExpression "pkgs.passworts";
      description = mdDoc "The Passworts package to use.";
    };
  };

  config = mkIf cfg.enable {
    systemd.services.passworts =
      let
        uwsgiConfig.uwsgi = {
          type = "normal";
          plugins = [ "python3" ];
          module = "passworts";

          chdir = cfg.package;
          http-socket = "${cfg.address}:${toString cfg.port}";

          # master = true;
          enable-threads = true;
          processes = 4;
          threads = 2;
          vacuum = true;
        };
        uwsgiConfigFile = pkgs.writeText "uwsgi-passworts.json" (builtins.toJSON uwsgiConfig);
      in
      {
        description = "Passworts server";
        wantedBy = [ "multi-user.target" ];
        serviceConfig = systemd-settings // {
          ExecStart = ''
            ${pkgs.uwsgi.override { plugins = ["python3"]; }}/bin/uwsgi --json ${uwsgiConfigFile}
          '';
        };
        environment = {
          PYTHONPATH = "${pkg.python3.pkgs.makePythonPath pkg.propagatedBuildInputs}:${pkg}";
        };
      };

    # sadly streaming does not work with gunicorn, therefor the uwsgi is used
    # systemd.services.passworts = {
    #   description = "Passworts server";
    #   wantedBy = [ "multi-user.target" ];

    #   serviceConfig = systemd-settings // {
    #     ExecStart = ''
    #       ${pkg.python3.pkgs.gunicorn}/bin/gunicorn passworts
    #     '';
    #   };

    #   environment = {
    #     GUNICORN_CMD_ARGS = "--bind=${cfg.address}:${toString cfg.port} --timeout 0 --worker-class=gevent";
    #     PYTHONPATH = "${pkg.python3.pkgs.makePythonPath pkg.propagatedBuildInputs}:${pkg}";
    #   };
    # };
  };
}